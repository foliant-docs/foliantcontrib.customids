# СustomIDs

CustomIDs is a preprocessor that allows to define custom identifiers (IDs) for headings in Markdown source by using Pandoc-style syntax in projects built with MkDocs. These IDs may be used in hyperlinks that refer to a specific part of a page.

## Installation

```bash
$ pip install foliantcontrib.customids
```

## Usage

To enable the preprocessor, add `customids` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - customids
```

Custom ID may be specified after a heading content at the same line. Examples of Markdown syntax:

```markdown
# Heading 1 {#custom_id_for_first_heading}

A paragraph.

## Heading 2 {#custom_id_for_second_heading}

Some another paragraph.
```

Custom IDs must not contain spaces and non-ASCII characters.

Examples of hyperlinks that refer to custom IDs:

```markdown
[Link to Heading 1](#custom_id_for_first_heading)

[Link to Heading 2 in some document at the current site](/some/page/#custom_id_for_second_heading)

[Link to some heading with custom ID at an external site](https://some.site/path/to/the/page/#some_custom_id)
```
