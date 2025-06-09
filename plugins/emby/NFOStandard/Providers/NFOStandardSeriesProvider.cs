using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Xml.Linq;
using MediaBrowser.Controller.Entities;
using MediaBrowser.Controller.Entities.TV;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using MediaBrowser.Model.Logging;
using MediaBrowser.Model.Configuration;

namespace NFOStandard.Providers
{
    /// <summary>
    /// NFO Standard TV series metadata provider for Emby/Jellyfin
    /// </summary>
    public class NFOStandardSeriesProvider : ILocalMetadataProvider<Series>, IHasItemChangeMonitor
    {
        private readonly ILogger _logger;
        private readonly IFileSystem _fileSystem;
        private readonly ILibraryManager _libraryManager;
        private const string NFONamespace = "NFOStandard";

        public string Name => "NFO Standard";

        public NFOStandardSeriesProvider(ILogger logger, IFileSystem fileSystem, ILibraryManager libraryManager)
        {
            _logger = logger;
            _fileSystem = fileSystem;
            _libraryManager = libraryManager;
        }

        public Task<MetadataResult<Series>> GetMetadata(ItemInfo info, LibraryOptions libraryOptions, IDirectoryService directoryService, CancellationToken cancellationToken)
        {
            var result = new MetadataResult<Series>();
            
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

                var tvshowElement = root.Descendants(XName.Get("tvshow", NFONamespace)).FirstOrDefault();
                if (tvshowElement == null)
                {
                    tvshowElement = root.Descendants("tvshow").FirstOrDefault();
                }

                if (tvshowElement != null)
                {
                    var series = new Series();
                    ParseSeriesElement(series, tvshowElement, result);
                    
                    result.HasMetadata = true;
                    result.Item = series;
                }
            }
            catch (Exception ex)
            {
                _logger.ErrorException($"Error parsing NFO file: {nfoPath}", ex);
            }

            return Task.FromResult(result);
        }

        private void ParseSeriesElement(Series series, XElement tvshowElement, MetadataResult<Series> result)
        {
            // Title
            series.Name = GetElementValue(tvshowElement, "title");
            series.OriginalTitle = GetElementValue(tvshowElement, "originaltitle");
            series.SortName = GetElementValue(tvshowElement, "sorttitle");

            // Year
            var yearStr = GetElementValue(tvshowElement, "year");
            if (int.TryParse(yearStr, out var year))
            {
                series.ProductionYear = year;
            }

            // Overview
            series.Overview = GetElementValue(tvshowElement, "plot");
            if (string.IsNullOrEmpty(series.Overview))
            {
                series.Overview = GetElementValue(tvshowElement, "outline");
            }

            // Tagline
            series.Tagline = GetElementValue(tvshowElement, "tagline");

            // Runtime
            var runtimeStr = GetElementValue(tvshowElement, "runtime");
            if (long.TryParse(runtimeStr, out var runtime))
            {
                series.RunTimeTicks = TimeSpan.FromMinutes(runtime).Ticks;
            }

            // Status
            var status = GetElementValue(tvshowElement, "status");
            if (!string.IsNullOrWhiteSpace(status))
            {
                if (status.Equals("ended", StringComparison.OrdinalIgnoreCase) ||
                    status.Equals("canceled", StringComparison.OrdinalIgnoreCase) ||
                    status.Equals("cancelled", StringComparison.OrdinalIgnoreCase))
                {
                    series.Status = SeriesStatus.Ended;
                }
                else if (status.Equals("continuing", StringComparison.OrdinalIgnoreCase) ||
                         status.Equals("returning series", StringComparison.OrdinalIgnoreCase))
                {
                    series.Status = SeriesStatus.Continuing;
                }
            }

            // Ratings
            ParseRatings(series, tvshowElement);

            // Content rating
            ParseContentRating(series, tvshowElement);

            // Genres
            series.Genres = tvshowElement.Elements("genre")
                .Select(e => e.Value)
                .Where(g => !string.IsNullOrWhiteSpace(g))
                .ToArray();

            // Tags
            series.Tags = tvshowElement.Elements("tag")
                .Select(e => e.Value)
                .Where(t => !string.IsNullOrWhiteSpace(t))
                .ToArray();

            // Studios
            var studios = tvshowElement.Elements("studio")
                .Select(e => e.Value)
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .ToList();
            
            if (studios.Any())
            {
                series.Studios = studios.ToArray();
            }

            // People
            ParsePeople(series, tvshowElement, result);

            // Premiered date
            var premieredStr = GetElementValue(tvshowElement, "premiered");
            if (DateTime.TryParse(premieredStr, out var premiered))
            {
                series.PremiereDate = premiered;
            }

            // Air time
            ParseAirSchedule(series, tvshowElement);

            // Provider IDs
            ParseProviderIds(series, tvshowElement);
        }

        private void ParseRatings(Series series, XElement tvshowElement)
        {
            var ratings = tvshowElement.Elements("rating");
            foreach (var rating in ratings)
            {
                var name = rating.Attribute("name")?.Value ?? "default";
                var valueStr = rating.Attribute("value")?.Value;
                var isDefault = rating.Attribute("default")?.Value == "true";

                if (float.TryParse(valueStr, out var value))
                {
                    if (isDefault || name == "tvdb" || name == "imdb")
                    {
                        series.CommunityRating = value;
                    }
                }
            }

            // User rating
            var userRatingStr = GetElementValue(tvshowElement, "userrating");
            if (float.TryParse(userRatingStr, out var userRating))
            {
                series.CustomRating = userRatingStr;
            }
        }

        private void ParseContentRating(Series series, XElement tvshowElement)
        {
            var contentRating = tvshowElement.Elements("contentrating").FirstOrDefault();
            if (contentRating != null)
            {
                var rating = contentRating.Attribute("rating")?.Value ?? contentRating.Value;
                if (!string.IsNullOrWhiteSpace(rating))
                {
                    series.OfficialRating = rating;
                }
            }
        }

        private void ParsePeople(Series series, XElement tvshowElement, MetadataResult<Series> result)
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
            foreach (var actor in tvshowElement.Elements("actor"))
            {
                if (actorCount >= maxActors)
                {
                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Reached maximum actor limit ({maxActors}) for series: {series.Name}");
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

            // Creators
            foreach (var creator in tvshowElement.Elements("creator"))
            {
                var name = GetElementValue(creator, "name");
                if (!string.IsNullOrWhiteSpace(name))
                {
                    var person = new PersonInfo
                    {
                        Name = name,
                        Type = PersonType.Producer // Creators are treated as producers in Emby
                    };

                    // Handle creator thumb/image
                    var thumb = GetElementValue(creator, "thumb");
                    if (!string.IsNullOrWhiteSpace(thumb))
                    {
                        person.ImageUrl = thumb;
                    }

                    people.Add(person);

                    if (config?.EnableDetailedLogging == true)
                    {
                        _logger.Debug($"Added creator: {name}");
                    }
                }
            }

            // Directors (for series-level directors)
            foreach (var director in tvshowElement.Elements("director"))
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

            // Producers
            foreach (var producer in tvshowElement.Elements("producer"))
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

                _logger.Info($"Loaded {people.Count} people for series: {series.Name} (Actors: {actorCount}, Creators: {people.Count(p => p.Type == PersonType.Producer)}, Directors: {people.Count(p => p.Type == PersonType.Director)})");
            }
        }

        private void ParseAirSchedule(Series series, XElement tvshowElement)
        {
            var schedule = tvshowElement.Element("schedule");
            if (schedule != null)
            {
                var airDay = GetElementValue(schedule, "airday");
                var airTime = GetElementValue(schedule, "airtime");

                if (!string.IsNullOrWhiteSpace(airDay))
                {
                    series.AirDays = new[] { (DayOfWeek)Enum.Parse(typeof(DayOfWeek), airDay, true) };
                }

                if (!string.IsNullOrWhiteSpace(airTime))
                {
                    series.AirTime = airTime;
                }
            }
        }

        private void ParseProviderIds(Series series, XElement tvshowElement)
        {
            foreach (var uniqueId in tvshowElement.Elements("uniqueid"))
            {
                var type = uniqueId.Attribute("type")?.Value;
                var value = uniqueId.Value;

                if (!string.IsNullOrWhiteSpace(type) && !string.IsNullOrWhiteSpace(value))
                {
                    switch (type.ToLowerInvariant())
                    {
                        case "imdb":
                            series.SetProviderId(MetadataProviders.Imdb, value);
                            break;
                        case "tvdb":
                            series.SetProviderId(MetadataProviders.Tvdb, value);
                            break;
                        case "tmdb":
                            series.SetProviderId(MetadataProviders.Tmdb, value);
                            break;
                        default:
                            series.SetProviderId(type, value);
                            break;
                    }
                }
            }
        }

        private string GetElementValue(XElement parent, string elementName)
        {
            return parent.Element(elementName)?.Value?.Trim();
        }

        private string GetNfoPath(string seriesPath)
        {
            if (string.IsNullOrWhiteSpace(seriesPath) || !_fileSystem.DirectoryExists(seriesPath))
            {
                return null;
            }

            var nfoPath = Path.Combine(seriesPath, "tvshow.nfo");
            if (_fileSystem.FileExists(nfoPath))
            {
                return nfoPath;
            }

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