using System.Xml.Schema;
using System.Xml.Serialization;

namespace NFOStandard.Xml;

public sealed partial class NfoRoot
{
    [XmlAttribute("schemaLocation", Namespace = XmlSchema.InstanceNamespace)]
    public string? SchemaLocation { get; set; }
}
