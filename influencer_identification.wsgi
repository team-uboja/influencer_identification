#!/usr/bin/python3
import sys
print(sys.executable)
sys.path.insert(0, '/var/www/html/influencer_identification')

from influencer_identification_main import app as application
