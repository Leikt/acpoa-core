import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Line automatically modified by acpoa-builder
# Do not modify it manually unless you know what you are doing
files = []

setuptools.setup(
    name="acpoa",
    version="0.0.8",
    author="Leikt",
    author_email="leikt.solreihin@gmail.com",
    description="Application Core for Plugin Oriented Applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leikt/acpoa-core",
    project_urls={
        "Bug Tracker": "https://github.com/Leikt/acpoa-core/issues",
        "Wiki": "https://github.com/Leikt/acpoa-core/wiki",
        "Discussions": "https://github.com/Leikt/acpoa-core/discussions"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    package_data={'': files}
)
