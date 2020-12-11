import csv
import sys
import argparse

'''
The list of dictionaries is chosen for storing data because this structure
 is easy to operate and write back to csv
'''


def read_csv(path):
    people = []
    if path.endswith('.csv'):  # check file type
        with open(path, encoding='utf-8', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                people.append(row)
            return people
    else:
        print('ERROR: You try to open not .csv file!')
        sys.exit()


'''
This format of printing person's data is chosen for its easy readability
'''


def print_person(dictionary):
    print('Name and Surname: ' + dictionary.get('Name') + ' ' + dictionary.get('Surname') +
          '\nAge: ' + dictionary.get('Age') + '\n' + 'Job: ' + dictionary.get('Job') + '\n')


def print_people(people):
    for person in people:
        print_person(person)


def print_specialists(people, job):
    print('All {0}s:\n'.format(job))
    isPrinted = False  # flag which shows if at least one person was printed
    for person in people:
        if person.get('Job') == job:
            print_person(person)
            isPrinted = True
    if isPrinted == False:
        print('There is no people with such job')


def print_middleAged(people):
    print('All people between 22 and 50 y.o.:\n')
    for person in people:
        # cast to int to avoid mistyping
        if int(person.get('Age')) < 50 and int(person.get('Age')) > 22:
            print_person(person)


def delete_nonWorkers(people):
    for person in people:
        if person.get('Job') == 'none':
            people.remove(person)
    print('All people without job removed')
    return people


def write_to_csv(people, path):
    with open(path, 'w') as csv_file:
        fieldnames = ['Name', 'Surname', 'Age', 'Job']
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, delimiter=';')
        csv_writer.writeheader()
        for person in people:
            csv_writer.writerow(person)


'''
Add some command line arguments to use functionality
'''

parser = argparse.ArgumentParser(description='CSV visualizer')

parser.add_argument('input', type=str, help='input file path')

parser.add_argument('--all', type=bool, default=False,
                    help='make this arg True to print all people in file')

parser.add_argument('--job', type=str, default='default',
                    help='type the job name in this arg to print all people with written job')

parser.add_argument('--age', type=bool, default=False,
                    help='make this arg True to print all people, who are older than 22 and youngr than 50 years old')

parser.add_argument('--remove', type=bool,
                    help='make this arg True to remove all people with no job set and save editted file directory')

'''
Main flow
'''
try:
    args = parser.parse_args()
except:
    print('ERROR: Something went wrong in arguments. Please check input or use -h to recive help.')
    sys.exit()

try:
    people = read_csv(args.input)
except:
    print('ERROR: File not found! Please, check input.')
    sys.exit()

'''
Check input arguments
'''
if args.all == True:
    print_people(people)

if args.job != 'default':
    print_specialists(people, args.job)

if args.age == True:
    print_middleAged(people)

if args.remove == True:
    delete_nonWorkers(people)
    print('Type the path and name of the new file (with .csv at the end).\n>>> ', end='')
    try:
        path = input()
        write_to_csv(people, path)
        print('Done')
    except:
        print('ERROR: Sometting went wrong during the file writing! Please check the path of output file or OS permissions')
        sys.exit()
