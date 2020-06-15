from db_interface import GenComDb
import json, sys, pprint

# declare a test object
indObj = GenComDb(GenComDb.MONGO_INDIVIDUALS)
indObj.dropCollection();
indObj.seed_data()

famObj = GenComDb(GenComDb.MONGO_FAMILIES)
famObj.dropCollection();
famObj.seed_data()


# print all the Individual Ids
ret=indObj.getAllIds()
for i in ret:
    print("Record for id: {}".format(i["INDI"]))
    doc=indObj.getDoc(i["INDI"])
    print(doc)

# print all the Individual Ids
ret=famObj.getAllIds()
for i in ret:
    print("Record for family: {}".format(i["FAM"]))
    doc=famObj.getDoc(i["FAM"])
    print(doc)


# Test adding just the ID of an individual
print("\n\nInserting Individual Record Field by Field");
ret=indObj.addId("I6")
if ret==None:
    print("FAILED ADDING OBJECT\n")
else:
    print("Created Individual record - id {}\n".format(ret))

#Update entry
ret=indObj.updateId("I6", "NAME", "Claire /Pritchett/")
#print("{} entries modified".format(ret))
ret=indObj.updateId("I6", "SEX", "F")
#print("{} entries modified".format(ret))
ret=indObj.updateId("I6", "BIRT", "3 MAR 1970")
#print("{} entries modified".format(ret))
ret=indObj.updateId("I6", "FAMS", ["F2","F6"])
#print("{} entries modified".format(ret))

print("\nUpdated Entry for {}".format("I6"))
ret=indObj.getDoc("I6")
print(ret)


# Test adding just the ID of an individual
print("\n\nInserting Family Record Field by Field");
ret=famObj.addId("F2")
if ret==None:
    print("FAILED ADDING OBJECT\n")
else:
    print("Created Family record - id {}\n".format(ret))

#Update entry
ret=famObj.updateId("F2", "HUSB", "I1")
#print("{} entries modified".format(ret))
ret=famObj.updateId("F2", "WIFE", "I3")
#print("{} entries modified".format(ret))
ret=famObj.updateId("F2", "CHIL", ["I4", "I6"])
#print("{} entries modified".format(ret))
ret=famObj.updateId("F2", "MARR", "1 JAN 1968")
#print("{} entries modified".format(ret))
ret=famObj.updateId("F2", "DIV", "1 JAN 2003")
#print("{} entries modified".format(ret))
ret=famObj.updateId("F2", "NOTE", "JAY/DEDEE FAMILY")
#print("{} entries modified".format(ret))

print("\nUpdated Entry for {}".format("F2"))
ret=famObj.getDoc("F2")
print(ret)

ret=famObj.updateId("F2", "CHIL", ["I5"])
ret=famObj.getDoc("F2")
print(ret)

print("\nGetting name for I1:")
ret=indObj.getName("I1")
if ret==None:
    print("ID NOT FOUND")
else:
    print("NAME is {}".format(ret))


# get matches as spouse
ret=famObj.getFamSpouse("I2")
if ret==None:
    print("ID NOT FOUND")
else:
    print("Found match as spouse for ID({}) in family records:{}".format("I2", ret))

# get matches as child 
ret=famObj.getFamChild("I4")
if ret==None:
    print("ID NOT FOUND")
else:
    print("Found match as child for ID({}) in family records:{}".format("I4", ret))
