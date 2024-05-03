from setuptools import setup, find_packages

setup(
    name="a3p",
    version="1.0.0",
    author="Moritz Hesche",
    author_email="mo.hesche@gmail.com",
    # description='A short description of your package',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["numpy", "matplotlib", "ipympl", "notebook", "palettable"],
    extras_require={
        "dev": ["black"],
    },
)
