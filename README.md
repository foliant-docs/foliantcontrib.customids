# СustomIDs

CustomIDs is a preprocessor that allows to define custom identifiers (IDs) for headings in Markdown source by using Pandoc-style syntax in projects built with MkDocs or another backend that provides HTML output. These IDs may be used in hyperlinks that refer to a specific part of a page.

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

The preprocessor supports the following options:

```yaml
    - customids:
        stylesheet_path: !path customids.css
        targets:
            - pre
            - mkdocs
            - site
            - ghp
```

`stylesheet_path`
:   Path to the CSS stylesheet file. This stylesheet should define rules for `.custom_id_anchor_container`, `.custom_id_anchor`, `.custom_id_anchor_first` and `.custom_id_anchor_ordinary` classes. Default path is `customids.css`. If stylesheet file does not exist, default built-in stylesheet will be used.

`targets`
:   Allowed targets for the preprocessor. If not specified (by default), the preprocessor applies to all targets.

Custom ID may be specified after a heading content at the same line. Examples of Markdown syntax:

```markdown
# First Heading {#custom_id_for_first_heading}

A paragraph.

## Ordinary Heading {#custom_id_for_second_heading}

Some another paragraph.
```

This Markdown source will be finally transformed into the HTML code:

```html
<div class="custom_id_anchor_container"><div id="custom_id_for_first_heading" class="custom_id_anchor custom_id_anchor_first"></div></div>

<h1>First Heading</h1>

<p>A paragraph.</p>

<div class="custom_id_anchor_container"><div id="custom_id_for_second_heading" class="custom_id_anchor custom_id_anchor_ordinary"></div></div>

<h2>Ordinary Heading</h2>

<p>Some another paragraph.</p>
```

(Note that CustomIDs preprocessor does not convert Markdown syntax into HTML; it only inserts HTML tags `<div class="custom_id_anchor_container">...</div>` into Markdown code.)

Custom IDs must not contain spaces and non-ASCII characters.

Examples of hyperlinks that refer to custom IDs:

```markdown
[Link to Heading 1](#custom_id_for_first_heading)

[Link to Heading 2 in some document at the current site](/some/page/#custom_id_for_second_heading)

[Link to some heading with custom ID at an external site](https://some.site/path/to/the/page/#some_custom_id)
```
