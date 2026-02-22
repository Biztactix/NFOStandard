---
assignee: claude
created: '2026-02-22'
id: US-NFO-2-4
points: 2
status: done
story_id: US-NFO-2
title: Define serviceLinksType in common.xsd and refactor consumers
updated: '2026-02-22'
---

Extract the duplicated inline serviceLinks complexType into a named type in common.xsd, then refactor music.xsd, musicvideo.xsd, and podcast.xsd to use it.

New type to add to common.xsd:
```xml
<xs:complexType name="serviceLinkType">
    <xs:sequence>
        <xs:element name="service" type="xs:string" minOccurs="1" maxOccurs="1"/>
        <xs:element name="url" type="xs:string" minOccurs="1" maxOccurs="1"/>
    </xs:sequence>
</xs:complexType>
```

Then in each consumer schema, replace the inline complexType with:
```xml
<xs:element name="serviceLinks" type="serviceLinkType" minOccurs="0" maxOccurs="unbounded"/>
```

Files: Schemas/common.xsd, Schemas/music.xsd, Schemas/musicvideo.xsd, Schemas/podcast.xsd