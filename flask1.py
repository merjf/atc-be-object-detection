#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 20:06:28 2018

@author: vivekkalyanarangan
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/hello_world', methods=['GET', 'POST'])
def add():
    #a = request.form["a"]
    #b = request.form["b"]
    #c = request.form["c"]
    return "Hello World!"#str( int(a) + int(b) + int(c) )

if __name__=='__main__':
    app.run(port=7000)