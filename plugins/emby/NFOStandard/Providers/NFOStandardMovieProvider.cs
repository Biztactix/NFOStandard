using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.Entities.Movies;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;
using MediaBrowser.Model.Providers;
using MediaBrowser.Model.Configuration;

namespace NFOStandard.Providers
{
    /// <summary>
    /// NFO Standard movie metadata provider for Emby/Jellyfin
    /// </summary>
    public class NFOStandardMovieProvider : ILocalMetadataProvider<Movie>, IHasItemChangeMonitor
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private readonly ILibraryManager _libraryManager;
        private const string NFONamespace = "NFOStandard";

        public string Name => "NFO Standard";

        public NFOStandardMovieProvider(ILogger logger, IFileSystem fileSystem, ILibraryManager libraryManager)
        {
            _logger = logger;
            _fileSystem = fileSystem;
            _libraryManager = libraryManager;
        }

        public Task<MetadataResult<Movie>> GetMetadata(ItemInfo info, LibraryOptions libraryOptions, IDirectoryService directoryService, CancellationToken cancellationToken)
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
                    ParseMovieElement(movie, movieElement, result);
                    
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

        private void ParseMovieElement(Movie movie, XElement movieElement, MetadataResult<Movie> result)
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
            ParsePeople(movie, movieElement, result);

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
                // CollectionName not directly settable in Emby 4.8
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

        private void ParsePeople(Movie movie, XElement movieElement, MetadataResult<Movie> result)
        {
            var config = NFOStandardPlugin.Instance?.Configuration;
            if (config != null && !config.EnablePeopleExtraction)
            {
                return;
            }

            var people = new List<PersonInfo>();
            var maxActors = config?.MaxActors ?? 50;
            var actorCount = 0;

            // Actors
            foreach (var actor in movieElement.Elements("actor"))
            {
                if (actorCount >= maxActors)
                {
                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Reached maximum actor limit ({maxActors}) for movie: {movie.Name}");
                    }
                    break;
                }

                var person = new PersonInfo
                {
                    Name = GetElementValue(actor, "name"),
                    Role = GetElementValue(actor, "role"),
                    Type = PersonType.Actor
                };

                // Handle actor order/sort
                var orderStr = GetElementValue(actor, "order");
                if (int.TryParse(orderStr, out var order))
                {
                    // SortOrder not available in Emby 4.8, but we preserve the data
                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Actor {person.Name} has order {order} (preserved for future use)");
                    }
                }

                // Handle actor thumb/image
                var thumb = GetElementValue(actor, "thumb");
                if (!string.IsNullOrWhiteSpace(thumb))
                {
                    person.ImageUrl = thumb;
                }

                if (!string.IsNullOrWhiteSpace(person.Name))
                {
                    people.Add(person);
                    actorCount++;

                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Added actor: {person.Name} as {person.Role ?? "[Unknown Role]"}");
                    }
                }
            }

            // Directors
            foreach (var director in movieElement.Elements("director"))
            {
                var name = GetElementValue(director, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    var person = new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Director
                    };

                    // Handle director thumb/image
                    var thumb = GetElementValue(director, "thumb");
                    if (!string.IsNullOrWhiteSpace(thumb))
                    {
                        person.ImageUrl = thumb;
                    }

                    people.Add(person);

                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Added director: {name}");
                    }
                }
            }

            // Writers
            foreach (var writer in movieElement.Elements("writer"))
            {
                var name = GetElementValue(writer, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    var person = new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Writer
                    };

                    // Handle writer thumb/image
                    var thumb = GetElementValue(writer, "thumb");
                    if (!string.IsNullOrWhiteSpace(thumb))
                    {
                        person.ImageUrl = thumb;
                    }

                    people.Add(person);

                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Added writer: {name}");
                    }
                }
            }

            // Producers
            foreach (var producer in movieElement.Elements("producer"))
            {
                var name = GetElementValue(producer, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    var person = new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Producer
                    };

                    // Handle producer thumb/image
                    var thumb = GetElementValue(producer, "thumb");
                    if (!string.IsNullOrWhiteSpace(thumb))
                    {
                        person.ImageUrl = thumb;
                    }

                    people.Add(person);

                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Added producer: {name}");
                    }
                }
            }

            if (people.Any())
            {
                // Store people in MetadataResult.People for Emby to process
                // The people will be handled by Emby's people management system
                result.People = people;

                _logger.Info($"Loaded {people.Count} people for movie: {movie.Name} (Actors: {actorCount}, Directors: {people.Count(p => p.Type == PersonType.Director)}, Writers: {people.Count(p => p.Type == PersonType.Writer)}, Producers: {people.Count(p => p.Type == PersonType.Producer)})");
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
                            movie.SetProviderId(MetadataProviders.Imdb, value);
                            break;
                        case "tmdb":
                            movie.SetProviderId(MetadataProviders.Tmdb, value);
                            break;
                        default:
                            movie.SetProviderId(type, value);
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

                // NFO Standard only uses video filename.nfo, not movie.nfo
            }
            // For directory-based movies, we can't determine the video filename
            // NFO Standard requires the NFO to match the video filename

            return null;
        }

        public bool HasChanged(BaseItem item, LibraryOptions libraryOptions, IDirectoryService directoryService)
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