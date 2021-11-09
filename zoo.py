""" 
A program to guide zoo visitors

Written by Elliot Stjernqvist

"""

from os import read
from pathlib import Path

class file_handling:


    def read_file(file):
        """
        Reads file and removes first line which only displays the format.
        Argument: the file to be read
        Return: list of contents in file
        """

        list = []

        file1 = open(file, 'r')
        
        lines = file1.readlines()
        for line in lines: 
            list.append(line.strip())
        list.pop(0)
        
        return list
        

    def format_list(list, delimiter):
        """
        Formats list by splitting it into multiple lists one for each animal
        Arguments: list to be formated and delimiter to split list by
        Return: Formated list of lists
        """

        split_list = []
        for i in range(len(list)):
            split_list.append((list[i].split(delimiter)))
        
        return split_list


    def fix_blankspace(list):
        """
        Removes the blankspace around every object in the list
        Argument: List to be fixed
        Return: Fixed list
        """
        
        for i in range(len(list)):
            for j in range(len(list[i])):
                list[i][j] = list[i][j].strip()
        
        return list


    def fix_type(list):
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


class dict_handling:
    
    
    def list_to_dict(list):
        """
        Converts list of lists with animal properties to a dictionary with key being the animals name
        Argument: List to be converted
        Return: Dictionary of animal data
        """
        
        animal_dict = {}

        for i in range(len(list)):
            animal_dict[list[i][0]] = [list[i][1], list[i][2], list[i][3], list[i][4]]

        return animal_dict 

    def get_key_list(dict):
        """Gives list of keys in dictionary
        Argument: dict: Dictionary to find keys in
        Return: List of dictionary keys
        """
        
        return [*dict]


class animal_checks:

    def animal_awake(dict, animal, time):
        """
        Checks if animal is awake in specified time frame
        Arguments: dict: dictionary with animal data, animal: animal in question, time: time frame visitors will visit in
        Return: True if animal is awake, False if sleeping
        """

        wakeup_time = dict[animal][1]
        sleep_time = dict[animal][2]

        if wakeup_time < sleep_time:
        
            if time[0] >= wakeup_time and time[0] <= sleep_time:
                return True
            
            elif time[1] >= wakeup_time and time[1] <= sleep_time:
                return True
            
            elif time[0] <= wakeup_time and time[1] >= sleep_time:
                return True

            else: 
                return False
        
        else:
            #After midnight
            
            if time[0] >= wakeup_time or time[0] <= sleep_time:
                return True
            
            elif time[1] >= wakeup_time or time[1] <= sleep_time:
                return True
            
            elif time[0] >= wakeup_time and time[1] >= sleep_time:
                return True
            
            else: 
                return False

    
    def animal_not_hibernating(dict, animal, date):
        """Checks if animal is hibernating during specified date
        Arguments: dict: dictionary with animal data, animal: animal in question, date: date visitors will visit
        Return: True if animal not hibernating, False if animal is hibernating
        """

        hibernation_season = dict[animal][0]
        month = date[1]

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
        

    def animal_feeding(dict, animal, time):
        """Checks if animal will recieve food in specified time frame
        Arguments: dict: dictionary with animal data, animal: animal in question, time: time frame visitors will visit in
        Return: True if animal will recieve food during specified time frame, False if not
        """
        time = range(time[0], time[1]) 
        feeding_time = dict[animal][3]
        if feeding_time == "-":
            return False
        elif feeding_time in time: 
            return True
        else:
            return False


class inputs:
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

def visit_planner(dict):
    date = inputs.get_input_list("What date would you like to visit the Stockholm zoo? Please enter the date in the format d/m using numbers ex. 6/8 ", "/")
    print("The zoo is open from 06-22")
    time = inputs.get_input_list("What time would you like to enter and leave the zoo? Please enter the time using numbers and full hours, ex. 12-16 ", "-")

    if time[0] > 22 or time[0] < 6:
       print("Sorry, the zoo is closed at this time")
    
    else: 
        print("The zoo is open")
        print("During your visit you will see:")
        animals = dict_handling.get_key_list(dict)
        for animal in animals:
            if animal_checks.animal_awake(dict, animal, time) and animal_checks.animal_not_hibernating(dict, animal, date) and animal_checks.animal_feeding(dict, animal, time):
                print(f"{animal} *** will be fed at {dict[animal][3]} ***")
            elif animal_checks.animal_awake(dict, animal, time) and animal_checks.animal_not_hibernating(dict, animal, date):
                print(f"{animal}")
            else:
                pass

class poster:
    
    
    def create_poster(date, dict):
        
        
        date = date.split("/")
        for i in range(2):
            date[i] = int(date[i])
        date_text = str(date[0]) + "-" + str(date[1])
        
        filename = Path(f"poster_for {date_text}")
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
        f = open(filename, "w")
        
        f.write(f"Welcome to the Stockholm zoo!\nAt the zoo today {date_text} you can see\n")
        animals = dict_handling.get_key_list(dict)
        
        for animal in animals:
            if animal_checks.animal_not_hibernating(dict, animal, date):
                f.write(f"{animal} *** will be fed at {dict[animal][3]} ***\n")
            else: 
                pass
        
        f.close

animals_list = file_handling.read_file('zoo_animals.txt')
animals_list = file_handling.format_list(animals_list, "/")
animals_list = file_handling.fix_blankspace(animals_list)
animals_list = file_handling.fix_type(animals_list)
print(animals_list)
animal_dict = dict_handling.list_to_dict(animals_list)
print(animal_dict)
#visit_planner(animal_dict)
poster.create_poster("6/8", animal_dict)


