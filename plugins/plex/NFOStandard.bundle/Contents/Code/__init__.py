# NFO Standard Plex Metadata Agent
# Reads NFO Standard compliant files and imports metadata into Plex

import os
import re
from lxml import etree

# Agent name
NFO_AGENT_NAME = 'NFO Standard'

def Start():
    """Initialize the agent."""
    Log.Info('NFO Standard Agent started')

def ValidatePrefs():
    """Validate preferences."""
    pass

class NFOStandardMovieAgent(Agent.Movies):
    """Movie agent for NFO Standard files."""
    
    name = NFO_AGENT_NAME
    ver = '1.0.0'
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ['com.plexapp.agents.localmedia']
    
    def search(self, results, media, lang):
        """Search for movie metadata."""
        Log.Info('Searching for movie: %s' % media.name)
        
        # Look for NFO file
        nfo_path = self._find_nfo_file(media)
        if nfo_path:
            Log.Info('Found NFO file: %s' % nfo_path)
            # Use filename as ID
            results.Append(MetadataSearchResult(
                id=nfo_path,
                name=media.name,
                year=media.year,
                score=100,
                lang=lang
            ))
    
    def update(self, metadata, media, lang):
        """Update movie metadata from NFO file."""
        nfo_path = metadata.id
        
        if not os.path.exists(nfo_path):
            Log.Error('NFO file not found: %s' % nfo_path)
            return
        
        try:
            # Parse NFO file
            tree = etree.parse(nfo_path)
            root = tree.getroot()
            
            # Find movie element
            movie = root.find('.//{{{0}}}movie'.format('NFOStandard'))
            if movie is None:
                movie = root.find('.//movie')
            
            if movie is None:
                Log.Error('No movie element found in NFO')
                return
            
            # Update metadata
            self._update_movie_metadata(metadata, movie)
            
        except Exception as e:
            Log.Error('Error parsing NFO file: %s' % str(e))
    
    def _find_nfo_file(self, media):
        """Find NFO file for the movie."""
        # Get movie file path
        if media.items and len(media.items) > 0:
            for item in media.items:
                if item.parts and len(item.parts) > 0:
                    video_path = item.parts[0].file
                    
                    # Check for movie.nfo in same directory
                    dir_path = os.path.dirname(video_path)
                    movie_nfo = os.path.join(dir_path, 'movie.nfo')
                    if os.path.exists(movie_nfo):
                        return movie_nfo
                    
                    # Check for same name as video file
                    base_name = os.path.splitext(video_path)[0]
                    same_name_nfo = base_name + '.nfo'
                    if os.path.exists(same_name_nfo):
                        return same_name_nfo
        
        return None
    
    def _update_movie_metadata(self, metadata, movie_elem):
        """Update movie metadata from NFO element."""
        # Title
        title = self._get_text(movie_elem, 'title')
        if title:
            metadata.title = title
        
        # Original title
        original_title = self._get_text(movie_elem, 'originaltitle')
        if original_title:
            metadata.original_title = original_title
        
        # Year
        year = self._get_text(movie_elem, 'year')
        if year:
            try:
                metadata.year = int(year)
            except:
                pass
        
        # Plot
        plot = self._get_text(movie_elem, 'plot')
        if plot:
            metadata.summary = plot
        
        # Tagline
        tagline = self._get_text(movie_elem, 'tagline')
        if tagline:
            metadata.tagline = tagline
        
        # Runtime (in minutes)
        runtime = self._get_text(movie_elem, 'runtime')
        if runtime:
            try:
                metadata.duration = int(runtime) * 60 * 1000  # Convert to milliseconds
            except:
                pass
        
        # Ratings
        self._update_ratings(metadata, movie_elem)
        
        # Content rating
        self._update_content_rating(metadata, movie_elem)
        
        # Genres
        metadata.genres.clear()
        for genre in movie_elem.findall('genre'):
            if genre.text:
                metadata.genres.add(genre.text)
        
        # Countries
        metadata.countries.clear()
        for country in movie_elem.findall('country'):
            if country.text:
                metadata.countries.add(country.text)
        
        # Studios
        for studio in movie_elem.findall('productioncompany'):
            if studio.text:
                metadata.studio = studio.text
                break
        
        # Collections
        setname = self._get_text(movie_elem, 'setname')
        if setname:
            metadata.collections.add(setname)
        
        # People
        self._update_people(metadata, movie_elem)
        
        # Release date
        release_date = self._get_text(movie_elem, 'releasedate')
        if release_date:
            try:
                metadata.originally_available_at = Datetime.ParseDate(release_date).date()
            except:
                pass
    
    def _update_ratings(self, metadata, movie_elem):
        """Update ratings from NFO."""
        # Look for ratings
        for rating in movie_elem.findall('rating'):
            name = rating.get('name', 'default')
            value = rating.get('value')
            
            if value:
                try:
                    rating_value = float(value)
                    if name in ['imdb', 'default'] or rating.get('default') == 'true':
                        metadata.rating = rating_value
                    elif name == 'audience':
                        metadata.audience_rating = rating_value
                except:
                    pass
        
        # User rating
        user_rating = self._get_text(movie_elem, 'userrating')
        if user_rating:
            try:
                metadata.rating = float(user_rating)
            except:
                pass
    
    def _update_content_rating(self, metadata, movie_elem):
        """Update content rating from NFO."""
        for content_rating in movie_elem.findall('contentrating'):
            rating = content_rating.get('rating')
            if not rating and content_rating.text:
                rating = content_rating.text
            
            if rating:
                metadata.content_rating = rating
                break
    
    def _update_people(self, metadata, movie_elem):
        """Update people (actors, directors, etc.) from NFO."""
        # Clear existing
        metadata.roles.clear()
        metadata.directors.clear()
        metadata.writers.clear()
        metadata.producers.clear()
        
        # Actors
        for actor in movie_elem.findall('actor'):
            role = metadata.roles.new()
            
            name = self._get_text(actor, 'name')
            if name:
                role.name = name
            
            character = self._get_text(actor, 'role')
            if character:
                role.role = character
            
            thumb = self._get_text(actor, 'thumb')
            if thumb:
                role.photo = thumb
        
        # Directors
        for director in movie_elem.findall('director'):
            name = self._get_text(director, 'name')
            if name:
                metadata.directors.add(name)
        
        # Writers
        for writer in movie_elem.findall('writer'):
            name = self._get_text(writer, 'name')
            if name:
                metadata.writers.add(name)
        
        # Producers
        for producer in movie_elem.findall('producer'):
            name = self._get_text(producer, 'name')
            if name:
                metadata.producers.add(name)
    
    def _get_text(self, elem, tag):
        """Get text content of a child element."""
        child = elem.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return None


class NFOStandardTVAgent(Agent.TV_Shows):
    """TV Show agent for NFO Standard files."""
    
    name = NFO_AGENT_NAME
    ver = '1.0.0'
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ['com.plexapp.agents.localmedia']
    
    def search(self, results, media, lang):
        """Search for TV show metadata."""
        Log.Info('Searching for TV show: %s' % media.show)
        
        # Look for tvshow.nfo
        nfo_path = self._find_show_nfo(media)
        if nfo_path:
            Log.Info('Found TV show NFO: %s' % nfo_path)
            results.Append(MetadataSearchResult(
                id=nfo_path,
                name=media.show,
                year=media.year,
                score=100,
                lang=lang
            ))
    
    def update(self, metadata, media, lang):
        """Update TV show metadata from NFO file."""
        # Update show metadata
        show_nfo = metadata.id
        if show_nfo and os.path.exists(show_nfo):
            self._update_show_from_nfo(metadata, show_nfo)
        
        # Update seasons and episodes
        for season_num in media.seasons:
            season = metadata.seasons[season_num]
            
            for episode_num in media.seasons[season_num].episodes:
                episode = season.episodes[episode_num]
                episode_media = media.seasons[season_num].episodes[episode_num]
                
                # Find episode NFO
                episode_nfo = self._find_episode_nfo(episode_media)
                if episode_nfo:
                    self._update_episode_from_nfo(episode, episode_nfo)
    
    def _find_show_nfo(self, media):
        """Find tvshow.nfo file."""
        # Try to find show directory
        if media.seasons:
            for season in media.seasons.values():
                if season.episodes:
                    for episode in season.episodes.values():
                        if episode.items:
                            for item in episode.items:
                                if item.parts:
                                    video_path = item.parts[0].file
                                    # Go up directories looking for tvshow.nfo
                                    dir_path = os.path.dirname(video_path)
                                    
                                    for _ in range(3):  # Check up to 3 levels
                                        tvshow_nfo = os.path.join(dir_path, 'tvshow.nfo')
                                        if os.path.exists(tvshow_nfo):
                                            return tvshow_nfo
                                        dir_path = os.path.dirname(dir_path)
        return None
    
    def _find_episode_nfo(self, episode_media):
        """Find episode NFO file."""
        if episode_media.items:
            for item in episode_media.items:
                if item.parts:
                    video_path = item.parts[0].file
                    base_name = os.path.splitext(video_path)[0]
                    episode_nfo = base_name + '.nfo'
                    if os.path.exists(episode_nfo):
                        return episode_nfo
        return None
    
    def _update_show_from_nfo(self, metadata, nfo_path):
        """Update TV show metadata from NFO."""
        try:
            tree = etree.parse(nfo_path)
            root = tree.getroot()
            
            # Find tvshow element
            tvshow = root.find('.//{{{0}}}tvshow'.format('NFOStandard'))
            if tvshow is None:
                tvshow = root.find('.//tvshow')
            
            if tvshow is None:
                Log.Error('No tvshow element found in NFO')
                return
            
            # Update show metadata
            title = self._get_text(tvshow, 'title')
            if title:
                metadata.title = title
            
            plot = self._get_text(tvshow, 'plot')
            if plot:
                metadata.summary = plot
            
            # Year
            year = self._get_text(tvshow, 'year')
            if year:
                try:
                    metadata.year = int(year)
                except:
                    pass
            
            # Premiered
            premiered = self._get_text(tvshow, 'premiered')
            if premiered:
                try:
                    metadata.originally_available_at = Datetime.ParseDate(premiered).date()
                except:
                    pass
            
            # Studio
            studio = self._get_text(tvshow, 'studio')
            if studio:
                metadata.studio = studio
            
            # Genres
            metadata.genres.clear()
            for genre in tvshow.findall('genre'):
                if genre.text:
                    metadata.genres.add(genre.text)
            
            # Content rating
            for content_rating in tvshow.findall('contentrating'):
                rating = content_rating.get('rating')
                if not rating and content_rating.text:
                    rating = content_rating.text
                if rating:
                    metadata.content_rating = rating
                    break
            
            # Actors
            metadata.roles.clear()
            for actor in tvshow.findall('actor'):
                role = metadata.roles.new()
                
                name = self._get_text(actor, 'name')
                if name:
                    role.name = name
                
                character = self._get_text(actor, 'role')
                if character:
                    role.role = character
                
                thumb = self._get_text(actor, 'thumb')
                if thumb:
                    role.photo = thumb
            
        except Exception as e:
            Log.Error('Error parsing show NFO: %s' % str(e))
    
    def _update_episode_from_nfo(self, episode, nfo_path):
        """Update episode metadata from NFO."""
        try:
            tree = etree.parse(nfo_path)
            root = tree.getroot()
            
            # Find episode element
            ep_elem = root.find('.//{{{0}}}episode'.format('NFOStandard'))
            if ep_elem is None:
                ep_elem = root.find('.//episode')
            
            if ep_elem is None:
                # Try episodedetails (Kodi format)
                ep_elem = root.find('.//episodedetails')
            
            if ep_elem is None:
                return
            
            # Update episode metadata
            title = self._get_text(ep_elem, 'title')
            if title:
                episode.title = title
            
            plot = self._get_text(ep_elem, 'plot')
            if plot:
                episode.summary = plot
            
            # Air date
            aired = self._get_text(ep_elem, 'aired')
            if aired:
                try:
                    episode.originally_available_at = Datetime.ParseDate(aired).date()
                except:
                    pass
            
            # Rating
            for rating in ep_elem.findall('rating'):
                value = rating.get('value')
                if value:
                    try:
                        episode.rating = float(value)
                        break
                    except:
                        pass
            
            # Directors
            episode.directors.clear()
            for director in ep_elem.findall('director'):
                name = self._get_text(director, 'name')
                if name:
                    episode.directors.add(name)
            
            # Writers
            episode.writers.clear()
            for writer in ep_elem.findall('writer'):
                name = self._get_text(writer, 'name')
                if name:
                    episode.writers.add(name)
            
        except Exception as e:
            Log.Error('Error parsing episode NFO: %s' % str(e))
    
    def _get_text(self, elem, tag):
        """Get text content of a child element."""
        child = elem.find(tag)
        if child is not None and child.text:
            return child.text.strip()
        return None