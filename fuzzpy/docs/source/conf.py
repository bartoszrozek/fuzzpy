import os
import sys

# Add project root to sys.path to autodoc can import the package
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

project = 'fuzzpy'
author = 'fuzzpy contributors'
release = '0.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'myst_parser',
    'sphinx_autodoc_typehints',
]

autosummary_generate = True
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Try to get package version from installed metadata (optional).
# Important: avoid importing `version` into the module namespace because
# Sphinx uses the name ``version`` for the configured project version string.
version = ''
try:
    # Python 3.8+: importlib.metadata
    from importlib.metadata import version as importlib_version, PackageNotFoundError
    release = importlib_version('fuzzpy')
    # short X.Y version for Sphinx's ``version`` variable
    version = '.'.join(release.split('.')[:2])
except Exception:
    # fallback to package attribute if available
    try:
        import fuzzpy
        release = getattr(fuzzpy, '__version__', release)
        version = '.'.join(str(release).split('.')[:2])
    except Exception:
        # leave defaults
        pass
