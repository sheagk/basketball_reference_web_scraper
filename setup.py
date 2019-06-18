import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_web_scraper",
    version="4.2.2",
    author="Jae Bradley",
    author_email="jae.b.bradley@gmail.com",
    license="MIT",
    description="A Basketball Reference client that generates data by scraping the website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaebradley/basketball_reference_web_scraper",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.4",
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "lxml",
        "pytz",
        "requests",
        "urllib3",
        'bs4',
        "soupsieve",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "NBA",
        "Basketball",
        "Basketball Reference",
        "basketball-reference.com",
    ],
)
