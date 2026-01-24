# NFOStandard.Xml

`NFOStandard.Xml` provides models and an offline-capable XML validator for the
NFO Standard schemas. It is designed to be packaged for NuGet and embedded in
.NET applications that need to validate `.nfo` files.

## Usage

```csharp
using NFOStandard.Xml;

var root = NfoSerializer.Load("movie.nfo");
var movie = root.Media.Movie;

var validator = new NfoValidator();
var result = validator.ValidateFile("movie.nfo", "./v2");
if (!result.IsValid)
{
    foreach (var error in result.Errors)
    {
        Console.WriteLine(error);
    }
}

NfoSerializer.Save(root, "movie.updated.nfo");
```

`schemaDir` should point to a directory that contains `main.xsd` and a
`Schemas/` folder. When omitted, the validator will look for `./v2`.

## Roadmap

- Add a source generator to keep the model classes synchronized with the XSDs.
