# GoIT-CoreProject
The console application 'bot-helper' is a useful helper that is able to sort out such 
tasks:
1. Sort files on your local machine using the path to the folder
2. Create the address book with different contacts and store information about their 
   names, phones, birthdays, email addresses, location
3. Update and delete information about existing contacts
4. Search contacts in the address book and all the data
5. Create notes with tags that can remind something
6. Update, delete notes
7. Search and sort notes by text and tags

Instructions how to install the console application 'bot-helper':
1. Download the project from the GitHub repository (master branch) using command: 
   ```bash  
    git clone https://github.com/Natali2411/GoIT-CoreProject
   ```
2. Download and install python and install 'build' package:
   
   Unix/macOS: 
    ```bash 
   python3 -m pip install build
   ```
    Windows OS:
   ```bash 
   py -m pip install build
   ```
3. Inside the directory of the project run the command to build the application:
   
   Unix/macOS: 
   ```bash 
   python3 -m build --sdist
   ```
    Windows OS:
   ```bash 
   py -m build --sdist
   ```
4. Install the package on the machine with a command:
   ```bash 
    pip install .
   ```
5. Open a Terminal and type the command:
   ```bash 
   bot-helper
   ```
6. Press <b>Enter</b>
7. Start typing commands in the Terminal and choose them from the list of the ordered 
   commands using arrows <b>'Up'</b>, <b>'Down'</b> on the keyboard and press 'Space' 
   button if you want to pass additional parameters
8. Press <b>Enter</b> if you want to finish typing commands and get the result
9. Use the command <b>'help'</b> to see the list of all possible bot commands with the 
   description
10. Use commands <b>'exit', 'close', 'good bye'</b> to exit from the bot mode
