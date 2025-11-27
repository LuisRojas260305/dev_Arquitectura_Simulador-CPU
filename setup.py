from setuptools import setup, find_packages

setup(
    name="simulador-cpu",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.8",
)
