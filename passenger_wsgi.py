"""
Passenger WSGI Handler for Shared Hosting (cPanel / Phusion Passenger).
Domain: orthobestcarehub.co.ke
Home Directory: /home/orthobes/OrthobestCareHub
Virtualenv: /home/orthobes/virtualenv/OrthobestCareHub/3.11/
"""
import os
import sys

# 1. Add application root to Python search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# 2. Ensure virtualenv site-packages are loaded in shared hosting
VENV_PATH = '/home/orthobes/virtualenv/OrthobestCareHub/3.11'
VENV_PYTHON = os.path.join(VENV_PATH, 'bin', 'python')
VENV_PACKAGES = os.path.join(VENV_PATH, 'lib', 'python3.11', 'site-packages')

if os.path.exists(VENV_PACKAGES) and VENV_PACKAGES not in sys.path:
    sys.path.insert(0, VENV_PACKAGES)

if sys.executable != VENV_PYTHON and os.path.exists(VENV_PYTHON):
    try:
        os.execl(VENV_PYTHON, VENV_PYTHON, *sys.argv)
    except Exception:
        pass

# 3. Initialize PyMySQL for MariaDB compatibility on shared hosting
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# 4. Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orthobestcarehub.settings')

# 5. Initialize WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
