"""
Setup configuration para Inventário Fitofisionômico - Método Küchler.
"""

from setuptools import setup, find_packages

setup(
    name="kuchlerapp",
    version="1.0.0",
    author="Pablo Guilherme de Melo Neves",
    author_email="11pabloguilherme@gmail.com",
    description="KuchlerApp - Aplicativo mobile para levantamento fitofisionômico utilizando o método de Küchler (1988)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/inventario-vegetal-kuchler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "kivymd>=1.1.1",
        "kivy>=2.2.0",
    ],
    extras_require={
        "windows": [
            "kivy-deps.sdl2>=0.6.0",
            "kivy-deps.glew>=0.3.1",
            "kivy-deps.angle>=0.3.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "kuchlerapp=main:KuchlerInventoryApp",
        ],
    },
)
