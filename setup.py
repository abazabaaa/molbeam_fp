from setuptools import setup, find_packages

setup(
    name="molbeam_fp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyarrow",
        "duckdb",
        "datamol",
        "rdkit",
        "pandas"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)