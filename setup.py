from setuptools import setup, find_packages

setup(
    name="pyvoicing",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A Python library for musical pitch, interval, and voicing analysis",
    author="",
    author_email="",
    url="",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 