using MediaBrowser.Model.Plugins;

namespace NFOStandard.Configuration
{
    /// <summary>
    /// NFO Standard plugin configuration
    /// </summary>
    public class PluginConfiguration : BasePluginConfiguration
    {
        /// <summary>
        /// Enable people metadata extraction from NFO files
        /// </summary>
        public bool EnablePeopleExtraction { get; set; } = true;

        /// <summary>
        /// Enable writing people metadata back to NFO files
        /// </summary>
        public bool EnablePeopleWriting { get; set; } = true;

        /// <summary>
        /// Maximum number of actors to extract from NFO files
        /// </summary>
        public int MaxActors { get; set; } = 50;

        /// <summary>
        /// Enable strict NFO Standard namespace validation
        /// </summary>
        public bool StrictNamespaceValidation { get; set; } = false;

        /// <summary>
        /// Enable detailed logging for people operations
        /// </summary>
        public bool EnableDetailedLogging { get; set; } = false;

        /// <summary>
        /// Fallback to legacy NFO format if NFO Standard format is not found
        /// </summary>
        public bool EnableLegacyFallback { get; set; } = true;
    }
}