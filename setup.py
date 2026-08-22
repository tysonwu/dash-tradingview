import json
import os
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

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
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    long_description='''
    # 🎛 Dash Tradingview Lightweight Charts Component 📊

    Dash Tradingview Lightweight Charts Components is a Dash component library. This component wraps the popular financial charting library [TradingView Lightweight Charts by TradingView](https://github.com/tradingview/lightweight-charts) written in Javascript, and renders it for use in Python [Dash](https://dash.plotly.com/) webapp.
    ''',
    long_description_content_type='text/markdown'
)
