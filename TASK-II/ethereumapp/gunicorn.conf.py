import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
max_requests = 1000
max_requests_jitter = 50
preload_app = True
daemon = True

# The name of the WSGI module to use
# Replace `ethereumapp` with the name of your project directory
# and `wsgi` with the name of your WSGI module
# This assumes that your WSGI module is located in `<project_dir>/ethereumapp/wsgi.py`
# If your WSGI module has a different name or location, update it here accordingly
# For example, if your WSGI module is named `my_wsgi_module`, change this line to:
# `module_name = "ethereumapp.my_wsgi_module"`
module_name = "ethereumapp.wsgi"

# Log configuration
accesslog = "-"
errorlog = "-"
loglevel = "info"
