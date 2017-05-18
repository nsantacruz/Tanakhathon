"""
Local Settings Example file for Sefaria-iOS export script.

Copy this file to `local_settings.py` and import values as needed.

`local_settings.py` is excluded from this Git repo.
"""

# Where does Sefaria-Project live
SEFARIA_PROJECT_PATH = "/where/is/sefaria/project"

import sys, os
sys.path.insert(0, SEFARIA_PROJECT_PATH)
sys.path.insert(0, SEFARIA_PROJECT_PATH + "/sefaria")
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"