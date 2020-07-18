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
* US01 date before current date: I10086 BIRT DEAT, I30/I31 BIRT, F13/F130 MARR
* US07 age more than 150 years: I10086
* US18 I10 I6 in F128 half siblings married
* US17 marry to child: F9
* US29 list deceased: I10086 I11 I12345 I128 I13 I27 I277 I278 I28 I3
* US23 I1 I128 unique name and birt
* US24 I1 I2 in F1 and F129 unique familys by spouse
* US32 I22 I23 multiple birt
# Sprint 2 Test Cases
* US02 birt before marr: I19 F9; I10 F128
* US03 birt before deat: I128
* US30 living married: I1 I10 I16 I17 I18 I19 I2 I20 I21 I23 I25 I26 I31 I4 I5 I6 I7
* US31 living single: I14 I15 I22 I24 I279 I280 I29 I30 I9
* US42 invalid date: I12345 deat
* US33 list orphan: F11 I26/I29, F70 I279/I280
* US38 list upcoming birt: I23 I22
* US11 bigamy I1, I2 & I6
# Sprint 3 Test Cases
* US04 marr before divorce: F11
* US21 right gender: I28 (male) is wrong gender for marriage role
* US16 all male same lastname: F4 & F130
* US39 upcoming anniversary, living couple: F128
* US13 sibings spacing: I279 & I280 bdays < 8 months for non-twins
* US12 parents too old: F12 I26 I30
* US05 marr before death: F130 I10086 I128
* US19 first cousins marry: F13 I23 I31
# Test File Note
* I10086 and I128 in family F129, they're listed only as erroneous examples
