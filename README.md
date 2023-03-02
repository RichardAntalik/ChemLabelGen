# ChemLabelGen
Label generator for chemical compounds

Usage
-----

Run label.py, enter name, formula or CID, optionally comment, it will spit out label.png. Drag this to `labels.odg` document and print

Under hood:
* Python script uses `pubchempy` and `Pillow`.
* There is bit of json and content parsing, which has downsides, but given, that database is how it is, it's quite necessary. I mean I am not going to train AI for this...
* Labels are designed to fit to 70x30mm rectangles. 
 
-----

Sample:


![Label](https://github.com/RichardAntalik/ChemLabelGen/blob/main/sample_label.png)
