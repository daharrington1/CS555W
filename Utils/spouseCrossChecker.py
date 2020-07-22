class spouseCrossChecker:

    def __init__(self, logger, fam, individuals):
        self.logger = logger
        self.fam = fam
        self.spouse = self.__retrieveSpouseInfo(fam, individuals)

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

    def __retrieveSpouseInfo(self, fam, individuals):
        result = []
        if 'HUSB' in fam:
            hs = fam['HUSB']
            for h in hs:
                result.append(individuals[h])
        if len(result) > 1:
            return result
        else:
            if 'WIFE' in fam:
                ws = fam['WIFE']
                for w in ws:
                    result.append(individuals[w])
        return result

    def us06_divBeforeDeat(self):
        if 'DIV' not in self.fam:
            return
        for person in self.spouse:
            if 'DEAT' in person:
                if not self.__compTwoDate(self.fam['DIV'], person['DEAT']):
                    self.logger.log_family_error(6, "{}: {} Death is before {} divorce."
                                                 .format(self.fam['FAM'], "/".join(str(x) for x in person['DEAT']),
                                                                          "/".join(str(x) for x in self.fam['DIV'])))

    def us10_marrAfter14(self):
        if 'MARR' not in self.fam:
            return
        for person in self.spouse:
            if 'BIRT' in person:
                if not self.__compTwoDate([person['BIRT'][0], person['BIRT'][1], person['BIRT'][2]+14], self.fam['MARR']):
                    self.logger.log_family_error(10, "{}: {} marriage is less 14 years than spouse' birthday {} ."
                                                 .format(self.fam['FAM'], "/".join(str(x) for x in self.fam['MARR']),
                                                                          "/".join(str(x) for x in person['BIRT'])))
