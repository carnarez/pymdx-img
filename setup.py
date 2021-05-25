"""Make `pymdx-img` installable (via `pip install git+https://...`)."""

import setuptools

setuptools.setup(
    author="carnarez",
    description="Add support for sizing in <img> tags to Python-Markdown.",
    install_requires = ["markdown"],
    name="pymdx-img",
    py_modules=["pymdx_img"],
    url="https://github.com/carnarez/pymdx-img",
    version="0.0.1",
)
