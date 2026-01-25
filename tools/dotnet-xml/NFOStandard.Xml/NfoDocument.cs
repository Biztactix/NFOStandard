using System;
using System.IO;
using System.Xml.Linq;

namespace NFOStandard.Xml;

public sealed class NfoDocument
{
    private NfoDocument(XDocument document)
    {
        Document = document;
    }

    public XDocument Document { get; }

    public XElement? Media => Document.Root?.Element(XName.Get("media", Document.Root?.Name.NamespaceName ?? string.Empty));

    public static NfoDocument Load(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            throw new ArgumentException("File path is required.", nameof(path));
        }

        using var stream = File.OpenRead(path);
        var document = XDocument.Load(stream, LoadOptions.PreserveWhitespace);
        return new NfoDocument(document);
    }

    public static NfoDocument Parse(string xml)
    {
        if (string.IsNullOrWhiteSpace(xml))
        {
            throw new ArgumentException("XML content is required.", nameof(xml));
        }

        var document = XDocument.Parse(xml, LoadOptions.PreserveWhitespace);
        return new NfoDocument(document);
    }

    public string ToXmlString()
    {
        using var writer = new StringWriter();
        Document.Save(writer, SaveOptions.DisableFormatting);
        return writer.ToString();
    }

    public void Save(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            throw new ArgumentException("File path is required.", nameof(path));
        }

        Document.Save(path, SaveOptions.DisableFormatting);
    }
}
