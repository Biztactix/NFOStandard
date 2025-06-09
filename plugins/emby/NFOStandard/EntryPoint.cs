using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediaBrowser.Controller.Library;
using MediaBrowser.Controller.Plugins;
using MediaBrowser.Controller.Providers;
using NFOStandard.Providers;
using NFOStandard.Savers;

namespace NFOStandard
{
    /// <summary>
    /// Entry point for the NFO Standard plugin
    /// </summary>
    public class EntryPoint : IServerEntryPoint
    {
        private readonly ILibraryManager _libraryManager;
        private readonly IProviderManager _providerManager;

        public EntryPoint(ILibraryManager libraryManager, IProviderManager providerManager)
        {
            _libraryManager = libraryManager;
            _providerManager = providerManager;
        }

        public void Run()
        {
            // Plugin is initialized
        }

        public void Dispose()
        {
            // Cleanup if needed
        }
    }
}