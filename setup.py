from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='xmltodict3',
    version='0.0.4',
    description='An open-source library that is used '
                'for converting XML to a python dictionary.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dart-neitro/xmltodict3',
    author='Konstantin Neitro',
    author_email='neitro88@gmail.com',
    packages=find_packages(include=['xmltodict3']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
