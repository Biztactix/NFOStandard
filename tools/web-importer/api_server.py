#!/usr/bin/env python3
"""
NFO Standard API Server
Provides API endpoints for fetching metadata from IMDB, TMDB, and TheTVDB.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for web access

# API Configuration (set these as environment variables)
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'YOUR_TMDB_API_KEY')
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'YOUR_OMDB_API_KEY')
TVDB_API_KEY = os.environ.get('TVDB_API_KEY', 'YOUR_TVDB_API_KEY')

# API Base URLs
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
OMDB_BASE_URL = 'http://www.omdbapi.com'
TVDB_BASE_URL = 'https://api4.thetvdb.com/v4'

# TVDB token (needs to be refreshed)
tvdb_token = None


def get_tvdb_token():
    """Get TVDB authentication token."""
    global tvdb_token
    if not tvdb_token:
        response = requests.post(f'{TVDB_BASE_URL}/login', 
                               json={'apikey': TVDB_API_KEY})
        if response.status_code == 200:
            tvdb_token = response.json()['data']['token']
    return tvdb_token


@app.route('/api/movie/<source>/<movie_id>')
def get_movie(source, movie_id):
    """Fetch movie metadata from specified source."""
    try:
        if source == 'imdb':
            return fetch_from_omdb(movie_id)
        elif source == 'tmdb':
            return fetch_from_tmdb('movie', movie_id)
        else:
            return jsonify({'error': 'Invalid source'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tv/<source>/<tv_id>')
def get_tv_show(source, tv_id):
    """Fetch TV show metadata from specified source."""
    try:
        if source == 'tvdb':
            return fetch_from_tvdb(tv_id)
        elif source == 'tmdb':
            return fetch_from_tmdb('tv', tv_id)
        elif source == 'imdb':
            return fetch_from_omdb(tv_id)
        else:
            return jsonify({'error': 'Invalid source'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/<media_type>')
def search(media_type):
    """Search for movies or TV shows."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        if media_type in ['movie', 'tv']:
            return search_tmdb(media_type, query)
        else:
            return jsonify({'error': 'Invalid media type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def fetch_from_omdb(imdb_id):
    """Fetch data from OMDB API."""
    params = {
        'apikey': OMDB_API_KEY,
        'i': imdb_id,
        'plot': 'full'
    }
    
    response = requests.get(OMDB_BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception('OMDB API request failed')
    
    data = response.json()
    if data.get('Response') == 'False':
        raise Exception(data.get('Error', 'Unknown error'))
    
    # Convert OMDB data to NFO Standard format
    metadata = {
        'type': 'movie' if data.get('Type') == 'movie' else 'tvshow',
        'title': data.get('Title'),
        'year': int(data.get('Year', '0').split('–')[0]) if data.get('Year') else None,
        'plot': data.get('Plot'),
        'runtime': parse_runtime(data.get('Runtime')),
        'genre': [g.strip() for g in data.get('Genre', '').split(',') if g.strip()],
        'director': [d.strip() for d in data.get('Director', '').split(',') if d.strip()],
        'writer': [w.strip() for w in data.get('Writer', '').split(',') if w.strip()],
        'actors': parse_actors(data.get('Actors', '')),
        'rating': {},
        'contentrating': data.get('Rated'),
        'country': [c.strip() for c in data.get('Country', '').split(',') if c.strip()],
        'language': [l.strip() for l in data.get('Language', '').split(',') if l.strip()],
        'imdbid': imdb_id,
        'poster': data.get('Poster')
    }
    
    # Add ratings
    if data.get('imdbRating') and data.get('imdbRating') != 'N/A':
        metadata['rating']['imdb'] = {
            'value': float(data.get('imdbRating')),
            'votes': parse_votes(data.get('imdbVotes'))
        }
    
    # Add other ratings
    for rating in data.get('Ratings', []):
        if rating['Source'] == 'Rotten Tomatoes':
            metadata['rating']['rottentomatoes'] = {
                'value': float(rating['Value'].rstrip('%')) / 10
            }
        elif rating['Source'] == 'Metacritic':
            metadata['rating']['metacritic'] = {
                'value': float(rating['Value'].split('/')[0]) / 10
            }
    
    return jsonify(metadata)


def fetch_from_tmdb(media_type, tmdb_id):
    """Fetch data from TMDB API."""
    endpoint = f'{TMDB_BASE_URL}/{media_type}/{tmdb_id}'
    params = {
        'api_key': TMDB_API_KEY,
        'append_to_response': 'credits,external_ids'
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise Exception('TMDB API request failed')
    
    data = response.json()
    
    # Convert TMDB data to NFO Standard format
    metadata = {
        'type': 'movie' if media_type == 'movie' else 'tvshow',
        'title': data.get('title') or data.get('name'),
        'originaltitle': data.get('original_title') or data.get('original_name'),
        'year': parse_year(data.get('release_date') or data.get('first_air_date')),
        'plot': data.get('overview'),
        'runtime': data.get('runtime'),
        'genre': [g['name'] for g in data.get('genres', [])],
        'rating': {},
        'tmdbid': str(tmdb_id)
    }
    
    # Add rating
    if data.get('vote_average'):
        metadata['rating']['tmdb'] = {
            'value': data.get('vote_average'),
            'votes': data.get('vote_count')
        }
    
    # Add external IDs
    if 'external_ids' in data:
        if data['external_ids'].get('imdb_id'):
            metadata['imdbid'] = data['external_ids']['imdb_id']
        if data['external_ids'].get('tvdb_id'):
            metadata['tvdbid'] = str(data['external_ids']['tvdb_id'])
    
    # Add credits
    if 'credits' in data:
        # Directors
        directors = [p['name'] for p in data['credits'].get('crew', []) 
                    if p.get('job') == 'Director']
        if directors:
            metadata['director'] = directors
        
        # Writers
        writers = [p['name'] for p in data['credits'].get('crew', []) 
                  if p.get('department') == 'Writing']
        if writers:
            metadata['writer'] = writers[:3]  # Limit to 3
        
        # Actors
        actors = []
        for actor in data['credits'].get('cast', [])[:10]:  # Top 10 actors
            actors.append({
                'name': actor['name'],
                'role': actor.get('character', '')
            })
        if actors:
            metadata['actors'] = actors
    
    # Movie specific fields
    if media_type == 'movie':
        metadata['releasedate'] = data.get('release_date')
        companies = [c['name'] for c in data.get('production_companies', [])]
        if companies:
            metadata['productioncompany'] = companies
    
    # TV show specific fields
    if media_type == 'tv':
        metadata['premiered'] = data.get('first_air_date')
        metadata['status'] = data.get('status')
        if data.get('created_by'):
            metadata['creator'] = [c['name'] for c in data['created_by']]
        if data.get('networks'):
            metadata['studio'] = [n['name'] for n in data['networks']]
        metadata['seasons'] = data.get('number_of_seasons')
        metadata['episodes'] = data.get('number_of_episodes')
    
    return jsonify(metadata)


def fetch_from_tvdb(tvdb_id):
    """Fetch data from TheTVDB API."""
    token = get_tvdb_token()
    if not token:
        raise Exception('TVDB authentication failed')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get series data
    response = requests.get(f'{TVDB_BASE_URL}/series/{tvdb_id}/extended',
                          headers=headers)
    if response.status_code != 200:
        raise Exception('TVDB API request failed')
    
    data = response.json()['data']
    
    # Convert TVDB data to NFO Standard format
    metadata = {
        'type': 'tvshow',
        'title': data.get('name'),
        'originaltitle': data.get('originalName'),
        'year': parse_year(data.get('firstAired')),
        'plot': data.get('overview'),
        'genre': [g['name'] for g in data.get('genres', [])],
        'rating': {},
        'tvdbid': str(tvdb_id),
        'status': data.get('status', {}).get('name'),
        'premiered': data.get('firstAired')
    }
    
    # Add rating
    if data.get('score'):
        metadata['rating']['tvdb'] = {
            'value': data.get('score'),
            'votes': data.get('scoreCount')
        }
    
    # Add network/studio
    if data.get('originalNetwork'):
        metadata['studio'] = [data['originalNetwork']['name']]
    
    # Add runtime
    if data.get('averageRuntime'):
        metadata['runtime'] = data['averageRuntime']
    
    # Get external IDs
    if data.get('remoteIds'):
        for remote_id in data['remoteIds']:
            if remote_id['type'] == 2:  # IMDB
                metadata['imdbid'] = remote_id['id']
    
    return jsonify(metadata)


def search_tmdb(media_type, query):
    """Search TMDB for movies or TV shows."""
    endpoint = f'{TMDB_BASE_URL}/search/{media_type}'
    params = {
        'api_key': TMDB_API_KEY,
        'query': query
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise Exception('TMDB search failed')
    
    data = response.json()
    results = []
    
    for item in data.get('results', [])[:10]:  # Limit to 10 results
        result = {
            'id': str(item['id']),
            'title': item.get('title') or item.get('name'),
            'year': parse_year(item.get('release_date') or item.get('first_air_date')),
            'overview': item.get('overview')
        }
        results.append(result)
    
    return jsonify(results)


def parse_runtime(runtime_str):
    """Parse runtime string to minutes."""
    if not runtime_str or runtime_str == 'N/A':
        return None
    match = re.search(r'(\d+)', runtime_str)
    return int(match.group(1)) if match else None


def parse_votes(votes_str):
    """Parse votes string to integer."""
    if not votes_str or votes_str == 'N/A':
        return 0
    return int(votes_str.replace(',', ''))


def parse_year(date_str):
    """Extract year from date string."""
    if not date_str:
        return None
    try:
        return int(date_str[:4])
    except:
        return None


def parse_actors(actors_str):
    """Parse actors string to list of actor objects."""
    if not actors_str:
        return []
    
    actors = []
    for actor in actors_str.split(','):
        actor = actor.strip()
        if actor:
            actors.append({'name': actor, 'role': ''})
    return actors


@app.route('/')
def index():
    """API documentation."""
    return jsonify({
        'endpoints': {
            'movie': {
                'imdb': '/api/movie/imdb/{imdb_id}',
                'tmdb': '/api/movie/tmdb/{tmdb_id}'
            },
            'tv': {
                'tvdb': '/api/tv/tvdb/{tvdb_id}',
                'tmdb': '/api/tv/tmdb/{tmdb_id}',
                'imdb': '/api/tv/imdb/{imdb_id}'
            },
            'search': {
                'movie': '/api/search/movie?q={query}',
                'tv': '/api/search/tv?q={query}'
            }
        },
        'note': 'Set API keys as environment variables: TMDB_API_KEY, OMDB_API_KEY, TVDB_API_KEY'
    })


if __name__ == '__main__':
    # Check for API keys
    if TMDB_API_KEY == 'YOUR_TMDB_API_KEY':
        print("Warning: TMDB_API_KEY not set. Get one at https://www.themoviedb.org/settings/api")
    if OMDB_API_KEY == 'YOUR_OMDB_API_KEY':
        print("Warning: OMDB_API_KEY not set. Get one at http://www.omdbapi.com/apikey.aspx")
    if TVDB_API_KEY == 'YOUR_TVDB_API_KEY':
        print("Warning: TVDB_API_KEY not set. Get one at https://thetvdb.com/api-information")
    
    app.run(debug=True, port=5000)