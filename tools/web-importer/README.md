# NFO Standard Web Importer

A web-based tool for importing metadata from IMDB, TMDB, and TheTVDB to create NFO Standard compliant files.

## Features

- **Multiple Sources**: Import from IMDB, TMDB, and TheTVDB
- **Search Functionality**: Search by title to find the correct media
- **ID/URL Support**: Enter IDs or full URLs from supported sites
- **Metadata Editing**: Edit imported metadata before generating NFO
- **Live Preview**: See the generated NFO XML in real-time
- **Download/Copy**: Download NFO files or copy to clipboard

## Quick Start

### Option 1: Standalone (Mock Data)

1. Open `index.html` in a web browser
2. The tool will work with mock data for testing
3. Search or enter IDs to see example metadata

### Option 2: With API Server

1. Set up API keys:
   ```bash
   export TMDB_API_KEY="your_tmdb_key"
   export OMDB_API_KEY="your_omdb_key"
   export TVDB_API_KEY="your_tvdb_key"
   ```

2. Start the API server:
   ```bash
   cd tools/web-importer
   python api_server.py
   ```

3. Update `config.js`:
   ```javascript
   API_SERVER: 'http://localhost:5000',
   FEATURES: {
       USE_MOCK_DATA: false
   }
   ```

4. Open `index.html` in a web browser

## Configuration

Edit `config.js` to customize the tool:

```javascript
const CONFIG = {
    // API server URL (null for mock data)
    API_SERVER: null,
    
    // Feature flags
    FEATURES: {
        USE_MOCK_DATA: true,
        ENABLE_EDITING: true,
        ENABLE_SEARCH: true
    }
};
```

## API Keys

To use real API data, you need keys from:

- **TMDB**: https://www.themoviedb.org/settings/api
- **OMDB**: http://www.omdbapi.com/apikey.aspx
- **TVDB**: https://thetvdb.com/api-information

## Usage

### Importing by ID

1. Select the media type (Movies or TV Shows)
2. Enter an ID or URL:
   - IMDB: `tt0111161` or `https://www.imdb.com/title/tt0111161/`
   - TMDB: `278` or `https://www.themoviedb.org/movie/278`
   - TVDB: `121361` or `https://thetvdb.com/series/game-of-thrones`
3. Click "Fetch Metadata"

### Searching

1. Enter a title in the search box
2. Click "Search"
3. Select from the results

### Editing Metadata

1. Click "Edit" after importing
2. Modify fields as needed
3. Click "Save Changes"

### Generating NFO

The NFO is automatically generated and displayed. You can:
- Click "Download NFO" to save the file
- Click "Copy to Clipboard" to copy the XML

## Architecture

### Frontend
- `index.html`: Main UI
- `styles.css`: Responsive styling
- `importer.js`: Core functionality
- `importer-api.js`: API integration
- `config.js`: Configuration

### Backend
- `api_server.py`: Flask API server
- Endpoints:
  - `/api/movie/<source>/<id>`
  - `/api/tv/<source>/<id>`
  - `/api/search/<type>?q=query`

## NFO Format

Generated files follow the NFO Standard specification:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Movie Title</title>
            <!-- Additional metadata -->
        </movie>
    </media>
</root>
```

## Development

### Running Locally

```bash
# Install dependencies
pip install flask flask-cors requests

# Start the API server
python api_server.py

# Open in browser
open index.html
```

### Adding New Sources

1. Add API integration in `api_server.py`
2. Update frontend options in `index.html`
3. Add ID extraction logic in `importer.js`

### Testing

```bash
# Test API endpoints
curl http://localhost:5000/api/movie/imdb/tt0111161
curl http://localhost:5000/api/search/movie?q=shawshank

# Validate generated NFO files
cd ../..
python tools/python-validator/nfo_validator.py generated.nfo
```

## Deployment

### Static Hosting

For mock data only:
1. Upload all files to a web server
2. Ensure `USE_MOCK_DATA: true` in config

### Full Deployment

1. Deploy API server (Heroku, AWS, etc.)
2. Set environment variables for API keys
3. Update `API_SERVER` in config.js
4. Enable CORS for your domain

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api_server.py"]
```

## Security Notes

- Never expose API keys in client-side code
- Use environment variables for sensitive data
- Implement rate limiting in production
- Consider authentication for public deployments

## Troubleshooting

### CORS Errors
- Use the API server instead of direct browser calls
- Or use a CORS proxy service

### API Limits
- OMDB: 1,000 requests/day (free tier)
- TMDB: No hard limit, be respectful
- TVDB: Rate limits apply

### Invalid NFO
- Check for special characters in metadata
- Validate against the XSD schema
- Ensure proper XML encoding

## Contributing

1. Test with various media types
2. Report issues with specific IDs
3. Suggest UI/UX improvements
4. Add support for new metadata sources

## License

MIT License - See LICENSE file

## Support

- NFO Standard: https://nfostandard.com
- GitHub Issues: https://github.com/Biztactix/NFOStandard/issues