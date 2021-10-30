"""Make `markdown-img` installable (via `pip install git+https://...`)."""

import setuptools  # type: ignore

setuptools.setup(
    author="carnarez",
    description="Add support for image sizing and centering to Python-Markdown.",
    install_requires=["markdown"],
    name="markdown-img",
    package_data={"": ["*.pyi"]},
    py_modules=["markdown_img"],
    url="https://github.com/carnarez/markdown-img",
    version="0.0.1",
)
