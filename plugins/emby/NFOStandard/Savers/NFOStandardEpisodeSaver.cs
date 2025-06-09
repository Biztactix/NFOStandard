using System;
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
using MediaBrowser.Model.Configuration;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;

namespace NFOStandard.Savers
{
    /// <summary>
    /// NFO Standard episode metadata saver for Emby
    /// </summary>
    public class NFOStandardEpisodeSaver : IMetadataSaver
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private readonly IServerConfigurationManager _config;
        private readonly ILibraryManager _libraryManager;
        private const string NFONamespace = "NFOStandard";

        /// <summary>
        /// Gets the name of this saver
        /// </summary>
        public string Name => "NFO Standard";

        /// <summary>
        /// Initializes a new instance of the <see cref="NFOStandardEpisodeSaver"/> class.
        /// </summary>
        public NFOStandardEpisodeSaver(
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

        /// <summary>
        /// Gets the save path for the NFO file
        /// </summary>
        public string GetSavePath(BaseItem item)
        {
            return GetEpisodeNfoPath(item.Path);
        }

        /// <summary>
        /// Determines if saving is enabled for this item
        /// </summary>
        public bool IsEnabledFor(BaseItem item, ItemUpdateType updateType)
        {
            return item is Episode && updateType >= ItemUpdateType.MetadataDownload;
        }

        /// <summary>
        /// Saves the episode metadata to NFO file
        /// </summary>
        public Task Save(BaseItem item, LibraryOptions libraryOptions, CancellationToken cancellationToken)
        {
            var episode = item as Episode;
            if (episode == null)
            {
                return Task.CompletedTask;
            }

            var path = GetEpisodeNfoPath(item.Path);
            if (string.IsNullOrEmpty(path))
            {
                return Task.CompletedTask;
            }

            var directory = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(directory))
            {
                Directory.CreateDirectory(directory);
            }

            var xml = GenerateNfoXml(episode);
            
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

            _logger.Info($"Saved NFO for {episode.Name} to {path}");
            
            return Task.CompletedTask;
        }

        private XDocument GenerateNfoXml(Episode episode)
        {
            var ns = XNamespace.Get(NFONamespace);
            var xsi = XNamespace.Get("http://www.w3.org/2001/XMLSchema-instance");
            
            var root = new XElement(ns + "root",
                new XAttribute(XNamespace.Xmlns + "xsi", xsi),
                new XAttribute(xsi + "schemaLocation", "NFOStandard https://xsd.nfostandard.com/main.xsd"));

            var media = new XElement("media");
            root.Add(media);

            var episodeElement = new XElement("episode");
            media.Add(episodeElement);

            // Basic info
            AddElement(episodeElement, "title", episode.Name);
            
            // Season and episode numbers
            if (episode.ParentIndexNumber.HasValue)
            {
                AddElement(episodeElement, "season", episode.ParentIndexNumber.Value.ToString());
            }
            
            if (episode.IndexNumber.HasValue)
            {
                AddElement(episodeElement, "episode", episode.IndexNumber.Value.ToString());
            }

            // Air date
            if (episode.PremiereDate.HasValue)
            {
                AddElement(episodeElement, "aired", episode.PremiereDate.Value.ToString("yyyy-MM-dd"));
            }

            AddElement(episodeElement, "plot", episode.Overview);
            
            if (episode.RunTimeTicks.HasValue)
            {
                var runtime = TimeSpan.FromTicks(episode.RunTimeTicks.Value).TotalMinutes;
                AddElement(episodeElement, "runtime", ((int)runtime).ToString());
            }

            // Ratings
            if (episode.CommunityRating.HasValue)
            {
                var ratingElement = new XElement("rating",
                    new XAttribute("name", "tvdb"),
                    new XAttribute("value", episode.CommunityRating.Value.ToString("F1")),
                    new XAttribute("default", "true"));
                episodeElement.Add(ratingElement);
            }

            if (!string.IsNullOrEmpty(episode.CustomRating))
            {
                AddElement(episodeElement, "userrating", episode.CustomRating);
            }

            // Directors and Writers are not available on Episode class in Emby 4.8
            // These would need to be retrieved from the parent series or through other means

            // Provider IDs
            var tvdbId = episode.GetProviderId(MetadataProviders.Tvdb);
            if (!string.IsNullOrEmpty(tvdbId))
            {
                episodeElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "tvdb"),
                    new XAttribute("default", "true"),
                    tvdbId));
            }
            
            var imdbId = episode.GetProviderId(MetadataProviders.Imdb);
            if (!string.IsNullOrEmpty(imdbId))
            {
                episodeElement.Add(new XElement("uniqueid",
                    new XAttribute("type", "imdb"),
                    imdbId));
            }

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

        private string GetEpisodeNfoPath(string episodePath)
        {
            if (string.IsNullOrWhiteSpace(episodePath))
            {
                return null;
            }

            // For episode file, use same name with .nfo extension
            if (_fileSystem.FileExists(episodePath))
            {
                return Path.ChangeExtension(episodePath, ".nfo");
            }

            return null;
        }
    }
}