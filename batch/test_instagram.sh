#!/bin/bash
source activate sobayonin
cd /c/work/app/sobayonin-v8/app
python manage.py test_instagram
