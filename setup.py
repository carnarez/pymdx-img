"""Make `markdown-img` installable (via `pip install git+https://...`)."""

import setuptools  # type: ignore

setuptools.setup(
    author="carnarez",
    description="Add support for image sizing and class-tagging to Python-Markdown.",
    install_requires=["markdown"],
    name="markdown-img",
    packages=["markdown_img"],
    package_data={"markdown_img": ["py.typed"]},
    url="https://github.com/carnarez/markdown-img",
    version="0.0.1",
)
