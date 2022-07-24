#!/bin/bash
source activate sobayonin
cd ../app
python manage.py test_instagram
