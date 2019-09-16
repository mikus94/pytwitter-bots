# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module taking care of raw Twitter JSONs received by API.
"""
from configs.db_config import *


def get_user(author_json):
    """
    Getting user info out of user json.
    Extracting information beeing used in following analizys.
    :param json: Tweet JSON which contains user informations.
    :returns: Shortened JSON of following structure.
    {
        user: {
                'id',
                'created_at',
                'screen_name',
                'default_profile',
                'default_profile_image',
                'profile_use_background_image',
                'statuses_count',
                'followers_count',
                'friends_count',
                'favourites_count',
                'listed_count',
                'geo_enabled',
                'verified',
                'protected',
                'version'
        },
        # additional info about user
        dsc_info: {
            'id',
            'description',
            'location',
            'lang',
            'version'
        }

    }
    """
    author = {}
    author_dsc = {}

    # field cointains tuples with name of field, default value and function
    # that transforms str to desired type
    for (field, default, func) in USR_FIELDS:
        if field == 'id':
            author['id'] = int(author_json['id_str'])
        else:
            author[field] = func(author_json.get(field, default))

    # the same with dsc
    for (field, default, func) in USR_DSC_FIELDS:
        if field == 'id':
            author_dsc['id'] = int(author_json['id_str'])
        else:
            author_dsc[field] = func(author_json.get(field, default))

    return {
        'user': author,
        'dsc_info': author_dsc
    }
