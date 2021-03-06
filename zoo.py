""" 
A program to guide zoo visitors

Written by Elliot Stjernqvist
"""

from pathlib import Path
from datetime import date, datetime
from tkinter import *
from tkinter import Button as button # use this one if not on mac
#from tkmacosx import Button as button # use this for mac as tkinter buttons do not work properly on latest mac OSX
from tkinter import messagebox
from calendar import monthrange
import tkinter

GUI = True
"""
Change to False to use program in terminal mode, note that terminal version of program is outdated. 
It can be used, but contains code repetition from the initial versions that was left only to allow the option of not using the GUI
"""

class FileHandling:
    """
    Handles reading and formating info from files
    """


    def __init__(self, file_name, delimiter):
        """
        Initializes class and attributes
        Arguements: Name of file to handle and delimiter used to separate values in the file
        """

        self.file_name = file_name
        self.delimiter = delimiter


    def read_file(self):
        """
        Reads file and removes first line which only displays the format and then turns lines in file into a list.
        Creates self.list for storing animal info
        """

        self.list = []

        open_file = open(self.file_name, 'r')
        
        lines = open_file.readlines()
        for line in lines: 
            self.list.append(line.strip())
        
        self.list.pop(0)    
        

    def format_list(self):
        """
        Formats list by splitting it into multiple lists one for each animal
        Argument: List to be formated
        Updates self.list
        """

        split_list = []
        for i in range(len(self.list)):
            split_list.append((self.list[i].split(self.delimiter)))
        
        self.list = split_list


    def fix_blankspace(self):
        """
        Removes the blankspace around every object in the list
        Argument: List to be fixed
        Updates self.list
        """
        
        for i in range(len(self.list)):
            for j in range(len(self.list[i])):
                self.list[i][j] = self.list[i][j].strip()
        

    def fix_type(self):
        """
        Converts all objects to the correct types and splits up objects representing a space of time for example 13-16
        Argument: List to be fixed
        Updates self.list
        """
        
        for i in range(len(self.list)):
            self.list[i][3] = int(self.list[i][3])
            time = self.list[i][2].split("-")
            self.list[i].pop(2)
            
            self.list[i].insert(2, int(time[0]))
            self.list[i].insert(3, int(time[1]))


    def get_list(self):
        """
        Carries out all methods in order to turn file contents into list
        Updates self.list
        """

        file.read_file()
        file.format_list()
        file.fix_blankspace()
        file.fix_type()
        
        return self.list


class DictHandling:
    """
    Handles turning lists of file info into dictionary and giving keys of said dictionary
    It would be possible to create an animal class and class instances for each animal, 
    but this did not simplify the code much as it still required things like 
    animal_list[i].get_sleep_time() instead of just dict[animal][3]
    """


    def __init__(self, list):
        """
        Initializes class and attributes
        Arguement: List of animal info
        """

        self.list = list
    
    
    def list_to_dict(self):
        """
        Converts list of lists with animal properties to a dictionary with key being the animals name, for information on the contents of the dict and their indexes see dict explanation file
        Return: Dictionary of animal data
        """
        
        animal_dict = {}

        for i in range(len(list)):
            animal_dict[list[i][0]] = [list[i][1], list[i][2], list[i][3], list[i][4]]

        return animal_dict 


    def get_key_list(self):
        """
        Gives list of keys in dictionary
        Return: List of dictionary keys
        """
        
        return [*animal_dict]


class AnimalChecks:
    """
    Carries out different checks for the state of the animals, always returns True or False
    """


    def __init__(self, dict, time, date):
        """
        Initializes class and attributes
        Arguments: dict: dictionary with animal data, animal: animal in question, date: date visitors will visit
        """
       
        self.dict = dict
        self.time = time
        self.date = date
        

    def animal_awake(self, animal):
        """
        Checks if animal is awake in specified time frame
        Argument: Animal in question
        Return: True if animal is awake, False if sleeping
        """

        wakeup_time = self.dict[animal][1]
        sleep_time = self.dict[animal][2]

        if wakeup_time < sleep_time:
            """
            Before midnight
            """
        
            if self.time[0] >= wakeup_time and self.time[0] <= sleep_time:
                return True
            
            elif self.time[1] >= wakeup_time and self.time[1] <= sleep_time:
                return True
            
            elif self.time[0] <= wakeup_time and self.time[1] >= sleep_time:
                return True

            else: 
                return False
        
        else:
            """
            After midnight
            """
            
            if self.time[0] >= wakeup_time or self.time[0] <= sleep_time:
                return True
            
            elif self.time[1] >= wakeup_time or self.time[1] <= sleep_time:
                return True
            
            elif self.time[0] >= wakeup_time and self.time[1] >= sleep_time:
                return True
            
            else: 
                return False

    
    def animal_not_hibernating(self, animal):
        """
        Checks if animal is hibernating during specified date
        Argument: Animal in question
        Return: True if animal not hibernating, False if animal is hibernating
        """

        hibernation_season = self.dict[animal][0]
        month = self.date[1]

        winter = [12, 1, 2]
        summer = range(6, 9)
        autumn = range(9, 12)
        spring = range(3, 6)
        
        if month in winter and hibernation_season == "winter":
            return False
        
        elif month in summer and hibernation_season == "summer":
            return False
            
        elif month in autumn and hibernation_season == "autumn":
            return False

        elif month in spring and hibernation_season == "spring":
            return False
        
        else: 
            return True
        

    def animal_feeding(self, animal):
        """
        Checks if animal will recieve food in specified time frame
        Argument: Animal in question
        Return: True if animal will recieve food during specified time frame, False if not
        """

        time = range(self.time[0], self.time[1]) 
        feeding_time = self.dict[animal][3]

        if feeding_time == "-":
            return False
        
        elif feeding_time in time: 
            return True
        
        else:
            return False


class TerminalMode:
    """
    Handles a visit at the zoo and printing out schedules 
    """


    def __init__(self, dict, animals):
        """
        Initializes class and attributes
        Arguments: dict: dictionary with animal data, animals: list of animals
        """
        
        self.dict = dict
        self.animals = animals


    def mode(self):
        """
        Handles choosing visitor or employee in terminal mode
        """

        wrong_input = True
        
        while wrong_input:
            
            answer = input("Would you like to enter visitor or employee mode? Please enter either v or e: ")
            
            try:
                answer = answer.lower()
                
                if answer == "v":
                    wrong_input = False
                    print("You have selected visitor mode")
                    TerminalMode.visitor(self)
                
                elif answer == "e":
                    wrong_input = False
                    print("You have chosen employee mode")
                    TerminalMode.employee(self)
            
            except:
                print("Please enter a correct input either v or e")

    
    def employee(self):
        """
        Handles zoo functions in the terminal for employees taking answers and creating posters 
        """
        
        wrong_input = True
        
        while wrong_input:
            
            answer = input("Would you like to create a poster for today or some other day? Enter either today or other: ")
            
            try:
                answer = answer.lower()
                
                if answer == "today":
                    wrong_input = False
                    poster.todays_poster()
                    print("Poster has been created and stored to files")
                
                elif answer == "other":
                    wrong_input = False
                    poster.poster_date()
                    print("Poster has been created and stored to files")
            
                else:
                    raise Exception
            
            except:
                print("Please enter a correct input either today or other")


    def visitor(self):
        """
        Handles a visit to the zoo and prints out what animals will be seen at the zoo during for a time and date
        """

        date = get_datetime_input_list("date", "What date would you like to visit the Stockholm zoo? Please enter the date in the format d/m using numbers ex. 6/8 ", "/")
        print("The zoo is open from 06-22")
        time = get_datetime_input_list("time", "What time would you like to enter and leave the zoo? Please enter the time using numbers and full hours, ex. 12-16 ", "-")

        if time[0] > 22 or time[0] < 6:
            print("Sorry, the zoo is closed at this time")
        
        else:
            check = AnimalChecks(self.dict, time, date) 
            print("The zoo is open")
            print("During your visit you will see:")
            
            for animal in self.animals:

                if check.animal_awake(animal) and check.animal_not_hibernating(animal) and check.animal_feeding(animal):
                    print(f"{animal} *** will be fed at {self.dict[animal][3]} ***")
                
                elif check.animal_awake(animal) and check.animal_not_hibernating(animal):
                    print(f"{animal}")
                
                else:
                    pass


class PosterCreation:
    """
    Handles creating posters with schedule for zoo
    """


    def __init__(self, dict, animals):
        """
        Initializes class and attributes
        Arguments: dict: dictionary with animal data, animals: list of animals
        """

        self.dict = dict
        self.animals = animals
    

    def todays_poster(self):
        """
        Creates a poster for todays date
        """

        today = datetime.today()
        date = today.strftime("%d/%m")
        date = date.split("/")
        
        for i in range(len(date)):
            date[i] = int(date[i])
        
        PosterCreation.create_poster(self, date)
    

    def poster_date(self):
        """
        Asks user which date they would like to create a poster for and creates poster for that date
        """

        date = get_datetime_input_list("date", "For what date would you like to create a poster? ", "/")

        PosterCreation.create_poster(self, date)
    

    def create_poster(self, date):
        """
        Creates poster for a specified date
        """
        
        date_text = str(date[0]) + "-" + str(date[1])
        
        filename = Path(f"poster_for {date_text}")
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
        f = open(filename, "w")
        
        f.write(animal_text.get_text(date))
        
        f.close


class ZooText:
    """
    Handles creating a text with all animals that can be seen for GUI
    """


    def __init__(self, dict, animals):
        """
        Initializes class and attributes
        Arguments: dict: dictionary with animal data, animals: list of animals
        """

        self.dict = dict
        self.animals = animals
    

    def get_text(self, date):
        """
        Gives text for which animals will be awake during a time
        Argument: Date to generate text for
        Return: Text of which animals will be awake and when they will be fed
        """

        date_text = str(date[0]) + "-" + str(date[1])
        
        text = (f"Welcome to the Stockholm zoo!\nAt the zoo today {date_text} you can see\n")
        check = AnimalChecks(self.dict, [0, 24], date) 
        
        for animal in self.animals:
            
            if check.animal_not_hibernating(animal):
                text += (f"{animal} *** will be fed at {self.dict[animal][3]} ***\n")
            
            else: 
                pass
        
        return text

class Click:
    """
    Handles button clicks in GUI
    """


    def __init__(self, date):
        """
        Initializes class and attributes
        Argument: Starting date for GUI
        """

        self.date = date
    

    def clicked_positive(self):
        """
        Changes text for moving 1 day forward in schedule
        """

        click.get_next_date_positive()
        
        lbl.configure(text = animal_text.get_text(self.date))
    

    def clicked_negative(self):
        """
        Changes text for moving 1 day backwards in schedule
        """

        click.get_next_date_negative()

        lbl.configure(text = animal_text.get_text(self.date))
    

    def get_next_date_positive(self):
        """
        Decides next date efter present date, handles overflow into next year
        Changes attribute date
        """

        day = self.date[0]
        month = self.date[1]
        days_in_month = monthrange(2021, month) # gives format [0, 30] for 30 days
        date_list = []
        
        if day in range(1, days_in_month[1]):
            day = day + 1
            date_list.append(day)
            date_list.append(month)
        
        else:
            
            if month == 12:
                month = 1
                day = 1
                date_list.append(day)
                date_list.append(month)
            
            else:
                month = month + 1
                day = 1
                date_list.append(day)
                date_list.append(month)
        
        self.date = date_list
    

    def get_next_date_negative(self):
        """
        Decides date before present date, handles overflow into last year
        Changes attribute date
        """

        day = self.date[0]
        month = self.date[1]
        days_in_month = monthrange(2021, month) # gives format [0, 30] for 30 days
        date_list = []
        
        if day in range(2, days_in_month[1] + 1):
            day = day - 1
            date_list.append(day)
            date_list.append(month)

        else:
            
            if month == 1:
                month = 12
                day = 31
                date_list.append(day)
                date_list.append(month)
            
            else:
                month = month -1
                day = monthrange(2021, month)[1]
                date_list.append(day)
                date_list.append(month)
        
        self.date = date_list
    

    def show_date_entry(self):
        """
        Changes text to show schedule for specific input date
        Changes attribute date
        """

        date_entered = entry.get()
        
        if date_entered == "execute order 66":
            tkinter.messagebox.showerror(title="Order 66", message="It will be done my lord!")
            window.destroy()
        
        else:
            try:
                date_entered = date_entered.split("/")
                date_entered = check_correct_datetime_format("date", date_entered)
                    
                lbl.configure(text = animal_text.get_text(date_entered))
                self.date = date_entered
            
            except:
                tkinter.messagebox.showerror(title="Invalid entry", message="You must enter your date using positive numbers in the format day/month, ex 6/7")


    def gui_poster(self):
        """
        Handles creating poster from GUI
        """

        poster.create_poster(self.date)
        tkinter.messagebox.showinfo(title="Info", message="Poster has been created and stored to files")
    
    
    def kth_popup(self):
        """
        Creates fun popup about the KTH student
        """

        tkinter.messagebox.showinfo(title="Info", message="The KTH student is a curious animal, it spends most of its time staring at a device referred to as a computer, and swearing at math problems or code errors usually made due to it's own stupidity. Due to early morning lessons and a characteristically bad sleep schedule, the student often has to rely on caffeine to stay awake. Due to this, KTH students have adapted to survive high doses of caffeine that would be considered lethal to most ordinary humans. They are easily agitated, so approach with caution.")


def get_datetime_input_list(format, question, delimiter):
    """
    Takes input from user for certain frames of time, handles wrong inputs
    Arguments: 
    format: if function should shoudl get input in a date or time format
    question: The question for the user to answer 
    delimiter: Where to split answer, for example 6-18 should be split at "-"
    Return: List with answer split
    """


    incorrect_input = True

    while incorrect_input:
            
        try:

            answer = input(question)
            answer = answer.split(delimiter)
            answer = check_correct_datetime_format(format, answer)
            incorrect_input = False
            
        except:
            print("Your input is incorrect, please try again")
            
    return answer

def check_correct_datetime_format(format, raw_input):
    """
    Checks if input is correct with no illegal numbers for example month 13 or day 32, raises exceptions if wrong input is encountered
    Arguments: format: if function should check for correct date or time format, raw_input: input to check for correct format
    Return: Input in correct format
    """
    
    
    if format == "date":
        if len(raw_input) != 2:
            raise Exception
        
        else:
            
            for i in range(2):
                raw_input[i] = int(raw_input[i])
                
                if raw_input[i] < 1:
                    raise Exception
                
                else:
                    pass
        
        days_in_month = monthrange(2021, raw_input[1]) # gives format [0, 30] for 30 days
        date_list = []
         
        if raw_input[1] > 12:
            raise Exception

        elif raw_input[0] not in range(1, days_in_month[1]+1):
            raise Exception

        else:
            return raw_input 
    
    elif format == "time":
        
        if len(raw_input) != 2:
            raise Exception
        
        else:
            
            for i in range(2):
                raw_input[i] = int(raw_input[i])
                
                if raw_input[i] < 1 or raw_input[i] > 24:
                    raise Exception
                
                else:
                    pass
            
            return raw_input


def get_date():
    """
    Gets current date
    Return: Current date in useable form [day, month]
    """

    today = datetime.today()
    date = today.strftime("%d/%m")
    date = date.split("/")
    
    for i in range(len(date)):
        date[i] = int(date[i])
    
    return date

if __name__ == '__main__':
    """
    Global variables were used for GUI functions
    """
 
    if GUI:
        file = FileHandling('zoo_animals.txt', "/")
        list = file.get_list()

        dict = DictHandling(list)
        animal_dict = dict.list_to_dict()
        animals = dict.get_key_list()

        poster = PosterCreation(animal_dict, animals)
        animal_text = ZooText(animal_dict, animals)

        window = Tk()
        window.title("Zoo calender")
        lbl = Label(window, text = animal_text.get_text(get_date()))
        lbl.grid(column=1, row=0)
        window.geometry('600x600')

        click = Click(get_date())

        btn = button(window, text="Next day", bg="blue", fg="white", command=click.clicked_positive)
        btn2 = button(window, text="Previous day", bg="blue", fg="white", command=click.clicked_negative)
        btn3 = button(window, text="Show schedule for date", bg="blue", fg="white", command=click.show_date_entry)
        btn4 = button(window, text="See information about our newest animal, the KTH student", bg="blue", fg="white", command=click.kth_popup)
        btn5 = button(window, text="Create poster for this day", bg="blue", fg="white", command=click.gui_poster)

        btn.grid(column=2, row=0)
        btn2.grid(column=0, row=0)
        btn3.grid(column=1, row=2)
        btn4.grid(column=1, row=4)
        btn5.grid(column=1, row=3)

        entry = Entry(window)
        entry.grid(column=1, row=1)

        canv = Canvas(window, width=313, height=313, bg='white')
        canv.grid(row=5, column=1)

        img = PhotoImage(file="welcome-the-the-zoo-background.gif")
        img = img.subsample(2)
        canv.create_image(313/2,313/2, image=img)

        window.mainloop()
        
    else:
        file = FileHandling('zoo_animals.txt', "/")
        list = file.get_list()

        dict = DictHandling(list)
        animal_dict = dict.list_to_dict()
        animals = dict.get_key_list()
        
        poster = PosterCreation(animal_dict, animals)
        animal_text = ZooText(animal_dict, animals)

        terminal = TerminalMode(animal_dict, animals)
        terminal.mode()
