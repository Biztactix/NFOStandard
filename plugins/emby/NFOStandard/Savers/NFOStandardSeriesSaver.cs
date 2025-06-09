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
using MediaBrowser.Controller.Entities.TV;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;
using MediaBrowser.Model.Configuration;

namespace NFOStandard.Savers
{
    /// <summary>
    /// NFO Standard TV series metadata saver for Emby/Jellyfin
    /// </summary>
    public class NFOStandardSeriesSaver : IMetadataSaver
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private readonly IServerConfigurationManager _config;
        private readonly ILibraryManager _libraryManager;
        private const string NFONamespace = "NFOStandard";

        public string Name => "NFO Standard";

        public NFOStandardSeriesSaver(
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
            return GetSeriesNfoPath(item.Path);
        }

        public bool IsEnabledFor(BaseItem item, ItemUpdateType updateType)
        {
            return item is Series && updateType >= ItemUpdateType.MetadataDownload;
        }

        public Task Save(BaseItem item, LibraryOptions libraryOptions, CancellationToken cancellationToken)
        {
            var series = item as Series;
            if (series == null)
            {
                return Task.CompletedTask;
            }

            var path = GetSeriesNfoPath(item.Path);
            if (string.IsNullOrEmpty(path))
            {
                return Task.CompletedTask;
            }

            var directory = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var xml = GenerateNfoXml(series);
            
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

            _logger.Info($"Saved NFO for {series.Name} to {path}");
            
            return Task.CompletedTask;
        }

        private XDocument GenerateNfoXml(Series series)
        {
            var ns = XNamespace.Get(NFONamespace);
            var xsi = XNamespace.Get("http://www.w3.org/2001/XMLSchema-instance");
            
            var root = new XElement(ns + "root",
                new XAttribute(XNamespace.Xmlns + "xsi", xsi),
                new XAttribute(xsi + "schemaLocation", "NFOStandard https://xsd.nfostandard.com/main.xsd"));

            var media = new XElement("media");
            root.Add(media);

            var tvshowElement = new XElement("tvshow");
            media.Add(tvshowElement);

            // Basic info
            AddElement(tvshowElement, "title", series.Name);
            AddElement(tvshowElement, "originaltitle", series.OriginalTitle);
            AddElement(tvshowElement, "sorttitle", series.SortName);
            
            if (series.ProductionYear.HasValue)
            {
                AddElement(tvshowElement, "year", series.ProductionYear.Value.ToString());
            }

            AddElement(tvshowElement, "plot", series.Overview);
            AddElement(tvshowElement, "tagline", series.Tagline);
            
            if (series.RunTimeTicks.HasValue)
            {
                var runtime = TimeSpan.FromTicks(series.RunTimeTicks.Value).TotalMinutes;
                AddElement(tvshowElement, "runtime", ((int)runtime).ToString());
            }

            // Status
            if (series.Status.HasValue)
            {
                var status = series.Status.Value == SeriesStatus.Ended ? "ended" : "continuing";
                AddElement(tvshowElement, "status", status);
            }

            // Ratings
            if (series.CommunityRating.HasValue)
            {
                var ratingElement = new XElement("rating",
                    new XAttribute("name", "tvdb"),
                    new XAttribute("value", series.CommunityRating.Value.ToString("F1")),
                    new XAttribute("default", "true"));
                tvshowElement.Add(ratingElement);
            }

            if (!string.IsNullOrEmpty(series.CustomRating))
            {
                AddElement(tvshowElement, "userrating", series.CustomRating);
            }

            // Content rating
            if (!string.IsNullOrEmpty(series.OfficialRating))
            {
                var (countryCode, board) = GetContentRatingInfo(series.OfficialRating, true);
                var contentRating = new XElement("contentrating",
                    new XAttribute("country", countryCode),
                    new XAttribute("board", board),
                    new XAttribute("rating", series.OfficialRating));
                tvshowElement.Add(contentRating);
            }

            // Genres
            foreach (var genre in series.Genres ?? Array.Empty<string>())
            {
                AddElement(tvshowElement, "genre", genre);
            }

            // Tags
            foreach (var tag in series.Tags ?? Array.Empty<string>())
            {
                AddElement(tvshowElement, "tag", tag);
            }

            // Studios
            foreach (var studio in series.Studios ?? Array.Empty<string>())
            {
                AddElement(tvshowElement, "studio", studio);
            }

            // Premiered date
            if (series.PremiereDate.HasValue)
            {
                AddElement(tvshowElement, "premiered", series.PremiereDate.Value.ToString("yyyy-MM-dd"));
            }

            // Air schedule
            if (series.AirDays != null && series.AirDays.Any())
            {
                var schedule = new XElement("schedule");
                AddElement(schedule, "airday", series.AirDays.First().ToString());
                if (!string.IsNullOrEmpty(series.AirTime))
                {
                    AddElement(schedule, "airtime", series.AirTime);
                }
                tvshowElement.Add(schedule);
            }

            // Provider IDs
            // Provider IDs
            var tvdbId = series.GetProviderId(MetadataProviders.Tvdb);
            if (!string.IsNullOrEmpty(tvdbId))
            {
                tvshowElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "tvdb"),
                    new XAttribute("default", "true"),
                    tvdbId));
            }
            
            var imdbId = series.GetProviderId(MetadataProviders.Imdb);
            if (!string.IsNullOrEmpty(imdbId))
            {
                tvshowElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "imdb"),
                    imdbId));
            }
            
            var tmdbId = series.GetProviderId(MetadataProviders.Tmdb);
            if (!string.IsNullOrEmpty(tmdbId))
            {
                tvshowElement.Add(new XElement("uniqueid",
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

        private (string countryCode, string board) GetContentRatingInfo(string rating, bool isTvSeries = false)
        {
            if (string.IsNullOrEmpty(rating))
                return ("US", isTvSeries ? "FCC" : "MPAA");

            var upperRating = rating.ToUpperInvariant();

            // US TV ratings (FCC/TV Parental Guidelines)
            if (isTvSeries && (upperRating is "TV-Y" or "TV-Y7" or "TV-G" or "TV-PG" or "TV-14" or "TV-MA"))
                return ("US", "FCC");

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
                return ("US", isTvSeries ? "FCC" : "MPAA");
            }

            // Australian general ratings
            if (upperRating is "M")
                return ("AU", "OFLC");

            // Default to US if we can't determine
            return ("US", isTvSeries ? "FCC" : "MPAA");
        }

        private string GetSeriesNfoPath(string seriesPath)
        {
            if (string.IsNullOrWhiteSpace(seriesPath) || !_fileSystem.DirectoryExists(seriesPath))
            {
                return null;
            }

            return Path.Combine(seriesPath, "tvshow.nfo");
        }
    }
}