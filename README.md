This is a python script used to automate the process of booking a library room for several people at UOIT.

It uses a user specified date, time, and room type from the command line to book the room. It has several layers or error checking for room and time conflictions. Currently it does not allow a user to specify a duration (it defaults to 2 hours), basically because we've never needed anything less. 

The credentials needed to fill a form should be placed in the same directory in a file called "studentInfo.txt". This file should contain 1 student number and 1 password per row, separated by a space.

The script uses selenium and a chrome web driver to perform.
