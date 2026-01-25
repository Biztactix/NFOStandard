# NFOStandard.Xml

`NFOStandard.Xml` provides generated models and an offline-capable XML
validator for the NFO Standard schemas. It is designed to be packaged for
NuGet and embedded in .NET applications that need to validate `.nfo` files
and work with strongly typed objects.

## Usage

```csharp
using NFOStandard.Xml;

var root = NfoSerializer.Load("movie.nfo");
var movie = root.Media.Movie;

if (movie != null)
{
    movie.Title = "Updated Title";
    movie.Genre.Add("Sci-Fi");
    movie.ContentRating.Add(new ContentRating
    {
        Country = "US",
        Board = "MPAA",
        Rating = "PG-13"
    });
}

NfoSerializer.Save(root, "movie.updated.nfo");
```

### Validate Files

```csharp
using NFOStandard.Xml;

var validator = new NfoValidator();
var result = validator.ValidateFile("movie.nfo", "./v2");

if (!result.IsValid)
{
    foreach (var error in result.Errors)
    {
        Console.WriteLine(error);
    }
}
```

If you omit `schemaDir`, the validator inspects `xsi:schemaLocation` and uses
the embedded schema version when available:

```csharp
var validator = new NfoValidator();
var result = validator.ValidateFile("movie.nfo");
```

### Create a New Document

```csharp
using NFOStandard.Xml;

var root = new NfoRoot
{
    Media = new Media
    {
        Movie = new Movie
        {
            Title = "New Movie",
            ReleaseDate = new List<DateTime> { new DateTime(2024, 5, 1) },
            Genre = new List<string> { "Drama" }
        }
    }
};

NfoSerializer.Save(root, "new_movie.nfo");
```

### Work With Enums

```csharp
using NFOStandard.Xml;

var file = new MediaFile
{
    Type = MediaFileTypeEnum.FanArt,
    Url = "https://example.com/fanart.jpg"
};

var person = new Person
{
    Name = "Jane Doe",
    Gender = PersonGenderEnum.NonBinary
};
```

`schemaDir` should point to a directory that contains `main.xsd` and a
`Schemas/` folder. When omitted, the validator will look for `./v2`.

## Model Generation

The package uses a source generator to produce strongly typed models from the
versioned XSD files embedded in the NuGet package. The generator runs at build
time and stays locked to the schema version shipped with the package; upgrading
the package is how you move to a newer schema.

## Compatibility Plan

- NuGet version aligns with schema version (v2 package ships v2 schemas/models).
- When v3 is released, `NFOStandard.Xml` v3 will embed both v2 and v3 schemas so
  it can read v2 or v3 inputs.
- The v3 package will only write v3 output; upgrading legacy content will be a
  one-way operation via `object.Migrate()` to a v3 model.
