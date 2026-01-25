using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;

namespace NFOStandard.Xml;

internal static class NfoSchemaRegistry
{
    private const string ResourcePrefix = "NFOStandard.Xml.Schemas/";
    private static readonly Regex VersionRegex = new(@"/v(?<version>\d+)/", RegexOptions.IgnoreCase | RegexOptions.Compiled);
    private static readonly Lazy<Dictionary<string, string>> ResourceIndex = new(BuildResourceIndex);

    public static string? DetectVersion(string? schemaLocation)
    {
        if (string.IsNullOrWhiteSpace(schemaLocation))
        {
            return null;
        }

        var match = VersionRegex.Match(schemaLocation);
        if (!match.Success)
        {
            return null;
        }

        return $"v{match.Groups["version"].Value}";
    }

    public static Stream? OpenSchema(string version, string relativePath)
    {
        var key = NormalizeKey(version, relativePath);
        if (!ResourceIndex.Value.TryGetValue(key, out var resourceName))
        {
            return null;
        }

        var assembly = Assembly.GetExecutingAssembly();
        return assembly.GetManifestResourceStream(resourceName);
    }

    public static bool HasVersion(string version)
    {
        var prefix = NormalizeKey(version, string.Empty);
        return ResourceIndex.Value.Keys.Any(key => key.StartsWith(prefix, StringComparison.OrdinalIgnoreCase));
    }

    private static Dictionary<string, string> BuildResourceIndex()
    {
        var assembly = Assembly.GetExecutingAssembly();
        var resources = assembly.GetManifestResourceNames()
            .Where(name => name.StartsWith(ResourcePrefix, StringComparison.OrdinalIgnoreCase))
            .ToList();

        var index = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var resource in resources)
        {
            var key = resource.Substring(ResourcePrefix.Length).Replace('\\', '/');
            index[key] = resource;
        }

        return index;
    }

    private static string NormalizeKey(string version, string relativePath)
    {
        var normalizedVersion = version.Trim().Trim('/');
        var normalizedPath = relativePath.Replace('\\', '/').TrimStart('/');
        return string.IsNullOrWhiteSpace(normalizedPath)
            ? normalizedVersion + "/"
            : $"{normalizedVersion}/{normalizedPath}";
    }
}
