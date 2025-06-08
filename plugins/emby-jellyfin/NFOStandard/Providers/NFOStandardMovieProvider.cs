using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using MediaBrowser.Controller.Entities.Movies;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;
using MediaBrowser.Model.Providers;

namespace NFOStandard.Providers
{
    /// <summary>
    /// NFO Standard movie metadata provider for Emby/Jellyfin
    /// </summary>
    public class NFOStandardMovieProvider : ILocalMetadataProvider<Movie>, IHasItemChangeMonitor
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private const string NFONamespace = "NFOStandard";

        public string Name => "NFO Standard";

        public NFOStandardMovieProvider(ILogger logger, IFileSystem fileSystem)
        {
            _logger = logger;
            _fileSystem = fileSystem;
        }

        public Task<MetadataResult<Movie>> GetMetadata(ItemInfo info, IDirectoryService directoryService, CancellationToken cancellationToken)
        {
            var result = new MetadataResult<Movie>();
            
            var nfoPath = GetNfoPath(info.Path);
            if (string.IsNullOrEmpty(nfoPath))
            {
                return Task.FromResult(result);
            }

            try
            {
                var doc = XDocument.Load(nfoPath);
                var root = doc.Root;
                
                if (root?.Name.LocalName != "root" || root.Name.Namespace != NFONamespace)
                {
                    _logger.Info($"NFO file is not NFO Standard compliant: {nfoPath}");
                    return Task.FromResult(result);
                }

                var movieElement = root.Descendants(XName.Get("movie", NFONamespace)).FirstOrDefault();
                if (movieElement == null)
                {
                    movieElement = root.Descendants("movie").FirstOrDefault();
                }

                if (movieElement != null)
                {
                    var movie = new Movie();
                    ParseMovieElement(movie, movieElement);
                    
                    result.HasMetadata = true;
                    result.Item = movie;
                }
            }
            catch (Exception ex)
            {
                _logger.ErrorException($"Error parsing NFO file: {nfoPath}", ex);
            }

            return Task.FromResult(result);
        }

        private void ParseMovieElement(Movie movie, XElement movieElement)
        {
            // Title
            movie.Name = GetElementValue(movieElement, "title");
            movie.OriginalTitle = GetElementValue(movieElement, "originaltitle");
            movie.SortName = GetElementValue(movieElement, "sorttitle");

            // Year
            var yearStr = GetElementValue(movieElement, "year");
            if (int.TryParse(yearStr, out var year))
            {
                movie.ProductionYear = year;
            }

            // Overview
            movie.Overview = GetElementValue(movieElement, "plot");
            if (string.IsNullOrEmpty(movie.Overview))
            {
                movie.Overview = GetElementValue(movieElement, "outline");
            }

            // Tagline
            movie.Tagline = GetElementValue(movieElement, "tagline");

            // Runtime
            var runtimeStr = GetElementValue(movieElement, "runtime");
            if (long.TryParse(runtimeStr, out var runtime))
            {
                movie.RunTimeTicks = TimeSpan.FromMinutes(runtime).Ticks;
            }

            // Ratings
            ParseRatings(movie, movieElement);

            // Content rating
            ParseContentRating(movie, movieElement);

            // Genres
            movie.Genres = movieElement.Elements("genre")
                .Select(e => e.Value)
                .Where(g => !string.IsNullOrWhiteSpace(g))
                .ToArray();

            // Tags
            movie.Tags = movieElement.Elements("tag")
                .Select(e => e.Value)
                .Where(t => !string.IsNullOrWhiteSpace(t))
                .ToArray();

            // Studios
            var studios = movieElement.Elements("productioncompany")
                .Select(e => e.Value)
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .ToList();
            
            if (studios.Any())
            {
                movie.Studios = studios.ToArray();
            }

            // People
            ParsePeople(movie, movieElement);

            // Release date
            var releaseDateStr = GetElementValue(movieElement, "releasedate");
            if (DateTime.TryParse(releaseDateStr, out var releaseDate))
            {
                movie.PremiereDate = releaseDate;
            }

            // Collection
            var setName = GetElementValue(movieElement, "setname");
            if (!string.IsNullOrWhiteSpace(setName))
            {
                movie.CollectionName = setName;
            }

            // Provider IDs
            ParseProviderIds(movie, movieElement);
        }

        private void ParseRatings(Movie movie, XElement movieElement)
        {
            var ratings = movieElement.Elements("rating");
            foreach (var rating in ratings)
            {
                var name = rating.Attribute("name")?.Value ?? "default";
                var valueStr = rating.Attribute("value")?.Value;
                var isDefault = rating.Attribute("default")?.Value == "true";

                if (float.TryParse(valueStr, out var value))
                {
                    if (isDefault || name == "imdb")
                    {
                        movie.CommunityRating = value;
                    }
                    else if (name == "critic")
                    {
                        movie.CriticRating = value * 10; // Convert to percentage
                    }
                }
            }

            // User rating
            var userRatingStr = GetElementValue(movieElement, "userrating");
            if (float.TryParse(userRatingStr, out var userRating))
            {
                movie.CustomRating = userRatingStr;
            }
        }

        private void ParseContentRating(Movie movie, XElement movieElement)
        {
            var contentRating = movieElement.Elements("contentrating").FirstOrDefault();
            if (contentRating != null)
            {
                var rating = contentRating.Attribute("rating")?.Value ?? contentRating.Value;
                if (!string.IsNullOrWhiteSpace(rating))
                {
                    movie.OfficialRating = rating;
                }
            }
        }

        private void ParsePeople(Movie movie, XElement movieElement)
        {
            var people = new List<PersonInfo>();

            // Actors
            foreach (var actor in movieElement.Elements("actor"))
            {
                var person = new PersonInfo
                {
                    Name = GetElementValue(actor, "name"),
                    Role = GetElementValue(actor, "role"),
                    Type = PersonType.Actor
                };

                var orderStr = GetElementValue(actor, "order");
                if (int.TryParse(orderStr, out var order))
                {
                    person.SortOrder = order;
                }

                if (!string.IsNullOrWhiteSpace(person.Name))
                {
                    people.Add(person);
                }
            }

            // Directors
            foreach (var director in movieElement.Elements("director"))
            {
                var name = GetElementValue(director, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    people.Add(new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Director
                    });
                }
            }

            // Writers
            foreach (var writer in movieElement.Elements("writer"))
            {
                var name = GetElementValue(writer, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    people.Add(new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Writer
                    });
                }
            }

            if (people.Any())
            {
                movie.People = people.ToArray();
            }
        }

        private void ParseProviderIds(Movie movie, XElement movieElement)
        {
            foreach (var uniqueId in movieElement.Elements("uniqueid"))
            {
                var type = uniqueId.Attribute("type")?.Value;
                var value = uniqueId.Value;

                if (!string.IsNullOrWhiteSpace(type) && !string.IsNullOrWhiteSpace(value))
                {
                    switch (type.ToLowerInvariant())
                    {
                        case "imdb":
                            movie.ProviderIds[MetadataProviders.Imdb.ToString()] = value;
                            break;
                        case "tmdb":
                            movie.ProviderIds[MetadataProviders.Tmdb.ToString()] = value;
                            break;
                        default:
                            movie.ProviderIds[type] = value;
                            break;
                    }
                }
            }
        }

        private string GetElementValue(XElement parent, string elementName)
        {
            return parent.Element(elementName)?.Value?.Trim();
        }

        private string GetNfoPath(string moviePath)
        {
            if (string.IsNullOrWhiteSpace(moviePath))
            {
                return null;
            }

            // For file, check same name with .nfo extension
            if (_fileSystem.FileExists(moviePath))
            {
                var nfoPath = Path.ChangeExtension(moviePath, ".nfo");
                if (_fileSystem.FileExists(nfoPath))
                {
                    return nfoPath;
                }

                // Check for movie.nfo in same directory
                var dir = Path.GetDirectoryName(moviePath);
                nfoPath = Path.Combine(dir, "movie.nfo");
                if (_fileSystem.FileExists(nfoPath))
                {
                    return nfoPath;
                }
            }
            // For directory, check for movie.nfo inside
            else if (_fileSystem.DirectoryExists(moviePath))
            {
                var nfoPath = Path.Combine(moviePath, "movie.nfo");
                if (_fileSystem.FileExists(nfoPath))
                {
                    return nfoPath;
                }
            }

            return null;
        }

        public bool HasChanged(BaseItem item, IDirectoryService directoryService)
        {
            var nfoPath = GetNfoPath(item.Path);
            if (string.IsNullOrEmpty(nfoPath))
            {
                return false;
            }

            var nfoInfo = _fileSystem.GetFileInfo(nfoPath);
            if (nfoInfo.Exists && nfoInfo.LastWriteTimeUtc > item.DateLastSaved)
            {
                return true;
            }

            return false;
        }
    }
}