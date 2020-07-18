# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:36:20 2020

@author: 韩逸堃
"""
import datetime


class indiDateChecker:

    def __init__(self, logger):
        self.logger = logger
        self.months = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG',
                       9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

    # input two dates date1, date2 in [mm, dd, yyyy]
    # output whether date2 is after or equal to date1
    def __compTwoDate(self, date1, date2):
        if date2[2] > date1[2]:
            return True
        elif date2[2] == date1[2] and date2[1] > date1[1]:
            return True
        elif date2[2] == date1[2] and date2[1] == date1[1] and date2[0] >= date1[0]:
            return True
        else:
            # date2 is before date1
            return False

    def us03_birtBeforeDeat(self, person):
        if 'DEAT' in person:
            if 'BIRT' in person:
                if not self.__compTwoDate(person['BIRT'], person['DEAT']):
                    self.logger.log_individual_error(3,
                                                     "{}: {} Death is before {} birthday."
                                                     .format(person['INDI'],
                                                             "/".join(str(x) for x in person['DEAT']),
                                                             "/".join(str(x) for x in person['BIRT'])))

    def us38_upcomingBirt(self, one):
        ret = []
        current_date = datetime.datetime.today()
        if (current_date.month == 12 and current_date.day > 1):
            try:
                date = datetime.datetime(current_date.year + 1, one['BIRT'][1], one['BIRT'][0])
            except Exception:
                pass
        else:
            try:
                date = datetime.datetime(current_date.year, one['BIRT'][1], one['BIRT'][0])
            except Exception:
                pass
        if (date - current_date > datetime.timedelta(days=0) and date - current_date < datetime.timedelta(days=30)):
            ret.append((one['INDI'], self.months[one['BIRT'][1]] + ' ' + str(one['BIRT'][0])))
        for indiid, date in ret:
            self.logger.log_individual_warning(38, "Individual {}'s birthday {} is coming soon".format(indiid, date))
