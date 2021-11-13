# CS555W GedCom Checker Program.


# Team Choices
* Programming Language: Python3
   * Dependent Packages: pymongo, nltk, tabulate, punkt
* Database: MongoDB
* To execute the current program:
   * python3 Main.py 
      * must have the ModernFamilyTest.ged file in the current directory

# Team Logistics
* Zoom Meeting: 8PM Eastern Time, Mondays & Thursdays
* Other times: Stevens Email
* Group Discussion board 

# Overall Roles/Responsiblities: 
* Scrum Master: Debbie Harrington
* Developer: Joseph Allen, Yikun Han, Debbie Harrington, Chengyi Zhang
* Tester: Joseph Allen, Yikun Han, Debbie Harrington, Chengyi Zhang
* GitHub Merge Adminstrator: Joseph Allen
* Customer Advocate: Professor Rowland

# Team Members
* Joseph Allen
* Debbie Harrington
* Yikun Han
* Chengyi Zhang

# Github Repository
* https://github.com/daharrington1/CS555W.git

# Sprint 1 Test Cases
* US01 date before current date: I10086 BIRT DEAT, I30/I31 BIRT, F13/F130 MARR, F130 DIV
* US07 age more than 150 years: I10086
* US17 marry to child: F9
* US18 I10 I6 in F128 half siblings married
* US23 I1 I128 unique name and birt
* US24 I1 I2 in F1 and F129 unique familys by spouse
* US29 list deceased: I10086 I11 I12345 I128 I13 I27 I277 I278 I28 I3
* US32 F10, F11
# Sprint 2 Test Cases
* US02 birt before marr: F9; F128
* US03 birt before deat: I128
* US11 bigamy: I1, I2 & I6
* US30 living married: I1,I10,I16-I21,I2,I23,I25,I26,I31,I4-I7
* US31 living single: I14,I15,I22,I24,I279-I281,I29,I30,I32-I46,I9
* US33 list orphan: F11, F70
* US38 list upcoming birt: I23 I22
* US42 invalid date: I12345 deat
# Sprint 3 Test Cases
* US04 marr before divorce: F11
* US05 marr before death: F130 
* US12 parents too old: F12 I26 I30
* US13 sibings spacing: I279 & I280 bdays < 8 months for non-twins
* US16 all male same lastname: F4 & F130
* US19 first cousins marry: I23 & I31
* US21 right gender: I28 (male) is wrong gender for marriage role
* US39 upcoming anniversary, living couple: F128
# Sprint 4 Test Cases
* US06 death before divorce: F130
* US10 marr <14 yrs of spouse bday: F9, F12, F13, F128
* US14 more than 5 siblings w/same bday: F11
* US15 less than 15 siblings in family: F11
* US28 children sorted in family table
* US34 siblings is more than twice as old: F13, F128, F130
* US35 born <30 days: I281
* US36 died <30 days: I11
# Test File Note
* I10086 and I128 in family F129, they're listed only as erroneous examples
