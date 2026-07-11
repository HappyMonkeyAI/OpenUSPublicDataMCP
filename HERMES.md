# HERMES — Agent Guide

Read `CONTEXT.md` before changing source adapters. Use `docs/plans/` for phased work and `research/` for external source notes.

Use typed FastMCP tools with explicit docstrings. Keep upstream HTTP in thin adapters, normalize only stable fields, and preserve provenance. Add mocked tests before live smoke tests.

The initial server is federal-first. State and local work belongs behind platform adapters (`socrata`, `arcgis`, `ckan`) and explicit jurisdiction metadata; do not copy UK assumptions into this project.
