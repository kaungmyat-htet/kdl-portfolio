import os
from path import Path as path
import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

APP_ROOT = (
    path(__file__).abspath().dirname().dirname()
)  # /blah/blah/blah/.../openedx-plugin-example/openedx_plugin_mobile_api
REPO_ROOT = APP_ROOT.dirname()  # /blah/blah/blah/.../openedx-plugin-example

# SECRET = os.environ.get('PORTFOLIO_SECRET', '11g2GS8Xxe') 

SECRET_TOKEN = env('SECRET_TOKEN')
LMS_URL = env('LMS_URL')

def plugin_settings(settings):
    # Update the provided settings module with any app-specific settings.
    # For example:
    #     settings.FEATURES['ENABLE_MY_APP'] = True
    #     settings.MY_APP_POLICY = 'foo'
    settings.SECRET_TOKEN = SECRET_TOKEN
    settings.LMS_URL = LMS_URL

