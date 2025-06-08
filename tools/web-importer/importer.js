// NFO Standard Web Importer JavaScript

// Current metadata object
let currentMetadata = null;
let currentType = 'movie';

// Tab switching
function switchTab(type) {
    currentType = type;
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`${type}-tab`).classList.add('active');
    
    // Hide other sections
    document.getElementById('search-results').style.display = 'none';
    document.getElementById('metadata-preview').style.display = 'none';
    document.getElementById('metadata-editor').style.display = 'none';
    document.getElementById('nfo-output').style.display = 'none';
}

// Fetch movie metadata
async function fetchMovie() {
    const movieId = document.getElementById('movie-id').value.trim();
    const source = document.getElementById('movie-source').value;
    
    if (!movieId) {
        alert('Please enter a movie ID or URL');
        return;
    }
    
    showLoading(true);
    
    try {
        const extractedId = source === 'imdb' ? extractIMDBId(movieId) : extractTMDBId(movieId);
        const metadata = await nfoAPI.fetchMovie(extractedId, source);
        
        if (metadata) {
            currentMetadata = metadata;
            displayMetadata(metadata);
        }
    } catch (error) {
        console.error('Error fetching movie:', error);
        alert('Error fetching movie data. Please check the ID and try again.');
    } finally {
        showLoading(false);
    }
}

// Fetch TV show metadata
async function fetchTVShow() {
    const tvId = document.getElementById('tv-id').value.trim();
    const source = document.getElementById('tv-source').value;
    
    if (!tvId) {
        alert('Please enter a TV show ID or URL');
        return;
    }
    
    showLoading(true);
    
    try {
        const extractedId = source === 'imdb' ? extractIMDBId(tvId) : extractTMDBId(tvId);
        const metadata = await nfoAPI.fetchTVShow(extractedId, source);
        
        if (metadata) {
            currentMetadata = metadata;
            displayMetadata(metadata);
        }
    } catch (error) {
        console.error('Error fetching TV show:', error);
        alert('Error fetching TV show data. Please check the ID and try again.');
    } finally {
        showLoading(false);
    }
}

// Search for movies
async function searchMovie() {
    const query = document.getElementById('movie-search').value.trim();
    if (!query) {
        alert('Please enter a movie title to search');
        return;
    }
    
    showLoading(true);
    
    try {
        const results = await nfoAPI.search('movie', query);
        displaySearchResults(results, 'movie');
    } catch (error) {
        console.error('Error searching movies:', error);
        alert('Error searching movies. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Search for TV shows
async function searchTVShow() {
    const query = document.getElementById('tv-search').value.trim();
    if (!query) {
        alert('Please enter a TV show title to search');
        return;
    }
    
    showLoading(true);
    
    try {
        const results = await nfoAPI.search('tv', query);
        displaySearchResults(results, 'tv');
    } catch (error) {
        console.error('Error searching TV shows:', error);
        alert('Error searching TV shows. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Extract IMDB ID from various formats
function extractIMDBId(input) {
    const match = input.match(/tt\d{7,}/);
    return match ? match[0] : input;
}

// Extract TMDB ID
function extractTMDBId(input) {
    const match = input.match(/\d+/);
    return match ? match[0] : input;
}


// Display search results
function displaySearchResults(results, type) {
    const resultsDiv = document.getElementById('search-results');
    const resultsList = document.getElementById('results-list');
    
    resultsList.innerHTML = '';
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'result-item';
        item.innerHTML = `
            <h4>${result.title} (${result.year || 'N/A'})</h4>
            <p>${result.overview || 'No overview available'}</p>
        `;
        item.onclick = () => selectSearchResult(result.id, type);
        resultsList.appendChild(item);
    });
    
    resultsDiv.style.display = 'block';
}

// Select a search result
async function selectSearchResult(id, type) {
    document.getElementById('search-results').style.display = 'none';
    
    if (type === 'movie') {
        document.getElementById('movie-id').value = id;
        document.getElementById('movie-source').value = 'tmdb';
        await fetchMovie();
    } else {
        document.getElementById('tv-id').value = id;
        document.getElementById('tv-source').value = 'tmdb';
        await fetchTVShow();
    }
}

// Display metadata preview
function displayMetadata(metadata) {
    const previewDiv = document.getElementById('metadata-preview');
    const titleElem = document.getElementById('preview-title');
    const contentElem = document.getElementById('preview-content');
    
    titleElem.textContent = `${metadata.title} (${metadata.year || 'N/A'})`;
    
    contentElem.innerHTML = '';
    
    // Build preview fields
    const fields = [
        { label: 'Type', value: metadata.type },
        { label: 'Original Title', value: metadata.originaltitle },
        { label: 'Year', value: metadata.year },
        { label: 'Plot', value: metadata.plot },
        { label: 'Runtime', value: metadata.runtime ? `${metadata.runtime} minutes` : null },
        { label: 'Genres', value: metadata.genre, isList: true },
        { label: 'Directors', value: metadata.director || metadata.creator, isList: true },
        { label: 'Writers', value: metadata.writer, isList: true },
        { label: 'Rating', value: formatRatings(metadata.rating) },
        { label: 'Content Rating', value: metadata.contentrating },
        { label: 'Status', value: metadata.status },
        { label: 'Studios', value: metadata.studio || metadata.productioncompany, isList: true }
    ];
    
    fields.forEach(field => {
        if (field.value) {
            const fieldDiv = document.createElement('div');
            fieldDiv.className = 'metadata-field';
            
            const label = document.createElement('label');
            label.textContent = field.label + ':';
            fieldDiv.appendChild(label);
            
            const valueDiv = document.createElement('div');
            valueDiv.className = 'value';
            
            if (field.isList && Array.isArray(field.value)) {
                valueDiv.className += ' list';
                field.value.forEach(item => {
                    const tag = document.createElement('span');
                    tag.className = 'tag';
                    tag.textContent = typeof item === 'object' ? item.name : item;
                    valueDiv.appendChild(tag);
                });
            } else {
                valueDiv.textContent = field.value;
            }
            
            fieldDiv.appendChild(valueDiv);
            contentElem.appendChild(fieldDiv);
        }
    });
    
    // Show actors
    if (metadata.actors && metadata.actors.length > 0) {
        const actorsDiv = document.createElement('div');
        actorsDiv.className = 'metadata-field';
        
        const label = document.createElement('label');
        label.textContent = 'Actors:';
        actorsDiv.appendChild(label);
        
        const valueDiv = document.createElement('div');
        valueDiv.className = 'value';
        
        const actorsList = metadata.actors.map(actor => 
            `${actor.name} as ${actor.role}`
        ).join(', ');
        valueDiv.textContent = actorsList;
        
        actorsDiv.appendChild(valueDiv);
        contentElem.appendChild(actorsDiv);
    }
    
    previewDiv.style.display = 'block';
    
    // Generate and show NFO
    generateNFO();
}

// Format ratings for display
function formatRatings(ratings) {
    if (!ratings) return null;
    
    const parts = [];
    for (const [source, data] of Object.entries(ratings)) {
        if (data.value) {
            parts.push(`${source.toUpperCase()}: ${data.value}/10 (${data.votes || 0} votes)`);
        }
    }
    
    return parts.join(', ');
}

// Edit metadata
function editMetadata() {
    const editorDiv = document.getElementById('metadata-editor');
    const fieldsDiv = document.getElementById('editor-fields');
    
    fieldsDiv.innerHTML = '';
    
    // Create edit fields
    const editableFields = [
        { name: 'title', label: 'Title', type: 'text' },
        { name: 'originaltitle', label: 'Original Title', type: 'text' },
        { name: 'year', label: 'Year', type: 'number' },
        { name: 'plot', label: 'Plot', type: 'textarea' },
        { name: 'runtime', label: 'Runtime (minutes)', type: 'number' },
        { name: 'contentrating', label: 'Content Rating', type: 'text' }
    ];
    
    editableFields.forEach(field => {
        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'editor-field';
        
        const label = document.createElement('label');
        label.textContent = field.label;
        label.setAttribute('for', `edit-${field.name}`);
        fieldDiv.appendChild(label);
        
        if (field.type === 'textarea') {
            const textarea = document.createElement('textarea');
            textarea.id = `edit-${field.name}`;
            textarea.value = currentMetadata[field.name] || '';
            fieldDiv.appendChild(textarea);
        } else {
            const input = document.createElement('input');
            input.type = field.type;
            input.id = `edit-${field.name}`;
            input.value = currentMetadata[field.name] || '';
            fieldDiv.appendChild(input);
        }
        
        fieldsDiv.appendChild(fieldDiv);
    });
    
    document.getElementById('metadata-preview').style.display = 'none';
    editorDiv.style.display = 'block';
}

// Save edited metadata
function saveMetadata() {
    const editableFields = ['title', 'originaltitle', 'year', 'plot', 'runtime', 'contentrating'];
    
    editableFields.forEach(field => {
        const elem = document.getElementById(`edit-${field}`);
        if (elem) {
            const value = elem.value.trim();
            if (value) {
                if (field === 'year' || field === 'runtime') {
                    currentMetadata[field] = parseInt(value);
                } else {
                    currentMetadata[field] = value;
                }
            }
        }
    });
    
    document.getElementById('metadata-editor').style.display = 'none';
    displayMetadata(currentMetadata);
}

// Cancel editing
function cancelEdit() {
    document.getElementById('metadata-editor').style.display = 'none';
    document.getElementById('metadata-preview').style.display = 'block';
}

// Generate NFO XML
function generateNFO() {
    if (!currentMetadata) return;
    
    const nfoContent = createNFOXML(currentMetadata);
    document.getElementById('nfo-content').textContent = nfoContent;
    document.getElementById('nfo-output').style.display = 'block';
}

// Create NFO XML string
function createNFOXML(metadata) {
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n';
    xml += '      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">\n';
    xml += '    <media>\n';
    
    const mediaType = metadata.type === 'tvshow' ? 'tvshow' : 'movie';
    xml += `        <${mediaType}>\n`;
    
    // Add title
    if (metadata.title) {
        xml += `            <title>${escapeXML(metadata.title)}</title>\n`;
    }
    
    // Add original title
    if (metadata.originaltitle && metadata.originaltitle !== metadata.title) {
        xml += `            <originaltitle>${escapeXML(metadata.originaltitle)}</originaltitle>\n`;
    }
    
    // Add year
    if (metadata.year) {
        xml += `            <year>${metadata.year}</year>\n`;
    }
    
    // Add plot
    if (metadata.plot) {
        xml += `            <plot>${escapeXML(metadata.plot)}</plot>\n`;
    }
    
    // Add runtime
    if (metadata.runtime) {
        xml += `            <runtime>${metadata.runtime}</runtime>\n`;
    }
    
    // Add ratings
    if (metadata.rating) {
        for (const [source, data] of Object.entries(metadata.rating)) {
            if (data.value) {
                xml += `            <rating name="${source}" value="${data.value}"`;
                if (data.votes) {
                    xml += ` votes="${data.votes}"`;
                }
                xml += ` max="10"`;
                if (source === 'imdb') {
                    xml += ` default="true"`;
                }
                xml += `/>\n`;
            }
        }
    }
    
    // Add content rating
    if (metadata.contentrating) {
        xml += `            <contentrating`;
        if (metadata.contentrating.startsWith('TV-')) {
            xml += ` country="USA" board="TV"`;
        } else if (['G', 'PG', 'PG-13', 'R', 'NC-17'].includes(metadata.contentrating)) {
            xml += ` country="USA" board="MPAA"`;
        }
        xml += ` rating="${metadata.contentrating}"/>\n`;
    }
    
    // Add genres
    if (metadata.genre && Array.isArray(metadata.genre)) {
        metadata.genre.forEach(genre => {
            xml += `            <genre>${escapeXML(genre)}</genre>\n`;
        });
    }
    
    // Add unique IDs
    if (metadata.imdbid) {
        xml += `            <uniqueid type="imdb" default="true">${metadata.imdbid}</uniqueid>\n`;
    }
    if (metadata.tmdbid) {
        xml += `            <uniqueid type="tmdb">${metadata.tmdbid}</uniqueid>\n`;
    }
    if (metadata.tvdbid) {
        xml += `            <uniqueid type="tvdb">${metadata.tvdbid}</uniqueid>\n`;
    }
    
    // Add countries
    if (metadata.country && Array.isArray(metadata.country)) {
        metadata.country.forEach(country => {
            xml += `            <country>${escapeXML(country)}</country>\n`;
        });
    }
    
    // Add studios/production companies
    const studios = metadata.studio || metadata.productioncompany;
    if (studios && Array.isArray(studios)) {
        studios.forEach(studio => {
            if (mediaType === 'movie') {
                xml += `            <productioncompany>${escapeXML(studio)}</productioncompany>\n`;
            } else {
                xml += `            <studio>${escapeXML(studio)}</studio>\n`;
            }
        });
    }
    
    // Add TV show specific fields
    if (mediaType === 'tvshow') {
        if (metadata.premiered) {
            xml += `            <premiered>${metadata.premiered}</premiered>\n`;
        }
        if (metadata.status) {
            xml += `            <status>${metadata.status}</status>\n`;
        }
        if (metadata.seasons) {
            xml += `            <season>${metadata.seasons}</season>\n`;
        }
        if (metadata.episodes) {
            xml += `            <episode>${metadata.episodes}</episode>\n`;
        }
    }
    
    // Add people
    if (metadata.director && Array.isArray(metadata.director)) {
        metadata.director.forEach(director => {
            xml += `            <director>\n`;
            xml += `                <name>${escapeXML(director)}</name>\n`;
            xml += `            </director>\n`;
        });
    }
    
    if (metadata.creator && Array.isArray(metadata.creator)) {
        metadata.creator.forEach(creator => {
            xml += `            <creator>\n`;
            xml += `                <name>${escapeXML(creator)}</name>\n`;
            xml += `            </creator>\n`;
        });
    }
    
    if (metadata.writer && Array.isArray(metadata.writer)) {
        metadata.writer.forEach(writer => {
            xml += `            <writer>\n`;
            xml += `                <name>${escapeXML(writer)}</name>\n`;
            xml += `            </writer>\n`;
        });
    }
    
    if (metadata.actors && Array.isArray(metadata.actors)) {
        metadata.actors.forEach((actor, index) => {
            xml += `            <actor>\n`;
            xml += `                <name>${escapeXML(actor.name)}</name>\n`;
            if (actor.role) {
                xml += `                <role>${escapeXML(actor.role)}</role>\n`;
            }
            xml += `                <order>${index + 1}</order>\n`;
            xml += `            </actor>\n`;
        });
    }
    
    xml += `        </${mediaType}>\n`;
    xml += '    </media>\n';
    xml += '</root>';
    
    return xml;
}

// Escape XML special characters
function escapeXML(str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
}

// Download NFO file
function downloadNFO() {
    const nfoContent = document.getElementById('nfo-content').textContent;
    const filename = `${currentMetadata.title.replace(/[^a-z0-9]/gi, '_')}.nfo`;
    
    const blob = new Blob([nfoContent], { type: 'text/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Copy NFO to clipboard
function copyNFO() {
    const nfoContent = document.getElementById('nfo-content').textContent;
    
    navigator.clipboard.writeText(nfoContent).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.backgroundColor = '#27ae60';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.backgroundColor = '#95a5a6';
        }, 2000);
    }).catch(err => {
        alert('Failed to copy to clipboard');
    });
}

// Show/hide loading indicator
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set up enter key handlers
    document.getElementById('movie-id').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') fetchMovie();
    });
    
    document.getElementById('movie-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchMovie();
    });
    
    document.getElementById('tv-id').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') fetchTVShow();
    });
    
    document.getElementById('tv-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchTVShow();
    });
});