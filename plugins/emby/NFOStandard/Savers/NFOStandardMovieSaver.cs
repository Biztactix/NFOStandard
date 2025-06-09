using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using MediaBrowser.Controller.Configuration;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.Entities.Movies;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;
using MediaBrowser.Model.Configuration;

namespace NFOStandard.Savers
{
    /// <summary>
    /// NFO Standard movie metadata saver for Emby/Jellyfin
    /// </summary>
    public class NFOStandardMovieSaver : IMetadataSaver
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private readonly IServerConfigurationManager _config;
        private readonly ILibraryManager _libraryManager;
        private const string NFONamespace = "NFOStandard";

        public string Name => "NFO Standard";

        public NFOStandardMovieSaver(
            ILogger logger, 
            IFileSystem fileSystem,
            IServerConfigurationManager config,
            ILibraryManager libraryManager)
        {
            _logger = logger;
            _fileSystem = fileSystem;
            _config = config;
            _libraryManager = libraryManager;
        }

        public string GetSavePath(BaseItem item)
        {
            return GetMovieNfoPath(item.Path);
        }

        public bool IsEnabledFor(BaseItem item, ItemUpdateType updateType)
        {
            return item is Movie && updateType >= ItemUpdateType.MetadataDownload;
        }

        public Task Save(BaseItem item, LibraryOptions libraryOptions, CancellationToken cancellationToken)
        {
            var movie = item as Movie;
            if (movie == null)
            {
                return Task.CompletedTask;
            }

            var path = GetMovieNfoPath(item.Path);
            if (string.IsNullOrEmpty(path))
            {
                return Task.CompletedTask;
            }

            var directory = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var xml = GenerateNfoXml(movie);
            
            var settings = new XmlWriterSettings
            {
                Indent = true,
                IndentChars = "    ",
                Encoding = System.Text.Encoding.UTF8,
                OmitXmlDeclaration = false
            };

            using (var writer = XmlWriter.Create(path, settings))
            {
                xml.WriteTo(writer);
            }

            _logger.Info($"Saved NFO for {movie.Name} to {path}");
            
            return Task.CompletedTask;
        }

        private XDocument GenerateNfoXml(Movie movie)
        {
            var ns = XNamespace.Get(NFONamespace);
            var xsi = XNamespace.Get("http://www.w3.org/2001/XMLSchema-instance");
            
            var root = new XElement(ns + "root",
                new XAttribute(XNamespace.Xmlns + "xsi", xsi),
                new XAttribute(xsi + "schemaLocation", "NFOStandard https://xsd.nfostandard.com/main.xsd"));

            var media = new XElement("media");
            root.Add(media);

            var movieElement = new XElement("movie");
            media.Add(movieElement);

            // Basic info
            AddElement(movieElement, "title", movie.Name);
            AddElement(movieElement, "originaltitle", movie.OriginalTitle);
            AddElement(movieElement, "sorttitle", movie.SortName);
            
            if (movie.ProductionYear.HasValue)
            {
                AddElement(movieElement, "year", movie.ProductionYear.Value.ToString());
            }

            AddElement(movieElement, "plot", movie.Overview);
            AddElement(movieElement, "tagline", movie.Tagline);
            
            if (movie.RunTimeTicks.HasValue)
            {
                var runtime = TimeSpan.FromTicks(movie.RunTimeTicks.Value).TotalMinutes;
                AddElement(movieElement, "runtime", ((int)runtime).ToString());
            }

            // Ratings
            if (movie.CommunityRating.HasValue)
            {
                var ratingElement = new XElement("rating",
                    new XAttribute("name", "imdb"),
                    new XAttribute("value", movie.CommunityRating.Value.ToString("F1")),
                    new XAttribute("default", "true"));
                movieElement.Add(ratingElement);
            }

            if (!string.IsNullOrEmpty(movie.CustomRating))
            {
                AddElement(movieElement, "userrating", movie.CustomRating);
            }

            // Content rating
            if (!string.IsNullOrEmpty(movie.OfficialRating))
            {
                var (countryCode, board) = GetContentRatingInfo(movie.OfficialRating);
                var contentRating = new XElement("contentrating",
                    new XAttribute("country", countryCode),
                    new XAttribute("board", board),
                    new XAttribute("rating", movie.OfficialRating));
                movieElement.Add(contentRating);
            }

            // Genres
            foreach (var genre in movie.Genres ?? Array.Empty<string>())
            {
                AddElement(movieElement, "genre", genre);
            }

            // Tags
            foreach (var tag in movie.Tags ?? Array.Empty<string>())
            {
                AddElement(movieElement, "tag", tag);
            }

            // Studios
            foreach (var studio in movie.Studios ?? Array.Empty<string>())
            {
                AddElement(movieElement, "productioncompany", studio);
            }

            // Release date
            if (movie.PremiereDate.HasValue)
            {
                AddElement(movieElement, "releasedate", movie.PremiereDate.Value.ToString("yyyy-MM-dd"));
            }

            // Collection - not available in Emby 4.8
            // Would need to query collections separately

            // Provider IDs
            // Provider IDs
            var imdbId = movie.GetProviderId(MetadataProviders.Imdb);
            if (!string.IsNullOrEmpty(imdbId))
            {
                movieElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "imdb"),
                    new XAttribute("default", "true"),
                    imdbId));
            }
            
            var tmdbId = movie.GetProviderId(MetadataProviders.Tmdb);
            if (!string.IsNullOrEmpty(tmdbId))
            {
                movieElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "tmdb"),
                    tmdbId));
            }

            // People/actors are not directly accessible in Emby 4.8
            // The GetPeople method has a different signature than expected
            // This would require additional research to implement properly

            return new XDocument(
                new XDeclaration("1.0", "UTF-8", null),
                root);
        }

        private void AddElement(XElement parent, string name, string value)
        {
            if (!string.IsNullOrWhiteSpace(value))
            {
                parent.Add(new XElement(name, value));
            }
        }

        private (string countryCode, string board) GetContentRatingInfo(string rating)
        {
            if (string.IsNullOrEmpty(rating))
                return ("US", "MPAA");

            var upperRating = rating.ToUpperInvariant();

            // German ratings (FSK) - check first as they have specific prefixes
            if (upperRating.StartsWith("FSK") || 
                upperRating is "FSK0" or "FSK6" or "FSK12" or "FSK16" or "FSK18")
                return ("DE", "FSK");

            // Australian ratings (specific patterns)
            if (upperRating is "MA15+" or "R18+" or "X18+" ||
                rating.Contains("15+", StringComparison.OrdinalIgnoreCase) || 
                rating.Contains("18+", StringComparison.OrdinalIgnoreCase))
                return ("AU", "OFLC");

            // Canadian ratings (specific patterns)
            if (upperRating is "14A" or "18A" ||
                (upperRating.StartsWith("14") && upperRating != "14") ||
                (upperRating.StartsWith("18") && upperRating != "18"))
                return ("CA", "CHVRS");

            // UK ratings (BBFC) - specific to UK
            if (upperRating is "U" or "12A" or "R18")
                return ("GB", "BBFC");

            // Japanese ratings (specific patterns)
            if (upperRating is "PG12" or "R15+" or "R18+")
                return ("JP", "EIRIN");

            // French ratings (specific patterns)
            if (upperRating is "TP" || rating.Contains("TOUS", StringComparison.OrdinalIgnoreCase))
                return ("FR", "CSA");

            // US ratings (MPAA) - most common, check after specific patterns
            if (upperRating is "G" or "PG" or "PG-13" or "R" or "NC-17" or "NR" or "UNRATED")
                return ("US", "MPAA");

            // Ambiguous ratings that could be multiple countries - use context or default to US
            if (upperRating is "12" or "15" or "16" or "18")
            {
                // These could be UK, FR, or other systems - default to US for now
                // In a real implementation, you might want to use library settings or metadata source
                return ("US", "MPAA");
            }

            // Australian general ratings
            if (upperRating is "M")
                return ("AU", "OFLC");

            // Default to US if we can't determine
            return ("US", "MPAA");
        }

        private string GetMovieNfoPath(string moviePath)
        {
            if (string.IsNullOrWhiteSpace(moviePath))
            {
                return null;
            }

            // For file, use same name with .nfo extension
            if (_fileSystem.FileExists(moviePath))
            {
                return Path.ChangeExtension(moviePath, ".nfo");
            }
            // For directory-based movies, we can't save NFO
            // NFO Standard requires matching the video filename

            return null;
        }
    }
}