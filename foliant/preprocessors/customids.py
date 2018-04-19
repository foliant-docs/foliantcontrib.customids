'''
Preprocessor for Foliant documentation authoring tool.
Provides Pandoc-style custom IDs for headings.
'''


from foliant.preprocessors.base import BasePreprocessor

import re


class Preprocessor(BasePreprocessor):
    defaults = {
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.first_heading_pattern = re.compile(
            "^(?P<first_hashes>#{1,6}) +(?P<first_heading>[^\n]+) +\{#(?P<first_custom_id>\S+)\}\n"
        )

        self.other_headings_pattern = re.compile(
            "\n+(?P<other_hashes>#{1,6}) +(?P<other_heading>[^\n]+) +\{#(?P<other_custom_id>\S+)\}\n"
        )

    def parse_custom_ids(self, content: str) -> str:
        content = re.sub(
            self.first_heading_pattern,
            "\g<first_hashes> \g<first_heading><a id=\"\g<first_custom_id>\" class=\"custom_id_anchor\"></a>\n",
            content
        )

        content = re.sub(
            self.other_headings_pattern,
            "<a id=\"\g<other_custom_id>\" class=\"custom_id_anchor\"></a>\n\n\g<other_hashes> \g<other_heading>\n",
            content
        )

        content = "<style>.custom_id_anchor::before {content: '\\00a0'}</style>\n\n" + content

        return content

    def apply(self):
        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            for markdown_file_path in self.working_dir.rglob('*.md'):
                with open(markdown_file_path, encoding='utf8') as markdown_file:
                    content = markdown_file.read()

                with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                    markdown_file.write(self.parse_custom_ids(content))
