from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app1 import app as app1

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)
