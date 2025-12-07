import sys
import os

# Add project directory to sys.path
project_home = '/home/teinvig/x-solo'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtualenv
virtualenv = '/home/teinvig/x-solo/venv'
activate_this = os.path.join(virtualenv, 'bin', 'activate_this.py')
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Import the Flask app
from app import app as application
