#!/usr/bin/env python3

import os
import json
import sys
import secret
import templates

print('Content-Type: text/html')

# Save username and password to dictionary
dictionary = {}
posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
if posted_bytes:
    posted = sys.stdin.read(int(posted_bytes))
    #print("<p> POSTED: <pre><ul>")
    for line in posted.splitlines():
        vals = line.split('&')
        for pair in vals:
            k, v = pair.split('=')
            dictionary.update({k:v})

# Set cookie if username matches
if 'username' in dictionary and 'password' in dictionary:
    if dictionary['username']==secret.username and dictionary['password']==secret.password:
        print(f'Set-Cookie: user={secret.username}')
        print(f'Set-Cookie: pwd={secret.password}')
        dictionary={}

# Show query string
print("""
<!doctype html>
<html>
<body>
<h1>This is from HTML</h1>""")
print()
if len(os.environ['QUERY_STRING']) >0:
    print(f"<p> QUERY_STRING: {os.environ['QUERY_STRING']}")
    for parameter in os.environ['QUERY_STRING'].split('&'):
        (name, value) = parameter.split('=')
        print(f"<li>{name}: {value}</li>")

# Show browser info
print(f"<p>Browser: {os.environ['HTTP_USER_AGENT']}</p>")

# Print secret form if cookie was set
if os.environ['HTTP_COOKIE']:
    for key_value in os.environ['HTTP_COOKIE'].split(';'):
        k, v = key_value.strip().split('=')
        if k=='user':
            user = v
        elif k=='pwd':
            pwd = v
    print(templates.secret_page(username=user, password=pwd))
# login form (if no cookies)
else:
    print(templates.login_page())
    
# Debug
print(json.dumps(dict(os.environ), indent=2))

# end
print("""</body>
</html>
""")  
