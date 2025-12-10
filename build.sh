#!/bin/bash
# Install Python Dependencies
pip install -r requirements.txt

# Install Node Environment for Frontend Build
cd frontend
npm install
npm run build
cd ..
