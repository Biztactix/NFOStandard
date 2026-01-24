using System;
using System.IO;
using System.Xml;

namespace NFOStandard.Xml;

internal sealed class LocalSchemaResolver : XmlUrlResolver
{
    private readonly string _schemaRoot;

    public LocalSchemaResolver(string schemaRoot)
    {
        _schemaRoot = schemaRoot;
    }

    public override object GetEntity(Uri absoluteUri, string? role, Type? ofObjectToReturn)
    {
        var localPath = TryResolveLocalPath(absoluteUri);
        if (localPath != null && File.Exists(localPath))
        {
            return new FileStream(localPath, FileMode.Open, FileAccess.Read, FileShare.Read);
        }

        return base.GetEntity(absoluteUri, role, ofObjectToReturn)!;
    }

    private string? TryResolveLocalPath(Uri absoluteUri)
    {
        var path = absoluteUri.AbsolutePath.Replace('\\', '/');
        if (path.EndsWith("/main.xsd", StringComparison.OrdinalIgnoreCase))
        {
            return Path.Combine(_schemaRoot, "main.xsd");
        }

        if (path.IndexOf("/Schemas/", StringComparison.OrdinalIgnoreCase) >= 0)
        {
            var filename = Path.GetFileName(path);
            return Path.Combine(_schemaRoot, "Schemas", filename);
        }

        return null;
    }
}
