from setuptools import setup, find_packages

setup(
    name="PskLOL",
    version="0.0.1",
    description="Scientific keyword search",
    long_description="""
    PskLOL is a package for Scientific Keyword Search on Local
    Database from OpenAlex Library.
    """,
    long_description_content_type="text/markdown",
    maintainer="Dalen Hsiao",
    maintainer_email="tungyuh@andrew.cmu.edu",
    license="MIT",
    packages=find_packages(),  # Automatically find and include packages
    include_package_data=True,  # Include package data as specified in MANIFEST.in
    install_requires=[
        "psycopg2-binary",  # List other dependencies here
        # "numpy", "pandas", etc.
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify minimum Python version
    entry_points={
        "console_scripts": [
            "psklol=psklol.pipeline:main",  # Example entry point for a CLI
        ],
    },
    project_urls={
        "Source": "https://github.com/dalenhsiao/PskLOL",
        "Tracker": "https://github.com/dalenhsiao/PskLOL/issues",
    },
)
