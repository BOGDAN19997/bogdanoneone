CREATE TABLE Voice_Patterns (
	ID SERIAL PRIMARY KEY,
	Login varchar(30) UNIQUE NOT NULL,
	Password varchar(50) NOT NULL,
	Email varchar(50) UNIQUE NOT NULL,
	Lastname varchar(30), 
	Firstname varchar(30),
	Created timestamp
);

CREATE TABLE Text_Data ( 
	ID SERIAL PRIMARY KEY,
	Name varchar(30) NOT NULL,
	Description text, 
	Created timestamp,
	CountOfCommand_Lists int NOT NULL DEFAULT 0,
	Voice_Pattern_ID int,
	CONSTRAINT FK_Voice_Pattern_ID FOREIGN KEY (Voice_Pattern_ID)
      REFERENCES Voice_Patterns (ID),
	CONSTRAINT Check_Count_Proj CHECK (CountOfCommand_Lists >= 0)
);

CREATE TABLE Command_List ( 
	ID SERIAL PRIMARY KEY,
	Name varchar(30) NOT NULL,
	Description text, 
	Created timestamp,
	CountOfFiles int NOT NULL DEFAULT 0,
	Text_Data_ID int,
	CONSTRAINT FK_Text_Data_ID FOREIGN KEY (Text_Data_ID)
      REFERENCES Text_Data (ID),
	CONSTRAINT Check_Count_File CHECK (CountOfFiles >= 0)
);

CREATE TABLE Files ( 
	ID SERIAL PRIMARY KEY,
	Name varchar(30) NOT NULL,
	File_text text,
	Expansion varchar(10) NOT NULL,
	Versions varchar(30) NOT NULL DEFAULT '1.0', 
	Created timestamp,
	Rating real NOT NULL,
	Command_List_ID int,
	CONSTRAINT FK_Command_List_ID FOREIGN KEY (Command_List_ID)
      REFERENCES Command_List (ID)
);

--ALTER TABLE Voice_Patterns ADD CONSTRAINT Chack_correct_email CHECK (Email like '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');