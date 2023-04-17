import sys
import site

# Add the app's directory to the PYTHONPATH
sys.path.insert(0, '/home/botastro/public_html/')

# Activate the virtual environment
activate_this = '/home/botastro/public_html/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application
