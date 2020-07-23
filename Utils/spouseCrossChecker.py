import datetime


class spouseCrossChecker:

    def __init__(self, logger, fam, individuals):
        self.logger = logger
        self.fam = fam
        self.individuals = individuals
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

    def _check_dates(self, dt1, dt2, span, units, upcoming=False):
        """
        check_dates: check if all the dates are within the specified range
                     This routine was based on CS555W class notes provided by Professor Rowland
                     It was adapted to support upcoming dates also.

                     dt1, dt2: 2 datetime dates are passed in (no time units should be passed, optimally).
                     span: range that the 2 dates must fall within
                     units: indicator if checking days, months or years
        :param dt1, dt2, span, units, upcoming
        :returns returns true or false depending if the dates are in range
        """
        dtMap = {"days": 1, "months": 30.4, "years": 365.25}
        if units not in dtMap:
            return False

        dt_diff = (dt1 - dt2).days
        if upcoming is True:
            return (dt_diff / dtMap[units] >= 0 and dt_diff / dtMap[units] <= span)
        else:
            return (abs(dt_diff) / dtMap[units] <= span)

    def _normalize_family(self):
        """
        Normalizes all arrays in family entry
        :param family: The family object
        :return: all the keys that take arrays are arrays
        """
        fam = self.fam.copy()
        for key in ["MARR", "DIV", "HUSB", "WIFE", "CHIL"]:
            if key not in fam or type(fam[key]) is not list:
                fam[key] = []
        return fam

    def __retrieveSpouseInfo(self, fam, individuals):
        result = []
        fam = self._normalize_family()
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

    def _getSpouses(self, fam):
        """
         Return all spouses in the family, excluding '-'
         All values returned in an array, including empty array
        :param a single family
        :returns my spouse(s) in the given family
        """
        spouses = []
        for key in ["HUSB", "WIFE"]:
            for spouse in fam[key]:
                spouses.append(spouse) if spouse not in spouses else spouses

        return spouses

    def _getMySpouses(self, id, fam):
        """
         Figure out My Spouse in the current family
         Calls getSpouses which skips '-' entries
        :param a single family
        :returns my spouse(s) in the given family
        """
        # get all the spouses in the family
        spouses = self._getSpouses(fam)
        mySpouses = []

        # remove myself from the list of all spouses
        for spouse in spouses:
            mySpouses.append(spouse) if spouse != id and spouse not in mySpouses else mySpouses

        return mySpouses

    def us16_male_last_names(self):
        """
        User Story 16: Checks for Male Last Names

        :param Individuals and Family lists
        :returns List of Familes where the males don't all have the same last name in their family
        """
        fam = self._normalize_family()
        lastNames = set()   # define as set to be unique names

        # look at all mail spouses
        for male in self._getSpouses(fam):
            if self.individuals[male]["SEX"] == 'M':
                lastNames.add(self.individuals[male]["NAME"].split("/")[1])

        # look at male children last names
        for child in fam["CHIL"]:
            if self.individuals[child]["SEX"] == 'M':
                lastNames.add(self.individuals[child]["NAME"].split("/")[1])

        # check for unique male last names in families
        if len(lastNames) > 1:
            self.logger.log_family_warning(16, "{} has multiple last names: {}".format(
                                      fam["FAM"], sorted(lastNames)))

    def us39_upcoming_anniversaries(self):
        """
        User Story 39: List all living couples in a GEDCOM file whose marriage
                       anniversaries occur in the next 30 days

        :param Individuals and Family lists
        :returns List of all living couples with upcoming anniversaries
        """
        fam = self._normalize_family()

        # check non-divorced couples and non-widowers
        if len(fam["DIV"]) > 0:
            return

        Widower = False
        for spouse in self._getSpouses(fam):
            if "DEAT" in self.individuals[spouse] and type(self.individuals[spouse]["DEAT"]) is list:
                Widower = True

        # check if the anniversary is within 30 days
        if not Widower:
            try:
                if self._check_dates(datetime.date(datetime.date.today().year, fam['MARR'][1],
                                     fam['MARR'][0]), datetime.date.today(), 30, 'days', upcoming=True):
                    self.logger.log_family_info(39, "FAMILY ({}) has an upcoming anniversary: {}".format(
                                                fam["FAM"], str(fam['MARR'][1])+'/'+str(fam['MARR'][0])+'/'+str(fam['MARR'][2])))
            except Exception:
                return  # problem with dates - just return without logging anything

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

    def us17_no_marr2child(self, parentId2Children):
        """
        User Story 17: Checks for Families where a spouse is married to a child

        :param Families and Individual lists
        :returns List of Familes that have a spouse married to a child
        """
        fam = self._normalize_family()

        # get all husband/wives in the family and check to see if their spouse is their child
        for spouse in self._getSpouses(fam):
            for myspouse in self._getMySpouses(spouse, fam):
                # get all my children and check if spouse is in them
                if spouse in parentId2Children:
                    if myspouse in parentId2Children[spouse]:
                        # my spouse is married to my child
                        self.logger.log_family_error(17, "{}: My spouse ({}) is one of my children: Parent ({}), Children ({})".format(fam["FAM"], myspouse, spouse, parentId2Children[spouse]))
