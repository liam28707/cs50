# SecurPass Nexus
#### Video Demo: https://youtu.be/C4Ok3pzkFsU
#### Description:
My project file has a folder(static) to store javascript files as well as icons or images used in the webapp

The templates folder is used to store the corresponding html files of the project. It has 11 HTML files for various purposes.

layout.html: Describes the general layout of the webpage and is imported using jinja into all other html files.

index.html: It is a HTML files used to store the opening page to the website, which feature information about the website itself

passbank.html: This HTML file is used to store the table through which stored passwords are displayed. This file also has some javascript code in order to implement the functionality of an eye icon to hide and unhide passwords.

addpass.html: It is used to add a password to the PassBank
edit_password.html: Is used to edit paswords stored in the PassBank

delete_password.html: This file is used to link the code from app.py to delete passwords.

password_generator.html: This HTML file is used to store he form for generating a random password.

register.html: Provide a form for users to register to the website.

login.html: Allows user to login.

change_password.html: Allows user to change the password to his account.

apology.html: Used to render a meme incase a user doesn't comply with website requirements.

function.py: This is a helper file in python that contains various helper functions including the apology function to render the meme that shows how the user didn't comply as well as functions to generate random passwords or to ensure that login is required to access certain ascpects of the website

app.py: This is the main python file that has the code for the back-end development of the website. It calls on the functions such as werkzeug for proper hashing of passwords, cs50's implemention of sql, importing of flask and also the function described in function.py. It has various routes for the various parts of the website as described in the html files. All the way from registration to storing passwords in the PassBank.

passbank.db: This is a sqlite3 file that stores tables to maintain data, such as the users registered, the passwords stored in the password bank. It also has a table to store user sessions

Struggles: If I were to mention struggles when it came to implementation, it would definitly me in the javascript code to add functionality to hide and unhide passwords. As well as while linking making random generation of passwords available on different aspects of the webpage.