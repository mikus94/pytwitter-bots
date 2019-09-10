"""
Config module for analysis part.
"""

import os

this_dir = os.path.dirname(os.path.realpath(__file__))

PLOTS_DIR = os.path.join(this_dir, 'plots')

DB_CONNECTION = ("""
    dbname='twitter'
    user='postgres'
    host='localhost'
    password='1234'
""")
