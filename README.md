# Module `pymdx_img`

Python-Markdown extension catching the `![]()` semantics to allow image sizing.

This is made via the `?size=...*...` keywords in the `alt` text to avoid breaking common
renderer behaviour (GitHub included). Either or both dimensions can be provided.

`pip install git+https://github.com/carnarez/pymdx-img` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

**Example:**

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

**Classes:**

* [`ImgSizingPreprocessor`](#pymdx_imgimgsizingpreprocessor)
* [`ImgSizingExtension`](#pymdx_imgimgsizingextension)

## Classes

### `pymdx_img.ImgSizingPreprocessor`

Preprocessor to catch and replace the `![]()` markers.

**Methods:**

* [`html()`](#pymdx_imgimgsizingpreprocessorhtml)
* [`run()`](#pymdx_imgimgsizingpreprocessorrun)

#### Constructor

```python
ImgSizingPreprocessor(md: Markdown)
```

All methods inherited, but the `run()` one below.

**Parameters:**

* `md` [`markdown.core.Markdown`]: Internal `Markdown` object to process.

#### Methods

##### `pymdx_img.ImgSizingPreprocessor.html`

```python
html(alt: str, src: str, w: str, h: str) -> str:
```

Return the HTML block including the parameters.

At the moment, the returned HTML is:

```html
<p><img alt="" src="" width="" height="" /></p>
```

**Parameters:**

* `alt` [`str`]: Alt text to add to the image tag in case the file is not available.
* `src` [`str`]: The path to the image.
* `w` [`str`]: Width of the image. Defaults to `None`.
* `h` [`str`]: Height of the image. Defaults to `None`.

**Returns:**

* [`str`]: HTML elements.

**Decoration** via `@staticmethod`.

##### `pymdx_img.ImgSizingPreprocessor.run`

```python
run(lines: typing.List[str]) -> typing.List[str]:
```

Overwritten method to process the input `Markdown` lines.

**Paramaters:**

* `lines` [`typing.List[str]`]: `Markdown` content (split by `\n`).

**Returns:**

* [`typing.List[str]`]: Same list of lines, processed.

### `pymdx_img.ImgSizingExtension`

Extension to be imported when calling for the renderer.

**Methods:**

* [`extendMarkdown()`](#pymdx_imgimgsizingextensionextendmarkdown)

#### Constructor

```python
ImgSizingExtension()
```

#### Methods

##### `pymdx_img.ImgSizingExtension.extendMarkdown`

```python
extendMarkdown(md: Markdown):
```

Overwritten method to process the content.

**Parameters:**

* `md` [`markdown.core.Markdown`]: Internal `Markdown` object to process.

**Notes:**

Since we are abusing the `Markdown` link syntax the preprocessor needs to be
called with a high priority.
