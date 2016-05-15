import sys
catalogpath = "/var/www/catalog"
if not catalogpath in sys.path:
    sys.path.insert(0, catalogpath)

from catalog import app as application
