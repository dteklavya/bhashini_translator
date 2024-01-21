from setuptools import setup, find_packages

setup(
    name="bhashini_translator",
    version="0.2",
    packages=["bhashini_translator"],
    install_requires=["requests"],
    author="Rajesh Pethe",
    author_email="rajesh.pethe@gmail.com",
    description="Python interface to Bhashini APIs.",
    url="https://github.com/dteklavya/bhashini_translator",
    package_dir={"": "src"},
    python_requires=">=3.7",
)
