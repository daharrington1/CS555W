# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:09:11 2020

@author: 韩逸堃
"""
from nltk import word_tokenize
import datetime

#parser and checker
class parser4:
    
    def __init__(self, filepath, logger):
        self.logger = logger
        temp1, temp2 = self.__raw2dic(filepath)
        self.indi_dic = temp1
        self.fam_dic = temp2
        
        
        
    #convert month abbreviate to number representation
    def month_str2num(self, mstring):
        if mstring == 'JAN':
            return 1
        elif mstring == 'FEB':
            return 2
        elif mstring == 'MAR':
            return 3
        elif mstring == 'APR':
            return 4
        elif mstring == 'MAY':
            return 5
        elif mstring == 'JUN':
            return 6
        elif mstring == 'JUL':
            return 7
        elif mstring == 'AUG':
            return 8
        elif mstring == 'SEP':
            return 9
        elif mstring == 'OCT':
            return 10
        elif mstring == 'NOV':
            return 11
        elif mstring == 'DEC':
            return 12
    
    
    def __raw2dic(self, file):
        """
        to use this function, nltk package is required, please install by
        >>> conda install -c anaconda nltk (if you're using Conda)
        OR
        >>> pip install --user -U nltk (normal pip install)
        
        in the same directory, import function by
        >>> from project3F import raw2dic
        
        input: GEDCOM file path, string type e.g 'ModernFamily.txt'
        output: individuals, familys two dic of dic, the inner dic may not have the same number of keys
                individuals{
                    individual_id:{
                        NAME: ... #name in string
                        SEX: ... #F or M in string
                        BIRT: [...] #list of day, month, year in int e.g [1,1,2020]
                        DEAT: [...] #list of day, month, year in int
                        FAMS: [...] #list of familys' id in string
                        FAMC: [...] #list of familys' id in string
                        NOTE: [...] 
                    }
                }
                familys{
                    family_id:{
                        HUSB: [...] #list of individuals' id in string e.g LGBT familys
                        WIFE: [...] #list of individuals' id in string
                        CHIL: [...] #list of individuals' id in string
                        MARR: [...] #list of day, month, year in int
                        DIV: [...] #list of day, month, year in int
                        NOTE: [...]
                    }
                }
        """
        
        filepath = file
        lines = []
        with open(filepath) as fp:
            for line in fp:
                lines.append(line.rstrip())
    #    valid_tags = ['INID', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR',
    #                 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
        valid_tags_level1 = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR',
                             'HUSB', 'WIFE', 'CHIL', 'DIV']
        #derived from project 2
        #remove all lines with invalid tags
        clean_lines = []
        for line in lines:
            tokens = word_tokenize(line)
            if tokens[0] == '0':
                if tokens[1] in ['HEAD', 'TRLR', 'NOTE']:
                    clean_lines.append(line)
                elif tokens[-1] in ['INDI', 'FAM']:
                    clean_lines.append(line)
            elif tokens[0] == '1':
                if tokens[1] in valid_tags_level1:
                    clean_lines.append(line)
            elif tokens[0] == '2':
                if tokens[1] == 'DATE':
                    clean_lines.append(line)
        #print(len(clean_lines))
        
        #aggregate info of an individual or a family
        individuals = {} #collection id 1
        familys = {} #collection id 2
        collection = -1
        index = ''
        i = 0
        while i < len(clean_lines):
            line = clean_lines[i]
            tokens = word_tokenize(line)
            if tokens[0] == '0' and tokens[-1] == 'INDI':
                inid = tokens[2]
                individuals[inid] = {}
                collection = 1
                index = inid
                i += 1
            elif tokens[0] == '0' and tokens[-1] == 'FAM':
                famid = tokens[2]
                familys[famid] = {}
                collection = 2
                index =  famid
                i += 1
            else:
                if collection == 1:
                    #premise: one DATE must follow below tags
                    if tokens[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']:
                        indi_feature = tokens[1]
                        i += 1
                        tempdate = word_tokenize(clean_lines[i])
                        tempdate[3] = self.month_str2num(tempdate[3])
                        individuals[index][indi_feature] = []
                        for di in range(2,5):
                            individuals[index][indi_feature].append(int(tempdate[di]))
                    elif tokens[1] in ['FAMS', 'FAMC']:
                        indi_feature = tokens[1]
                        if indi_feature not in individuals[index]:
                            individuals[index][indi_feature] = []
                        individuals[index][indi_feature].append(tokens[3])
                    else:
                        indi_feature = tokens[1]
                        individuals[index][indi_feature] = " ".join(tokens[2:])
                elif collection == 2:
                    #premise: one DATE must follow below tags
                    if tokens[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']:
                        fam_feature = tokens[1]
                        i += 1
                        tempdate = word_tokenize(clean_lines[i])
                        tempdate[3] = self.month_str2num(tempdate[3])
                        familys[index][fam_feature] = []
                        for di in range(2,5):
                            familys[index][fam_feature].append(int(tempdate[di]))
                    elif tokens[1] in ['CHIL', 'HUSB', 'WIFE']:
                        fam_feature = tokens[1]
                        if fam_feature not in familys[index]:
                            familys[index][fam_feature] = []
                        familys[index][fam_feature].append(tokens[3])
                    else:
                        fam_feature = tokens[1]
                        familys[index][fam_feature] = " ".join(tokens[2:])
                i += 1
        return individuals, familys

        
        
    #compute, add age to dic and valid it's less than 150
    #US07
    def add_valid_age(self):
        """
        input: dic of individuals
        output: dic added 'AGE' attribute of individuals
        individuals{
                individual_id:{
                    NAME: ... #name in string
                    SEX: ... #F or M in string
                    AGE: ... #age in int
                    BIRT: [...] #list of day, month, year in int e.g [1,1,2020]
                    DEAT: [...] #list of day, month, year in int
                    FAMS: [...] #list of familys' id in string
                    FAMC: [...] #list of familys' id in string
                    NOTE: [...] 
                }
        }
        list of ids of individuals have invalid age
        """
        invalid_list = []
        for id in self.indi_dic.keys():
            if 'DEAT' in self.indi_dic[id]:
                agetemp = self.indi_dic[id]['DEAT'][2] - self.indi_dic[id]['BIRT'][2]
                if agetemp >= 150:
                    self.logger.log_individual_error(7, "{} is More than 150 years old. - Birthday: {} Death: {}"
                                                     .format(id,
                                                             "/".join(str(x) for x in self.indi_dic[id]['BIRT']),
                                                             "/".join(str(x) for x in self.indi_dic[id]['DEAT']))
                                                     )
                    invalid_list.append(id)
                self.indi_dic[id]['AGE'] = agetemp
            else:
                current_time = datetime.datetime.now()
                agetemp = current_time.year - self.indi_dic[id]['BIRT'][2]
                if agetemp >= 150:
                    self.logger.log_individual_error(7, "{} is More than 150 years old. - Birthday: {} "
                                                     .format(id,
                                                             "/".join(str(x) for x in self.indi_dic[id]['BIRT'])))
                    invalid_list.append(id)
                self.indi_dic[id]['AGE'] = agetemp
        return invalid_list
        
    #input two dates date1, date2 in [mm, dd, yyyy]
    #output whether date2 is after or equal to date1
    def compTwoDate(self, date1, date2):
        if date2[2] > date1[2]:
            return True
        elif date2[2] == date1[2] and date2[1] > date1[1]:
            return True
        elif date2[2] == date1[2] and date2[1] == date1[1] and date2[0] >= date1[0]:
            return True
        else:
            #date2 is before date1
            return False
    
    #return False when error detected else True
    def us01_currentDate(self, date):
        current_time = datetime.datetime.now()
        return self.compTwoDate(date, [current_time.day, current_time.month, current_time.year])
        
    
    #date check traversal function
    #output: dic of individuals' id and familys' id,  whose date is invalid and what date is invalid
    #        list of (fam_id, indi_id) tuples: whose marriage date is before their birthday
    #        list of id: whose death day is before their birthday
    def dateCheck(self):
        current_result = {}
        birthMarr_result = []
        birthDeat_result = []
        for indi_id, person in self.indi_dic.items():
            if 'BIRT' in person:
                if not self.us01_currentDate(person['BIRT']):
                    self.logger.log_individual_error(1,
                                                     "{} Birthday: {} Occurs in the future"
                                                     .format(indi_id,
                                                             "/".join(str(x) for x in person['BIRT'])))
                    if indi_id not in current_result:
                        current_result[indi_id] = []
                    current_result[indi_id].append('BIRT')
            if 'DEAT' in person:
                if not self.us01_currentDate(person['DEAT']):
                    self.logger.log_individual_error(1,
                                                     "{} Death: {} Occurs in the future"
                                                     .format(indi_id,
                                                             "/".join(str(x) for x in person['DEAT'])))

                    if indi_id not in current_result:
                        current_result[indi_id] = []
                    current_result[indi_id].append('DEAT')
                if 'BIRT' in person:
                    if not self.compTwoDate(person['BIRT'], person['DEAT']):
                        self.logger.log_individual_error(3,
                                                     "{}: {} Death is before {} birthday."
                                                     .format(indi_id,
                                                             "/".join(str(x) for x in person['DEAT']),
                                                             "/".join(str(x) for x in person['BIRT'])))
                        birthDeat_result.append(indi_id)
        for fam_id, family in self.fam_dic.items():
            if 'MARR' in family:
                if not self.us01_currentDate(family['MARR']):
                    self.logger.log_family_error(1, "{} Marriage Date: {} Occurs in the future"
                                                 .format(fam_id,
                                                         "/".join(str(x) for x in family['MARR'])))
                    if fam_id not in current_result:
                        current_result[fam_id] = []
                    current_result[fam_id].append('MARR')
                if 'HUSB' in family:
                    for hid in family['HUSB']:
                        h = self.indi_dic[hid]
                        if 'BIRT' in h:
                            b = h['BIRT']
                        if not self.compTwoDate(b, family['MARR']):
                            self.logger.log_family_error(2,
                                                         "{}: {} Marriage Date is before husband {} 's {} birthday."
                                                         .format(fam_id,
                                                                 "/".join(str(x) for x in family['MARR']),
                                                                 family['HUSB'],
                                                                 "/".join(str(x) for x in b)))
                            birthMarr_result.append((fam_id, hid))
                if 'WIFE' in family:
                    for wid in family['WIFE']:
                        w = self.indi_dic[wid]
                        if 'BIRT' in w:
                            b = w['BIRT']
                        if not self.compTwoDate(b, family['MARR']):
                            self.logger.log_family_error(2,
                                                         "{}: {} Marriage Date is before wife {} 's {} birthday."
                                                         .format(fam_id,
                                                                 "/".join(str(x) for x in family['MARR']),
                                                                 family['WIFE'],
                                                                 "/".join(str(x) for x in b)))
                            birthMarr_result.append((fam_id, wid))        
            if 'DIV' in family:
                if not self.us01_currentDate(family['DIV']):
                    self.logger.log_family_error(1, "{} Divorce Date: {} Occurs in the future"
                                                 .format(fam_id,
                                                         "/".join(str(x) for x in family['DIV'])))
                    if fam_id not in current_result:
                        current_result[fam_id] = []
                    current_result[fam_id].append('DIV')
        return current_result, birthMarr_result, birthDeat_result
