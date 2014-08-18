"""
Test http server
"""

import subprocess, time

python_test_code = """import mpld3; mpld3.show(open_browser=False)"""

p = subprocess.Popen(['python', '-c', python_test_code])
time.sleep(1) # wait for plot subprocess to get started
              # TODO: use a more robust approach for this

assert p.poll() is None, \
    'polling http server should return None if it is running'

# TODO: use casperjs to fetch figure from server and ensure it has
# proper parts

p.terminate()
