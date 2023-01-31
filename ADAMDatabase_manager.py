import sqlite3

class ADAM_DATABASE_MANAGER:
    def __init__(self):
        
        self.database = sqlite3.connect('ADAM_DATABASE.db')
        self.cursor = self.database.cursor()

    def query_all_table_names(self):      # searches all the database for table names and returns a list of them
        #reconnect 
        
        sql_table_query = """SELECT name FROM sqlite_master WHERE type='table'"""
        self.cursor.execute(sql_table_query)
        list_of_tables = self.cursor.fetchall()
        return list_of_tables

    def search_for_Language_ROWS(self, language):
        rowSearch = f"""SELECT HelpName, ShortDescription, Rating, DateTimeEntry FROM {language}"""
        self.cursor.execute(rowSearch)
        list_of_Rows = self.cursor.fetchall()
        return list_of_Rows


    def user_search_for_Language_ROWS(self, language, searchTerm):
        rowSearch = f"""SELECT HelpName, ShortDescription, Rating, DateTimeEntry FROM {language} WHERE HelpName LIKE '%{searchTerm}%';"""
        self.cursor.execute(rowSearch)
        list_of_Rows = self.cursor.fetchall()
        return list_of_Rows

    def searchForhelpSection(self, Language, helpSearch):
        entrySearch = f"""SELECT Solution, ExtendedDescription, ExtraNotes, LinkToHelp FROM {Language} WHERE HelpName LIKE '{helpSearch}';"""
        self.cursor.execute(entrySearch)
        DataList = self.cursor.fetchall()
        return DataList

    def searchForEntryReturnNote(self, Language, helpSearch):
        entrySearch = f"""SELECT HelpName,ShortDescription,Solution,ExtendedDescription,ExtraNotes,Rating,LinkToHelp FROM {Language} WHERE HelpName LIKE '{helpSearch}';"""
        self.cursor.execute(entrySearch)
        DataList = self.cursor.fetchall()
        return DataList

    def removeNote(self, language, HelpName):
        deleteQuery = f"DELETE FROM {language} WHERE HelpName = '{HelpName}';"
        self.cursor.execute(deleteQuery)
        self.database.commit()

    def removeTable(self, language):
        dropQuery = f"DROP TABLE {language};"
        self.cursor.execute(dropQuery)
        self.database.commit()


    def createNewNote(self, language, helpName, shortDescription, solution, extendedDescription, extraNotes, rating, helpLink):
        newNoteQuery = f"""INSERT INTO {language} (HelpName,ShortDescription,Solution,ExtendedDescription,ExtraNotes,Rating,LinkToHelp) VALUES (?,?,?,?,?,?,?);"""
        HoldingList = [helpName, shortDescription, solution, extendedDescription, extraNotes, rating, helpLink]
        self.cursor.execute(newNoteQuery, HoldingList)
        self.database.commit()


    def updateNote(self, OldEntryName,language, newhelpName, newshortDescription, newsolution, newextendedDescription, newextraNotes, newrating, newhelpLink):
        
        #for every possible entry on the update screen, this part checks if something was entered, if nothing was then the function ignores that secion and only updates parts with text
        if newhelpName == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET HelpName = ? WHERE HelpName=?"""
            self.__updateList = [newhelpName, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newshortDescription == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET ShortDescription = ? WHERE HelpName=?"""
            self.__updateList = [newshortDescription, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newsolution == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET Solution = ? WHERE HelpName=?"""
            self.__updateList = [newsolution, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newextendedDescription == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET ExtendedDescription = ? WHERE HelpName=?"""
            self.__updateList = [newextendedDescription, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newextraNotes == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET ExtraNotes = ? WHERE HelpName=?"""
            self.__updateList = [newextraNotes, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newrating == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET Rating = ? WHERE HelpName=?"""
            self.__updateList = [newrating, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)

        if newhelpLink == '':
            pass
        else:
            self.__updateQuery = f"""UPDATE {language} SET LinkToHelp = ? WHERE HelpName=?"""
            self.__updateList = [newhelpLink, OldEntryName]
            self.cursor.execute(self.__updateQuery, self.__updateList)
        
        self.database.commit()
        


        
        



    def newTableEntry(self, tableName):
        try:
            newTableEntry = f"""CREATE TABLE {tableName}(
id INTEGER PRIMARY KEY, 
Language TEXT DEFAULT '{tableName}',
HelpName TEXT NOT NULL,
ShortDescription TEXT NOT NULL,
Solution TEXT NOT NULL,
ExtendedDescription TEXT NOT NULL,
ExtraNotes TEXT DEFAULT 'None',
Rating INTEGER NOT NULL,
LinkToHelp TEXT NOT NULL,
DateTimeEntry TEXT);
"""


            newTriggerEntry=f"""CREATE TRIGGER makeDate{tableName} AFTER INSERT ON {tableName}
BEGIN
    UPDATE {tableName} SET DateTimeEntry = DATE('now') WHERE {tableName}.id = NEW.id;
END
;"""

            
            self.cursor.execute(newTableEntry)
            self.cursor.execute(newTriggerEntry)
            
            return False
        except sqlite3.OperationalError:
            
            return True


        






    
    
        