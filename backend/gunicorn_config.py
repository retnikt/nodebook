"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
# this file contains the gunicorn configuration
import os

# if the workers environment variable is set, and is >= 1 then use it,
# otherwise use cpu_count * 4 + 1
# (if cpu_count is None or 0 then assume it is 1)
workers = max(0, int(os.getenv("WORKERS") or "0")) or ((os.cpu_count() or 1) * 4 + 1)
bind = "0.0.0.0:80"
keepalive = 120
loglevel = os.getenv("LOG_LEVEL", "info")
errorlog = "-"
