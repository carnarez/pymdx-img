# Module `markdown_img`

Python-Markdown extension catching the `![]()` semantics to allow... more.

`pip install git+https://github.com/carnarez/markdown-img` and refer to the brilliant
[`Python` implementation](https://github.com/Python-Markdown/markdown).

- **Sizing** is made available via the `?size=...*...` keyword in the alt text. Either
  or both dimensions can be provided in any unit you fancy.
- **Styling** is made available via the `?class=...` keyword in the alt text. Initially
  Implemented to allow image centering, but any CSS class can be provided. One or
  several classes can be provided separated by commas; no spaces!

Those keywords are located in the alt text to avoid breaking common renderer behaviour
(GitHub included).

**Example:**

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

**Classes:**

- [`ImgPreprocessor`](#markdown_imgimgpreprocessor): Preprocessor to catch and replace
  the `![]()` markers.
- [`ImgExtension`](#markdown_imgimgextension): Extension to be imported when calling for
  the renderer.

## Classes

### `markdown_img.ImgPreprocessor`

Preprocessor to catch and replace the `![]()` markers.

**Methods:**

- [`html()`](#markdown_imgimgpreprocessorhtml): Return the HTML block including the
  parameters.
- [`run()`](#markdown_imgimgpreprocessorrun): Overwritten method to process the input
  `Markdown` lines.

#### Constructor

```python
ImgPreprocessor(md: Markdown)
```

All methods inherited, but the `run()` one below.

**Parameters:**

- `md` \[`markdown.core.Markdown`\]: Internal `Markdown` object to process.

#### Methods

##### `markdown_img.ImgPreprocessor.html`

```python
html(alt: str, src: str, cls: typing.List[str], w: str, h: str) -> str:
```

Return the HTML block including the parameters.

Returned HTML:

```html
<p class=""><img alt="" src="" width="" height="" /></p>
```

**Parameters:**

- `alt` \[`str`\]: Alt text to add to the image tag in case the file is not available.
- `src` \[`str`\]: The path to the image.
- `cls` \[`typing.List[str]`\]: List of the CSS class(es) to provide to the parent `<p>`
  element. Defaults to an empty list.
- `w` \[`str`\]: Width of the image. Defaults to `None`.
- `h` \[`str`\]: Height of the image. Defaults to `None`.

**Returns:**

- \[`str`\]: HTML elements.

**Decoration** via `@staticmethod`.

##### `markdown_img.ImgPreprocessor.run`

```python
run(lines: typing.List[str]) -> typing.List[str]:
```

Overwritten method to process the input `Markdown` lines.

**Parameters:**

- `lines` \[`typing.List[str]`\]: `Markdown` content (split by `\n`).

**Returns:**

- \[`typing.List[str]`\]: Same list of lines, processed.

### `markdown_img.ImgExtension`

Extension to be imported when calling for the renderer.

**Methods:**

- [`extendMarkdown()`](#markdown_imgimgextensionextendmarkdown): Overwritten method to
  process the content.

#### Constructor

```python
ImgExtension()
```

#### Methods

##### `markdown_img.ImgExtension.extendMarkdown`

```python
extendMarkdown(md: Markdown):
```

Overwritten method to process the content.

**Parameters:**

- `md` \[`markdown.core.Markdown`\]: Internal `Markdown` object to process.

**Notes:**

Since we are clobbering the regular `Markdown` syntax the preprocessor needs to be
called with a high priority (100) to be run *before* the regular processing.
