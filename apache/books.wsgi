import os
import site
import sys

def grandparent(path):
    return os.path.dirname(os.path.dirname(path))

def greatgrandparent(path):
    return os.path.dirname(grandparent(path))

def activate_virtualenv():
    site_packages = greatgrandparent(os.path.abspath(__file__))
    if sys.platform == 'win32':
        base = grandparent(site_packages)
    else:
        base = greatgrandparent(site_packages)

    prev_sys_path = list(sys.path)
    site.addsitedir(site_packages)
    sys.real_prefix = sys.prefix
    sys.prefix = base
    # Move the added items to the front of the path:
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


activate_virtualenv()
# put the Django project on sys.path
print os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ["DJANGO_SETTINGS_MODULE"] = "bookdiscovery.settings.local"
from django.core.handlers.wsgi import WSGIHandler
# application = WSGIHandler()
_application = WSGIHandler()

def application(environ, start_response):
  os.environ['DB_USERNAME'] = environ['DB_USERNAME']
  os.environ['DB_PASSWORD'] = environ['DB_PASSWORD']
  os.environ['SECRET_KEY'] = environ['SECRET_KEY']
  return _application(environ, start_response)

