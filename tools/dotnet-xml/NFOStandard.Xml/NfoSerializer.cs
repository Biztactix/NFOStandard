using System.IO;
using System.Text;
using System.Xml;
using System.Xml.Schema;
using System.Xml.Serialization;

namespace NFOStandard.Xml;

public static class NfoSerializer
{
    private static readonly XmlSerializer Serializer = new(typeof(NfoRoot));

    public static NfoRoot Load(string path)
    {
        using var stream = File.OpenRead(path);
        return (NfoRoot)Serializer.Deserialize(stream)!;
    }

    public static NfoRoot Deserialize(string xml)
    {
        using var reader = new StringReader(xml);
        return (NfoRoot)Serializer.Deserialize(reader)!;
    }

    public static string Serialize(NfoRoot root, string? schemaLocation = null)
    {
        EnsureSchemaLocation(root, schemaLocation);

        using var writer = new Utf8StringWriter();
        using var xmlWriter = XmlWriter.Create(writer, new XmlWriterSettings
        {
            Indent = true,
            OmitXmlDeclaration = false
        });

        Serializer.Serialize(xmlWriter, root, BuildNamespaces());
        return writer.ToString();
    }

    public static void Save(NfoRoot root, string path, string? schemaLocation = null)
    {
        EnsureSchemaLocation(root, schemaLocation);

        using var stream = File.Create(path);
        using var xmlWriter = XmlWriter.Create(stream, new XmlWriterSettings
        {
            Indent = true,
            Encoding = new UTF8Encoding(false),
            OmitXmlDeclaration = false
        });

        Serializer.Serialize(xmlWriter, root, BuildNamespaces());
    }

    private static void EnsureSchemaLocation(NfoRoot root, string? schemaLocation)
    {
        if (string.IsNullOrWhiteSpace(root.SchemaLocation))
        {
            root.SchemaLocation = schemaLocation ?? NfoConstants.SchemaLocation;
        }
    }

    private static XmlSerializerNamespaces BuildNamespaces()
    {
        var namespaces = new XmlSerializerNamespaces();
        namespaces.Add(string.Empty, NfoConstants.Namespace);
        namespaces.Add("xsi", XmlSchema.InstanceNamespace);
        return namespaces;
    }

    private sealed class Utf8StringWriter : StringWriter
    {
        public override Encoding Encoding => Encoding.UTF8;
    }
}
