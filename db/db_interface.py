#########################################################
# Database Interface for the GenCom Parser
# Author: Debbie Harrington
# Date: June, 2020
#
# Thisp oroject is using mongodb.   There is one database defined by MONGO_URI.
# There are 2 collections in the database: MONGO_INDIVIDUALS & MONGO_FAMILYS
#############################################################################
import json, sys, pprint

import pymongo 
from pymongo import MongoClient
from bson import ObjectId
import pymongo.errors
from pprint import pprint


# COllection Layouts
#Individual Document:
#    INDI: ID read in  
#    NAME: entire name - string
#    SEX: string
#    BIRTH: string
#    FAM: list of string IDs
#    DEATH: date
                           
#Family document:
#    FAM: family ID
#    HUSB: ID
#    WIFE: ID
#    CHILDREN: list of string ids
#    MARR: string
#    DIV: string


class GenComDb:
    # declare variables
    client = None
    db = None
    collection = None
    collection_id = None

    MONGO_URI='mongodb://localhost:27017/'
    MONGO_DB='gemcon_data'
    MONGO_INDIVIDUALS='individuals'
    MONGO_FAMILIES='families'

    VALID_IND_FLDS = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMS', 'NOTE', "AGE"]

    VALID_FAM_FLDS = ['HUSB', 'WIFE', 'CHIL', 'MARR', 'DIV', 'NOTE']

    def __init__(self, collection):
        self.client = MongoClient(self.MONGO_URI)
        self.db=self.client[self.MONGO_DB]
        self.collection = self.db[collection]
        self.collection_id = collection

    def show_collections(self):
        print self.db.collection_names()

    def my_collection(self):
        pprint (self.collection)

    def addId(self, ID=None):
        print("[addId] adding ID: {}".format(ID))

        if (ID =="") or (ID is None):
                print ("ID MUST BE SPECIFIED and NON BLANK");
                return None;

        if self.collection_id==self.MONGO_INDIVIDUALS:
            tag="INDI";
        else:
            tag="FAM";

        count=self.collection.find({tag:ID}).count()
        if (count>0):
             print ("FAILURE: {} with ID of {} ALREADY EXISTS".format(tag, ID));
             return None;
        else:
             result=self.collection.insert_one({tag:ID})
             #print("Created record - id {}\n".format(result.inserted_id))
             return result.inserted_id;


    def AddObj(self, obj):
        #print("[addObj] Adding object.....");
        #pprint(obj);

        if self.collection_id==self.MONGO_INDIVIDUALS:
            tag="INDI";
        else:
            tag="FAM";

        if tag in obj:
            count=self.collection.find({tag:obj[tag]}).count()
            if (count>0):
                print ("FAILURE: {} ALREADY EXISTS".format(tag));
                return None;
            else:
                result=self.collection.insert_one(obj)
                #print("Created record - id {}\n".format(result.inserted_id))
                return result.inserted_id;
        else:
            print ("FAILURE: {} MUST BE SPECIFIED".format(tag));
            return None;



    def updateId(self, genComId=None, tag=None, val=None):
        # update an individual document
        print("[updateId] updating ID: {}: tag: {}, val:{}".format(genComId, tag, val))

        if (genComId=="") or (genComId is None):
                print ("GenCom ID MUST BE SPECIFIED and NON BLANK");
                return 0;

        if (tag=="") or (tag is None):
                print ("TAG MUST BE SPECIFIED and NON BLANK");
                return 0;

        if self.collection_id==self.MONGO_INDIVIDUALS and (tag not in self.VALID_IND_FLDS):
                print ("TAG {} IS NOT A VALID INDIVIDUAL TAG".format(tag));
                return 0;

        if self.collection_id==self.MONGO_FAMILIES and (tag not in self.VALID_FAM_FLDS):
                print ("TAG {} IS NOT A VALID FAMILY TAG".format(tag));
                return 0;

        if self.collection_id==self.MONGO_INDIVIDUALS:
              genComIdTag="INDI"
        else:
              genComIdTag="FAM"

        count=self.collection.find({genComIdTag:genComId}).count()
        if (count<1):
             print ("{} DOES NOT EXIST YET".format(genComIdTag));
             return 0;
        
        #update the entry with the tag and value
        result=self.collection.update({genComIdTag:genComId}, {"$set": {tag:val}})
        return result["nModified"]   # number modified


    def getDocMatch(self, tag, val):
        ind={tag:val}
        docs=[]

        #if self.collection_id==self.MONGO_INDIVIDUALS:
              #print("Received Individual tag: {}, val: {}\n".format(tag, val))
        #else:
              #print("Received Family tag: {}, val: {}\n".format(tag, val))

        #print("ind:")
        #pprint(ind)
        try:
             #get the data from the database and throw into a list
             docs=list(self.collection.find(ind))
             #pprint(docs)
        except:
             print("Exception finding index {}".format(ind));

        return docs


    def getDoc(self, ID):
        if self.collection_id==self.MONGO_INDIVIDUALS:
              genComId="INDI"
        else:
              genComId="FAM"

        doc=None
        try:
             #get the data from the database
             doc=self.collection.find_one({genComId:ID})
        except:
             print("Exception finding index {}".format(ID));

        return doc


    def getName(self, ID):
        if self.collection_id==self.MONGO_INDIVIDUALS:
              #print("Setting tag to INDI");
              genComTag="INDI"
        else:
              print("Function not supported for families yet")
              return

        try:
             #get the data from the database
             count=self.collection.find({genComTag:ID}).count();
             if count<1:
                 print("Tag {} with ID {} not found".format(genComTag, ID))
                 return None

             doc=self.collection.find_one({genComTag:ID})
             return doc["NAME"]
        except:
             print("Exception retieving NAME for index {}".format(ID));
             return None


    def getAllIds(self):
        # get all individual ids
        docs=[]

        if self.collection_id==self.MONGO_INDIVIDUALS:
              genComTag="INDI"
        else:
              genComTag="FAM"

        try:
            count=self.collection.find().count()
            #print("Number of records: {}\n".format(count))
            docs=list(self.collection.find({}, {genComTag: 1, "_id":0}))
            #for doc in docs:
            #        pprint(doc[genComTag])
        except:
            print("Error in getting all {} ids\n".format(genComTag))

        return docs

    def seed_data(self):

        if self.collection_id==self.MONGO_INDIVIDUALS:
             print("Seeing data in Individual Collection");
             # Add individual one
             indiv = {
                'INDI' : 'I1',
                'NAME' : 'Jay /Pritchett/',
                'SEX' : 'M',
                'BIRT' : '23 MAY 1947',
                'FAMS' : ['F1', 'F2']
             }
             self.AddObj(indiv)
             indiv1 = {
                'INDI' : 'I2',
                'NAME' : 'Gloria /Pritchett/',
                'SEX' : 'F',
                'BIRT' : '10 MAY 1971',
                'FAMS' : ['F1', 'F3']
             }
             self.AddObj(indiv1)
             indiv2 = {
                'INDI' : 'I4',
                'NAME' : 'Mitchell /Pritchett/',
                'SEX' : 'M',
                'BIRT' : '1 JUN 1975',
                'FAMS' : ['F2', 'F4']
             }
             self.AddObj(indiv2)
             indiv3 = {
                'INDI' : 'I5',
                'NAME' : 'Cameron /Tucker/',
                'SEX' : 'M',
                'BIRT' : '29 FEB 1972',
                'FAMS' : ['F4', 'F5']
             }
             self.AddObj(indiv3)
        else:
             print("Seeing data in Family Collection");
             fam = {
                'FAM' : 'F1',
                'HUSB' : 'I1',
                'WIFE' : 'I2',
                'CHIL' : ['I10'],
                'MARR' : '1 JAN 1968',
                'DIV' : '1 JAN 2003',
                'NOTE' : 'JAY/GLORIA FAMILY'
             }
             self.AddObj(fam)
             fam1 = {
                'FAM' : 'F3',
                'HUSB' : 'I8',
                'WIFE' : 'I2',
                'CHIL' : ['I9'],
                'MARR' : '1 JAN 1995',
                'DIV' : '1 JAN 2006',
                'NOTE' : 'GLORIA/JAVIER FAMILY'
             }
             self.AddObj(fam1)
             fam2 = {
                'FAM' : 'F4',
                'HUSB' : 'I4',
                'WIFE' : 'I5',
                'CHIL' : ['I14', 'I15'],
                'MARR' : '1 JAN 2014',
                'NOTE' : 'MITCHELL/CAMERON FAMILY'
             }
             self.AddObj(fam2)
             fam3 = {
                'FAM' : 'F6',
                'HUSB' : 'I7',
                'WIFE' : 'I6',
                'CHIL' : ['I20', 'I24'],
                'MARR' : '1 APR 1993',
                'NOTE' : 'PHIL/CLAIRE FAMILY'
             }
             self.AddObj(fam3)

            
    #find all families where you are the spouse
    def getFamSpouse(self, ID):
        docs=[]
        if self.collection_id==self.MONGO_INDIVIDUALS:
              print("Function not supported for Individuals")
              return
        else:
              genComTag="FAM"

        try:
            ret=self.getDocMatch("HUSB", ID)
            #print("Found Husband Match:")
            for i in ret:
                #pprint(i)
                docs.append(ret["FAM"])

            ret=self.getDocMatch("WIFE", ID)
            for i in ret:
                #pprint(i)
                docs.append(i["FAM"])

            #pprint(docs)
            return docs
        except:
            print("Exception matching spouse index {}".format(ID));
            return None

                                    
    #gives list of families where you are a child-addInd(Id)
    def getFamChild(self, ID):
        docs=[]
        if self.collection_id==self.MONGO_INDIVIDUALS:
              print("Function not supported for Individuals")
              return
        else:
              genComTag="FAM"

        try:
            #print("Matching on CHIL for ID {}".format(ID))
            ret=self.getDocMatch("CHIL", ID)
            for i in ret:
                #pprint(i)
                docs.append(i["FAM"])

            #print("Found as Child in Family IDs:")
            #pprint(docs)
            return docs
        except:
            print("Exception matching child index {}".format(ID));
            return None


    def dropCollection(self):
        print("+++++++++++++DROPPING COLLECTION: {} ++++++++++++++++++".format(self.collection))
        self.collection.drop();

    def dropDatabase(self):
        print("+++++++++++++DROPPING DATABASE: {} ++++++++++++++++++".format(MONGO_DB))
        self.client.drop_database(MONGO_DB);

