"""
Config module for analysis part.
"""
# path to data from DB
# ubuntu
# USER_DATA_PATH = '/home/miko/msc/trollemagisterka/src/users.csv'
# osx
USER_DATA_PATH = '/Users/miko/studia/msc/users.csv'
# path to varol data exported from DB
# osx
VAROL_USER_DATA_PATH = '/Users/miko/studia/msc/varol_users.csv'


# path do cresci data
# ubuntu
# CRESCI_DATA = '/home/miko/msc/allData/ml_datasets/cresci-2017.csv/datasets_full.csv'
# osx
CRESCI_DATA = '/Users/miko/studia/msc/ready_data/ml_datasets/cresci-2017.csv/datasets_full.csv'


# fields needed to classifier
DESIRED_FIELDS = ["id", "statuses_count", "followers_count", "friends_count",
                    "favourites_count", "listed_count", "default_profile",
                    "geo_enabled", "profile_use_background_image", "verified",
                    "protected"
]

# cresci data fields
CRESCI_FIELDS = {
    # genuine accounts data
    'genuine' : ["id", "name", "screen_name", "statuses_count", "followers_count",
                 "friends_count", "favourites_count", "listed_count", "url", "lang",
                 "time_zone", "location", "default_profile",
                 "default_profile_image", "geo_enabled", "profile_image_url",
                 "profile_banner_url", "profile_use_background_image",
                 "profile_background_image_url_https", "profile_text_color",
                 "profile_image_url_https", "profile_sidebar_border_color",
                 "profile_background_tile", "profile_sidebar_fill_color",
                 "profile_background_image_url", "profile_background_color",
                 "profile_link_color", "utc_offset", "is_translator",
                 "follow_request_sent", "protected", "verified", "notifications",
                 "description", "contributors_enabled", "following", "created_at",
                 "timestamp", "crawled_at", "updated", "test_set_1", "test_set_2"
    ],
    # social_spambots1
    'social_spambots1' : ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image","geo_enabled",
                        "profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color","profile_background_tile"
                        ,"profile_sidebar_fill_color",
                        "profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated","test_set_1"
    ],
    # socialspambots2
    'social_spambots2' : ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image","geo_enabled",
                        "profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color",
                        "profile_background_tile","profile_sidebar_fill_color"
                        ,"profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated"
    ],
    # social spambots 3
    'social_spambots3' : ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image",
                        "geo_enabled","profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color",
                        "profile_background_tile","profile_sidebar_fill_color",
                        "profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated","test_set_2"
    ],
    # traditional spambots 1
    'traditional_spambots1' : ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color",
                            "profile_link_color","utc_offset","is_translator",
                            "follow_request_sent","protected","verified",
                            "notifications","description",
                            "contributors_enabled","following","created_at",
                            "timestamp","crawled_at","updated"
    ],
    # traditional spambots 2
    'traditional_spambots2' : ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color",
                            "profile_link_color","utc_offset","is_translator",
                            "follow_request_sent","protected","verified",
                            "notifications","description",
                            "contributors_enabled","following",
                            "created_at","timestamp","crawled_at","updated"
    ],
    # traditional spambots 3
    'traditional_spambots3' : ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color","profile_link_color",
                            "utc_offset","is_translator","follow_request_sent",
                            "protected","verified","notifications",
                            "description","contributors_enabled",
                            "following","created_at","timestamp","crawled_at",
                            "updated"
    ],
    # traditional spambots 4
    'traditional_spambots4' : [
                            "id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color","profile_link_color",
                            "utc_offset","is_translator","follow_request_sent",
                            "protected","verified","notifications",
                            "description","contributors_enabled","following",
                            "created_at","timestamp","crawled_at","updated"
    ],
    # fake followers
    'fake_followers' : [
        "id","name","screen_name","statuses_count","followers_count",
        "friends_count","favourites_count","listed_count","created_at","url",
        "lang","time_zone","location","default_profile","default_profile_image",
        "geo_enabled","profile_image_url","profile_banner_url",
        "profile_use_background_image","profile_background_image_url_https",
        "profile_text_color","profile_image_url_https",
        "profile_sidebar_border_color","profile_background_tile",
        "profile_sidebar_fill_color","profile_background_image_url",
        "profile_background_color","profile_link_color","utc_offset",
        "is_translator","follow_request_sent","protected","verified",
        "notifications","description","contributors_enabled","following",
        "updated"
    ]
}