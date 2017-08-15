#!/usr/bin/env/python

from jinja2 import Environment

HTML = """
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
Hello.
</body>
</html>
"""

def print_html_doc():
    print Environment().from_string(HTML).render(title='Hellow Gist from GutHub')

if __name__ == '__main__':
    print_html_doc()
