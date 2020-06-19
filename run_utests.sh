
echo ""
echo ""
echo "Running DBInterfaceTests Tests:"
python3 -m unittest GroupGedcomTest/DBInterfaceTest.py  
echo ""
echo ""
echo "Running TablePrinterTests Tests:"
python3 -m unittest GroupGedcomTest/TablePrinterTest.py  
echo ""
echo ""
echo "Running US18Test Tests:"
python3 -m unittest GroupGedcomTest/US18Test.py  
echo ""
echo ""
echo "Running US17Test Tests:"
python3 -m unittest GroupGedcomTest/US17Test.py  
echo ""
echo ""
echo "Running Project4Test Tests:"
python3 -m unittest GroupGedcomTest/project4Test.py
echo ""
echo ""
echo "Running usrun Tests:"
python3 -m unittest GroupGedcomTest/usrun_test.py
