from setuptools import setup, find_packages

setup(
    name="avocado-cli",
    version="1.0.0",
    description="Native macOS Terminal Dashboard & CLI App",
    author="RnR-io",
    url="https://github.com/RnR-io/Avacado",
    packages=find_packages(),
    scripts=["bin/avocado"],
    entry_points={
        "console_scripts": [
            "avocado = avocado.main:main",
        ],
    },
    classifiers=[
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
