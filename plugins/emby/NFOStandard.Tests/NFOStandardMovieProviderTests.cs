using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using FluentAssertions;
using MediaBrowser.Controller.Entities.Movies;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.IO;
using Microsoft.Extensions.Logging;
using Moq;
using NFOStandard.Providers;
using Xunit;

namespace NFOStandard.Tests
{
    public class NFOStandardMovieProviderTests
    {
        private readonly Mock<ILogger<NFOStandardMovieProvider>> _loggerMock;
        private readonly Mock<IFileSystem> _fileSystemMock;
        private readonly Mock<IDirectoryService> _directoryServiceMock;
        private readonly NFOStandardMovieProvider _provider;

        public NFOStandardMovieProviderTests()
        {
            _loggerMock = new Mock<ILogger<NFOStandardMovieProvider>>();
            _fileSystemMock = new Mock<IFileSystem>();
            _directoryServiceMock = new Mock<IDirectoryService>();
            _provider = new NFOStandardMovieProvider(_loggerMock.Object, _fileSystemMock.Object);
        }

        [Fact]
        public async Task GetMetadata_WithValidNfoFile_ReturnsCorrectMetadata()
        {
            // Arrange
            var moviePath = "/movies/The Matrix (1999)/The Matrix.mkv";
            var nfoPath = "/movies/The Matrix (1999)/The Matrix.nfo";
            var nfoContent = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" 
      xsi:schemaLocation=""NFOStandard https://xsd.nfostandard.com/main.xsd"">
    <media>
        <movie>
            <title>The Matrix</title>
            <originaltitle>The Matrix Original</originaltitle>
            <sorttitle>Matrix, The</sorttitle>
            <year>1999</year>
            <plot>A computer hacker learns about the true nature of reality.</plot>
            <tagline>Welcome to the Real World</tagline>
            <runtime>136</runtime>
            <rating name=""imdb"" value=""8.7"" votes=""1800000"" default=""true""/>
            <rating name=""critic"" value=""8.8""/>
            <userrating>9.0</userrating>
            <contentrating country=""USA"" board=""MPAA"" rating=""R""/>
            <genre>Science Fiction</genre>
            <genre>Action</genre>
            <tag>Cyberpunk</tag>
            <tag>Virtual Reality</tag>
            <productioncompany>Warner Bros.</productioncompany>
            <productioncompany>Village Roadshow Pictures</productioncompany>
            <releasedate>1999-03-31</releasedate>
            <setname>The Matrix Collection</setname>
            <uniqueid type=""imdb"" default=""true"">tt0133093</uniqueid>
            <uniqueid type=""tmdb"">603</uniqueid>
            <actor>
                <name>Keanu Reeves</name>
                <role>Neo</role>
                <order>0</order>
            </actor>
            <actor>
                <name>Laurence Fishburne</name>
                <role>Morpheus</role>
                <order>1</order>
            </actor>
            <director>
                <name>The Wachowskis</name>
            </director>
            <writer>
                <name>The Wachowskis</name>
            </writer>
        </movie>
    </media>
</root>";

            var itemInfo = new ItemInfo { Path = moviePath };
            
            _fileSystemMock.Setup(fs => fs.FileExists(moviePath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            
            // Create temp file for testing
            var tempFile = Path.GetTempFileName();
            File.WriteAllText(tempFile, nfoContent);
            _fileSystemMock.Setup(fs => fs.FileExists(Path.ChangeExtension(moviePath, ".nfo"))).Returns(true);

            // Override the provider to use our test file
            var testProvider = new TestableNFOStandardMovieProvider(_loggerMock.Object, _fileSystemMock.Object, tempFile);

            // Act
            var result = await testProvider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeTrue();
            result.Item.Should().NotBeNull();
            
            var movie = result.Item;
            movie.Name.Should().Be("The Matrix");
            movie.OriginalTitle.Should().Be("The Matrix Original");
            movie.SortName.Should().Be("Matrix, The");
            movie.ProductionYear.Should().Be(1999);
            movie.Overview.Should().Be("A computer hacker learns about the true nature of reality.");
            movie.Tagline.Should().Be("Welcome to the Real World");
            movie.RunTimeTicks.Should().Be(TimeSpan.FromMinutes(136).Ticks);
            movie.CommunityRating.Should().Be(8.7f);
            movie.CriticRating.Should().Be(88f); // 8.8 * 10
            movie.CustomRating.Should().Be("9");
            movie.OfficialRating.Should().Be("R");
            movie.Genres.Should().BeEquivalentTo("Science Fiction", "Action");
            movie.Tags.Should().BeEquivalentTo("Cyberpunk", "Virtual Reality");
            movie.Studios.Should().BeEquivalentTo("Warner Bros.", "Village Roadshow Pictures");
            movie.PremiereDate.Should().Be(new DateTime(1999, 3, 31));
            movie.CollectionName.Should().Be("The Matrix Collection");
            
            movie.ProviderIds.Should().ContainKey("Imdb");
            movie.ProviderIds["Imdb"].Should().Be("tt0133093");
            movie.ProviderIds.Should().ContainKey("Tmdb");
            movie.ProviderIds["Tmdb"].Should().Be("603");
            
            movie.People.Should().HaveCount(4);
            movie.People[0].Name.Should().Be("Keanu Reeves");
            movie.People[0].Role.Should().Be("Neo");
            movie.People[0].Type.Should().Be(MediaBrowser.Model.Entities.PersonType.Actor);
            movie.People[0].SortOrder.Should().Be(0);

            // Cleanup
            File.Delete(tempFile);
        }

        [Fact]
        public async Task GetMetadata_WithNoNfoFile_ReturnsEmptyResult()
        {
            // Arrange
            var moviePath = "/movies/NonExistent.mkv";
            var itemInfo = new ItemInfo { Path = moviePath };
            
            _fileSystemMock.Setup(fs => fs.FileExists(It.IsAny<string>())).Returns(false);
            _fileSystemMock.Setup(fs => fs.DirectoryExists(It.IsAny<string>())).Returns(false);

            // Act
            var result = await _provider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeFalse();
            result.Item.Should().BeNull();
        }

        [Fact]
        public async Task GetMetadata_WithInvalidXml_ReturnsEmptyResult()
        {
            // Arrange
            var moviePath = "/movies/Invalid.mkv";
            var nfoPath = "/movies/Invalid.nfo";
            var invalidXml = "This is not valid XML";

            var itemInfo = new ItemInfo { Path = moviePath };
            
            _fileSystemMock.Setup(fs => fs.FileExists(moviePath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            
            var tempFile = Path.GetTempFileName();
            File.WriteAllText(tempFile, invalidXml);

            var testProvider = new TestableNFOStandardMovieProvider(_loggerMock.Object, _fileSystemMock.Object, tempFile);

            // Act
            var result = await testProvider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeFalse();
            result.Item.Should().BeNull();
            _loggerMock.Verify(l => l.Log(
                LogLevel.Error,
                It.IsAny<EventId>(),
                It.IsAny<It.IsAnyType>(),
                It.IsAny<Exception>(),
                (Func<It.IsAnyType, Exception, string>)It.IsAny<object>()), Times.Once);

            // Cleanup
            File.Delete(tempFile);
        }

        [Fact]
        public async Task GetMetadata_WithMinimalNfo_ReturnsBasicMetadata()
        {
            // Arrange
            var moviePath = "/movies/Minimal.mkv";
            var nfoContent = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <movie>
            <title>Minimal Movie</title>
        </movie>
    </media>
</root>";

            var itemInfo = new ItemInfo { Path = moviePath };
            
            var tempFile = Path.GetTempFileName();
            File.WriteAllText(tempFile, nfoContent);
            
            _fileSystemMock.Setup(fs => fs.FileExists(It.IsAny<string>())).Returns(true);
            var testProvider = new TestableNFOStandardMovieProvider(_loggerMock.Object, _fileSystemMock.Object, tempFile);

            // Act
            var result = await testProvider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeTrue();
            result.Item.Should().NotBeNull();
            result.Item.Name.Should().Be("Minimal Movie");

            // Cleanup
            File.Delete(tempFile);
        }

        [Fact]
        public void HasChanged_WithNewerNfoFile_ReturnsTrue()
        {
            // Arrange
            var moviePath = "/movies/Movie.mkv";
            var nfoPath = "/movies/Movie.nfo";
            var movie = new Movie 
            { 
                Path = moviePath,
                DateLastSaved = DateTime.UtcNow.AddHours(-1)
            };

            _fileSystemMock.Setup(fs => fs.FileExists(moviePath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.GetFileInfo(nfoPath)).Returns(new MockFileSystemMetadata
            {
                Exists = true,
                LastWriteTimeUtc = DateTime.UtcNow
            });

            // Act
            var hasChanged = _provider.HasChanged(movie, _directoryServiceMock.Object);

            // Assert
            hasChanged.Should().BeTrue();
        }

        [Fact]
        public void HasChanged_WithOlderNfoFile_ReturnsFalse()
        {
            // Arrange
            var moviePath = "/movies/Movie.mkv";
            var nfoPath = "/movies/Movie.nfo";
            var movie = new Movie 
            { 
                Path = moviePath,
                DateLastSaved = DateTime.UtcNow
            };

            _fileSystemMock.Setup(fs => fs.FileExists(moviePath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.GetFileInfo(nfoPath)).Returns(new MockFileSystemMetadata
            {
                Exists = true,
                LastWriteTimeUtc = DateTime.UtcNow.AddHours(-1)
            });

            // Act
            var hasChanged = _provider.HasChanged(movie, _directoryServiceMock.Object);

            // Assert
            hasChanged.Should().BeFalse();
        }

        private class TestableNFOStandardMovieProvider : NFOStandardMovieProvider
        {
            private readonly string _testFilePath;

            public TestableNFOStandardMovieProvider(ILogger<NFOStandardMovieProvider> logger, IFileSystem fileSystem, string testFilePath)
                : base(logger, fileSystem)
            {
                _testFilePath = testFilePath;
            }

            protected string GetNfoPathOverride(string moviePath)
            {
                return _testFilePath;
            }

            public new Task<MetadataResult<Movie>> GetMetadata(ItemInfo info, IDirectoryService directoryService, CancellationToken cancellationToken)
            {
                var result = new MetadataResult<Movie>();
                
                try
                {
                    var doc = System.Xml.Linq.XDocument.Load(_testFilePath);
                    var root = doc.Root;
                    
                    if (root?.Name.LocalName != "root")
                    {
                        return Task.FromResult(result);
                    }

                    var movieElement = root.Descendants("movie").FirstOrDefault();
                    if (movieElement != null)
                    {
                        var movie = new Movie();
                        var baseMethod = typeof(NFOStandardMovieProvider).GetMethod("ParseMovieElement", 
                            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                        baseMethod?.Invoke(this, new object[] { movie, movieElement });
                        
                        result.HasMetadata = true;
                        result.Item = movie;
                    }
                }
                catch (Exception)
                {
                    // Let the base class handle logging
                    return base.GetMetadata(info, directoryService, cancellationToken);
                }

                return Task.FromResult(result);
            }
        }

        private class MockFileSystemMetadata : FileSystemMetadata
        {
            public MockFileSystemMetadata()
            {
                Attributes = FileAttributes.Normal;
                FullName = "";
                Name = "";
                Extension = "";
            }
        }
    }
}