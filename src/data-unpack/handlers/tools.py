# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module taking care of raw Twitter JSONs received by API.
"""
import time
from datetime import datetime

def parse_time(time_str):
    """
    Parsing twitter time to python time.
    """
    ts = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.strptime(
            time_str,
            '%a %b %d %H:%M:%S +0000 %Y'
        )
    )
    return ts

def datetime_to_date(time_str):
    """
    Parsing datetime string to just date in python.
    """
    date = str(datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').date())
    return date