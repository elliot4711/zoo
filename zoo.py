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






animals_list = read_file('zoo_animals.txt')
print(format_list(animals_list))

 