echo "UserStory23/29 Tests:"
python3 -m unittest GroupGedcomTest/DBInterfaceTest.py
echo ""
python3 -m unittest GroupGedcomTest/TablePrinterTest.py
echo ""
echo "UserStory17 Tests:"
python3 -m unittest GroupGedcomTest/US17Test.py
echo ""
echo "UserStory18 Tests:"
python3 -m unittest GroupGedcomTest/US18Test.py
echo ""
echo "UserStory 24/32 Tests:"
python3 -m unittest GroupGedcomTest/usrun_test.py

echo "UserStory 01/07 Tests:"
python3 -m unittest GroupGedcomTest/project4Test.py
