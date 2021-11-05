""" 
A program to guide zoo visitors

Written by Elliot Stjernqvist

"""


from os import read


def read_file(file):
    animals_list = []
    file1 = open(file, 'r')
    lines = file1.readlines()
    for line in lines: 
        animals_list.append(line.strip())
    animals_list.pop(0)
    return animals_list
    

def format_list(list):
    split_list = []
    for i in range(len(list)):
        split_list.append((list[i].split("/")))
    return split_list


def fix_whitespace(list):
    for i in range(len(list)):
        for j in range(len(list[i])):
            list[i][j] = list[i][j].strip()
    return list


def fix_type(list):
    for i in range(len(list)):
        list[i][3] = int(list[i][3])
        time = list[i][2].split("-")
        list[i].pop(2)
        list[i].insert(2, int(time[0]))
        list[i].insert(3, int(time[1]))
    return list


def list_to_dict(list):
    animal_dict = {}
    for i in range(len(list)):
        animal_dict[list[i][0]] = [list[i][1], list[i][2], list[i][3], list[i][4]]

    return animal_dict 


def animal_awake(dict, animal, time):

    wakeup_time = dict[animal][1]
    sleep_time = dict[animal][2]
    if wakeup_time < sleep_time:
        if time[0] >= wakeup_time and time[0] <= sleep_time:
            return True
        elif time[1] >= wakeup_time and time[1] <= sleep_time:
            return True
        else: 
            return False
    
    else:
        #After midnight
        if time[0] >= wakeup_time or time[0] <= sleep_time:
            return True
        elif time[1] >= wakeup_time or time[1] <= sleep_time:
            return True
        else: 
            return False


def animal_not_hibernating(dict, animal, date):
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
    time = range(time[0], time[1]) 
    feeding_time = dict[animal][3]
    if feeding_time == "-":
        return False
    elif feeding_time in time: 
        return True


def get_list(dict):
      
    return [*dict]


def visit_planner(dict):
    date = input("What date would you like to visit the Stockholm zoo? ")
    print("The zoo is open from 06-22")
    time = input("What time would you like to enter and leave the zoo? ")
    time = time.split("-")
    time[0] = int(time[0])
    time[1] = int(time[1])
    print(time)

    date = date.split("/")
    date[0] = int(date[0])
    date[1] = int(date[1])

    if time[0] > 22 or time[0] < 6:
       print("Sorry, the zoo is closed at this time")
    
    else: 
        print("The zoo is open")
        print("During your visit you will see:")
        animals = get_list(dict)
        for animal in animals:
            if animal_awake(dict, animal, time) and animal_not_hibernating(dict, animal, date) and animal_feeding(dict, animal, time):
                print(f"{animal} *** will be fed at {dict[animal][3]} ***")
            elif animal_awake(dict, animal, time) and animal_not_hibernating(dict, animal, date):
                print(f"{animal}")
            else:
                pass



animals_list = read_file('zoo_animals.txt')
animals_list = format_list(animals_list)
animals_list = fix_whitespace(animals_list)
animals_list = fix_type(animals_list)
animal_dict = list_to_dict(animals_list)
print(animal_dict)
visit_planner(animal_dict)


