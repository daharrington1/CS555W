#!/usr/bin/env python
# coding: utf-8

# In[9]:


from nltk import word_tokenize

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
                NAME: [...] #list of full name in string
                SEX: [...] #list of F or M in string
                BIRT: [...] #list of birthday in string
                DEAT: [...] #list of death date in string
                FAMS: [...] #list of familys' id in string
                FAMC: [...] #list of familys' id in string
                NOTE: [...] 
            }
        }
        familys{
            family_id:{
                HUSB: [...] #list of individuals' id in string
                WIFE: [...] #list of individuals' id in string
                CHIL: [...] #list of individuals' id in string
                MARR: [...] #list of marry date in string
                DIV: [...] #list of divorce date in string
                NOTE: [...]
            }
        }
call function by 
>> raw2dic('ModernFamily.txt')
"""
def raw2dic(file):
    filepath = file
    lines = []
    with open(filepath) as fp:
        for line in fp:
            lines.append(line.rstrip())
    valid_tags = ['INID', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR',
                  'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
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
    print(len(clean_lines))
    #premise: input {list of list} is valid within the scope of a single line or the whole document 
    individuals = {} #collection id 1
    familys = {} #collection id 2
    collection = -1
    index = ''
    i = 0
    while i < len(clean_lines):
        line = clean_lines[i]
        tokens = word_tokenize(line)
        if tokens[0] == '0' and tokens[-1] == 'INDI':
            inid = tokens[1]
            individuals[inid] = {}
            collection = 1
            index = inid
            i += 1
        elif tokens[0] == '0' and tokens[-1] == 'FAM':
            famid = tokens[1]
            familys[famid] = {}
            collection = 2
            index =  famid
            i += 1
        else:
            if collection == 1:
                #premise: one DATE must follow below tags
                if tokens[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']:
                    indi_feature = tokens[1]
                    if indi_feature not in individuals[index]:
                        individuals[index][indi_feature] = []
                    i += 1
                    tempdate = word_tokenize(clean_lines[i])
                    individuals[index][indi_feature].append(" ".join(tempdate[2:]))
                else:
                    indi_feature = tokens[1]
                    if indi_feature not in individuals[index]:
                        individuals[index][indi_feature] = []
                    individuals[index][indi_feature].append(" ".join(tokens[2:]))
            elif collection == 2:
                #premise: one DATE must follow below tags
                if tokens[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']:
                    fam_feature = tokens[1]
                    if fam_feature not in familys[index]:
                        familys[index][fam_feature] = []
                    i += 1
                    tempdate = word_tokenize(clean_lines[i])
                    familys[index][fam_feature].append(" ".join(tempdate[2:]))
                else:
                    fam_feature = tokens[1]
                    if fam_feature not in familys[index]:
                        familys[index][fam_feature] = []
                    familys[index][fam_feature].append(" ".join(tokens[2:]))
            i += 1
    return individuals, familys


# In[10]:


raw2dic('ModernFamily.txt')


# In[ ]:




