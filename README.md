# Сustom heading ID's for Foliant

CustomIDs preprocessor lets user define custom identifiers for each heading. These custom ID's can be used later to create short links to a specific parts of any page. 

## Installation

```bash
$ pip install foliantcontrib.customids
```

## Usage

To apply a preprocessor add it's name to a preprocessor list in `foliant.yaml` config file, e.g.:

```yaml
preprocessors:
    - customids
```

Custom ID must be written after heading on the same line in curly brackets. Custom ID must not contain spaces and shoud be written using latin symbols.

```markdown
# Heading 1 {custom_id_for_first_heading}

Some text goes here.

## Heading 2 {custom_id_for_second_heading}

Some more text
```

Custom ID will replace long slug which is created automatically when building a site. Resulting URL when using custom ID will look like this:

```
http://.../index.html#custom_id 
```

