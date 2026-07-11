# HERMES — Agent Guide

Read `CONTEXT.md` before changing source adapters. Use `docs/plans/` for phased work and `research/` for external source notes.

Use typed FastMCP tools with explicit docstrings. Keep upstream HTTP in thin adapters, normalize only stable fields, and preserve provenance. Add mocked tests before live smoke tests.

The server is federal-first and currently has curated state packs for CA, NY, TX, WA and FL. It supports stdio and Streamable HTTP (`openuspublicdata_mcp.http_server:app`). Use `docs/tests/Q2-executive-report.md` for the latest verified status.

The next planned slice is a climate/environment workflow; preserve jurisdiction and platform distinctions while adding it.
