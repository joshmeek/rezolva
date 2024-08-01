from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rezolva",
    version="0.2.2",
    author="Josh Meek",
    author_email="mail@josh.dev",
    description="Entity resolution for everyone. Minimal. No dependencies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshmeek/rezolva",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License"],
)
