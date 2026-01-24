# NFOStandard .NET XML Toolkit

This tool provides generated .NET models and validation for NFO Standard XML
files. It includes a class library for integration and a small CLI wrapper for
local validation.

## Projects

- `NFOStandard.Xml`: class library intended for NuGet packaging
- `NFOStandard.Xml.Console`: CLI for validating XML files

## Requirements

- .NET 8.0 SDK or later

## Build

```bash
dotnet build tools/dotnet-xml/NFOStandard.Xml.Console/NFOStandard.Xml.Console.csproj
```

## CLI Usage

```bash
dotnet run --project tools/dotnet-xml/NFOStandard.Xml.Console -- \
  --file examples/tvshow.xml \
  --schema-dir v2
```

Arguments:
- `--file`, `-f`: XML file to validate (required)
- `--schema-dir`, `-s`: Path containing `main.xsd` and `Schemas/` (defaults to `./v2` when present)
- `--json`: Output results as JSON

## Library Usage

```csharp
using NFOStandard.Xml;

var root = NfoSerializer.Load("movie.nfo");
var movie = root.Media.Movie;

// Make edits using the strongly typed model
if (movie != null)
{
    movie.Title = "Updated Title";
}

NfoSerializer.Save(root, "movie.updated.nfo");
```

## NuGet Packaging

```bash
dotnet pack tools/dotnet-xml/NFOStandard.Xml/NFOStandard.Xml.csproj -c Release
```

The package metadata is configured in `NFOStandard.Xml.csproj` and is
ready for future publishing.

## Model Generation

The models are generated at build time from the `v2` XSDs using a source
generator. Updating the schema files will regenerate the models automatically.
