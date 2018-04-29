#!/usr/bin/env python

import sys

if sys.version_info < (2,7,5): # send to stderr to enure install visibility
  sys.stdout.write('ERROR: Python >= 2.7.5 required.\n')
  sys.stderr.write('ERROR: Python >= 2.7.5 required.\n')
  exit(1)

if sys.version_info[0] != 2:
  import os
  os.execv('/usr/bin/env', ['/usr/bin/env','python2'] + sys.argv)

from nobs.tool_main import main
from nobs.async import shutdown

try:
  main()
except KeyboardInterrupt:
  exit(1)
else:
  shutdown()
