'''
Preprocessor for Foliant documentation authoring tool.
Provides Pandoc-style custom IDs for headings.
'''


import re
from pathlib import Path

from foliant.preprocessors.base import BasePreprocessor

from foliant.contrib.utils import prepend_file


class Preprocessor(BasePreprocessor):
    defaults = {
        'stylesheet_path': 'customids.css',
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('customids')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._stylesheet = self._get_stylesheet(Path(self.options['stylesheet_path']).resolve())

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
    margin-left: 0;
    margin-right: 0;
    margin-bottom: 0;
    padding: 0;
    }
.custom_id_anchor_container_level_1 {
    margin-top: 0;
    }
.custom_id_anchor_container_level_2,
.custom_id_anchor_container_level_3,
.custom_id_anchor_container_level_4,
.custom_id_anchor_container_level_5,
.custom_id_anchor_container_level_6 {
    margin-top: -.8rem;
    }
.custom_id_anchor {
    position: relative;
    }
.custom_id_anchor::before {
    content: '\\00a0';
    }
.custom_id_anchor_level_1 {
    top: -3.45rem;
    }
.custom_id_anchor_level_2 {
    top: -1.4rem;
    }
.custom_id_anchor_level_3 {
    top: -1.85rem;
    }
.custom_id_anchor_level_4 {
    top: -2.65rem;
    }
.custom_id_anchor_level_5 {
    top: -2.75rem;
    }
.custom_id_anchor_level_6 {
    top: -2.75rem;
    }
'''

    def process_custom_ids(self, content: str) -> str:
        processed_content = ''

        heading_pattern = re.compile(
            r'(^\#{1,6}\s+.*\S+\s*$)',
            flags=re.MULTILINE
        )

        content_parts = heading_pattern.split(content)

        for content_part in content_parts:
            heading = heading_pattern.fullmatch(content_part)

            if heading:
                self.logger.debug(f'Heading found: {heading}')

                identified_heading_pattern = re.compile(
                    r'^(?P<hashes>\#{1,6})\s+(?P<heading_content>.*\S+)\s+\{\#(?P<custom_id>\S+)\}\s*$',
                    flags=re.MULTILINE
                )

                identified_heading = identified_heading_pattern.fullmatch(content_part)

                if identified_heading:
                    level = len(identified_heading.group('hashes'))

                    self.logger.debug(
                        f'Adding an anchor to the identified heading of level {level}: {identified_heading}'
                    )

                    content_part = re.sub(
                        identified_heading_pattern,
                        f'\n\n<div class="custom_id_anchor_container custom_id_anchor_container_level_{level}">' +
                        f'<div id="\g<custom_id>" class="custom_id_anchor custom_id_anchor_level_{level}">' +
                        '</div></div>\n\n\g<hashes> \g<heading_content>\n\n',
                        content_part
                    )

                else:
                    self.logger.debug('This heading has no custom ID, skipping')

            processed_content += content_part

        # processed_content = f'<style>\n{self._stylesheet}\n</style>\n\n{processed_content}'

        self.logger.debug('Content modified')

        return processed_content

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

                    self.logger.debug(f'Adding styles to {markdown_file}')
                    prepend_file(markdown_file_path, f'<style>\n{self._stylesheet}\n</style>\n\n')

        self.logger.info('Preprocessor applied')
