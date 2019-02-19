#!/bin/bash

./manage.py migrate
gunicorn skilletz.wsgi
