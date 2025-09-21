#!/usr/bin/env python3
from flask import Flask
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config['SECRET_KEY'] = 'my_secret_key'
    return app