"""Python-Markdown extension catching the `![]()` semantics to allow... more.

`pip install git+https://github.com/carnarez/markdown-img` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

* **Sizing** is made available via the `?size=...*...` keyword in the alt text. Either
  or both dimensions can be provided in any unit you fancy.
* **Styling** is made available via the `?class=...` keyword in the alt text. Initially
  Implemented to allow image centering, but any CSS class can be provided. One or
  several classes can be provided separated by commas; no spaces!

Those keywords are located in the alt text to avoid breaking common renderer behaviour
(GitHub included).

Example:
-------
```python
import markdown
provided = "![Alt text ?class=align-center ?size=200px*400px](/wherever/image.png)"
rendered = markdown.markdown(provided, extensions=[ImgExtension()])
expected = (
    '<p class="align-center">'
    '<img alt="Alt text" src="/wherever/image.png" width="200px" height="400px" />'
    "</p>"
)
assert rendered == expected
```

"""

import re

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class ImgPreprocessor(Preprocessor):
    """Preprocessor to catch and replace the `![]()` markers."""

    def __init__(self, md: Markdown) -> None:
        """All methods inherited, but the `run()` one below.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        """
        super().__init__(md)

    @staticmethod
    def html(
        alt: str,
        src: str,
        cls: list[str] | None = None,
        w: str | None = None,
        h: str | None = None,
    ) -> str:
        """Return the HTML block including the parameters.

        Returned HTML:

        ```html
        <p class=""><img alt="" src="" width="" height="" /></p>
        ```

        Parameters
        ----------
        alt : str
            Alt text to add to the image tag in case the file is not available.
        src : str
            The path to the image.
        cls : list[str] | None
            List of the CSS class(es) to provide to the parent `<p>` element. Defaults
            to `None`.
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

        css = "" if cls is None else f' class="{" ".join(cls)}"'

        if w is not None:
            dimensions += f'width="{w}" '

        if h is not None:
            dimensions += f'height="{h}" '

        return f'<p{css}><img alt="{alt}" src="{src}" {dimensions}/></p>'

    def run(self, lines: list[str]) -> list[str]:
        r"""Overwritten method to process the input `Markdown` lines.

        Parameters
        ----------
        lines : list[str]
            `Markdown` content (split by `\n`).

        Returns
        -------
        : list[str]
            Same list of lines, processed.

        """
        escaped = 0

        cls: list[str] = []
        w = None
        h = None

        for i, line in enumerate(lines):
            if line.startswith("```"):
                escaped = line.count("`")

            if escaped and line == escaped * "`":
                escaped = 0

            if not escaped:
                for m in re.finditer(r"!\[(.*?)\]\((.+?)\)", line):
                    alt, src = m.groups()

                    # sizing
                    m_ = re.search(r"\?size=(.*)\*([^\s\?]*)", alt)
                    if m_ is not None:
                        w = m_.group(1) or None
                        h = m_.group(2) or None

                    alt = re.sub(r"\?size=[^\s]*\*[^\s\?]*", "", alt).strip()

                    # styling
                    m_ = re.search(r"\?class=([^\s\?]+)", alt)
                    if m_ is not None:
                        cls = m_.group(1).split(",") or []

                    alt = re.sub(r"\?class=[^\s\?]+", "", alt).strip()

                    # reprocessed line
                    lines[i] = line.replace(m.group(0), self.html(alt, src, cls, w, h))

        return lines


class ImgExtension(Extension):
    """Extension to be imported when calling for the renderer."""

    def extendMarkdown(self, md: Markdown) -> None:
        """Overwritten method to process the content.

        Parameters
        ----------
        md : markdown.core.Markdown
            Internal `Markdown` object to process.

        Notes
        -----
        Since we are clobbering the regular `Markdown` syntax the preprocessor needs to
        be called with a high priority (100) to be run *before* the regular processing.

        """
        md.preprocessors.register(ImgPreprocessor(md), name="img-tag", priority=100)
