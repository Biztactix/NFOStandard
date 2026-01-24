using System;
using System.Collections.Generic;
using System.Xml.Schema;
using System.Xml.Serialization;

namespace NFOStandard.Xml;

[XmlRoot("root", Namespace = NfoConstants.Namespace)]
public sealed class NfoRoot
{
    [XmlElement("media")]
    public Media Media { get; set; } = new();

    [XmlElement("library")]
    public List<LibraryMetadata> Library { get; set; } = new();

    [XmlElement("stats")]
    public List<Stats> Stats { get; set; } = new();

    [XmlAttribute("schemaLocation", Namespace = XmlSchema.InstanceNamespace)]
    public string? SchemaLocation { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Media
{
    [XmlElement("movie")]
    public Movie? Movie { get; set; }

    [XmlElement("tvshow")]
    public TvShow? TvShow { get; set; }

    [XmlElement("adult")]
    public Adult? Adult { get; set; }

    [XmlElement("anime")]
    public Anime? Anime { get; set; }

    [XmlElement("video")]
    public Video? Video { get; set; }

    [XmlElement("music")]
    public Music? Music { get; set; }

    [XmlElement("audiobook")]
    public Audiobook? Audiobook { get; set; }

    [XmlElement("podcast")]
    public Podcast? Podcast { get; set; }

    [XmlElement("musicvideo")]
    public MusicVideo? MusicVideo { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Rating
{
    [XmlAttribute("name")]
    public string? Name { get; set; }

    [XmlAttribute("value")]
    public decimal Value { get; set; }

    [XmlAttribute("max")]
    public int? Max { get; set; }

    [XmlAttribute("votes")]
    public int? Votes { get; set; }

    [XmlAttribute("default")]
    public bool? IsDefault { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class UniqueId
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("type")]
    public string? Type { get; set; }

    [XmlAttribute("default")]
    public bool? IsDefault { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class ContentRating
{
    [XmlElement("rating")]
    public string? Rating { get; set; }

    [XmlElement("reason")]
    public string? Reason { get; set; }

    [XmlElement("image")]
    public string? Image { get; set; }

    [XmlAttribute("country")]
    public string? Country { get; set; }

    [XmlAttribute("board")]
    public string? Board { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class MediaFile
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("type")]
    public string? Type { get; set; }

    [XmlAttribute("width")]
    public int? Width { get; set; }

    [XmlAttribute("height")]
    public int? Height { get; set; }

    [XmlAttribute("url")]
    public string? Url { get; set; }

    [XmlAttribute("season")]
    public string? Season { get; set; }

    [XmlAttribute("language")]
    public string? Language { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Person
{
    [XmlElement("name")]
    public string? Name { get; set; }

    [XmlElement("role")]
    public string? Role { get; set; }

    [XmlElement("order")]
    public int? Order { get; set; }

    [XmlElement("thumb")]
    public string? Thumb { get; set; }

    [XmlElement("bio")]
    public string? Bio { get; set; }

    [XmlElement("url")]
    public List<string> Urls { get; set; } = new();

    [XmlElement("gender")]
    public string? Gender { get; set; }

    [XmlElement("tag")]
    public List<string> Tags { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class LibraryMetadata
{
    [XmlElement("appID")]
    public string? AppId { get; set; }

    [XmlElement("uniqueid")]
    public string? UniqueId { get; set; }

    [XmlElement("libraryid")]
    public string? LibraryId { get; set; }

    [XmlElement("librarysubid")]
    public string? LibrarySubId { get; set; }

    [XmlElement("dateAdded")]
    public DateTime? DateAdded { get; set; }

    [XmlElement("dateUpdated")]
    public DateTime? DateUpdated { get; set; }

    [XmlElement("lastMetadataScan")]
    public DateTime? LastMetadataScan { get; set; }

    [XmlElement("lastChapterSearch")]
    public DateTime? LastChapterSearch { get; set; }

    [XmlElement("lastIntroSearch")]
    public DateTime? LastIntroSearch { get; set; }

    [XmlElement("thumbnails")]
    public List<MediaFile> Thumbnails { get; set; } = new();

    [XmlElement("fanart")]
    public List<MediaFile> Fanart { get; set; } = new();

    [XmlElement("banner")]
    public List<MediaFile> Banner { get; set; } = new();

    [XmlElement("internalLink")]
    public string? InternalLink { get; set; }

    [XmlElement("externalLink")]
    public string? ExternalLink { get; set; }

    [XmlElement("tags")]
    public List<string> Tags { get; set; } = new();

    [XmlElement("liked")]
    public int? Liked { get; set; }

    [XmlElement("duration")]
    public List<long> Duration { get; set; } = new();

    [XmlElement("collection")]
    public LibraryCollection? Collection { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class LibraryCollection
{
    [XmlAttribute("name")]
    public string? Name { get; set; }

    [XmlAttribute("id")]
    public string? Id { get; set; }

    [XmlAttribute("description")]
    public string? Description { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Stats
{
    [XmlElement("watchCount")]
    public int? WatchCount { get; set; }

    [XmlElement("liked")]
    public bool? Liked { get; set; }

    [XmlElement("userRating")]
    public decimal? UserRating { get; set; }

    [XmlElement("watched")]
    public bool? Watched { get; set; }

    [XmlElement("progress")]
    public decimal? Progress { get; set; }

    [XmlAttribute("userId")]
    public string? UserId { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class TimedMarker
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("start")]
    public int Start { get; set; }

    [XmlAttribute("end")]
    public int End { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Chapter
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("name")]
    public string? Name { get; set; }

    [XmlAttribute("start")]
    public int Start { get; set; }

    [XmlAttribute("end")]
    public int End { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Movie
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("originaltitle")]
    public string? OriginalTitle { get; set; }

    [XmlElement("sorttitle")]
    public string? SortTitle { get; set; }

    [XmlElement("alternatetitle")]
    public List<string> AlternateTitle { get; set; } = new();

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("userrating")]
    public decimal? UserRating { get; set; }

    [XmlElement("outline")]
    public string? Outline { get; set; }

    [XmlElement("plot")]
    public string? Plot { get; set; }

    [XmlElement("tagline")]
    public string? Tagline { get; set; }

    [XmlElement("runtime")]
    public int? Runtime { get; set; }

    [XmlElement("banner")]
    public List<MediaFile> Banner { get; set; } = new();

    [XmlElement("thumb")]
    public List<MediaFile> Thumb { get; set; } = new();

    [XmlElement("fanart")]
    public List<MediaFile> Fanart { get; set; } = new();

    [XmlElement("contentrating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("uniqueid")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("setname")]
    public string? SetName { get; set; }

    [XmlElement("setoverview")]
    public string? SetOverview { get; set; }

    [XmlElement("country")]
    public List<string> Country { get; set; } = new();

    [XmlElement("productioncompany")]
    public List<string> ProductionCompany { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("releasedate")]
    public List<DateTime> ReleaseDate { get; set; } = new();

    [XmlElement("award")]
    public List<string> Award { get; set; } = new();

    [XmlElement("subtitlelanguage")]
    public List<string> SubtitleLanguage { get; set; } = new();

    [XmlElement("soundtrack")]
    public string? Soundtrack { get; set; }

    [XmlElement("parentalguide")]
    public string? ParentalGuide { get; set; }

    [XmlElement("actor")]
    public List<Person> Actor { get; set; } = new();

    [XmlElement("director")]
    public List<Person> Director { get; set; } = new();

    [XmlElement("writer")]
    public List<Person> Writer { get; set; } = new();

    [XmlElement("composer")]
    public List<Person> Composer { get; set; } = new();

    [XmlElement("producers")]
    public List<Person> Producers { get; set; } = new();

    [XmlElement("collection")]
    public string? Collection { get; set; }

    [XmlElement("intro")]
    public TimedMarker? Intro { get; set; }

    [XmlElement("credits")]
    public TimedMarker? Credits { get; set; }

    [XmlElement("chapter")]
    public List<Chapter> Chapter { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class TvShow
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("originaltitle")]
    public string? OriginalTitle { get; set; }

    [XmlElement("showtitle")]
    public string? ShowTitle { get; set; }

    [XmlElement("sorttitle")]
    public string? SortTitle { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("season")]
    public int? Season { get; set; }

    [XmlElement("episode")]
    public int? Episode { get; set; }

    [XmlElement("altorder")]
    public List<AlternateOrder> AltOrder { get; set; } = new();

    [XmlElement("plot")]
    public string? Plot { get; set; }

    [XmlElement("tagline")]
    public string? Tagline { get; set; }

    [XmlElement("thumb")]
    public List<MediaFile> Thumb { get; set; } = new();

    [XmlElement("fanart")]
    public List<MediaFile> Fanart { get; set; } = new();

    [XmlElement("contentrating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("uniqueid")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("premiered")]
    public DateTime? Premiered { get; set; }

    [XmlElement("year")]
    public int? Year { get; set; }

    [XmlElement("status")]
    public string? Status { get; set; }

    [XmlElement("studio")]
    public List<string> Studio { get; set; } = new();

    [XmlElement("trailer")]
    public string? Trailer { get; set; }

    [XmlElement("actor")]
    public List<Person> Actor { get; set; } = new();

    [XmlElement("namedseason")]
    public List<NamedSeason> NamedSeason { get; set; } = new();

    [XmlElement("intro")]
    public TimedMarker? Intro { get; set; }

    [XmlElement("credits")]
    public TimedMarker? Credits { get; set; }

    [XmlElement("chapter")]
    public List<Chapter> Chapter { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class AlternateOrder
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("altseason")]
    public int? AltSeason { get; set; }

    [XmlAttribute("altepisode")]
    public int? AltEpisode { get; set; }

    [XmlAttribute("name")]
    public string? Name { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class NamedSeason
{
    [XmlText]
    public string? Value { get; set; }

    [XmlAttribute("number")]
    public int Number { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Anime
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("language")]
    public List<string> Language { get; set; } = new();

    [XmlElement("season")]
    public int? Season { get; set; }

    [XmlElement("episode")]
    public int? Episode { get; set; }

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("isAdult")]
    public int? IsAdult { get; set; }

    [XmlElement("director")]
    public List<Person> Director { get; set; } = new();

    [XmlElement("voiceActor")]
    public List<Person> VoiceActor { get; set; } = new();

    [XmlElement("translationVoice")]
    public List<Person> TranslationVoice { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("contentRating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("banner")]
    public List<MediaFile> Banner { get; set; } = new();

    [XmlElement("thumb")]
    public List<MediaFile> Thumb { get; set; } = new();

    [XmlElement("fanart")]
    public List<MediaFile> Fanart { get; set; } = new();

    [XmlElement("links")]
    public List<string> Links { get; set; } = new();

    [XmlElement("intro")]
    public TimedMarker? Intro { get; set; }

    [XmlElement("credits")]
    public TimedMarker? Credits { get; set; }

    [XmlElement("chapter")]
    public List<Chapter> Chapter { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Adult
{
    [XmlElement("name")]
    public string? Name { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("siteName")]
    public string? SiteName { get; set; }

    [XmlElement("VideoURL")]
    public string? VideoUrl { get; set; }

    [XmlElement("TrailerURL")]
    public string? TrailerUrl { get; set; }

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("director")]
    public List<Person> Director { get; set; } = new();

    [XmlElement("performer")]
    public List<Person> Performer { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("link")]
    public List<string> Link { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("thumbnail")]
    public List<MediaFile> Thumbnail { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Video
{
    [XmlElement("name")]
    public string? Name { get; set; }

    [XmlElement("filmingDate")]
    public DateTime? FilmingDate { get; set; }

    [XmlElement("producer")]
    public Person? Producer { get; set; }

    [XmlElement("collectionName")]
    public string? CollectionName { get; set; }

    [XmlElement("people")]
    public List<Person> People { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public Rating? Rating { get; set; }

    [XmlElement("uniqueId")]
    public UniqueId? UniqueId { get; set; }

    [XmlElement("contentRating")]
    public ContentRating? ContentRating { get; set; }

    [XmlElement("thumbnail")]
    public List<MediaFile> Thumbnail { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Music
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("album")]
    public List<MusicAlbum> Album { get; set; } = new();

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("producer")]
    public List<Person> Producer { get; set; } = new();

    [XmlElement("writer")]
    public List<Person> Writer { get; set; } = new();

    [XmlElement("artist")]
    public List<Person> Artist { get; set; } = new();

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("language")]
    public string? Language { get; set; }

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("contentRating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("cover")]
    public List<MediaFile> Cover { get; set; } = new();

    [XmlElement("serviceLinks")]
    public List<ServiceLink> ServiceLinks { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class MusicAlbum
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("position")]
    public int? Position { get; set; }

    [XmlElement("artist")]
    public string? Artist { get; set; }

    [XmlElement("uniqueid")]
    public string? UniqueId { get; set; }

    [XmlElement("url")]
    public string? Url { get; set; }

    [XmlElement("cover")]
    public List<MediaFile> Cover { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class ServiceLink
{
    [XmlElement("service")]
    public string? Service { get; set; }

    [XmlElement("url")]
    public string? Url { get; set; }
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Audiobook
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("isbn")]
    public string? Isbn { get; set; }

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("language")]
    public string? Language { get; set; }

    [XmlElement("genre")]
    public string? Genre { get; set; }

    [XmlElement("writer")]
    public List<Person> Writer { get; set; } = new();

    [XmlElement("voiceActor")]
    public List<Person> VoiceActor { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("contentRating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("cover")]
    public List<MediaFile> Cover { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class Podcast
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("host")]
    public List<Person> Host { get; set; } = new();

    [XmlElement("guest")]
    public List<Person> Guest { get; set; } = new();

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("language")]
    public string? Language { get; set; }

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("contentRating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("cover")]
    public List<MediaFile> Cover { get; set; } = new();

    [XmlElement("serviceLinks")]
    public List<ServiceLink> ServiceLinks { get; set; } = new();
}

[XmlType(Namespace = NfoConstants.Namespace)]
public sealed class MusicVideo
{
    [XmlElement("title")]
    public string? Title { get; set; }

    [XmlElement("releaseDate")]
    public DateTime? ReleaseDate { get; set; }

    [XmlElement("productionCompany")]
    public string? ProductionCompany { get; set; }

    [XmlElement("producer")]
    public List<Person> Producer { get; set; } = new();

    [XmlElement("writer")]
    public List<Person> Writer { get; set; } = new();

    [XmlElement("artist")]
    public List<Person> Artist { get; set; } = new();

    [XmlElement("genre")]
    public List<string> Genre { get; set; } = new();

    [XmlElement("duration")]
    public int? Duration { get; set; }

    [XmlElement("language")]
    public string? Language { get; set; }

    [XmlElement("keyword")]
    public List<string> Keyword { get; set; } = new();

    [XmlElement("tag")]
    public List<string> Tag { get; set; } = new();

    [XmlElement("description")]
    public string? Description { get; set; }

    [XmlElement("rating")]
    public List<Rating> Rating { get; set; } = new();

    [XmlElement("uniqueId")]
    public List<UniqueId> UniqueId { get; set; } = new();

    [XmlElement("contentRating")]
    public List<ContentRating> ContentRating { get; set; } = new();

    [XmlElement("cover")]
    public List<MediaFile> Cover { get; set; } = new();

    [XmlElement("serviceLinks")]
    public List<ServiceLink> ServiceLinks { get; set; } = new();
}
