'''
Preprocessor for Foliant documentation authoring tool.
Provides Pandoc-style custom IDs for headings.
'''


import re
from pathlib import Path

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'stylesheet_path': Path('customids.css'),
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('customids')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._stylesheet = self._get_stylesheet(self.options['stylesheet_path'])

    def _get_stylesheet(self, stylesheet_file_path: Path) -> str:
        self.logger.debug(f'Stylesheet file path: {stylesheet_file_path}')

        if stylesheet_file_path.exists():
            self.logger.debug('Using stylesheet from the file')

            with open(stylesheet_file_path, encoding='utf8') as stylesheet_file:
                return stylesheet_file.read()

        else:
            self.logger.debug('Stylesheet file does not exist; using default stylesheet')

            return '''
.custom_id_anchor_container {
    height: 0;
    overflow: hidden;
    margin: -1.6rem 0 0;
    padding: 0;
    }
.custom_id_anchor {
    position: relative;
    }
.custom_id_anchor::before {
    content: '\\00a0';
    }
.custom_id_anchor_first {
    top: -999rem;
    }
.custom_id_anchor_ordinary {
    top: -2.8rem;
    }
'''

    def process_custom_ids(self, content: str) -> str:
        first_heading_pattern = re.compile(
            "^(?P<first_hashes>#{1,6}) +(?P<first_heading>[^\n]+) +\{#(?P<first_custom_id>\S+)\}\n"
        )

        ordinary_headings_pattern = re.compile(
            "\n+(?P<ordinary_hashes>#{1,6}) +(?P<ordinary_heading>[^\n]+) +\{#(?P<ordinary_custom_id>\S+)\}\n"
        )

        content = re.sub(
            first_heading_pattern,
            "<div class=\"custom_id_anchor_container\">" +
            "<div id=\"\g<first_custom_id>\" class=\"custom_id_anchor custom_id_anchor_first\">" +
            "</div></div>\n\n\g<first_hashes> \g<first_heading>\n\n",
            content
        )

        content = re.sub(
            ordinary_headings_pattern,
            "\n\n<div class=\"custom_id_anchor_container\">" +
            "<div id=\"\g<ordinary_custom_id>\" class=\"custom_id_anchor custom_id_anchor_ordinary\">" +
            "</div></div>\n\n\g<ordinary_hashes> \g<ordinary_heading>\n\n",
            content
        )

        content = f'<style>\n{self._stylesheet}\n</style>\n\n{content}'

        self.logger.debug('Content modified')

        return content

    def apply(self):
        self.logger.info('Applying preprocessor')

        self.logger.debug(f'Allowed targets: {self.options["targets"]}')
        self.logger.debug(f'Current target: {self.context["target"]}')

        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            for markdown_file_path in self.working_dir.rglob('*.md'):
                self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

                with open(markdown_file_path, encoding='utf8') as markdown_file:
                    content = markdown_file.read()

                processed_content = self.process_custom_ids(content)

                if processed_content:
                    with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                        markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied')
