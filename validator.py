#!/usr/bin/env python -
"""
Example usage:
$ f=`cat test.json`; echo -e "$f"; python validate_json.py "$f"
{
  "foo": true,
  "bar": false,
  baz: -23
}
Invalid JSON
  Expecting property name: line 4 column 3 (char 35)
    baz: -23
    ^-- Expecting property name
"""

import re
import sys
try:
  import json
except:
  import simplejson as json
from cStringIO import StringIO

def parse_error(err):
  """
  "Parse" error string (formats) raised by (simple)json:
  '%s: line %d column %d (char %d)'
  '%s: line %d column %d - line %d column %d (char %d - %d)'
  """
  return re.match(r"""^
      (?P<msg>[^:]+):\s+
      line\ (?P<lineno>\d+)\s+
      column\ (?P<colno>\d+)\s+
      (?:-\s+
        line\ (?P<endlineno>\d+)\s+
        column\ (?P<endcolno>\d+)\s+
      )?
      \(char\ (?P<pos>\d+)(?:\ -\ (?P<end>\d+))?\)
  $""", err, re.VERBOSE)

src = sys.argv[1]
try:
  json.loads(src)
  print "Valid JSON"
except ValueError, err:
  print "Invalid JSON"
  msg = err.message
  err = parse_error(msg).groupdict()
  # cast int captures to int
  for k, v in err.items():
    if v and v.isdigit():
      err[k] = int(v)
  src = StringIO(src)
  for ii, line in enumerate(src.readlines()):
    if ii == err["lineno"] - 1:
      break
  print """
  %s
  %s
  %s^-- %s
  """ % (msg, line.replace("\n", ""), " " * (err["colno"] - 1), err["msg"])
