""" 
A program to guide zoo visitors

Written by Elliot Stjernqvist

"""

from os import read
from pathlib import Path
from datetime import date, datetime
from tkinter import *
from tkmacosx import Button as button
from calendar import monthrange
from functools import partial


class file_handling:

    def __init__(self, file_name, delimiter):
        self.file_name = file_name
        self.delimiter = delimiter

    def read_file(self):
        """
        Reads file and removes first line which only displays the format.
        Argument: the file to be read
        Return: list of contents in file
        """

        list = []

        file1 = open(self.file_name, 'r')
        
        lines = file1.readlines()
        for line in lines: 
            list.append(line.strip())
        list.pop(0)
        
        return list
        

    def format_list(self, list):
        """
        Formats list by splitting it into multiple lists one for each animal
        Arguments: list to be formated and delimiter to split list by
        Return: Formated list of lists
        """

        split_list = []
        for i in range(len(list)):
            split_list.append((list[i].split(self.delimiter)))
        return split_list


    def fix_blankspace(self, list):
        """
        Removes the blankspace around every object in the list
        Argument: List to be fixed
        Return: Fixed list
        """
        
        for i in range(len(list)):
            for j in range(len(list[i])):
                list[i][j] = list[i][j].strip()
        
        return list


    def fix_type(self, list):
        """
        Converts all objects to the correct types and splits up objects representing a space of time for example 13-16
        Argument: List to be fixed
        Return: Fixed list
        """
        
        for i in range(len(list)):
            list[i][3] = int(list[i][3])
            time = list[i][2].split("-")
            list[i].pop(2)
            
            list[i].insert(2, int(time[0]))
            list[i].insert(3, int(time[1]))
        
        return list

    def get_list(self):
        self.animals_list = file.read_file()
        self.animals_list = file.format_list(self.animals_list)
        self.animals_list = file.fix_blankspace(self.animals_list)
        self.animals_list = file.fix_type(self.animals_list)
        
        return self.animals_list


class dict_handling:

    def __init__(self, list):
        self.list = list
    
    
    def list_to_dict(self):
        """
        Converts list of lists with animal properties to a dictionary with key being the animals name
        Argument: List to be converted
        Return: Dictionary of animal data
        """
        
        animal_dict = {}

        for i in range(len(list)):
            animal_dict[list[i][0]] = [list[i][1], list[i][2], list[i][3], list[i][4]]

        return animal_dict 

    def get_key_list(self):
        """Gives list of keys in dictionary
        Argument: dict: Dictionary to find keys in
        Return: List of dictionary keys
        """
        
        return [*animal_dict]


class animal_checks:

    def __init__(self, dict, time, date):
        self.dict = dict
        self.time = time
        self.date = date
        

    def animal_awake(self, animal):
        """
        Checks if animal is awake in specified time frame
        Arguments: dict: dictionary with animal data, animal: animal in question, time: time frame visitors will visit in
        Return: True if animal is awake, False if sleeping
        """

        wakeup_time = self.dict[animal][1]
        sleep_time = self.dict[animal][2]

        if wakeup_time < sleep_time:
        
            if self.time[0] >= wakeup_time and self.time[0] <= sleep_time:
                return True
            
            elif self.time[1] >= wakeup_time and self.time[1] <= sleep_time:
                return True
            
            elif self.time[0] <= wakeup_time and self.time[1] >= sleep_time:
                return True

            else: 
                return False
        
        else:
            #After midnight
            
            if self.time[0] >= wakeup_time or self.time[0] <= sleep_time:
                return True
            
            elif self.time[1] >= wakeup_time or self.time[1] <= sleep_time:
                return True
            
            elif self.time[0] >= wakeup_time and self.time[1] >= sleep_time:
                return True
            
            else: 
                return False

    
    def animal_not_hibernating(self, animal):
        """Checks if animal is hibernating during specified date
        Arguments: dict: dictionary with animal data, animal: animal in question, date: date visitors will visit
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
        """Checks if animal will recieve food in specified time frame
        Arguments: dict: dictionary with animal data, animal: animal in question, time: time frame visitors will visit in
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



def get_input_list(question, delimiter):
    """
    Takes input from user for certain frames of time, handles wrong inputs
    Arguments: question: The question for the user to answer, delimiter: Where to split answer, for example 6-18 should be split at -
    Return: List with answer split
    """

    incorrect_input = True

    while incorrect_input:
            
        try:

            answer = input(question)
            answer = answer.split(delimiter)
                
            for i in range(2):
                answer[i] = int(answer[i])

            if answer[0] <= 0 or answer[1] <= 0: 
                print("Your input is incorrect, please try again")
                
            else: 
                incorrect_input = False
            
        except:
            print("Your input is incorrect, please try again")
            
    return answer


class visit_planner:

    def __init__(self, dict, animals):
        self.dict = dict
        self.animals = animals
        
    
    def visit(self):
        date = get_input_list("What date would you like to visit the Stockholm zoo? Please enter the date in the format d/m using numbers ex. 6/8 ", "/")
        print("The zoo is open from 06-22")
        time = get_input_list("What time would you like to enter and leave the zoo? Please enter the time using numbers and full hours, ex. 12-16 ", "-")

        if time[0] > 22 or time[0] < 6:
            print("Sorry, the zoo is closed at this time")
        
        else:
            check = animal_checks(self.dict, time, date) 
            print("The zoo is open")
            print("During your visit you will see:")
            for animal in self.animals:
                if check.animal_awake(animal) and check.animal_not_hibernating(animal) and check.animal_feeding(animal):
                    print(f"{animal} *** will be fed at {self.dict[animal][3]} ***")
                elif check.animal_awake(animal) and check.animal_not_hibernating(animal):
                    print(f"{animal}")
                else:
                    pass

class poster_creation:

    def __init__(self, dict, animals):
        self.dict = dict
        self.animals = animals
    
    def todays_poster(self):

        today = datetime.today()
        # dd/mm/YY
        date = today.strftime("%d/%m")
        date = date.split("/")
        for i in range(len(date)):
            date[i] = int(date[i])
        poster_creation.create_poster(self, date)
    
    def poster_date(self):
        date = get_input_list("For what date would you like to create a poster? ", "/")

        poster_creation.create_poster(self, date)
    
    def create_poster(self, date):
        

        date_text = str(date[0]) + "-" + str(date[1])
        
        filename = Path(f"poster_for {date_text}")
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
        f = open(filename, "w")
        
        f.write(f"Welcome to the Stockholm zoo!\nAt the zoo today {date_text} you can see\n")
        check = animal_checks(self.dict, [0, 24], date) 
        for animal in self.animals:
            if check.animal_not_hibernating(animal):
                f.write(f"{animal} *** will be fed at {self.dict[animal][3]} ***\n")
            else: 
                pass
        
        f.close

class zoo_text:
    def __init__(self, dict, animals):
        self.dict = dict
        self.animals = animals
    
    def get_text(self, date):
        

        date_text = str(date[0]) + "-" + str(date[1])
        
        text = (f"Welcome to the Stockholm zoo!\nAt the zoo today {date_text} you can see\n")
        check = animal_checks(self.dict, [0, 24], date) 
        for animal in self.animals:
            if check.animal_not_hibernating(animal):
                text += (f"{animal} *** will be fed at {self.dict[animal][3]} ***\n")
            else: 
                pass
        
        return text

class click:
    def __init__(self, date):
        self.date = date
        print(date)
    
    def clicked(self):
        date = click.get_next_date()
        print(self.date)
        lbl.configure(text = text1.get_text(self.date))
    
    def get_next_date(self):
        day = self.date[0]
        month = self.date[1]
        days_in_month = monthrange(2021, month) # gives format [0, 30] for 30 days
        date_list = []
        date_list.append(day + 1)
        date_list.append(month)
        """
        if day in range(days_in_month[0], days_in_month[1]):
            date_list.append(day + 1)
            date_list.append(month)
        else:
            date_list.append(1)
            date_list.append(month + 1)
        """
        self.date = date_list

file = file_handling('zoo_animals.txt', "/")
list = file.get_list()
#print(file.get_list())

dict = dict_handling(list)
animal_dict = dict.list_to_dict()
#print(animal_dict)
animals = dict.get_key_list()

visit = visit_planner(animal_dict, animals)
#visit.visit()

poster = poster_creation(animal_dict, animals)
text1 = zoo_text(animal_dict, animals)
#poster.poster_date()
#poster.todays_poster()

today = datetime.today()
date = today.strftime("%d/%m")
date = date.split("/")
for i in range(len(date)):
    date[i] = int(date[i])

window = Tk()
window.title("Zoo calender")
lbl = Label(window, text = text1.get_text(date))
lbl.grid(column=0, row=0)
window.geometry('800x600')
click = click(date)
btn = button(window, text="Click Me", bg="blue", fg="white", command=click.clicked)
btn.grid(column=1, row=0)

window.mainloop()

