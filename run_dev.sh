#!/usr/bin/env bash
exec gunicorn -b 0.0.0.0:3000 --workers=2 --threads=4 wsgi:app
