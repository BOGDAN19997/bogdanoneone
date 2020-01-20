CREATE TABLE Voice_Patterns (
	ID SERIAL PRIMARY KEY,
	Voice_body varchar(30) UNIQUE NOT NULL,
	Voice_data varchar(50) NOT NULL,
	Voice_HMM varchar(50) UNIQUE NOT NULL,
	Voice_emotion_logic_accent varchar(30), 
	Voice_similar_words varchar(30),
	Pronunciation_date timestamp
);

CREATE TABLE Text_Data ( 
	ID SERIAL PRIMARY KEY,
	Taglist_check varchar(30) NOT NULL,
	Full_body text, 
	Pronunciation_date timestamp,
	CountOfCommand_Lists int NOT NULL DEFAULT 0,
	Voice_Pattern_ID int,
	CONSTRAINT FK_Voice_Pattern_ID FOREIGN KEY (Voice_Pattern_ID)
      REFERENCES Voice_Patterns (ID));

CREATE TABLE Command_List ( 
	ID SERIAL PRIMARY KEY,
	Taglist_check varchar(30) NOT NULL,
	Full_body text, 
	Pronunciation_date timestamp,
	CountOfCommands int NOT NULL DEFAULT 0,
	Text_Data_ID int,
	CONSTRAINT FK_Text_Data_ID FOREIGN KEY (Text_Data_ID)
      REFERENCES Text_Data (ID),
	CONSTRAINT Check_Count_Command CHECK (CountOfCommands >= 0)
);

CREATE TABLE Commands ( 
	ID SERIAL PRIMARY KEY,
	Taglist_check varchar(30) NOT NULL,
	Command_body text,
	Expansion varchar(10) NOT NULL,
	Versions varchar(30) NOT NULL DEFAULT '1.0', 
	Pronunciation_date timestamp,
	Rating real NOT NULL,
	Command_List_ID int,
	CONSTRAINT FK_Command_List_ID FOREIGN KEY (Command_List_ID)
      REFERENCES Command_List (ID)
);

--ALTER TABLE Voice_Patterns ADD CONSTRAINT Chack_correct_voice_hmm CHECK (Voice_HMM like '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');