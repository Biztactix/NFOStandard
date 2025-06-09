# Content Rating Country Code Testing

## Test Results for GetContentRatingInfo Method

### US Ratings (MPAA)
- "G" → country: "US", board: "MPAA" ✅
- "PG" → country: "US", board: "MPAA" ✅  
- "PG-13" → country: "US", board: "MPAA" ✅
- "R" → country: "US", board: "MPAA" ✅
- "NC-17" → country: "US", board: "MPAA" ✅

### US TV Ratings (FCC)
- "TV-Y" → country: "US", board: "FCC" ✅
- "TV-PG" → country: "US", board: "FCC" ✅
- "TV-14" → country: "US", board: "FCC" ✅
- "TV-MA" → country: "US", board: "FCC" ✅

### UK Ratings (BBFC)
- "U" → country: "GB", board: "BBFC" ✅
- "12A" → country: "GB", board: "BBFC" ✅
- "R18" → country: "GB", board: "BBFC" ✅

### German Ratings (FSK)
- "FSK12" → country: "DE", board: "FSK" ✅
- "FSK16" → country: "DE", board: "FSK" ✅

### Australian Ratings (OFLC)
- "MA15+" → country: "AU", board: "OFLC" ✅
- "R18+" → country: "AU", board: "OFLC" ✅
- "M" → country: "AU", board: "OFLC" ✅

### Canadian Ratings (CHVRS)
- "14A" → country: "CA", board: "CHVRS" ✅
- "18A" → country: "CA", board: "CHVRS" ✅

### Japanese Ratings (EIRIN)
- "PG12" → country: "JP", board: "EIRIN" ✅
- "R15+" → country: "JP", board: "EIRIN" ✅

### French Ratings (CSA)
- "TP" → country: "FR", board: "CSA" ✅

## XML Output Examples

### Before (Incorrect)
```xml
<contentrating country="USA" board="MPAA" rating="PG-13"/>
```

### After (Correct - ISO 3166-1)
```xml
<contentrating country="US" board="MPAA" rating="PG-13"/>
```

## Changes Made

1. **Updated NFOStandardMovieSaver.cs**: Added GetContentRatingInfo() method
2. **Updated NFOStandardSeriesSaver.cs**: Added GetContentRatingInfo() method with TV rating support
3. **ISO 3166-1 Country Codes**: Now uses proper 2-letter codes (US, GB, DE, AU, CA, JP, FR)
4. **Board Detection**: Automatically detects rating boards based on rating patterns
5. **TV Ratings**: Special handling for TV series with FCC/TV Parental Guidelines

## Implementation Details

The detection logic prioritizes:
1. Specific patterns (FSK prefixes, + symbols, A suffixes)
2. Unique ratings (12A, R18, MA15+, etc.)  
3. Common but ambiguous ratings (G, PG, R) - defaults to US
4. Special TV rating patterns for series

This ensures accurate country and board detection for international content.