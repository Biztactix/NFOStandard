# NFOStandard

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Biztactix/NFOStandard/releases)
[![License](https://img.shields.io/badge/license-Unlicense-green.svg)](LICENSE)
[![Validation](https://img.shields.io/badge/examples-100%25%20valid-green.svg)](#validation)

Welcome to the Open NFO Standard repository! This project aims to create a unified, open standard for .nfo files used in various media applications, eliminating the need for each application to create its own format. This standard is designed to cover 95% of use cases, with built-in extensibility for fringe cases.

## Current Version: 2.0.0

🚨 **Version 2.0.0 contains breaking changes from v1.0.0**. See the [CHANGELOG](CHANGELOG.md) for migration details.

### Implementation Status
- ✅ **Schemas**: Complete v2.0.0 with 100% validation success
- ✅ **User Guides**: All 7 guides completed
- ✅ **Migration Guides**: All 3 guides completed  
- ✅ **Test Infrastructure**: Comprehensive test suite
- ✅ **Emby Plugin**: v1.0.0 for Emby 4.8+
- ⚠️ **API Reference**: 25% complete (missing detailed docs)
- ❌ **Contributing Guide**: Not yet created
- ❌ **Package Distribution**: PyPI/npm packages pending

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Example XML File](#example-xml-file)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The NFO Standard is designed to provide a consistent and comprehensive metadata format for media files. By adopting this standard, applications can save countless hours reinventing the wheel and ensure compatibility across different platforms.

## Features

- **Unified Structure**: A single, comprehensive format for .nfo files.
- **Extensibility**: Easily extendable to cover fringe use cases.
- **Modularity**: Separate XSLT files for different types of content (Movies, TV Shows, Porn Videos, Anime).
- **Open Source**: Licensed under The Unlicense, making it free for everyone to use and contribute.

## File Structure

- `main.xsd`: The master XSD file that includes or imports other XSD files based on the content type.
- `common.xsd`: Contains common custom content types.
- `person.xsd`: Contains common elements for the person types associated with the content.
- `library.xsd`: Contains common elements for Library Software to use.
- `adult.xsd`: Specific schema definitions for adult video content.
- `anime.xsd`: Specific schema definitions for anime content.
- `audiobook.xsd`: Specific schema definitions for audiobook content.
- `movie.xsd`: Specific schema definitions for movie content.
- `music.xsd`: Specific schema definitions for music content.
- `musicvideo.xsd`: Specific schema definitions for music video content.
- `podcast.xsd`: Specific schema definitions for podcast content.
- `tvshow.xsd`: Specific schema definitions for TV show content.
- `video.xsd`: Specific schema definitions for general video content.

## Example XML File
This is an example of how to use the XSDs to reference it so that it's easy for others to understand and apps to extract the content.
```
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/v2/main.xsd">
	<media>
	  <movie>
		<title>Inception</title>
		<originaltitle>Inception</originaltitle>
		<sorttitle>Inception</sorttitle>
		<alternatetitle>Origem</alternatetitle>
		<alternatetitle>Début</alternatetitle>
		<rating name="imdb" max="10" default="true" value="8.8" votes="200000"/>
		<userrating>9.0</userrating>
		<outline>A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.</outline>
		<plot>Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction: stealing valuable secrets from deep within the subconscious during the dream state when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted player in this treacherous new world of corporate espionage, but it has also made him an international fugitive and cost him everything he has ever loved. Now Cobb is being offered a chance at redemption. One last job could give him his life back but only if he can accomplish the impossible, inception.</plot>
		<tagline>Your mind is the scene of the crime.</tagline>
		<runtime>148</runtime>
		<banner type="poster" width="300" height="450" url="http://example.com/banner1.jpg"/>
        <thumb type="thumbnail" width="150" height="150" url="http://example.com/thumb1.jpg"/>
        <fanart type="background" width="1920" height="1080" url="http://example.com/fanart1.jpg"/>
		<contentrating country="US" board="MPAA">
			<rating>PG-13</rating>
			<image>mpaa_pg13.png</image>
		</contentrating>
		<uniqueid type="imdb" default="true">tt1375666</uniqueid>
		<uniqueid type="tmdb">12345</uniqueid>
		<genre>Action</genre>
		<genre>Sci-Fi</genre>
		<tag>Heist</tag>
		<tag>Dream</tag>
		<setname>Inception Series</setname>
		<setoverview>Movies about dream extraction.</setoverview>
		<country>USA</country>
		<productioncompany>Warner Bros.</productioncompany>
		<keyword>dream</keyword>
		<keyword>heist</keyword>
		<releasedate>2010-07-16</releasedate>
		<award>Academy Award for Best Cinematography</award>
		<subtitlelanguage>English</subtitlelanguage>
		<soundtrack>Inception OST</soundtrack>
		<parentalguide>Some material may be inappropriate for children under 13.</parentalguide>
		<actor>
		  <name>Leonardo DiCaprio</name>
		  <role>Dom Cobb</role>
		  <order>1</order>
		  <thumb>leo.jpg</thumb>
		  <bio>Leonardo Wilhelm DiCaprio is an American actor and film producer.</bio>
		  <url>https://www.imdb.com/name/nm0000138/</url>
		</actor>
		<actor>
		  <name>Joseph Gordon-Levitt</name>
		  <role>Arthur</role>
		  <order>2</order>
		  <thumb>joseph.jpg</thumb>
		  <bio>Joseph Leonard Gordon-Levitt is an American actor and filmmaker.</bio>
		  <url>https://www.imdb.com/name/nm0330687/</url>
		</actor>
		<director>
		  <name>Christopher Nolan</name>
		  <thumb>nolan.jpg</thumb>
		  <bio>Christopher Edward Nolan is a British-American film director, screenwriter, and producer.</bio>
		  <url>https://www.imdb.com/name/nm0634240/</url>
		</director>
		<writer>
		  <name>Christopher Nolan</name>
		  <thumb>nolan.jpg</thumb>
		  <bio>Christopher Edward Nolan is a British-American film director, screenwriter, and producer.</bio>
		  <url>https://www.imdb.com/name/nm0634240/</url>
		</writer>
	  </movie>
	</media>
</root>

```

## Contributing

We welcome contributions from the community! 
I will endeavor to review and approve pull requests in a timely manner.

## License

This project is licensed under The Unlicense, which means it is free to use for everyone. See the LICENSE file for more details.

## Contact

For any questions or comments, please open an issue on this repository.

---

Thank you for your interest in the NFO Standard. Together, we can make media metadata management easier and more consistent for everyone!
