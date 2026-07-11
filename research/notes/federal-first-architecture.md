# Federal-first architecture

The federal layer has enough common, documented sources to justify a single MCP server. State and local sources should be represented by jurisdiction-aware adapters and platform drivers rather than a false universal schema.

Initial platform drivers to investigate after federal MVP: Socrata, ArcGIS REST and CKAN. Each source record must preserve authority, jurisdiction, auth, licence, freshness and upstream URL.
