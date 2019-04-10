# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module handling validation needed for downloader module.
In case of error validation module terminates execution of application.
"""


class Validator:
    """
    Class handling validation of downloading module.
    """

    @staticmethod
    def execute_error(where, what):
        """
        Method executing errors.
        :param where: String where error was found.
        :param what: String what field caused error.
        :return: None
        """
        print("Error in configuration of {}.".format(where))
        print("Error in field {}.".format(what))
        exit()

    def validate_downloader_config(self, json):
        """
        Function validating downloader config file.
        :param json: JSON with config.
        :return: None
        """
        self.validate_twitter_api(json['twitter_api'])
        self.validate_cursor(json['cursor'])
        pass

    def validate_twitter_api(self, json):
        """
        Function validating Twitter API.
        :param json: JSON containing Twitter API credentials.
        :return: None
        """
        fields= ['acc_key', 'acc_skey', 'cost_key', 'cost_skey']
        for field in fields:
            if json.get(field, None) is None:
                self.execute_error('Twitter API', field)

    def validate_cursor(self, json):
        """
        Function validating cursor options.
        :param json:
        :return:
        """
        # check if keywords are declared
        if json.get('keywords', None) is None:
            self.execute_error('Cursor options', 'keywords')

        # check timeline
        for field in ['since', 'until']:
            if json.get(field, None) is None:
                self.execute_error('Cursor options', field)
        pass
