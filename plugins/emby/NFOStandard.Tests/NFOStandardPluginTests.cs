using System;
using System.Linq;
using FluentAssertions;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Model.Serialization;
using Moq;
using NFOStandard;
using Xunit;

namespace NFOStandard.Tests
{
    public class NFOStandardPluginTests
    {
        private readonly Mock<IApplicationPaths> _appPathsMock;
        private readonly Mock<IXmlSerializer> _xmlSerializerMock;
        private readonly NFOStandardPlugin _plugin;

        public NFOStandardPluginTests()
        {
            _appPathsMock = new Mock<IApplicationPaths>();
            _xmlSerializerMock = new Mock<IXmlSerializer>();
            
            _appPathsMock.Setup(x => x.PluginConfigurationsPath).Returns("/config/plugins");
            
            _plugin = new NFOStandardPlugin(_appPathsMock.Object, _xmlSerializerMock.Object);
        }

        [Fact]
        public void Plugin_ShouldHaveCorrectName()
        {
            // Assert
            _plugin.Name.Should().Be("NFO Standard Metadata");
        }

        [Fact]
        public void Plugin_ShouldHaveCorrectId()
        {
            // Assert
            _plugin.Id.Should().Be(Guid.Parse("e4a0e5a6-7c8b-4f86-a916-7e3c89552289"));
        }

        [Fact]
        public void Plugin_ShouldHaveCorrectDescription()
        {
            // Assert
            _plugin.Description.Should().Be("Read and write metadata using the NFO Standard format");
        }

        [Fact]
        public void Plugin_ShouldReturnConfigurationPage()
        {
            // Act
            var pages = _plugin.GetPages().ToList();

            // Assert
            pages.Should().HaveCount(1);
            pages[0].Name.Should().Be("NFO Standard Metadata");
            pages[0].EmbeddedResourcePath.Should().Be("NFOStandard.Configuration.configPage.html");
        }

        [Fact]
        public void Plugin_InstanceShouldBeSetAfterConstruction()
        {
            // Assert
            NFOStandardPlugin.Instance.Should().NotBeNull();
            NFOStandardPlugin.Instance.Should().BeSameAs(_plugin);
        }
    }
}