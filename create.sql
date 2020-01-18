CREATE TABLE Users (
	ID SERIAL PRIMARY KEY,
	Login varchar(30) UNIQUE NOT NULL,
	Password varchar(50) NOT NULL,
	Email varchar(50) UNIQUE NOT NULL,
	Lastname varchar(30), 
	Firstname varchar(30),
	Created timestamp
);

CREATE TABLE Reposytoty ( 
	ID SERIAL PRIMARY KEY,
	Name varchar(30) NOT NULL,
	Description text, 
	Created timestamp,
	CountOfProjects int NOT NULL DEFAULT 0,
	User_ID int,
	CONSTRAINT FK_User_ID FOREIGN KEY (User_ID)
      REFERENCES Users (ID),
	CONSTRAINT Check_Count_Proj CHECK (CountOfProjects >= 0)
);

CREATE TABLE Project ( 
	ID SERIAL PRIMARY KEY,
	Name varchar(30) NOT NULL,
	Description text, 
	Created timestamp,
	CountOfFiles int NOT NULL DEFAULT 0,
	Reposytoty_ID int,
	CONSTRAINT FK_Reposytoty_ID FOREIGN KEY (Reposytoty_ID)
      REFERENCES Reposytoty (ID),
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
	Project_ID int,
	CONSTRAINT FK_Project_ID FOREIGN KEY (Project_ID)
      REFERENCES Project (ID)
);

--ALTER TABLE Users ADD CONSTRAINT Chack_correct_email CHECK (Email like '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');