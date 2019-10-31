#!/usr/bin/python3.5

import urllib.parse
import sys


print( urllib.parse.quote(  ''.join(sys.argv[1:])   )  )
