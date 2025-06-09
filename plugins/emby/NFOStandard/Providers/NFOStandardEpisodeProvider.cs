using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.Entities.TV;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.Configuration;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;

namespace NFOStandard.Providers
{
    /// <summary>
    /// NFO Standard episode metadata provider for Emby
    /// </summary>
    public class NFOStandardEpisodeProvider : ILocalMetadataProvider<Episode>, IHasItemChangeMonitor
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private const string NFONamespace = "NFOStandard";

        /// <summary>
        /// Gets the name of this provider
        /// </summary>
        public string Name => "NFO Standard";

        /// <summary>
        /// Initializes a new instance of the <see cref="NFOStandardEpisodeProvider"/> class.
        /// </summary>
        public NFOStandardEpisodeProvider(ILogger logger, IFileSystem fileSystem)
        {
            _logger = logger;
            _fileSystem = fileSystem;
        }

        /// <summary>
        /// Gets metadata for an episode from NFO file
        /// </summary>
        public Task<MetadataResult<Episode>> GetMetadata(ItemInfo info, LibraryOptions libraryOptions, IDirectoryService directoryService, CancellationToken cancellationToken)
        {
            var result = new MetadataResult<Episode>();
            
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

                var episodeElement = root.Descendants(XName.Get("episode", NFONamespace)).FirstOrDefault();
                if (episodeElement == null)
                {
                    episodeElement = root.Descendants("episode").FirstOrDefault();
                }

                if (episodeElement != null)
                {
                    var episode = new Episode();
                    ParseEpisodeElement(episode, episodeElement);
                    
                    result.HasMetadata = true;
                    result.Item = episode;
                }
            }
            catch (Exception ex)
            {
                _logger.ErrorException($"Error parsing NFO file: {nfoPath}", ex);
            }

            return Task.FromResult(result);
        }

        private void ParseEpisodeElement(Episode episode, XElement episodeElement)
        {
            // Title
            episode.Name = GetElementValue(episodeElement, "title");

            // Episode and season numbers
            var seasonStr = GetElementValue(episodeElement, "season");
            if (int.TryParse(seasonStr, out var season))
            {
                episode.ParentIndexNumber = season;
            }

            var episodeStr = GetElementValue(episodeElement, "episode");
            if (int.TryParse(episodeStr, out var episodeNum))
            {
                episode.IndexNumber = episodeNum;
            }

            // Air date
            var airedStr = GetElementValue(episodeElement, "aired");
            if (DateTime.TryParse(airedStr, out var aired))
            {
                episode.PremiereDate = aired;
            }

            // Plot
            episode.Overview = GetElementValue(episodeElement, "plot");

            // Runtime
            var runtimeStr = GetElementValue(episodeElement, "runtime");
            if (long.TryParse(runtimeStr, out var runtime))
            {
                episode.RunTimeTicks = TimeSpan.FromMinutes(runtime).Ticks;
            }

            // Ratings
            ParseRatings(episode, episodeElement);

            // Directors and Writers would be parsed here
            // but Episode class in Emby 4.8 doesn't have these properties

            // Provider IDs
            ParseProviderIds(episode, episodeElement);
        }

        private void ParseRatings(Episode episode, XElement episodeElement)
        {
            var ratings = episodeElement.Elements("rating");
            foreach (var rating in ratings)
            {
                var name = rating.Attribute("name")?.Value ?? "default";
                var valueStr = rating.Attribute("value")?.Value;
                var isDefault = rating.Attribute("default")?.Value == "true";

                if (float.TryParse(valueStr, out var value) && value <= 10)
                {
                    if (isDefault || name == "tvdb")
                    {
                        episode.CommunityRating = value;
                    }
                }
            }

            // User rating
            var userRatingStr = GetElementValue(episodeElement, "userrating");
            if (float.TryParse(userRatingStr, out var userRating))
            {
                episode.CustomRating = userRatingStr;
            }
        }

        private void ParseProviderIds(Episode episode, XElement episodeElement)
        {
            foreach (var uniqueId in episodeElement.Elements("uniqueid"))
            {
                var type = uniqueId.Attribute("type")?.Value;
                var value = uniqueId.Value;

                if (!string.IsNullOrWhiteSpace(type) && !string.IsNullOrWhiteSpace(value))
                {
                    switch (type.ToLowerInvariant())
                    {
                        case "imdb":
                            episode.SetProviderId(MetadataProviders.Imdb, value);
                            break;
                        case "tvdb":
                            episode.SetProviderId(MetadataProviders.Tvdb, value);
                            break;
                        case "tmdb":
                            episode.SetProviderId(MetadataProviders.Tmdb, value);
                            break;
                        default:
                            episode.SetProviderId(type, value);
                            break;
                    }
                }
            }
        }

        private string GetElementValue(XElement parent, string elementName)
        {
            return parent.Element(elementName)?.Value?.Trim();
        }

        private string GetNfoPath(string episodePath)
        {
            if (string.IsNullOrWhiteSpace(episodePath))
            {
                return null;
            }

            // For episode file, check same name with .nfo extension
            if (_fileSystem.FileExists(episodePath))
            {
                var nfoPath = Path.ChangeExtension(episodePath, ".nfo");
                if (_fileSystem.FileExists(nfoPath))
                {
                    return nfoPath;
                }
            }

            return null;
        }

        /// <summary>
        /// Checks if the NFO file has changed since last scan
        /// </summary>
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