#!/bin/sh

# Copy everything that people edited
cp app.py PHASE_2/Application_SourceCode/frontend
cp -R templates PHASE_2/Application_SourceCode/frontend
cp *scraper.py PHASE_2/Application_SourceCode/scraper
cp *.json PHASE_2/Application_SourceCode/scraper
cp PHASE_1/API_SourceCode/*.py PHPHASE_2/Application_SourceCode/backend
cp PHASE_1/API_SourceCode/*.json PHPHASE_2/Application_SourceCode/backend

# Merge it in into the right folders
git add -A
git commit -m 'merged in new changes from different folders'
git push