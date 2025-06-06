from setuptools import setup

setup(
    name="markdown2pdf",
    version="1.1",
    description="Convertisseur de fichiers Markdown en PDF avec interface graphique",
    author="BeerCan.fr",
    author_email="contact@beercan.fr",
    url="https://github.com/beercan-fr/markdown-2-pdf",
    py_modules=["main"],
    install_requires=[
        "PyQt5>=5.15.0",
        "markdown>=3.3.0",
        "pdfkit>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'markdown2pdf=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.6",
)
