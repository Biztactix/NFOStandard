using System;
using System.Collections.Generic;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Plugins;
using MediaBrowser.Model.Plugins;
using MediaBrowser.Model.Serialization;
using NFOStandard.Configuration;

namespace NFOStandard
{
    /// <summary>
    /// NFO Standard plugin for Emby
    /// </summary>
    public class NFOStandardPlugin : BasePlugin<PluginConfiguration>, IHasWebPages
    {
        public override string Name => "NFO Standard Metadata";

        public override Guid Id => Guid.Parse("e4a0e5a6-7c8b-4f86-a916-7e3c89552289");

        public override string Description => "Read and write metadata using the NFO Standard format";

        public static NFOStandardPlugin? Instance { get; private set; }

        public NFOStandardPlugin(IApplicationPaths applicationPaths, IXmlSerializer xmlSerializer)
            : base(applicationPaths, xmlSerializer)
        {
            Instance = this;
        }

        public IEnumerable<PluginPageInfo> GetPages()
        {
            return new[]
            {
                new PluginPageInfo
                {
                    Name = "NFO Standard",
                    EmbeddedResourcePath = GetType().Namespace + ".Configuration.configPage.html",
                    EnableInMainMenu = true,
                    DisplayName = "NFO Standard"
                }
            };
        }
    }
}