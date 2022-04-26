from setuptools import setup, find_packages

# Get the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get requirements from the .txt file:
with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='alda',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,
    url='https://github.com/Alhern/alda',
    license='GNU General Public License v3.0',
    author='Alhern',
    author_email='',
    description='A programming language created with the SLY library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={'alda': ['programs/*.alda']},
    entry_points={'console_scripts': ['alda=alda.main:main']}
)
