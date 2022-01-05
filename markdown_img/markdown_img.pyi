import typing

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class ImgPreprocessor(Preprocessor):
    def __init__(self, md: Markdown): ...
    @staticmethod
    def html(alt: str, src: str, cls: str = ..., w: str = ..., h: str = ...) -> str: ...
    def run(self, lines: typing.List[str]) -> typing.List[str]: ...

class ImgExtension(Extension):
    def extendMarkdown(self, md: Markdown): ...
