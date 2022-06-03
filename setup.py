from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='python-wfscript',
    version='1.0',
    description='A Python runtime for wfscript: a declarative, graph-oriented language for authoring workflow content',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dylanbenden/python-wfscript/',
    author='Dylan Benden',
    author_email='dylan@wfscript.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    project_urls={
        'Bug Reports': 'https://github.com/dylanbenden/python-wfscript/issues',
        'Source': 'https://github.com/dylanbenden/python-wfscript/',
    },
)