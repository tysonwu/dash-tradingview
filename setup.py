import json
import os
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

# The PyPI project page is the README, rather than a copy of it that drifts.
# MANIFEST.in ships README.md, so it is present in the sdist too.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'README.md'), encoding='utf-8') as f:
    long_description = f.read()

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=['dash>=3.0.0'],
    python_requires='>=3.9',
    classifiers=[
        'Framework :: Dash',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
