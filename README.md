# std_helper_bot
<i> Tairzhan Kassenov, Darkhan Bekuzak
SE-2113 </i>

[Link](https://t.me/std_helper_01_bot)

### Introduction:
 The std_helper telegram bot project is designed to assist students with recording deadlines, assignments, and reminders. Additionally, the bot can be used as a regular to-do list and has the ability to download music from various social networks and allow users to listen to them. The primary goal of the project is to provide individualized reminders to students, which can help to develop discipline and improve their academic performance. The project was developed using Python, telegram.ext, python-telegram-bot API, TelegramAPI, and MongoDB.


### Goals:
The goals of the std_helper telegram bot project were to develop a system that could:
1.	Provide individualized reminders to students.
2.	Help develop student discipline.
3.	Allow users to download music from any social network and listen to it.
4.	Implement a CRUD system that could interact with MongoDB.
5.	Explore new technologies, especially MongoDB.


### Technical response:
The std_helper telegram bot project utilized several key technical requirements, including:

#### CRUD:
 The project was designed to implement CRUD functionality to interact with the MongoDB database.

##### Create, read, update:
 

##### Delete:
 

### Data Schemas and Modeling:
The project utilized nested documents and relations with multiple collections for data modeling.

#### ERD:
 

#### CRD:
 

### Documents structure:



### Advanced Methods for Data Updating and Deletion:
With help of $pop aggregate function we delete one specific document in embedded structure. Example:
db.students.update( { _id: 1 }, { $pop: { scores: -1 } } )


### Stack and Technologies:

The std_helper telegram bot project was developed using Python, telegram.ext, python-telegram-bot API, TelegramAPI, and MongoDB. 

The Telegram API was used to interact with the Telegram platform, while the
 python-telegram-bot API was used to develop the bot's functionality. 

MongoDB was utilized as the project's primary database, and the 
PyMongo library was used to interact with the database.

## cryptography fernet is used to encrypt the username of the telegram user and it can also help encrypt the password.

## pafy is used to have the function of downloading video or audio from platforms like YouTube and etc.


### Conclusion:
In conclusion, the std_helper telegram bot project was designed to provide students with individualized reminders and help develop their discipline. The project utilized several key technical requirements, including CRUD functionality, data schemas and modeling, advanced methods for data updating and deletion, and optimized indexes. The project was developed using Python, telegram.ext, python-telegram-bot API, TelegramAPI, and MongoDB. Overall, the project was a success and achieved its intended goals.
![image](https://user-images.githubusercontent.com/94629077/220839161-49a596d0-a118-40ee-aa8a-52c092187eaf.png)
