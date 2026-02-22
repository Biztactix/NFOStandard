# NFOStandard

Welcome to the Open NFO Standard repository! This project aims to create a unified, open standard for .nfo files used in various media applications, eliminating the need for each application to create its own format. This standard is designed to cover 95% of use cases, with built-in extensibility for fringe cases.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Example XML File](#example-xml-file)
- [Local Validation](#local-validation)
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
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
	<media>
	  <movie>
		<title>Inception</title>
		<originalTitle>Inception</originalTitle>
		<sortTitle>Inception</sortTitle>
		<alternateTitle>Origem</alternateTitle>
		<alternateTitle>Début</alternateTitle>
		<rating name="imdb" max="10" default="true" value="8.8" votes="200000"/>
		<userRating>9.0</userRating>
		<outline>A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.</outline>
		<plot>Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction: stealing valuable secrets from deep within the subconscious during the dream state when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted player in this treacherous new world of corporate espionage, but it has also made him an international fugitive and cost him everything he has ever loved. Now Cobb is being offered a chance at redemption. One last job could give him his life back but only if he can accomplish the impossible, inception.</plot>
		<tagline>Your mind is the scene of the crime.</tagline>
		<runtime>148</runtime>
		<banner type="poster" width="300" height="450" url="http://example.com/banner1.jpg"/>
        <thumb type="thumbnail" width="150" height="150" url="http://example.com/thumb1.jpg"/>
        <fanart type="background" width="1920" height="1080" url="http://example.com/fanart1.jpg"/>
		<contentRating country="USA" board="MPAA" rating="PG-13" image="mpaa_pg13.png"/>
		<uniqueId type="imdb" default="true">tt1375666</uniqueId>
		<uniqueId type="tmdb">12345</uniqueId>
		<genre>Action</genre>
		<genre>Sci-Fi</genre>
		<tag>Heist</tag>
		<tag>Dream</tag>
		<setName>Inception Series</setName>
		<setOverview>Movies about dream extraction.</setOverview>
		<country>USA</country>
		<productionCompany>Warner Bros.</productionCompany>
		<keyword>dream</keyword>
		<keyword>heist</keyword>
		<releaseDate>2010-07-16</releaseDate>
		<award>Academy Award for Best Cinematography</award>
		<subtitleLanguage>English</subtitleLanguage>
		<soundtrack>Inception OST</soundtrack>
		<parentalGuide>Some material may be inappropriate for children under 13.</parentalGuide>
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

## Local Validation

You can validate the XSD schemas and example XML files locally using the provided validation script.

### Prerequisites

Install `libxml2-utils` which provides `xmllint`:

```bash
# Ubuntu / Debian
sudo apt-get install -y libxml2-utils

# macOS (via Homebrew)
brew install libxml2
```

### Running Validation

```bash
./validate.sh
```

This checks:
- **XSD well-formedness** — all schema files parse correctly
- **Example XML validation** — all `Example*.xml` and `Sample*.xml` files validate against `main.xsd`

### Continuous Integration

Validation runs automatically on pushes to `main` and on pull requests via GitHub Actions. See `.github/workflows/validate.yml`.

## Contributing

We welcome contributions from the community!
I will endeavor to review and approve pull requests in a timely manner.

## License

This project is licensed under The Unlicense, which means it is free to use for everyone. See the LICENSE file for more details.

## Contact

For any questions or comments, please open an issue on this repository.

---

Thank you for your interest in the NFO Standard. Together, we can make media metadata management easier and more consistent for everyone!
