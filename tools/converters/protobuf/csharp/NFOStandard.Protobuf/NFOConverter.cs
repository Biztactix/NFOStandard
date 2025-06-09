using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Google.Protobuf;
using NFOStandard.Protobuf;

namespace NFOStandard.Protobuf.Converter
{
    /// <summary>
    /// Converts between NFOStandard XML format and Protocol Buffer format
    /// </summary>
    public class NFOConverter
    {
        private const string NFONamespace = "NFOStandard";

        /// <summary>
        /// Converts XML NFO file to Protocol Buffer format
        /// </summary>
        public static NFORoot XmlToProtobuf(string xmlContent)
        {
            var doc = XDocument.Parse(xmlContent);
            var root = doc.Root;
            
            if (root?.Name.LocalName != "root")
                throw new InvalidOperationException("Invalid NFO XML: root element not found");

            var nfoRoot = new NFORoot();
            var mediaElement = root.Element(XName.Get("media", NFONamespace));
            
            if (mediaElement != null)
            {
                nfoRoot.Media = ParseMedia(mediaElement);
            }

            // Parse library metadata if present
            var libraryElements = root.Elements(XName.Get("library", NFONamespace));
            foreach (var libElement in libraryElements)
            {
                nfoRoot.Library.Add(ParseLibraryMetadata(libElement));
            }

            return nfoRoot;
        }

        /// <summary>
        /// Converts Protocol Buffer NFO to XML format
        /// </summary>
        public static string ProtobufToXml(NFORoot nfoRoot)
        {
            var doc = new XDocument(
                new XDeclaration("1.0", "UTF-8", null)
            );

            var root = new XElement(XName.Get("root", NFONamespace),
                new XAttribute(XNamespace.Xmlns + "xsi", "http://www.w3.org/2001/XMLSchema-instance"),
                new XAttribute(XName.Get("schemaLocation", "http://www.w3.org/2001/XMLSchema-instance"), 
                    "NFOStandard https://xsd.nfostandard.com/main.xsd")
            );

            if (nfoRoot.Media != null)
            {
                root.Add(MediaToXml(nfoRoot.Media));
            }

            foreach (var library in nfoRoot.Library)
            {
                root.Add(LibraryMetadataToXml(library));
            }

            doc.Add(root);
            return doc.Declaration + Environment.NewLine + doc.ToString();
        }

        /// <summary>
        /// Saves Protocol Buffer NFO to file
        /// </summary>
        public static void SaveProtobuf(NFORoot nfoRoot, string filePath)
        {
            using var output = File.Create(filePath);
            nfoRoot.WriteTo(output);
        }

        /// <summary>
        /// Loads Protocol Buffer NFO from file
        /// </summary>
        public static NFORoot LoadProtobuf(string filePath)
        {
            using var input = File.OpenRead(filePath);
            return NFORoot.Parser.ParseFrom(input);
        }

        private static Media ParseMedia(XElement mediaElement)
        {
            var media = new Media();
            var ns = mediaElement.Name.Namespace;

            // Check each media type
            var movieElement = mediaElement.Element(XName.Get("movie", ns));
            if (movieElement != null)
            {
                media.Movie = ParseMovie(movieElement);
                return media;
            }

            var tvshowElement = mediaElement.Element(XName.Get("tvshow", ns));
            if (tvshowElement != null)
            {
                media.Tvshow = ParseTVShow(tvshowElement);
                return media;
            }

            var musicElement = mediaElement.Element(XName.Get("music", ns));
            if (musicElement != null)
            {
                media.Music = ParseMusic(musicElement);
                return media;
            }

            var audiobookElement = mediaElement.Element(XName.Get("audiobook", ns));
            if (audiobookElement != null)
            {
                media.Audiobook = ParseAudioBook(audiobookElement);
                return media;
            }

            var podcastElement = mediaElement.Element(XName.Get("podcast", ns));
            if (podcastElement != null)
            {
                media.Podcast = ParsePodcast(podcastElement);
                return media;
            }

            var animeElement = mediaElement.Element(XName.Get("anime", ns));
            if (animeElement != null)
            {
                media.Anime = ParseAnime(animeElement);
                return media;
            }

            var musicvideoElement = mediaElement.Element(XName.Get("musicvideo", ns));
            if (musicvideoElement != null)
            {
                media.Musicvideo = ParseMusicVideo(musicvideoElement);
                return media;
            }

            var videoElement = mediaElement.Element(XName.Get("video", ns));
            if (videoElement != null)
            {
                media.Video = ParseVideo(videoElement);
                return media;
            }

            return media;
        }

        private static Movie ParseMovie(XElement movieElement)
        {
            var movie = new Movie();
            var ns = movieElement.Name.Namespace;

            movie.Title = movieElement.Element(XName.Get("title", ns))?.Value ?? "";
            movie.Originaltitle = movieElement.Element(XName.Get("originaltitle", ns))?.Value ?? "";
            movie.Sorttitle = movieElement.Element(XName.Get("sorttitle", ns))?.Value ?? "";
            
            // Parse alternate titles
            foreach (var altTitle in movieElement.Elements(XName.Get("alternatetitle", ns)))
            {
                movie.Alternatetitle.Add(altTitle.Value);
            }

            // Parse ratings
            foreach (var ratingElement in movieElement.Elements(XName.Get("rating", ns)))
            {
                movie.Rating.Add(ParseRating(ratingElement));
            }

            movie.Userrating = ParseFloat(movieElement.Element(XName.Get("userrating", ns))?.Value);
            movie.Outline = movieElement.Element(XName.Get("outline", ns))?.Value ?? "";
            movie.Plot = movieElement.Element(XName.Get("plot", ns))?.Value ?? "";
            movie.Tagline = movieElement.Element(XName.Get("tagline", ns))?.Value ?? "";
            movie.Runtime = ParseInt(movieElement.Element(XName.Get("runtime", ns))?.Value);
            movie.Year = ParseInt(movieElement.Element(XName.Get("year", ns))?.Value);

            // Parse media files
            foreach (var banner in movieElement.Elements(XName.Get("banner", ns)))
            {
                movie.Banner.Add(ParseMediaFile(banner));
            }

            foreach (var thumb in movieElement.Elements(XName.Get("thumb", ns)))
            {
                movie.Thumb.Add(ParseMediaFile(thumb));
            }

            foreach (var fanart in movieElement.Elements(XName.Get("fanart", ns)))
            {
                movie.Fanart.Add(ParseMediaFile(fanart));
            }

            // Parse content ratings
            foreach (var contentRating in movieElement.Elements(XName.Get("contentrating", ns)))
            {
                movie.Contentrating.Add(ParseContentRating(contentRating));
            }

            // Parse unique IDs
            foreach (var uniqueId in movieElement.Elements(XName.Get("uniqueid", ns)))
            {
                movie.Uniqueid.Add(ParseUniqueId(uniqueId));
            }

            // Parse genres
            foreach (var genre in movieElement.Elements(XName.Get("genre", ns)))
            {
                movie.Genre.Add(genre.Value);
            }

            // Parse tags
            foreach (var tag in movieElement.Elements(XName.Get("tag", ns)))
            {
                movie.Tag.Add(tag.Value);
            }

            // Parse set information
            movie.Setname = movieElement.Element(XName.Get("setname", ns))?.Value ?? "";
            movie.Setoverview = movieElement.Element(XName.Get("setoverview", ns))?.Value ?? "";

            // Parse countries
            foreach (var country in movieElement.Elements(XName.Get("country", ns)))
            {
                movie.Country.Add(country.Value);
            }

            // Parse production companies
            foreach (var company in movieElement.Elements(XName.Get("productioncompany", ns)))
            {
                movie.Productioncompany.Add(company.Value);
            }

            // Parse people
            foreach (var actor in movieElement.Elements(XName.Get("actor", ns)))
            {
                movie.Actor.Add(ParsePerson(actor));
            }

            foreach (var director in movieElement.Elements(XName.Get("director", ns)))
            {
                movie.Director.Add(ParsePerson(director));
            }

            foreach (var writer in movieElement.Elements(XName.Get("writer", ns)))
            {
                movie.Writer.Add(ParsePerson(writer));
            }

            return movie;
        }

        private static Rating ParseRating(XElement ratingElement)
        {
            var rating = new Rating();
            var ns = ratingElement.Name.Namespace;

            rating.Name = ratingElement.Attribute("name")?.Value ?? "";
            rating.Value = ParseFloat(ratingElement.Element(XName.Get("value", ns))?.Value);
            rating.Votes = ParseInt(ratingElement.Element(XName.Get("votes", ns))?.Value);
            rating.Max = ParseInt(ratingElement.Attribute("max")?.Value);
            rating.Default = ParseBool(ratingElement.Attribute("default")?.Value);

            return rating;
        }

        private static MediaFile ParseMediaFile(XElement mediaFileElement)
        {
            var mediaFile = new MediaFile();
            
            mediaFile.Type = mediaFileElement.Attribute("type")?.Value ?? "";
            mediaFile.Width = ParseInt(mediaFileElement.Attribute("width")?.Value);
            mediaFile.Height = ParseInt(mediaFileElement.Attribute("height")?.Value);
            mediaFile.Url = mediaFileElement.Attribute("url")?.Value ?? mediaFileElement.Value;
            mediaFile.Season = mediaFileElement.Attribute("season")?.Value ?? "";
            mediaFile.Preview = mediaFileElement.Attribute("preview")?.Value ?? "";

            return mediaFile;
        }

        private static ContentRating ParseContentRating(XElement contentRatingElement)
        {
            var contentRating = new ContentRating();
            var ns = contentRatingElement.Name.Namespace;

            contentRating.Country = contentRatingElement.Attribute("country")?.Value ?? "";
            contentRating.Board = contentRatingElement.Attribute("board")?.Value ?? "";
            contentRating.Rating = contentRatingElement.Element(XName.Get("rating", ns))?.Value ?? "";
            contentRating.Image = contentRatingElement.Element(XName.Get("image", ns))?.Value ?? "";

            return contentRating;
        }

        private static UniqueID ParseUniqueId(XElement uniqueIdElement)
        {
            var uniqueId = new UniqueID();
            
            uniqueId.Type = uniqueIdElement.Attribute("type")?.Value ?? "";
            uniqueId.Value = uniqueIdElement.Value;
            uniqueId.Default = ParseBool(uniqueIdElement.Attribute("default")?.Value);

            return uniqueId;
        }

        private static Person ParsePerson(XElement personElement)
        {
            var person = new Person();
            var ns = personElement.Name.Namespace;

            person.Name = personElement.Element(XName.Get("name", ns))?.Value ?? "";
            person.Role = personElement.Element(XName.Get("role", ns))?.Value ?? "";
            person.Order = ParseInt(personElement.Element(XName.Get("order", ns))?.Value);
            person.Thumb = personElement.Element(XName.Get("thumb", ns))?.Value ?? "";
            person.Bio = personElement.Element(XName.Get("bio", ns))?.Value ?? "";
            person.Url = personElement.Element(XName.Get("url", ns))?.Value ?? "";
            person.Birthdate = personElement.Element(XName.Get("birthdate", ns))?.Value ?? "";
            person.Birthplace = personElement.Element(XName.Get("birthplace", ns))?.Value ?? "";
            person.Deathdate = personElement.Element(XName.Get("deathdate", ns))?.Value ?? "";
            person.Deathplace = personElement.Element(XName.Get("deathplace", ns))?.Value ?? "";

            return person;
        }

        private static TVShow ParseTVShow(XElement tvshowElement)
        {
            var tvshow = new TVShow();
            var ns = tvshowElement.Name.Namespace;

            // Parse basic fields similar to movie
            tvshow.Title = tvshowElement.Element(XName.Get("title", ns))?.Value ?? "";
            tvshow.Originaltitle = tvshowElement.Element(XName.Get("originaltitle", ns))?.Value ?? "";
            tvshow.Sorttitle = tvshowElement.Element(XName.Get("sorttitle", ns))?.Value ?? "";
            tvshow.Plot = tvshowElement.Element(XName.Get("plot", ns))?.Value ?? "";
            tvshow.Year = ParseInt(tvshowElement.Element(XName.Get("year", ns))?.Value);
            tvshow.Runtime = ParseInt(tvshowElement.Element(XName.Get("runtime", ns))?.Value);
            tvshow.Status = tvshowElement.Element(XName.Get("status", ns))?.Value ?? "";
            tvshow.Premiered = tvshowElement.Element(XName.Get("premiered", ns))?.Value ?? "";

            // Parse studios
            foreach (var studio in tvshowElement.Elements(XName.Get("studio", ns)))
            {
                tvshow.Studio.Add(studio.Value);
            }

            // Parse season/episode info
            tvshow.Season = ParseInt(tvshowElement.Element(XName.Get("season", ns))?.Value);
            tvshow.Episode = ParseInt(tvshowElement.Element(XName.Get("episode", ns))?.Value);

            // Parse genres
            foreach (var genre in tvshowElement.Elements(XName.Get("genre", ns)))
            {
                tvshow.Genre.Add(genre.Value);
            }

            // Parse actors
            foreach (var actor in tvshowElement.Elements(XName.Get("actor", ns)))
            {
                tvshow.Actor.Add(ParsePerson(actor));
            }

            return tvshow;
        }

        private static Music ParseMusic(XElement musicElement)
        {
            var music = new Music();
            var ns = musicElement.Name.Namespace;

            music.Title = musicElement.Element(XName.Get("title", ns))?.Value ?? "";
            music.Artist = musicElement.Element(XName.Get("artist", ns))?.Value ?? "";
            music.Albumartist = musicElement.Element(XName.Get("albumartist", ns))?.Value ?? "";
            music.Album = musicElement.Element(XName.Get("album", ns))?.Value ?? "";
            music.Year = ParseInt(musicElement.Element(XName.Get("year", ns))?.Value);
            music.Compilation = ParseBool(musicElement.Element(XName.Get("compilation", ns))?.Value);
            music.Label = musicElement.Element(XName.Get("label", ns))?.Value ?? "";
            music.Type = musicElement.Element(XName.Get("type", ns))?.Value ?? "";

            // Parse genres
            foreach (var genre in musicElement.Elements(XName.Get("genre", ns)))
            {
                music.Genre.Add(genre.Value);
            }

            // Parse tracks
            foreach (var track in musicElement.Elements(XName.Get("track", ns)))
            {
                music.Track.Add(ParseTrack(track));
            }

            return music;
        }

        private static Track ParseTrack(XElement trackElement)
        {
            var track = new Track();
            var ns = trackElement.Name.Namespace;

            track.Position = ParseInt(trackElement.Element(XName.Get("position", ns))?.Value);
            track.Title = trackElement.Element(XName.Get("title", ns))?.Value ?? "";
            track.Duration = ParseInt(trackElement.Element(XName.Get("duration", ns))?.Value);
            track.Artist = trackElement.Element(XName.Get("artist", ns))?.Value ?? "";

            return track;
        }

        private static AudioBook ParseAudioBook(XElement audiobookElement)
        {
            var audiobook = new AudioBook();
            var ns = audiobookElement.Name.Namespace;

            audiobook.Title = audiobookElement.Element(XName.Get("title", ns))?.Value ?? "";
            audiobook.Author = audiobookElement.Element(XName.Get("author", ns))?.Value ?? "";
            audiobook.Narrator = audiobookElement.Element(XName.Get("narrator", ns))?.Value ?? "";
            audiobook.Publisher = audiobookElement.Element(XName.Get("publisher", ns))?.Value ?? "";
            audiobook.Year = ParseInt(audiobookElement.Element(XName.Get("year", ns))?.Value);
            audiobook.Description = audiobookElement.Element(XName.Get("description", ns))?.Value ?? "";
            audiobook.Runtime = ParseInt(audiobookElement.Element(XName.Get("runtime", ns))?.Value);
            audiobook.Language = audiobookElement.Element(XName.Get("language", ns))?.Value ?? "";
            audiobook.Isbn = audiobookElement.Element(XName.Get("isbn", ns))?.Value ?? "";

            return audiobook;
        }

        private static Podcast ParsePodcast(XElement podcastElement)
        {
            var podcast = new Podcast();
            var ns = podcastElement.Name.Namespace;

            podcast.Title = podcastElement.Element(XName.Get("title", ns))?.Value ?? "";
            podcast.Author = podcastElement.Element(XName.Get("author", ns))?.Value ?? "";
            podcast.Description = podcastElement.Element(XName.Get("description", ns))?.Value ?? "";
            podcast.Language = podcastElement.Element(XName.Get("language", ns))?.Value ?? "";
            podcast.PubDate = podcastElement.Element(XName.Get("pubDate", ns))?.Value ?? "";
            podcast.Link = podcastElement.Element(XName.Get("link", ns))?.Value ?? "";
            podcast.Copyright = podcastElement.Element(XName.Get("copyright", ns))?.Value ?? "";
            podcast.Duration = ParseInt(podcastElement.Element(XName.Get("duration", ns))?.Value);
            podcast.Explicit = ParseBool(podcastElement.Element(XName.Get("explicit", ns))?.Value);

            return podcast;
        }

        private static Anime ParseAnime(XElement animeElement)
        {
            var anime = new Anime();
            var ns = animeElement.Name.Namespace;

            anime.Title = animeElement.Element(XName.Get("title", ns))?.Value ?? "";
            anime.Originaltitle = animeElement.Element(XName.Get("originaltitle", ns))?.Value ?? "";
            anime.Plot = animeElement.Element(XName.Get("plot", ns))?.Value ?? "";
            anime.Premiered = animeElement.Element(XName.Get("premiered", ns))?.Value ?? "";
            anime.Status = animeElement.Element(XName.Get("status", ns))?.Value ?? "";
            anime.Source = animeElement.Element(XName.Get("source", ns))?.Value ?? "";
            anime.Type = animeElement.Element(XName.Get("type", ns))?.Value ?? "";

            return anime;
        }

        private static MusicVideo ParseMusicVideo(XElement musicvideoElement)
        {
            var musicvideo = new MusicVideo();
            var ns = musicvideoElement.Name.Namespace;

            musicvideo.Title = musicvideoElement.Element(XName.Get("title", ns))?.Value ?? "";
            musicvideo.Artist = musicvideoElement.Element(XName.Get("artist", ns))?.Value ?? "";
            musicvideo.Album = musicvideoElement.Element(XName.Get("album", ns))?.Value ?? "";
            musicvideo.Year = ParseInt(musicvideoElement.Element(XName.Get("year", ns))?.Value);
            musicvideo.Runtime = ParseInt(musicvideoElement.Element(XName.Get("runtime", ns))?.Value);
            musicvideo.Releasedate = musicvideoElement.Element(XName.Get("releasedate", ns))?.Value ?? "";

            return musicvideo;
        }

        private static Video ParseVideo(XElement videoElement)
        {
            var video = new Video();
            var ns = videoElement.Name.Namespace;

            video.Title = videoElement.Element(XName.Get("title", ns))?.Value ?? "";
            video.Description = videoElement.Element(XName.Get("description", ns))?.Value ?? "";
            video.Runtime = ParseInt(videoElement.Element(XName.Get("runtime", ns))?.Value);
            video.Date = videoElement.Element(XName.Get("date", ns))?.Value ?? "";

            return video;
        }

        private static LibraryMetadata ParseLibraryMetadata(XElement libraryElement)
        {
            var library = new LibraryMetadata();
            var ns = libraryElement.Name.Namespace;

            library.Type = libraryElement.Attribute("type")?.Value ?? "";

            foreach (var prop in libraryElement.Elements())
            {
                library.Properties[prop.Name.LocalName] = prop.Value;
            }

            return library;
        }

        // XML serialization methods
        private static XElement MediaToXml(Media media)
        {
            var mediaElement = new XElement(XName.Get("media", NFONamespace));

            switch (media.MediaTypeCase)
            {
                case Media.MediaTypeOneofCase.Movie:
                    mediaElement.Add(MovieToXml(media.Movie));
                    break;
                case Media.MediaTypeOneofCase.Tvshow:
                    mediaElement.Add(TVShowToXml(media.Tvshow));
                    break;
                case Media.MediaTypeOneofCase.Music:
                    mediaElement.Add(MusicToXml(media.Music));
                    break;
                case Media.MediaTypeOneofCase.Audiobook:
                    mediaElement.Add(AudioBookToXml(media.Audiobook));
                    break;
                case Media.MediaTypeOneofCase.Podcast:
                    mediaElement.Add(PodcastToXml(media.Podcast));
                    break;
                case Media.MediaTypeOneofCase.Anime:
                    mediaElement.Add(AnimeToXml(media.Anime));
                    break;
                case Media.MediaTypeOneofCase.Musicvideo:
                    mediaElement.Add(MusicVideoToXml(media.Musicvideo));
                    break;
                case Media.MediaTypeOneofCase.Video:
                    mediaElement.Add(VideoToXml(media.Video));
                    break;
            }

            return mediaElement;
        }

        private static XElement MovieToXml(Movie movie)
        {
            var movieElement = new XElement(XName.Get("movie", NFONamespace));

            AddElement(movieElement, "title", movie.Title);
            AddElement(movieElement, "originaltitle", movie.Originaltitle);
            AddElement(movieElement, "sorttitle", movie.Sorttitle);
            
            foreach (var altTitle in movie.Alternatetitle)
            {
                AddElement(movieElement, "alternatetitle", altTitle);
            }

            foreach (var rating in movie.Rating)
            {
                movieElement.Add(RatingToXml(rating));
            }

            if (movie.Userrating > 0)
                AddElement(movieElement, "userrating", movie.Userrating.ToString());

            AddElement(movieElement, "outline", movie.Outline);
            AddElement(movieElement, "plot", movie.Plot);
            AddElement(movieElement, "tagline", movie.Tagline);
            
            if (movie.Runtime > 0)
                AddElement(movieElement, "runtime", movie.Runtime.ToString());
            
            if (movie.Year > 0)
                AddElement(movieElement, "year", movie.Year.ToString());

            foreach (var genre in movie.Genre)
            {
                AddElement(movieElement, "genre", genre);
            }

            foreach (var actor in movie.Actor)
            {
                movieElement.Add(PersonToXml(actor, "actor"));
            }

            foreach (var director in movie.Director)
            {
                movieElement.Add(PersonToXml(director, "director"));
            }

            return movieElement;
        }

        private static XElement RatingToXml(Rating rating)
        {
            var ratingElement = new XElement(XName.Get("rating", NFONamespace));
            
            if (!string.IsNullOrEmpty(rating.Name))
                ratingElement.Add(new XAttribute("name", rating.Name));
            
            if (rating.Max > 0)
                ratingElement.Add(new XAttribute("max", rating.Max));
            
            if (rating.Default)
                ratingElement.Add(new XAttribute("default", "true"));

            AddElement(ratingElement, "value", rating.Value.ToString());
            
            if (rating.Votes > 0)
                AddElement(ratingElement, "votes", rating.Votes.ToString());

            return ratingElement;
        }

        private static XElement PersonToXml(Person person, string elementName)
        {
            var personElement = new XElement(XName.Get(elementName, NFONamespace));

            AddElement(personElement, "name", person.Name);
            AddElement(personElement, "role", person.Role);
            
            if (person.Order > 0)
                AddElement(personElement, "order", person.Order.ToString());
            
            AddElement(personElement, "thumb", person.Thumb);
            AddElement(personElement, "bio", person.Bio);

            return personElement;
        }

        private static XElement TVShowToXml(TVShow tvshow)
        {
            var tvshowElement = new XElement(XName.Get("tvshow", NFONamespace));

            AddElement(tvshowElement, "title", tvshow.Title);
            AddElement(tvshowElement, "originaltitle", tvshow.Originaltitle);
            AddElement(tvshowElement, "plot", tvshow.Plot);
            
            if (tvshow.Year > 0)
                AddElement(tvshowElement, "year", tvshow.Year.ToString());

            AddElement(tvshowElement, "status", tvshow.Status);

            foreach (var studio in tvshow.Studio)
            {
                AddElement(tvshowElement, "studio", studio);
            }

            return tvshowElement;
        }

        private static XElement MusicToXml(Music music)
        {
            var musicElement = new XElement(XName.Get("music", NFONamespace));

            AddElement(musicElement, "title", music.Title);
            AddElement(musicElement, "artist", music.Artist);
            AddElement(musicElement, "albumartist", music.Albumartist);
            AddElement(musicElement, "album", music.Album);
            
            if (music.Year > 0)
                AddElement(musicElement, "year", music.Year.ToString());

            return musicElement;
        }

        private static XElement AudioBookToXml(AudioBook audiobook)
        {
            var audiobookElement = new XElement(XName.Get("audiobook", NFONamespace));

            AddElement(audiobookElement, "title", audiobook.Title);
            AddElement(audiobookElement, "author", audiobook.Author);
            AddElement(audiobookElement, "narrator", audiobook.Narrator);

            return audiobookElement;
        }

        private static XElement PodcastToXml(Podcast podcast)
        {
            var podcastElement = new XElement(XName.Get("podcast", NFONamespace));

            AddElement(podcastElement, "title", podcast.Title);
            AddElement(podcastElement, "author", podcast.Author);
            AddElement(podcastElement, "description", podcast.Description);

            return podcastElement;
        }

        private static XElement AnimeToXml(Anime anime)
        {
            var animeElement = new XElement(XName.Get("anime", NFONamespace));

            AddElement(animeElement, "title", anime.Title);
            AddElement(animeElement, "originaltitle", anime.Originaltitle);
            AddElement(animeElement, "type", anime.Type);

            return animeElement;
        }

        private static XElement MusicVideoToXml(MusicVideo musicvideo)
        {
            var musicvideoElement = new XElement(XName.Get("musicvideo", NFONamespace));

            AddElement(musicvideoElement, "title", musicvideo.Title);
            AddElement(musicvideoElement, "artist", musicvideo.Artist);

            return musicvideoElement;
        }

        private static XElement VideoToXml(Video video)
        {
            var videoElement = new XElement(XName.Get("video", NFONamespace));

            AddElement(videoElement, "title", video.Title);
            AddElement(videoElement, "description", video.Description);

            return videoElement;
        }

        private static XElement LibraryMetadataToXml(LibraryMetadata library)
        {
            var libraryElement = new XElement(XName.Get("library", NFONamespace));
            
            if (!string.IsNullOrEmpty(library.Type))
                libraryElement.Add(new XAttribute("type", library.Type));

            foreach (var prop in library.Properties)
            {
                AddElement(libraryElement, prop.Key, prop.Value);
            }

            return libraryElement;
        }

        // Helper methods
        private static void AddElement(XElement parent, string name, string value)
        {
            if (!string.IsNullOrEmpty(value))
                parent.Add(new XElement(XName.Get(name, NFONamespace), value));
        }

        private static int ParseInt(string? value)
        {
            return int.TryParse(value, out var result) ? result : 0;
        }

        private static float ParseFloat(string? value)
        {
            return float.TryParse(value, out var result) ? result : 0f;
        }

        private static bool ParseBool(string? value)
        {
            return bool.TryParse(value, out var result) && result;
        }
    }
}