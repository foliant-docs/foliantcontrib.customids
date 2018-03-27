'''
Preprocessor for Foliant documentation authoring tool.
Provides Pandoc-style custom IDs for headings.
'''


from foliant.preprocessors.base import BasePreprocessor

import re


class Preprocessor(BasePreprocessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headings_pattern = re.compile(
            "\n+(?P<hashes>#+) +(?P<heading>[^\{\}#\n]+) +\{#(?P<custom_id>\S+)\}\n",
        )

    def parse_custom_id(self, content: str) -> str:
        content = re.sub(self.headings_pattern,
                         "<a id=\"\g<custom_id>\" class=\"custom_id_anchor\"></a>\n\n\g<hashes> \g<heading>\n",
                         content)
        content = "<style>.custom_id_anchor:before {content: '\\a0'}</style>\n\n" + content
        return content

    def apply(self):
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()
            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(self.parse_custom_id(content))
