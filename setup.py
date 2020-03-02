import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpsd_pindrop",
    version="1.1.3",
    author="Adam Musciano",
    author_email="amusciano@gmail.com",
    description="CLI GPSD Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/needmorecowbell/pindrop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
          'gpsd-py3',
          'requests',
          'simplekml'
    ],
    entry_points = {
                    'console_scripts': ['pindrop = pindrop.pindrop:main'],
                        },
    python_requires='>=3.6',
    ),

