// NFO Standard Web Importer - API Integration Module

// API Client for server-side integration
class NFOImporterAPI {
    constructor(config) {
        this.config = config;
        this.apiServer = config.API_SERVER;
        this.useMockData = config.FEATURES.USE_MOCK_DATA || !this.apiServer;
    }
    
    // Fetch movie metadata
    async fetchMovie(movieId, source) {
        if (this.useMockData) {
            return this.getMockMovieData(movieId, source);
        }
        
        try {
            const response = await fetch(`${this.apiServer}/api/movie/${source}/${movieId}`);
            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching movie:', error);
            // Fallback to mock data on error
            return this.getMockMovieData(movieId, source);
        }
    }
    
    // Fetch TV show metadata
    async fetchTVShow(tvId, source) {
        if (this.useMockData) {
            return this.getMockTVShowData(tvId, source);
        }
        
        try {
            const response = await fetch(`${this.apiServer}/api/tv/${source}/${tvId}`);
            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching TV show:', error);
            // Fallback to mock data on error
            return this.getMockTVShowData(tvId, source);
        }
    }
    
    // Search for movies or TV shows
    async search(type, query) {
        if (this.useMockData) {
            return this.getMockSearchResults(type, query);
        }
        
        try {
            const response = await fetch(`${this.apiServer}/api/search/${type}?q=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error searching:', error);
            // Fallback to mock data on error
            return this.getMockSearchResults(type, query);
        }
    }
    
    // Mock data methods
    getMockMovieData(movieId, source) {
        return {
            type: 'movie',
            title: 'The Shawshank Redemption',
            originaltitle: 'The Shawshank Redemption',
            year: 1994,
            plot: 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            runtime: 142,
            genre: ['Drama'],
            director: ['Frank Darabont'],
            writer: ['Stephen King', 'Frank Darabont'],
            actors: [
                { name: 'Tim Robbins', role: 'Andy Dufresne' },
                { name: 'Morgan Freeman', role: 'Ellis Boyd \'Red\' Redding' }
            ],
            rating: {
                imdb: { value: 9.3, votes: 2500000 }
            },
            contentrating: 'R',
            country: ['USA'],
            language: ['English'],
            imdbid: movieId.startsWith('tt') ? movieId : 'tt0111161',
            poster: 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg'
        };
    }
    
    getMockTVShowData(tvId, source) {
        if (source === 'tvdb') {
            return {
                type: 'tvshow',
                title: 'Game of Thrones',
                originaltitle: 'Game of Thrones',
                year: 2011,
                plot: 'Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.',
                genre: ['Adventure', 'Drama', 'Fantasy'],
                creator: ['David Benioff', 'D.B. Weiss'],
                actors: [
                    { name: 'Emilia Clarke', role: 'Daenerys Targaryen' },
                    { name: 'Peter Dinklage', role: 'Tyrion Lannister' },
                    { name: 'Kit Harington', role: 'Jon Snow' }
                ],
                rating: {
                    tvdb: { value: 9.3, votes: 1800000 }
                },
                contentrating: 'TV-MA',
                status: 'Ended',
                premiered: '2011-04-17',
                studio: ['HBO'],
                seasons: 8,
                episodes: 73,
                tvdbid: tvId,
                imdbid: 'tt0944947'
            };
        } else {
            return {
                type: 'tvshow',
                title: 'Breaking Bad',
                originaltitle: 'Breaking Bad',
                year: 2008,
                plot: 'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family\'s future.',
                genre: ['Crime', 'Drama', 'Thriller'],
                creator: ['Vince Gilligan'],
                actors: [
                    { name: 'Bryan Cranston', role: 'Walter White' },
                    { name: 'Aaron Paul', role: 'Jesse Pinkman' },
                    { name: 'Anna Gunn', role: 'Skyler White' }
                ],
                rating: {
                    tmdb: { value: 8.7, votes: 8000 }
                },
                contentrating: 'TV-MA',
                status: 'Ended',
                premiered: '2008-01-20',
                studio: ['AMC'],
                seasons: 5,
                episodes: 62,
                tmdbid: tvId,
                imdbid: 'tt0903747'
            };
        }
    }
    
    getMockSearchResults(type, query) {
        if (type === 'movie') {
            return [
                {
                    id: '278',
                    title: 'The Shawshank Redemption',
                    year: 1994,
                    overview: 'Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison.'
                },
                {
                    id: '238',
                    title: 'The Godfather',
                    year: 1972,
                    overview: 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family.'
                },
                {
                    id: '424',
                    title: 'Schindler\'s List',
                    year: 1993,
                    overview: 'The true story of how businessman Oskar Schindler saved over a thousand Jewish lives from the Nazis.'
                }
            ];
        } else {
            return [
                {
                    id: '1396',
                    title: 'Breaking Bad',
                    year: 2008,
                    overview: 'When Walter White, a New Mexico chemistry teacher, is diagnosed with Stage III cancer and given a prognosis of only two years left to live.'
                },
                {
                    id: '1399',
                    title: 'Game of Thrones',
                    year: 2011,
                    overview: 'Seven noble families fight for control of the mythical land of Westeros. Friction between the houses leads to full-scale war.'
                },
                {
                    id: '1418',
                    title: 'The Big Bang Theory',
                    year: 2007,
                    overview: 'A woman who moves into an apartment across the hall from two brilliant but socially awkward physicists shows them how little they know about life outside of the laboratory.'
                }
            ];
        }
    }
}

// Create global API instance
const nfoAPI = new NFOImporterAPI(CONFIG);