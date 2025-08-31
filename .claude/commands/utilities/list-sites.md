---
description: List all configured Atlassian sites available in Conduit
argument-hint: ""
allowed-tools: ["mcp__Conduit__list_atlassian_sites"]
---

I'll list all configured Atlassian sites that Conduit can connect to.

## Fetching Site Configuration

Use mcp__Conduit__list_atlassian_sites to retrieve all configured sites.

This will show:
- Site aliases (used in commands)
- Site URLs
- Site types (Jira/Confluence)

You can use any of the listed site aliases with commands that require a [SITE-ALIAS] parameter.