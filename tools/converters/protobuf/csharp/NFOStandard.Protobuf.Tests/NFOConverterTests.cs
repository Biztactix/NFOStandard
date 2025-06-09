using System;
using System.IO;
using System.Xml.Linq;
using FluentAssertions;
using NFOStandard.Protobuf;
using NFOStandard.Protobuf.Converter;
using Xunit;

namespace NFOStandard.Protobuf.Tests
{
    public class NFOConverterTests
    {
        private const string NFONamespace = "NFOStandard";

        [Fact]
        public void XmlToProtobuf_WithValidMovieXml_ConvertsCorrectly()
        {
            // Arrange
            var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" 
      xsi:schemaLocation=""NFOStandard https://xsd.nfostandard.com/main.xsd"">
    <media>
        <movie>
            <title>Inception</title>
            <originaltitle>Inception</originaltitle>
            <year>2010</year>
            <runtime>148</runtime>
            <plot>A thief who steals corporate secrets through dream-sharing technology.</plot>
            <rating name=""imdb"" max=""10"" default=""true"">
                <value>8.8</value>
                <votes>2000000</votes>
            </rating>
            <genre>Action</genre>
            <genre>Sci-Fi</genre>
            <actor>
                <name>Leonardo DiCaprio</name>
                <role>Dom Cobb</role>
                <order>1</order>
            </actor>
            <director>
                <name>Christopher Nolan</name>
            </director>
        </movie>
    </media>
</root>";

            // Act
            var result = NFOConverter.XmlToProtobuf(xml);

            // Assert
            result.Should().NotBeNull();
            result.Media.Should().NotBeNull();
            result.Media.MediaTypeCase.Should().Be(Media.MediaTypeOneofCase.Movie);
            
            var movie = result.Media.Movie;
            movie.Title.Should().Be("Inception");
            movie.Originaltitle.Should().Be("Inception");
            movie.Year.Should().Be(2010);
            movie.Runtime.Should().Be(148);
            movie.Plot.Should().Contain("thief who steals");
            
            movie.Rating.Should().HaveCount(1);
            movie.Rating[0].Name.Should().Be("imdb");
            movie.Rating[0].Value.Should().Be(8.8f);
            movie.Rating[0].Votes.Should().Be(2000000);
            movie.Rating[0].Max.Should().Be(10);
            movie.Rating[0].Default.Should().BeTrue();
            
            movie.Genre.Should().HaveCount(2);
            movie.Genre.Should().Contain("Action");
            movie.Genre.Should().Contain("Sci-Fi");
            
            movie.Actor.Should().HaveCount(1);
            movie.Actor[0].Name.Should().Be("Leonardo DiCaprio");
            movie.Actor[0].Role.Should().Be("Dom Cobb");
            movie.Actor[0].Order.Should().Be(1);
            
            movie.Director.Should().HaveCount(1);
            movie.Director[0].Name.Should().Be("Christopher Nolan");
        }

        [Fact]
        public void ProtobufToXml_WithValidMovie_ConvertsCorrectly()
        {
            // Arrange
            var nfoRoot = new NFORoot
            {
                Media = new Media
                {
                    Movie = new Movie
                    {
                        Title = "The Matrix",
                        Year = 1999,
                        Runtime = 136,
                        Plot = "A computer hacker learns about the true nature of reality."
                    }
                }
            };

            nfoRoot.Media.Movie.Genre.Add("Action");
            nfoRoot.Media.Movie.Genre.Add("Sci-Fi");

            // Act
            var xml = NFOConverter.ProtobufToXml(nfoRoot);

            // Assert
            xml.Should().NotBeNullOrEmpty();
            xml.Should().Contain("<?xml version=\"1.0\" encoding=\"utf-8\"?>");
            xml.Should().Contain("<title>The Matrix</title>");
            xml.Should().Contain("<year>1999</year>");
            xml.Should().Contain("<runtime>136</runtime>");
            xml.Should().Contain("<genre>Action</genre>");
            xml.Should().Contain("<genre>Sci-Fi</genre>");
        }

        [Fact]
        public void RoundTrip_MovieData_PreservesAllInformation()
        {
            // Arrange
            var originalXml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"">
    <media>
        <movie>
            <title>Test Movie</title>
            <year>2024</year>
            <runtime>120</runtime>
            <userrating>9.5</userrating>
            <plot>Test plot</plot>
            <outline>Test outline</outline>
            <tagline>Test tagline</tagline>
            <genre>Drama</genre>
            <tag>Test Tag</tag>
            <country>USA</country>
            <actor>
                <name>Test Actor</name>
                <role>Main Character</role>
                <order>1</order>
                <thumb>actor.jpg</thumb>
                <bio>Test bio</bio>
            </actor>
        </movie>
    </media>
</root>";

            // Act
            var protobuf = NFOConverter.XmlToProtobuf(originalXml);
            var resultXml = NFOConverter.ProtobufToXml(protobuf);
            var roundTripProtobuf = NFOConverter.XmlToProtobuf(resultXml);

            // Assert
            var movie1 = protobuf.Media.Movie;
            var movie2 = roundTripProtobuf.Media.Movie;

            movie2.Title.Should().Be(movie1.Title);
            movie2.Year.Should().Be(movie1.Year);
            movie2.Runtime.Should().Be(movie1.Runtime);
            movie2.Userrating.Should().Be(movie1.Userrating);
            movie2.Plot.Should().Be(movie1.Plot);
            movie2.Outline.Should().Be(movie1.Outline);
            movie2.Tagline.Should().Be(movie1.Tagline);
            movie2.Genre.Should().BeEquivalentTo(movie1.Genre);
            movie2.Tag.Should().BeEquivalentTo(movie1.Tag);
            movie2.Country.Should().BeEquivalentTo(movie1.Country);
            movie2.Actor.Should().HaveCount(movie1.Actor.Count);
        }

        [Fact]
        public void XmlToProtobuf_WithTVShow_ConvertsCorrectly()
        {
            // Arrange
            var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <tvshow>
            <title>Breaking Bad</title>
            <year>2008</year>
            <plot>A high school chemistry teacher turned meth producer.</plot>
            <status>Ended</status>
            <studio>AMC</studio>
            <genre>Crime</genre>
            <genre>Drama</genre>
        </tvshow>
    </media>
</root>";

            // Act
            var result = NFOConverter.XmlToProtobuf(xml);

            // Assert
            result.Media.MediaTypeCase.Should().Be(Media.MediaTypeOneofCase.Tvshow);
            var tvshow = result.Media.Tvshow;
            tvshow.Title.Should().Be("Breaking Bad");
            tvshow.Year.Should().Be(2008);
            tvshow.Status.Should().Be("Ended");
            tvshow.Studio.Should().Contain("AMC");
            tvshow.Genre.Should().HaveCount(2);
        }

        [Fact]
        public void XmlToProtobuf_WithMusic_ConvertsCorrectly()
        {
            // Arrange
            var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <music>
            <title>The Dark Side of the Moon</title>
            <artist>Pink Floyd</artist>
            <albumartist>Pink Floyd</albumartist>
            <album>The Dark Side of the Moon</album>
            <year>1973</year>
            <genre>Progressive Rock</genre>
            <compilation>false</compilation>
        </music>
    </media>
</root>";

            // Act
            var result = NFOConverter.XmlToProtobuf(xml);

            // Assert
            result.Media.MediaTypeCase.Should().Be(Media.MediaTypeOneofCase.Music);
            var music = result.Media.Music;
            music.Title.Should().Be("The Dark Side of the Moon");
            music.Artist.Should().Be("Pink Floyd");
            music.Year.Should().Be(1973);
            music.Compilation.Should().BeFalse();
        }

        [Fact]
        public void SaveAndLoadProtobuf_WorksCorrectly()
        {
            // Arrange
            var tempFile = Path.GetTempFileName();
            var nfoRoot = new NFORoot
            {
                Media = new Media
                {
                    Movie = new Movie
                    {
                        Title = "Test Movie",
                        Year = 2024
                    }
                }
            };

            try
            {
                // Act
                NFOConverter.SaveProtobuf(nfoRoot, tempFile);
                var loaded = NFOConverter.LoadProtobuf(tempFile);

                // Assert
                loaded.Should().NotBeNull();
                loaded.Media.Movie.Title.Should().Be("Test Movie");
                loaded.Media.Movie.Year.Should().Be(2024);
            }
            finally
            {
                // Cleanup
                if (File.Exists(tempFile))
                    File.Delete(tempFile);
            }
        }

        [Fact]
        public void XmlToProtobuf_WithInvalidXml_ThrowsException()
        {
            // Arrange
            var invalidXml = "<invalid>Not valid NFO XML</invalid>";

            // Act & Assert
            Action act = () => NFOConverter.XmlToProtobuf(invalidXml);
            act.Should().Throw<InvalidOperationException>()
                .WithMessage("Invalid NFO XML: root element not found");
        }

        [Fact]
        public void XmlToProtobuf_WithMultipleRatings_ConvertsAllRatings()
        {
            // Arrange
            var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <movie>
            <title>Test Movie</title>
            <rating name=""imdb"" max=""10"" default=""true"">
                <value>8.5</value>
                <votes>1000000</votes>
            </rating>
            <rating name=""tmdb"" max=""10"">
                <value>8.2</value>
                <votes>5000</votes>
            </rating>
            <rating name=""metacritic"" max=""100"">
                <value>85</value>
            </rating>
        </movie>
    </media>
</root>";

            // Act
            var result = NFOConverter.XmlToProtobuf(xml);

            // Assert
            var movie = result.Media.Movie;
            movie.Rating.Should().HaveCount(3);
            
            var imdbRating = movie.Rating.First(r => r.Name == "imdb");
            imdbRating.Value.Should().Be(8.5f);
            imdbRating.Max.Should().Be(10);
            imdbRating.Default.Should().BeTrue();
            imdbRating.Votes.Should().Be(1000000);
            
            var tmdbRating = movie.Rating.First(r => r.Name == "tmdb");
            tmdbRating.Value.Should().Be(8.2f);
            tmdbRating.Votes.Should().Be(5000);
            
            var metacriticRating = movie.Rating.First(r => r.Name == "metacritic");
            metacriticRating.Value.Should().Be(85f);
            metacriticRating.Max.Should().Be(100);
        }

        [Fact]
        public void BinarySize_SmallerThanXml()
        {
            // Arrange
            var xml = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <movie>
            <title>Inception</title>
            <originaltitle>Inception</originaltitle>
            <year>2010</year>
            <runtime>148</runtime>
            <plot>A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.</plot>
            <rating name=""imdb"" max=""10"">
                <value>8.8</value>
                <votes>2000000</votes>
            </rating>
            <genre>Action</genre>
            <genre>Sci-Fi</genre>
            <genre>Thriller</genre>
        </movie>
    </media>
</root>";

            // Act
            var protobuf = NFOConverter.XmlToProtobuf(xml);
            var xmlSize = System.Text.Encoding.UTF8.GetByteCount(xml);
            var protobufSize = protobuf.CalculateSize();

            // Assert
            protobufSize.Should().BeLessThan(xmlSize);
            var reduction = (1 - (double)protobufSize / xmlSize) * 100;
            reduction.Should().BeGreaterThan(70); // Should be at least 70% smaller
        }
    }
}