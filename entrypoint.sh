#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 goalblog:app