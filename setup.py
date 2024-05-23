from setuptools import setup, find_packages
import os
import codee

this_directory = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]


setup(
    name="codee",
    packages=["codee"],
    include_package_data=True,
    python_requires=">=3.5",
    version=codee.__version__,
    platforms=["linux", "windows", "macos"],
    description="Basic Utilities for Encoding and Decoding",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Alexander Ezharjan",
    author_email="mysoft@111.com",
    url="https://github.com/Ezharjan/codee",
    license="MIT",
    extra_requires={"setuptools", "numpy", "Pillow"},
    entry_points={
        "console_scripts": [
            "codee = codee.__main__:main",
        ]
    },
    zip_safe=False,
)
