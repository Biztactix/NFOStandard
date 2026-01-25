using System;
using System.IO;
using System.Xml;

namespace NFOStandard.Xml;

internal sealed class EmbeddedSchemaResolver : XmlUrlResolver
{
    private readonly string _version;

    public EmbeddedSchemaResolver(string version)
    {
        _version = version;
    }

    public override object GetEntity(Uri absoluteUri, string? role, Type? ofObjectToReturn)
    {
        var relativePath = GetRelativePath(absoluteUri);
        if (relativePath != null)
        {
            var stream = NfoSchemaRegistry.OpenSchema(_version, relativePath);
            if (stream != null)
            {
                return stream;
            }
        }

        return base.GetEntity(absoluteUri, role, ofObjectToReturn)!;
    }

    private static string? GetRelativePath(Uri absoluteUri)
    {
        var path = absoluteUri.AbsolutePath.Replace('\\', '/');
        if (path.EndsWith("/main.xsd", StringComparison.OrdinalIgnoreCase))
        {
            return "main.xsd";
        }

        var schemasIndex = path.IndexOf("/Schemas/", StringComparison.OrdinalIgnoreCase);
        if (schemasIndex >= 0)
        {
            var fileName = Path.GetFileName(path);
            if (!string.IsNullOrWhiteSpace(fileName))
            {
                return $"Schemas/{fileName}";
            }
        }

        return null;
    }
}
