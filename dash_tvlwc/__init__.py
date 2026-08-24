from __future__ import print_function as _

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__

if not hasattr(_dash, '__plotly_dash') and not hasattr(_dash, 'development'):
    print('Dash was not successfully imported. '
          'Make sure you don\'t have a file '
          'named \n"dash.py" in your current directory.', file=_sys.stderr)
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, 'package-info.json'))
with open(_filepath) as f:
    package = json.load(f)

package_name = package['name'].replace(' ', '_').replace('-', '_')
__version__ = package['version']

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = []

# Apps running with `serve_locally=False` fetch the bundles from jsDelivr,
# which serves them straight out of the `v<version>` tag on GitHub. Tag the
# release before publishing to PyPI, or these URLs 404 for those apps.
_repo = package['homepage'].replace('https://github.com/', '')
_cdn_base = 'https://cdn.jsdelivr.net/gh/{0}@v{1}/{2}'.format(
    _repo, __version__, package_name)

_js_dist = []

_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js".format(async_resource),
            "external_url": "{0}/async-{1}.js".format(
                _cdn_base, async_resource),
            "namespace": package_name,
            "async": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js.map".format(async_resource),
            "external_url": "{0}/async-{1}.js.map".format(
                _cdn_base, async_resource),
            "namespace": package_name,
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            'relative_package_path': 'dash_tvlwc.min.js',
            'external_url': '{0}/{1}.min.js'.format(_cdn_base, package_name),
            'namespace': package_name
        },
        {
            'relative_package_path': 'dash_tvlwc.min.js.map',
            'external_url': '{0}/{1}.min.js.map'.format(
                _cdn_base, package_name),
            'namespace': package_name,
            'dynamic': True
        }
    ]
)

# Runtime prop-type validation for the TypeScript component, served only when
# the app runs with dev tools enabled.
_js_dist.append(dict(
    dev_package_path="proptypes.js",
    dev_only=True,
    namespace="dash_tvlwc"
))

_css_dist = []


for _component in __all__:
    setattr(locals()[_component], '_js_dist', _js_dist)
    setattr(locals()[_component], '_css_dist', _css_dist)
