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

def visit_planner(list):
    date = input("What date would you like to visit the Stockholm zoo? ")
    print("The zoo is open from 06-22")
    time = int(input("What time would you like to enter and leave the zoo? "))

    if time > 22 or time < 6:
       print("Sorry, the zoo is closed at this time")
    
    else: 
        print("The zoo is open")

animals_list = read_file('zoo_animals.txt')
animals_list = format_list(animals_list)
animals_list = fix_whitespace(animals_list)
animals_list = fix_type(animals_list)
print(animals_list)
visit_planner(animals_list)

