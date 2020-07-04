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
* US01 date before current date: I10086 BIRT DEAT
* US07 age more than 150 years: I10086
* US18 I10 I6 in F128 half siblings married
* US17 marry to child: F8 & F9
* US29 list deceased: I10086 I11 I128 I13 I27 I28 I3
* US23 I1 I128 unique name and birt
* US24 I1 I2 in F1 and F129 unique familys by spouse
* US32 I22 I23 multiple birt
# Sprint 2 Test Cases
* US02 birt before marr: I19 F9; I10 F128
* US03 birt before deat: I128
* US30 living married: I1 I10 I16 I17 I18 I19 I2 I20 I21 I25 I26 I4 I5 I6 I7
* US31 living single: I14 I15 I22 I23 I24 I9
* US42 invalid date: I10086 DEAT
* US33 list orphan: I26
* US38 list upcoming birt: I23 I22
* US11 bigamy I1, I2 & I6 
# Test File Note
* I10086 and I128 should not appear in any family, they're listed only as erroneous examples
