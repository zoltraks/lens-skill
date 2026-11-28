# Report Languages

## Purpose

> **Scope:** Index of the report-language rendering files

> **Key items:** load condition, single-pass rendering, large-file reading

Open this index when a phase needs a `translations/` file the routed procedure does not name.

## Files

Load the matching file when the report language is not English.

Analysis runs in English and the report renders into the report language in a single pass,
per `principles/output-style.md`:

- **`translations/polish-language.md`** - Polish rendering: vocabulary, terminology, style rules.
  Large file - read the vocabulary and style sections first,
  then resolve each section block by heading as the report emits it.
