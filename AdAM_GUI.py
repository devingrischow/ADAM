from tkinter import *
import customtkinter
import ADAMDatabase_manager
import functools
import webbrowser
import sys
import os
import re
import clipboard as clip

#this class is a wrapper for the customtkinter textbox, that allows the program to highlight text inside the textbox and make certain letters different colors, code is from stack overflow 
class CustomText(customtkinter.CTkTextbox):
    """
    Wrapper for the tkinter.Text widget with additional methods for
    highlighting and matching regular expressions.

    highlight_all(pattern, tag) - Highlights all matches of the pattern.
    highlight_pattern(pattern, tag) - Cleans all highlights and highlights all matches of the pattern.
    clean_highlights(tag) - Removes all highlights of the given tag.
    search_re(pattern) - Uses the python re library to match patterns.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        
        # sample tag
        self.tag_config("match", foreground="red")

    def highlight(self, tag, start, end):
        self.tag_add(tag, start, end)
    
    def highlight_all(self, pattern, tag):
        for match in self.search_re(pattern):
            self.highlight(tag, match[0], match[1])

    def clean_highlights(self, tag):
        self.tag_remove(tag, "1.0", customtkinter.END)

    def search_re(self, pattern):
        """
        Uses the python re library to match patterns.

        Arguments:
            pattern - The pattern to match.
        Return value:
            A list of tuples containing the start and end indices of the matches.
            e.g. [("0.4", "5.9"]
        """
        matches = []
        text = self.get("1.0", customtkinter.END).splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        
        return matches

    def highlight_pattern(self, pattern, tag="match"):
        """
        Cleans all highlights and highlights all matches of the pattern.

        Arguments:
            pattern - The pattern to match.
            tag - The tag to use for the highlights.
        """
        self.clean_highlights(tag)
        self.highlight_all(pattern, tag)


#theme 
customtkinter.set_default_color_theme("blue")

closedState = ''

# uses tkinter to get the screen size of the monitor in use
def get_screen_size():
    root = Tk()
    
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    resolution = (height, width)
    root.destroy()
    return resolution



class ADAM_GUI:      # drives the main GUI elements
    def __init__(self):
        self.main_window = customtkinter.CTk()
        
        
        self.main_window.title('ADAM Notes App')

        self.screenSize = get_screen_size()
        
        #Screen Size Dependent Setting: Main Screen Size
        
        self.main_window.geometry("1350x600")
        
        #self.main_window.resizable(width=False, height=False)

        self.updatingNotesFrame = customtkinter.CTkFrame(self.main_window,fg_color='transparent',height=100, width=450)
        self.updatingNotesFrame.pack(anchor='se',side='bottom',padx=(0,45))
        self.updatingNotesFrame.pack_propagate(False)

        self.codeResultFrame = customtkinter.CTkFrame(self.main_window, fg_color='transparent')
        self.codeResultFrame.pack(side='right', anchor='ne') 

        
        
        #code for presenting all tables in button form
        self.dbDRIVER = ADAMDatabase_manager.ADAM_DATABASE_MANAGER()
        self.Languages = self.dbDRIVER.query_all_table_names()
        lang = []
        for l in self.Languages:
            lang.append(l[0])
        self.langFrame = customtkinter.CTkFrame(self.main_window, fg_color='transparent')
        self.languageBox = customtkinter.CTkComboBox(self.langFrame, values=lang, command=self.searchSelectedLanguage, width=400, height=50)
        self.languageBox.pack(anchor='w', padx=(10,5), pady=(10,25))
        self.langFrame.pack(anchor='w')

               

  
        self.entryResultsFrame = customtkinter.CTkFrame(self.main_window, fg_color='transparent',height=700)
        self.entryResultsFrame.pack(anchor='w')

        
 

        #Screen Size Dependent Setting: Main Menu Font
        if self.screenSize[0] < 1000:
            #mac size
            self.mainMenu_fontFormat = ("Arial", 22.5)
        else:
            #big windows way
            self.mainMenu_fontFormat = ("Arial", 45)

        


        #entry/note buttons
        buttonFont = ('arial', 11)

        

        self.newNoteButton = customtkinter.CTkButton(self.updatingNotesFrame, text='Create A New Note', fg_color='#696969', width=300, command=lambda:self.createNewNote())
        self.newNoteButton.pack(anchor='center', side='top', pady=(0,4), padx=(30,0))


        self.dropTableButton = customtkinter.CTkButton(self.updatingNotesFrame, text='Remove A Language',fg_color='#696969', width=60, font=buttonFont, command=lambda:self.removeALanguage())
        self.dropTableButton.pack(anchor='n', side='right', padx=(2,2))

        self.removeNoteButton = customtkinter.CTkButton(self.updatingNotesFrame, text='Remove a Note',fg_color='#696969', width=60, font=buttonFont, command= lambda:self.removeANote())
        self.removeNoteButton.pack(anchor='n', side='right')
        
        self.updateNoteButton = customtkinter.CTkButton(self.updatingNotesFrame, text='Update A Note',fg_color='#696969', width=60, font=buttonFont, command= lambda: self.updateANote())
        self.updateNoteButton.pack(anchor='n', side='right', padx=(0,3))

        self.newTableButton = customtkinter.CTkButton(self.updatingNotesFrame, text='Add a New Language Tab',fg_color='#696969', command= self.newTableBox, width=60, font=buttonFont)
        self.newTableButton.pack(anchor='n', side='right', padx=(2,2))

        

        
        
        self.main_window.mainloop()


    def searchSelectedLanguage(self, value):
        #clears frame holding buttons
        try:
            self.searchbutton.destroy()
            self.searchEntry.destroy()
        except AttributeError:
            pass
        self.searchEntry = customtkinter.CTkEntry(self.langFrame, width=200, height=40, placeholder_text='Enter a search Term')
        self.searchbutton = customtkinter.CTkButton(self.langFrame, height=40, width=40, text='Search', command=lambda:self.searchForEntry(self.currentSelectedLanguage, self.searchEntry.get()))

        self.searchEntry.pack(anchor='n', side='left', padx=(30,0))


        self.searchbutton.pack(anchor='n', side='left', pady=(0,30))

        

        self.currentSelectedLanguage = value
       
        try:
            self.chaningButtonZone.destroy()
        except AttributeError:
            pass
        self.chaningButtonZone = customtkinter.CTkFrame(self.entryResultsFrame, height=1500, fg_color='transparent')
        self.chaningButtonZone.pack(anchor='n', fill='both', expand=1)
        
        #new scrollbar on this zone 
        #new canvas
        self.resultsCanvas = customtkinter.CTkCanvas(self.chaningButtonZone, width=700, height=1000)
        self.resultsCanvas.pack(padx=(0,10), side='right', fill='both', expand=1)
        #adding scrollbar
        self.resultsScrollBar = customtkinter.CTkScrollbar(self.chaningButtonZone, orientation=VERTICAL, command=self.resultsCanvas.yview, height=1000,width=18)
        self.resultsScrollBar.pack(side='right', fill='y', padx=(4,0))
        #configure Canvas
        self.resultsCanvas.configure(yscrollcommand=self.resultsScrollBar.set)
        self.resultsCanvas.bind('<Configure>', lambda e:self.resultsCanvas.configure(scrollregion = self.resultsCanvas.bbox("all")))
        #newbuttonsFrame
        self.newresultsHoldingFrame = customtkinter.CTkFrame(self.resultsCanvas, fg_color='transparent')
        self.resultsCanvas.create_window((0,0),window=self.newresultsHoldingFrame)
        
        tableRows = self.dbDRIVER.search_for_Language_ROWS(value)
        


        #Screen Size Dependent Setting: Row Button Font
        if self.screenSize[0] < 1000:
            #mac size
            #font for every button generated
            rowButtonFont = ('Arial', 15)
        else:
            #big windows way
            #font for every button generated
            rowButtonFont = ('Arial', 30)


        
        for row in tableRows:
            #functools.partial allows the button function to use a partial version of the function, and allowing for the more easier unique button creating with advanced functioning 
            x = functools.partial(self.codeSection, value, row[0])
            #for every row in the tablerows list, make a button 
            buttonText = f"""{row[0]}\t{row[2]}\n\n\t\t{row[1]}\t{row[3]}"""


            #Screen Size Dependent Setting: RowButton Sizing
            self.__rowButon = customtkinter.CTkButton(self.newresultsHoldingFrame, text=buttonText, font=rowButtonFont, width=900, command=x).grid(row=tableRows.index(row), column=0,pady=(10,5))
            
            
            
            
            #When pressing a button it brings up the help code section, and while also clearing the old one if there was anything present 
        

    def openLink(self, Url):
        c = webbrowser.get('safari')
        c.open_new_tab(Url)


    
 

    def codeSection(self, Language, Search):
        print(Search, 'lesearch')
        DescriptionFont = ("Arial", 17)
        # a changing frame, to be destroyed everytime the row button is pressed

        #Screen Size Dependent Setting: Row Button Font
        #mac size
            #font for every button generated
            #clears frame holding buttons
        try:
            self.__changingFrame.destroy()
        except AttributeError:                
            pass
        self.__changingFrame = customtkinter.CTkFrame(self.codeResultFrame, corner_radius=7.5, fg_color='#1F6AA5',height=900, width=500)
         
        

        
        
        #retrive list of information 
        searchData = self.dbDRIVER.searchForhelpSection(Language, Search)



        # #Screen Size Dependent Setting: Row Button Font
        self.entryName = customtkinter.CTkTextbox(self.__changingFrame)
        self.entryName.insert('0.0', Search)
        self.entryName.configure(state='disabled', fg_color='gray', width=560, height=35, font=DescriptionFont)
        
        self.entryName.pack(pady=(15,0), padx=(5,5))
            

            #Solution Design Area

        SolutionFont = ("Arial", 17)
        #self.solutionArea = customtkinter.CTkTextbox(self.__changingFrame)
        self.solutionArea = CustomText(self.__changingFrame, state='normal')
        
        self.solutionArea.insert("0.0", searchData[0][0])
        print(searchData[0][0])
            #Solution Box
        
        self.solutionArea.configure(state='disabled', width=560, height=200, font=SolutionFont)
        self.solutionArea.bind('<Button-1>', command=lambda e:self.copySolutionToClipBoard(searchData[0][0]))
        self.solutionArea.pack(side='top', pady=(5,0), padx=(5,5))
        #SOLUTION TAGS
        self.solutionArea.tag_config('import', foreground='red')
        self.solutionArea.tag_config('def', foreground='light blue')
        self.solutionArea.tag_config('class', foreground='light blue')
        self.solutionArea.tag_config('self', foreground='yellow')

        #######
        self.solutionArea.bind('<Configure>', self.highlight_TEXT)
        

       


            #Description Design Area

        
        self.descriptionArea = customtkinter.CTkTextbox(self.__changingFrame)
        self.descriptionArea.insert("0.0", searchData[0][1])
            #Description Box
        self.descriptionArea.configure(state='disabled', fg_color='gray', width=560, height=115, font=DescriptionFont)
        self.descriptionArea.pack(pady=(15,0), padx=(5,5))


            #Extra Notes Design Area

        ExNotesFont = ("Arial", 12)
        self.extraNotesArea = customtkinter.CTkTextbox(self.__changingFrame)
        self.extraNotesArea.insert("0.0", searchData[0][2])
        #extraNotes Box
        self.extraNotesArea.configure(state='disabled', fg_color='gray', width=560, height=30, font=ExNotesFont)
        self.extraNotesArea.pack(pady=(11,6), padx=(5,5))

        
            #Link Area

        LinkFont = customtkinter.CTkFont(family="Arial", size=10, underline=True, weight='bold', slant='italic')
        self.LinkTitle = customtkinter.CTkTextbox(self.__changingFrame)   #, font=LinkFont, text=searchData[0][3], width=450)
        self.LinkTitle.insert("0.0", searchData[0][3])
        self.LinkTitle.configure(state='disabled', fg_color='gray', width=560, font=LinkFont, height=20)
             
        self.LinkTitle.bind("<Button-1>",lambda e: self.openLink(f"{searchData[0][3]}"))
        self.LinkTitle.pack(anchor='center', expand=False)
            
            
            
            
        self.__changingFrame.pack(side='right', anchor='n',padx=[25,17.5], expand=1)
        self.__changingFrame.pack_propagate(True)
        self.codeResultFrame.pack(side='right', anchor='n')

        

    #replaces the current note selection box with one with search entries from the user

    def highlight_TEXT(self, *args):
        self.solutionArea.highlight_pattern('import', 'import')  
        self.solutionArea.highlight_pattern('class', 'class')
        self.solutionArea.highlight_pattern('def', 'def')
        self.solutionArea.highlight_pattern('self', 'self')
        

    def searchForEntry(self, language, query):
        

        try:
            self.chaningButtonZone.destroy()
        except AttributeError:
            pass
        self.chaningButtonZone = customtkinter.CTkFrame(self.entryResultsFrame, height=700, fg_color='transparent')
        
        #new scrollbar on this zone 
        #new canvas
        self.resultsCanvas = customtkinter.CTkCanvas(self.chaningButtonZone, width=700, height=800)
        self.resultsCanvas.pack(side='right', padx=(0,10))
        #adding scrollbar
        self.resultsScrollBar = customtkinter.CTkScrollbar(self.chaningButtonZone, orientation=VERTICAL, command=self.resultsCanvas.yview, width=50)
        self.resultsScrollBar.pack(side='left', fill='both', padx=(4,0))
        #configure Canvas
        self.resultsCanvas.configure(yscrollcommand=self.resultsScrollBar.set)
        self.resultsCanvas.bind('<Configure>', lambda e:self.resultsCanvas.configure(scrollregion=self.resultsCanvas.bbox('all')))
        #newbuttonsFrame
        self.newresultsHoldingFrame = customtkinter.CTkFrame(self.resultsCanvas, fg_color='transparent')
        self.resultsCanvas.create_window((0,0),window=self.newresultsHoldingFrame)
        
        tableRows = self.dbDRIVER.user_search_for_Language_ROWS(language, query)


        #Screen Size Dependent Setting: Row Button Font
        if self.screenSize[0] < 1000:
            #mac size
            #font for every button generated
            rowButtonFont = ('Arial', 15)
        else:
            #big windows way
            #font for every button generated
            rowButtonFont = ('Arial', 30)


        
        for row in tableRows:
            #functools.partial allows the button function to use a partial version of the function, and allowing for the more easier unique button creating with advanced functioning 
            x = functools.partial(self.codeSection, language, row[0])
            #for every row in the tablerows list, make a button 
            buttonText = f"""{row[0]}\t{row[2]}\n\n\t\t{row[1]}\t{row[3]}"""

           
            #Screen Size Dependent Setting: RowButton Sizing
            self.__rowButon = customtkinter.CTkButton(self.newresultsHoldingFrame, text=buttonText, font=rowButtonFont, width=750, command=x).grid(row=tableRows.index(row), column=0,pady=(5,5))
            
            
            
            
            
            #When pressing a button it brings up the help code section, and while also clearing the old one if there was anything present 
        self.chaningButtonZone.pack(anchor='nw')


    def copySolutionToClipBoard(self,solution):
        clip.copy(solution)
    #CRUD ELEMENTS 
    def newTableBox(self):
        self.newTableEntryBox = customtkinter.CTkInputDialog(text="Enter The Name Of the New Language", title="Enter A New Language")
        newLanguage = self.newTableEntryBox.get_input()
        #returns true if name exists, false if the name not exsists
        newLanguage = self.dbDRIVER.newTableEntry(newLanguage)

        if newLanguage == False:
            #just close and re open program
            self.restart()
            
        else:
            errorWindow = customtkinter.CTkToplevel(self.main_window)
            errorWindow.geometry('300x100')
            errorLabel = customtkinter.CTkLabel(errorWindow, text="An Error Occured Adding A New Language")
            errorLabel.pack(padx=(20,20), pady=(20,20))
            errorcloseButtom = customtkinter.CTkButton(errorWindow, text="Close window", command=lambda:errorWindow.destroy())
            errorcloseButtom.pack()






    def createNewNote(self):
        self.newNoteWindow = customtkinter.CTkToplevel(self.main_window)
        self.newNoteWindow.geometry("460x730")
        self.newNoteWindow.title('Add a New Note')
        self.newNoteWindow.resizable(width=False, height=False)


        #language comboxbox, lets the user select which language table to add the note to
        allLanguages = self.dbDRIVER.query_all_table_names()
        temp = []
        for lang in allLanguages:
            temp.append(lang[0])
        self.languageSelect = customtkinter.CTkComboBox(self.newNoteWindow, values=temp, width=430, height=40, state='readonly')
        self.languageSelect.pack(pady=(10,15))
        #name entry box, for the user to enter a name of the note
        self.noteNameEntry = customtkinter.CTkEntry(self.newNoteWindow, placeholder_text="Enter the New Notes Name",width=430, height=40)
        self.noteNameEntry.pack(pady=(10,15))
        #a short entry box for a short description of the note
        self.noteShortDescriptionEntry = customtkinter.CTkEntry(self.newNoteWindow, placeholder_text="Enter a short Description of the Note",width=430, height=40)
        self.noteShortDescriptionEntry.pack(pady=(5,15))
        #label to guide the user what the box is meant for 
        self.noteLabel = customtkinter.CTkLabel(self.newNoteWindow, text="Type Your Code Below", font=('arial', 12))
        self.noteLabel.pack()
        #text zone for the note
        self.noteZone = customtkinter.CTkTextbox(self.newNoteWindow, width=430, height=200)
        self.noteZone.pack()
        #label to tell the user the purpose of the below box
        self.noteLabelDescription = customtkinter.CTkLabel(self.newNoteWindow, text="Enter a Description for the Note", font=('arial', 12))
        self.noteLabelDescription.pack()
        #text box for a description of the note
        self.noteDescription = customtkinter.CTkTextbox(self.newNoteWindow, width=430, height=50)
        self.noteDescription.pack()
        #double entry frame zone
        self.entryZone = customtkinter.CTkFrame(self.newNoteWindow, fg_color='transparent')
        
        #small entry box for extra notes
        self.extraNotesEntry = customtkinter.CTkEntry(self.entryZone, placeholder_text='Enter some entra Notes', width=260, height=40)
        self.extraNotesEntry.pack(side='left')
        #Rating entry box for extra notes
        self.RatingsEntry = customtkinter.CTkEntry(self.entryZone, placeholder_text='Enter a rating for the note', width=170, height=40)
        self.RatingsEntry.pack(side='left')
        self.entryZone.pack(pady=(10,10))
        #link entry 
        self.linkentry = customtkinter.CTkEntry(self.newNoteWindow, placeholder_text='Enter a link (if one) where you found the help', width=430, height=50)
        self.linkentry.pack(pady=(10,10))
        #submit button(activates and creates the new note)
        




        self.createNoteButton = customtkinter.CTkButton(self.newNoteWindow, width=215, height=215, command=lambda:self.getEntries(), text="Create New Note")
        self.createNoteButton.pack(pady=(0,15))
    #this function gets the entries from the entires and creates a new note, and then destroys the window after
    def getEntries(self):
        languagevar = self.languageSelect.get()
        hlpName = self.noteNameEntry.get()
        shortdscrptn = self.noteShortDescriptionEntry.get()
        note = self.noteZone.get('0.0', 'end')
        extdescr = self.noteDescription.get('0.0', 'end')
        extNotes = self.extraNotesEntry.get()
        Rating = self.RatingsEntry.get()
        link = self.linkentry.get()
        
        self.dbDRIVER.createNewNote(language=languagevar, helpName=hlpName, shortDescription=shortdscrptn, solution=note, extendedDescription=extdescr, extraNotes=extNotes,rating=Rating, helpLink=link)
        self.newNoteWindow.destroy()


    def removeANote(self):
        self.deleteNoteWindow = customtkinter.CTkToplevel(self.main_window)
        self.deleteNoteWindow.geometry("460x800")
        self.deleteNoteWindow.title('Remove a Note')
        #self.deleteNoteWindow.resizable(width=False, height=False)

        #takes the unorganized all languages and takes every entry and only places the text into a list
        allLanguages = self.dbDRIVER.query_all_table_names()
        temp = []
        for lang in allLanguages:
            temp.append(lang[0])
        

        self.languageKIllSelect = customtkinter.CTkComboBox(self.deleteNoteWindow, values=temp, width=430, height=40, state='readonly', command=self.finishRemoval)
        self.languageKIllSelect.pack(pady=(10,15))
    #another function is required to remove a note, the first function opens the window and has the display box, when the user selects a option it then calls this next function, which will 
    #display all the buttons in the selected table (in a similar fashion to the home screen), but when you click a button it deletes the entry
    def finishRemoval(self,selectedLanguage):


        try:
            self.zone3.destroy()
        except AttributeError:
            pass
        self.zone3 = customtkinter.CTkFrame(self.deleteNoteWindow, height=700, width=400, fg_color='transparent')

        self.removeLabel = customtkinter.CTkLabel(self.zone3, text="Click a Note to Delete It")
        self.removeLabel.pack()
        #new scrollbar on this zone 
        #new canvas
        self.resultsCanvas2 = customtkinter.CTkCanvas(self.zone3, width=400, height=800)
        self.resultsCanvas2.pack(side='right', padx=(0,10), fill='both', expand=1)
        #adding scrollbar
        self.resultsScrollBar2 = customtkinter.CTkScrollbar(self.zone3, orientation=VERTICAL, command=self.resultsCanvas2.yview, width=50)
        self.resultsScrollBar2.pack(side='left', fill='y', padx=(4,0))
        #configure Canvas
        self.resultsCanvas2.configure(yscrollcommand=self.resultsScrollBar2.set)
        self.resultsCanvas2.bind('<Configure>', lambda e:self.resultsCanvas2.configure(scrollregion=self.resultsCanvas2.bbox('all')))
        #newbuttonsFrame
        self.newresultsHoldingFrame2 = customtkinter.CTkFrame(self.resultsCanvas2, fg_color='transparent')
        self.resultsCanvas2.create_window((0,0),window=self.newresultsHoldingFrame2)
        tableRows = self.dbDRIVER.search_for_Language_ROWS(selectedLanguage)


        #Screen Size Dependent Setting: Row Button Font
        if self.screenSize[0] < 1000:
            #mac size
            #font for every button generated
            rowButtonFont = ('Arial', 9)
        else:
            #big windows way
            #font for every button generated
            rowButtonFont = ('Arial', 30)


        
        for row in tableRows:
            #functools.partial allows the button function to use a partial version of the function, and allowing for the more easier unique button creating with advanced functioning 
            
            x = functools.partial(self.finalRemove, selectedLanguage, row[0])
            
            #for every row in the tablerows list, make a button 
            buttonText = f"""{row[0]}   {row[2]}\n\n{row[1]}            {row[3]}"""

          
            #Screen Size Dependent Setting: RowButton Sizing
            self.__rowButon2 = customtkinter.CTkButton(self.newresultsHoldingFrame2, text=buttonText, font=rowButtonFont, width=440, command=x).grid(row=tableRows.index(row), column=0,pady=(5,5), padx=(6,0))
            
            
            
            
            #When pressing a button it brings up the help code section, and while also clearing the old one if there was anything present 
        self.zone3.pack(anchor='nw')
    #calls the function to remove the entry
    def finalRemove(self, lang, helpNAME):
        self.dbDRIVER.removeNote(lang, helpNAME)
        self.deleteNoteWindow.destroy()

    #drop a table button(very simple)
    def removeALanguage(self):
        self.deleteTableWindow = customtkinter.CTkToplevel(self.main_window)
        self.deleteTableWindow.geometry("470x100")
        self.deleteTableWindow.title('Remove a Language')
        self.deleteTableWindow.resizable(width=False, height=False)

        #takes the unorganized all languages and takes every entry and only places the text into a list
        allLanguages = self.dbDRIVER.query_all_table_names()
        temp = []
        for lang in allLanguages:
            temp.append(lang[0])
        
        #label to instruct
        self.instructLabel = customtkinter.CTkLabel(self.deleteTableWindow, text="Select a Language from the Drop Down Bar to Delete It Perminently", font=('arial', 15))
        self.instructLabel.pack(pady=(0,5))

        self.__languageKIllSelect = customtkinter.CTkComboBox(self.deleteTableWindow, values=temp, width=430, height=40, state='readonly', command=self.removeLanguage)
        self.__languageKIllSelect.pack(pady=(10,15))
    #function to call drop table function, and close window 
    def removeLanguage(self, language):
        self.dbDRIVER.removeTable(language)
        self.restart()


    def updateANote(self):
        self.updateNoteWindow = customtkinter.CTkToplevel(self.main_window)
        self.updateNoteWindow.geometry("620x380")
        self.updateNoteWindow.title('Update a Note')
        self.updateNoteWindow.resizable(width=False, height=False)

        #takes the unorganized all languages and takes every entry and only places the text into a list
        allLanguages = self.dbDRIVER.query_all_table_names()
        temp = []
        for lang in allLanguages:
            temp.append(lang[0])
        
        #label to instruct
        self.__instructLabel = customtkinter.CTkLabel(self.updateNoteWindow, text="Select a Language from the Drop Down Bar To select The Language the Note is Located in", font=('arial', 15))
        self.__instructLabel.pack()

        self.__languageSelector = customtkinter.CTkComboBox(self.updateNoteWindow, values=temp, width=430, height=40, state='readonly', command=self.displayEntriesToUpdate)
        self.__languageSelector.pack(pady=(10,15))

    def displayEntriesToUpdate(self,selectedLanguage):
        self.SelectedLanguage = selectedLanguage

        try:
            self.__zone3.destroy()
        except AttributeError:
            pass
        self.__zone3 = customtkinter.CTkFrame(self.updateNoteWindow, height=700, width=400, fg_color='transparent')

        self.__updateLabel = customtkinter.CTkLabel(self.__zone3, text="Click a Note to Update It It")
        self.__updateLabel.pack()

        

        #new scrollbar on this zone 
        #new canvas
        self.__resultsCanvas2 = customtkinter.CTkCanvas(self.__zone3, width=400, height=800)
        self.__resultsCanvas2.pack(side='right', padx=(0,10))
        #adding scrollbar
        self.__resultsScrollBar2 = customtkinter.CTkScrollbar(self.__zone3, orientation=VERTICAL, command=self.__resultsCanvas2.yview, width=50)
        self.__resultsScrollBar2.pack(side='left', fill='both', padx=(4,0))
        #configure Canvas
        self.__resultsCanvas2.configure(yscrollcommand=self.__resultsScrollBar2.set)
        self.__resultsCanvas2.bind('<Configure>', lambda e:self.__resultsCanvas2.configure(scrollregion=self.__resultsCanvas2.bbox('all')))
        #newbuttonsFrame
        self.__newresultsHoldingFrame2 = customtkinter.CTkFrame(self.__resultsCanvas2, fg_color='transparent')
        self.__resultsCanvas2.create_window((0,0),window=self.__newresultsHoldingFrame2)
        tableRows = self.dbDRIVER.search_for_Language_ROWS(selectedLanguage)


        #Screen Size Dependent Setting: Row Button Font
        if self.screenSize[0] < 1000:
            #mac size
            #font for every button generated
            rowButtonFont = ('Arial', 9)
        else:
            #big windows way
            #font for every button generated
            rowButtonFont = ('Arial', 30)


        
        for row in tableRows:
            #functools.partial allows the button function to use a partial version of the function, and allowing for the more easier unique button creating with advanced functioning 
            
            x = functools.partial(self.updateSelectedNoteScreen, row[0], selectedLanguage)
            
            #for every row in the tablerows list, make a button 
            buttonText = f"""{row[0]}   {row[2]}\n\n{row[1]}            {row[3]}"""

            self.__rowButon2 = customtkinter.CTkButton(self.__newresultsHoldingFrame2, text=buttonText, font=rowButtonFont, width=440, command=x).grid(row=tableRows.index(row), column=0,pady=(5,5), padx=(10,0))
            
            
            
            
            #When pressing a button it brings up the help code section, and while also clearing the old one if there was anything present 
        self.__zone3.pack(anchor='nw')

    def updateSelectedNoteScreen(self, entryName, selectedLanguage):
        self.updateNoteWindow.destroy()
        self.entryTochange = entryName
        self.updateNoteWindow = customtkinter.CTkToplevel(self.main_window)
        self.updateNoteWindow.geometry("460x730")
        self.updateNoteWindow.title('Update a Note')
        self.updateNoteWindow.resizable(width=False, height=False)

        selectedEntry = self.dbDRIVER.searchForEntryReturnNote(selectedLanguage, entryName)
        storage = []
        for item in selectedEntry[0]:
            print(item,'\n')
            storage.append(item)

        print(storage)
            

            

        
        #name entry box, for the user to enter a name of the note
        self.noteNameEntry = customtkinter.CTkEntry(self.updateNoteWindow, placeholder_text=storage[0],width=430, height=40)
        self.noteNameEntry.pack(pady=(10,15))
        #a short entry box for a short description of the note
        self.noteShortDescriptionEntry = customtkinter.CTkEntry(self.updateNoteWindow, placeholder_text=storage[1],width=430, height=40)
        self.noteShortDescriptionEntry.pack(pady=(5,15))
        #label to guide the user what the box is meant for 
        self.noteLabel = customtkinter.CTkLabel(self.updateNoteWindow, text='Type Your Note Below', font=('arial', 12))
        self.noteLabel.pack()
        #text zone for the note
        self.noteZone = customtkinter.CTkTextbox(self.updateNoteWindow, width=430, height=200)
        self.noteZone.insert('0.0', storage[2])
        self.noteZone.pack()
        #label to tell the user the purpose of the below box
        self.noteLabelDescription = customtkinter.CTkLabel(self.updateNoteWindow, text='Enter A Description', font=('arial', 12))
        self.noteLabelDescription.pack()
        #text box for a description of the note
        self.noteDescription = customtkinter.CTkTextbox(self.updateNoteWindow,width=430, height=50)
        self.noteDescription.insert('0.0', storage[3])
        self.noteDescription.pack()
        #double entry frame zone
        self.entryZone = customtkinter.CTkFrame(self.updateNoteWindow, fg_color='transparent')
        
        #small entry box for extra notes
        self.extraNotesEntry = customtkinter.CTkEntry(self.entryZone, placeholder_text=storage[4], width=260, height=40)
        self.extraNotesEntry.pack(side='left')
        #Rating entry box for extra notes
        self.RatingsEntry = customtkinter.CTkEntry(self.entryZone, placeholder_text=storage[5], width=170, height=40)
        self.RatingsEntry.pack(side='left')
        self.entryZone.pack(pady=(10,10))
        #link entry 
        self.linkentry = customtkinter.CTkEntry(self.updateNoteWindow, placeholder_text=storage[6], width=430, height=50)
        self.linkentry.pack(pady=(10,10))
        #submit button(activates and creates the new note)
        



        
        self.createNoteButton = customtkinter.CTkButton(self.updateNoteWindow, width=215, height=215, command=lambda:self.getupdateEntrys(), text="Update Note")
        self.createNoteButton.pack(pady=(0,15))

    def getupdateEntrys(self):
        
        hlpName = self.noteNameEntry.get()
        shortdscrptn = self.noteShortDescriptionEntry.get()
        note = self.noteZone.get('0.0', 'end')
        extdescr = self.noteDescription.get('0.0', 'end')
        extNotes = self.extraNotesEntry.get()
        Rating = self.RatingsEntry.get()
        link = self.linkentry.get()
        
        self.dbDRIVER.updateNote(self.entryTochange,self.SelectedLanguage, hlpName, shortdscrptn, note, extdescr, extNotes,Rating, link)
        self.updateNoteWindow.destroy()

    def restart(self):
        self.main_window.destroy()
       
        os.system('open Adam_GUI.py')

    







        

        

        
    


    

            
            

        


        

        

        
        




            

ADAM_GUI()







