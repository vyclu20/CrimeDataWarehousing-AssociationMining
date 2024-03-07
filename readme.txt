What each file represents:

ProjectDW8 - Multidimensional Project Solution folder

crime.csv - the table used before splitting them into separate csv files

crimeIDS, dateIDS, loc1IDS and loc2IDS csv files - the tables used to get the keys for the fact table

dimcrime, dimdate,dimloc1,dimloc2 csv files - the tables used for the dimensions 

fact.csv - the table used for the fact table

ETLscript.py - the python script used to make all the above files

SQLscript.sql - the sql query used to populate the database

Project2.pbix - the power bi file. note that i imported, not connect live
