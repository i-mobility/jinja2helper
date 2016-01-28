#!/usr/bin/python

activate_this = '.ve/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import io
import os.path
import jinja2
import json
import BaseHTTPServer

PORT = 1234


class JinjaRenderHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(request):
        request.send_response(200)
        request.send_header("Content-Type", "text/html")
        request.end_headers()

    def do_GET(request):
        try:
            template, jsonfile = request.path[1:].split("?")
        except ValueError:
            request.send_response(400)
            request.send_header("Content-Type", "text/plain")
            request.end_headers()
            request.wfile.write(
                "Call the endpoint like this: /template.html?data.json"
            )
            return

        if not os.path.isfile(template):
            request.send_response(404)
            request.send_header("Content-Type", "text/plain")
            request.end_headers()
            request.wfile.write("Template not found.")
            return

        if not os.path.isfile(jsonfile):
            request.send_response(404)
            request.send_header("Content-Type", "text/plain")
            request.end_headers()
            request.wfile.write("JSON not found.")
            return

        with io.open(template, 'r') as fh:
            tmpl = fh.read()

        with io.open(jsonfile, 'rb') as fh:
            data = json.load(fh)

        request.send_response(200)
        request.send_header("Content-Type", "text/html")
        request.end_headers()

        try:
            out = jinja2.Template(tmpl).render(**data)
            request.wfile.write(out)
        except Exception as e:
            request.wfile.write("<h1>Error</h1><p>" + e.message + "</p>")


if __name__ == "__main__":
    httpd = BaseHTTPServer.HTTPServer(("", PORT), JinjaRenderHandler)
    print "Starting server on port " + str(PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ""
