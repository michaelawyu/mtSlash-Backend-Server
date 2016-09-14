import sys, os
sys.path.insert(0, '/var/www/html/api')
os.chdir('/var/www/html/api')
from mtslash_mobile_api_access import app as application
