This is a python script used to automate the process of booking a library room at UOIT

It uses selenium and a chromedriver. Requests a time and day, and

finds the first available room with those specifications. It searches

the 3 person rooms first. If none of those are available at the specified

times then it will search the three person rooms.

It uses credentials stored in studentInfo.txt that should be stored in the same directory

The credential should be a student number and a password, 1 set per line,

separated by a space.

Next Steps include making it smarted. If only 2 sets of numbers are available.

It will select from the second floor rooms.
