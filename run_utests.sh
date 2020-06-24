for file in `ls GroupGedcomTest/*.py`
do
echo $file ":"
python3 -m unittest $file
done
