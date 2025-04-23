import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'SecureSim'
author = 'SecureSim Contributors'
release = '1.0'

extensions = ['recommonmark', 
            'sphinx_rtd_theme', 
            'sphinx.ext.autodoc',
            'sphinx.ext.napoleon',  # for Google-style or NumPy-style docstrings
            'sphinx.ext.viewcode' # adds links to source code
            ]
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,        # Show full nested structure
    'collapse_navigation': False, # Keep tree expanded
    'titles_only': False          # Show full sidebar titles
}
html_static_path = ['_static']