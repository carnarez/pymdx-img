"""Python-Markdown extension catching the `![]()` semantics to allow image sizing.

This is made via the `?size=...*...` keywords in the `alt` text to avoid breaking common
renderer behaviour (GitHub included). Either or both dimensions can be provided.

`pip install git+https://github.com/carnarez/pymdx-img` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

Example
-------
```python
import markdown
provided = "![Alt text ?size=200px*400px](/wherever/image.png)"
rendered = markdown.markdown(provided, extensions=[ImgSizingExtension()])
expected = (
    "<p>"
    '<img alt="Alt text" src="/wherever/image.png" width="200px" height="400px" />'
    "</p>"
)
assert rendered == expected
```
"""

import re
import typing

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class ImgSizingPreprocessor(Preprocessor):
    """Preprocessor to catch and replace the `![]()` markers."""

    def __init__(self, md: Markdown):
        """All methods inherited, but the `run()` one below.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.
        """
        super().__init__(md)

    @staticmethod
    def html(alt: str, src: str, w: str = None, h: str = None) -> str:
        """Return the HTML block including the parameters.

        At the moment, the returned HTML is:

        ```html
        <p><img alt="" src="" width="" height="" /></p>
        ```

        Parameters
        ----------
        alt : str
            Alt text to add to the image tag in case the file is not available.
        src : str
            The path to the image.
        w : str
            Width of the image. Defaults to `None`.
        h : str
            Height of the image. Defaults to `None`.

        Returns
        -------
        : str
            HTML elements.
        """
        dimensions = ""

        if w is not None:
            dimensions += f'width="{w}" '

        if h is not None:
            dimensions += f'height="{h}" '

        return f'<p><img alt="{alt}" src="{src}" {dimensions}/></p>'

    def run(self, lines: typing.List[str]) -> typing.List[str]:
        r"""Overwritten method to process the input `Markdown` lines.

        Paramaters
        ----------
        lines : typing.List[str]
            `Markdown` content (split by `\n`).

        Returns
        -------
        : typing.List[str]
            Same list of lines, processed.
        """
        w = None
        h = None

        for i, line in enumerate(lines):
            for decl in re.findall(r"(!\[.*?\]\(.+?\))", line):
                alt, src = re.match(r"!\[(.*)\]\((.*)\)", decl).groups()

                m = re.search(r"\?size=(.*)\*(.*)", alt)
                if m is not None:
                    w = m.group(1) or None
                    h = m.group(2) or None

                alt = re.sub(r"\?size=.*\*.*", "", alt).strip()

                lines[i] = line.replace(decl, self.html(alt, src, w, h))

        return lines


class ImgSizingExtension(Extension):
    """Extension to be imported when calling for the renderer."""

    def extendMarkdown(self, md: Markdown):
        """Overwritten method to process the content.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        Notes
        -----
        Since we are abusing the `Markdown` link syntax the preprocessor needs to be
        called with a high priority.
        """
        md.preprocessors.register(
            ImgSizingPreprocessor(md), name="img-tag", priority=100
        )
