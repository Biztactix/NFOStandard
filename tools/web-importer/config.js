// NFO Standard Web Importer Configuration

const CONFIG = {
    // API Server Configuration
    // Set to null to use mock data, or specify your API server URL
    API_SERVER: null, // e.g., 'http://localhost:5000'
    
    // API Keys (only needed if using direct browser access - not recommended)
    // For production, use the API server with keys set as environment variables
    API_KEYS: {
        TMDB: '', // Get from https://www.themoviedb.org/settings/api
        OMDB: '', // Get from http://www.omdbapi.com/apikey.aspx
        TVDB: ''  // Get from https://thetvdb.com/api-information
    },
    
    // CORS Proxy (for direct browser access - development only)
    CORS_PROXY: 'https://api.allorigins.win/raw?url=',
    
    // Feature Flags
    FEATURES: {
        USE_MOCK_DATA: true,  // Set to false to use real APIs
        ENABLE_EDITING: true,
        ENABLE_SEARCH: true
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}