from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nfo-validate",
    version="1.0.0",
    author="NFO Standard Contributors",
    author_email="contact@nfostandard.com",
    description="A validation tool for NFO Standard files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Biztactix/NFOStandard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: The Unlicense",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "lxml>=4.6.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "nfo-validate=nfo_validator:main",
        ],
    },
)