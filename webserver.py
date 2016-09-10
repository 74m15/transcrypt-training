# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 00:59:21 2016

@author: p.capuano
"""

from flask import Flask
from flask import render_template, make_response, url_for, send_file

app = Flask("mandel")
app.template_folder = "./"
app.static_folder = "./"

@app.route("/cache.manifest")
def manifest():
  print("/cache.manifest")
  
  resp = make_response(render_template("cache.manifest"), 200)
  resp.headers["Content-Type"] = "text/cache-manifest"
  return resp
  
@app.route("/<path:filename>")
def content(filename):
  print("/%s" % filename)

  return send_file(filename)

app.run(host="0.0.0.0", port=8000)