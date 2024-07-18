from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tiny_er",
    version="0.1.0",
    author="Josh Meek",
    author_email="mail@josh.dev",
    description="A minimalist entity resolution library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshmeek/tiny_er",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
)