#!/bin/sh
gunicorn wsgi:app -w 1 --threads 1 -b 0.0.0.0:5000 --reload