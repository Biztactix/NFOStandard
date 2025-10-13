using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using FluentAssertions;
using MediaBrowser.Controller.Entities.TV;
using MediaBrowser.Controller.Providers;
using MediaBrowser.Model.Entities;
using MediaBrowser.Model.IO;
using Microsoft.Extensions.Logging;
using Moq;
using NFOStandard.Providers;
using Xunit;

namespace NFOStandard.Tests
{
    public class NFOStandardSeriesProviderTests
    {
        private readonly Mock<ILogger<NFOStandardSeriesProvider>> _loggerMock;
        private readonly Mock<IFileSystem> _fileSystemMock;
        private readonly Mock<IDirectoryService> _directoryServiceMock;
        private readonly NFOStandardSeriesProvider _provider;

        public NFOStandardSeriesProviderTests()
        {
            _loggerMock = new Mock<ILogger<NFOStandardSeriesProvider>>();
            _fileSystemMock = new Mock<IFileSystem>();
            _directoryServiceMock = new Mock<IDirectoryService>();
            _provider = new NFOStandardSeriesProvider(_loggerMock.Object, _fileSystemMock.Object);
        }

        [Fact]
        public async Task GetMetadata_WithValidNfoFile_ReturnsCorrectMetadata()
        {
            // Arrange
            var seriesPath = "/tv/Breaking Bad";
            var nfoPath = "/tv/Breaking Bad/tvshow.nfo";
            var nfoContent = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" 
      xsi:schemaLocation=""NFOStandard https://xsd.nfostandard.com/main.xsd"">
    <media>
        <tvshow>
            <title>Breaking Bad</title>
            <originaltitle>Breaking Bad Original</originaltitle>
            <sorttitle>Breaking Bad Sort</sorttitle>
            <year>2008</year>
            <plot>A high school chemistry teacher turned methamphetamine producer.</plot>
            <tagline>All Hail the King</tagline>
            <runtime>47</runtime>
            <status>ended</status>
            <rating name=""tvdb"" value=""9.5"" default=""true""/>
            <userrating>9.8</userrating>
            <contentrating country=""USA"" board=""TV"" rating=""TV-MA""/>
            <genre>Drama</genre>
            <genre>Crime</genre>
            <tag>Chemistry</tag>
            <tag>Drug Trade</tag>
            <studio>AMC</studio>
            <studio>Sony Pictures Television</studio>
            <premiered>2008-01-20</premiered>
            <schedule>
                <airday>Sunday</airday>
                <airtime>21:00</airtime>
            </schedule>
            <uniqueid type=""imdb"" default=""true"">tt0903747</uniqueid>
            <uniqueid type=""tvdb"">81189</uniqueid>
            <uniqueid type=""tmdb"">1396</uniqueid>
            <actor>
                <name>Bryan Cranston</name>
                <role>Walter White</role>
                <order>0</order>
            </actor>
            <actor>
                <name>Aaron Paul</name>
                <role>Jesse Pinkman</role>
                <order>1</order>
            </actor>
            <creator>
                <name>Vince Gilligan</name>
            </creator>
        </tvshow>
    </media>
</root>";

            var itemInfo = new ItemInfo { Path = seriesPath };
            
            _fileSystemMock.Setup(fs => fs.DirectoryExists(seriesPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            
            // Create temp file for testing
            var tempFile = Path.GetTempFileName();
            File.WriteAllText(tempFile, nfoContent);

            // Override the provider to use our test file
            var testProvider = new TestableNFOStandardSeriesProvider(_loggerMock.Object, _fileSystemMock.Object, tempFile);

            // Act
            var result = await testProvider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeTrue();
            result.Item.Should().NotBeNull();
            
            var series = result.Item;
            series.Name.Should().Be("Breaking Bad");
            series.OriginalTitle.Should().Be("Breaking Bad Original");
            series.SortName.Should().Be("Breaking Bad Sort");
            series.ProductionYear.Should().Be(2008);
            series.Overview.Should().Be("A high school chemistry teacher turned methamphetamine producer.");
            series.Tagline.Should().Be("All Hail the King");
            series.RunTimeTicks.Should().Be(TimeSpan.FromMinutes(47).Ticks);
            series.Status.Should().Be(SeriesStatus.Ended);
            series.CommunityRating.Should().Be(9.5f);
            series.CustomRating.Should().Be("9.8");
            series.OfficialRating.Should().Be("TV-MA");
            series.Genres.Should().BeEquivalentTo("Drama", "Crime");
            series.Tags.Should().BeEquivalentTo("Chemistry", "Drug Trade");
            series.Studios.Should().BeEquivalentTo("AMC", "Sony Pictures Television");
            series.PremiereDate.Should().Be(new DateTime(2008, 1, 20));
            series.AirDays.Should().ContainSingle().Which.Should().Be(DayOfWeek.Sunday);
            series.AirTime.Should().Be("21:00");
            
            series.ProviderIds.Should().ContainKey("Imdb");
            series.ProviderIds["Imdb"].Should().Be("tt0903747");
            series.ProviderIds.Should().ContainKey("Tvdb");
            series.ProviderIds["Tvdb"].Should().Be("81189");
            series.ProviderIds.Should().ContainKey("Tmdb");
            series.ProviderIds["Tmdb"].Should().Be("1396");
            
            series.People.Should().HaveCount(3);
            series.People[0].Name.Should().Be("Bryan Cranston");
            series.People[0].Role.Should().Be("Walter White");
            series.People[0].Type.Should().Be(PersonType.Actor);
            series.People[2].Name.Should().Be("Vince Gilligan");
            series.People[2].Type.Should().Be(PersonType.Producer);

            // Cleanup
            File.Delete(tempFile);
        }

        [Fact]
        public async Task GetMetadata_WithContinuingStatus_SetsContinuingStatus()
        {
            // Arrange
            var seriesPath = "/tv/OngoingSeries";
            var nfoContent = @"<?xml version=""1.0"" encoding=""UTF-8""?>
<root xmlns=""NFOStandard"">
    <media>
        <tvshow>
            <title>Ongoing Series</title>
            <status>continuing</status>
        </tvshow>
    </media>
</root>";

            var itemInfo = new ItemInfo { Path = seriesPath };
            
            var tempFile = Path.GetTempFileName();
            File.WriteAllText(tempFile, nfoContent);
            
            _fileSystemMock.Setup(fs => fs.DirectoryExists(seriesPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(It.IsAny<string>())).Returns(true);
            
            var testProvider = new TestableNFOStandardSeriesProvider(_loggerMock.Object, _fileSystemMock.Object, tempFile);

            // Act
            var result = await testProvider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeTrue();
            result.Item.Status.Should().Be(SeriesStatus.Continuing);

            // Cleanup
            File.Delete(tempFile);
        }

        [Fact]
        public async Task GetMetadata_WithNoNfoFile_ReturnsEmptyResult()
        {
            // Arrange
            var seriesPath = "/tv/NonExistent";
            var itemInfo = new ItemInfo { Path = seriesPath };
            
            _fileSystemMock.Setup(fs => fs.DirectoryExists(seriesPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(It.IsAny<string>())).Returns(false);

            // Act
            var result = await _provider.GetMetadata(itemInfo, _directoryServiceMock.Object, CancellationToken.None);

            // Assert
            result.HasMetadata.Should().BeFalse();
            result.Item.Should().BeNull();
        }

        [Fact]
        public void HasChanged_WithNewerNfoFile_ReturnsTrue()
        {
            // Arrange
            var seriesPath = "/tv/Series";
            var nfoPath = "/tv/Series/tvshow.nfo";
            var series = new Series 
            { 
                Path = seriesPath,
                DateLastSaved = DateTime.UtcNow.AddHours(-1)
            };

            _fileSystemMock.Setup(fs => fs.DirectoryExists(seriesPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.FileExists(nfoPath)).Returns(true);
            _fileSystemMock.Setup(fs => fs.GetFileInfo(nfoPath)).Returns(new MockFileSystemMetadata
            {
                Exists = true,
                LastWriteTimeUtc = DateTime.UtcNow
            });

            // Act
            var hasChanged = _provider.HasChanged(series, _directoryServiceMock.Object);

            // Assert
            hasChanged.Should().BeTrue();
        }

        private class TestableNFOStandardSeriesProvider : NFOStandardSeriesProvider
        {
            private readonly string _testFilePath;

            public TestableNFOStandardSeriesProvider(ILogger<NFOStandardSeriesProvider> logger, IFileSystem fileSystem, string testFilePath)
                : base(logger, fileSystem)
            {
                _testFilePath = testFilePath;
            }

            public new Task<MetadataResult<Series>> GetMetadata(ItemInfo info, IDirectoryService directoryService, CancellationToken cancellationToken)
            {
                var result = new MetadataResult<Series>();
                
                try
                {
                    var doc = System.Xml.Linq.XDocument.Load(_testFilePath);
                    var root = doc.Root;
                    
                    if (root?.Name.LocalName != "root")
                    {
                        return Task.FromResult(result);
                    }

                    var tvshowElement = root.Descendants("tvshow").FirstOrDefault();
                    if (tvshowElement != null)
                    {
                        var series = new Series();
                        var baseMethod = typeof(NFOStandardSeriesProvider).GetMethod("ParseSeriesElement", 
                            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
                        baseMethod?.Invoke(this, new object[] { series, tvshowElement });
                        
                        result.HasMetadata = true;
                        result.Item = series;
                    }
                }
                catch (Exception)
                {
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