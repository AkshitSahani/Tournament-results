1) Download Virtual Box, Git and vagrant and follow instructions to properly set them up.

2) In terminal, go to the directory where you have vagrant installed. You should find a folder there called Tournament. Change directory into that folder. Then type vagrant up to start the machine. Once it starts, type vagrant ssh to log in.

3) Once you’ve logged in, type psql. Once the sql interface starts, import the tournament.sql file into it. This is done by typing \i tournament.sql into the psql interface. 

4) Once its imported, you will have your database and tables (that you created in the .sql file) and you will be connected to your database tournament. 

5) Exit the psql with the \q command. Then run tests to make sure that all your code in your tournament.py file is functional. Type python tournament_test.py in terminal and the test file will run tests on your code. If your code is all right, it should say “All tests passed!” at the bottom. If not, it will tell you where and what the error is and you can edit it accordingly. 
