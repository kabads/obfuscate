import csv
import random
import argparse
import re
import time

LOWER_VOWEL_LIST = ['a', 'e', 'i', 'o', 'u']
UPPER_VOWEL_LIST = ['A', 'E', 'I', 'O', 'U']
LOWER_CONSONANT_LIST = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y',
                        'z']
UPPER_CONSONANT_LIST = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y',
                        'Z']
DIGIT_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

HEADER=["ACCOUNT","NAME","ADDRESS(1)", "ADDRESS(2)", "ADDRESS(3)", "ADDRESS(4)", "POSTCODE", "COUNTRY",
        "EMAIL", "PHONE(1)", "HOSTAC", "INVACC", "STATACC", "BRANCH", "BRAND", "REGISTRATION",
        "ownership"]


def obfuscate_number(number):
    new_number = ''
    for i in number:
        if i != ' ':
            tmp = random.randint(0, 9)
            new_number = new_number + str(tmp)
        else:
            new_number = new_number + ' '
    return new_number


def obfuscate(string):
    new_string = ''
    for i in string:
        if i in LOWER_VOWEL_LIST:
            i = random.choice(LOWER_VOWEL_LIST)
        elif i in UPPER_VOWEL_LIST:
            i = random.choice(UPPER_VOWEL_LIST)
        elif i in LOWER_CONSONANT_LIST:
            i = random.choice(LOWER_CONSONANT_LIST)
        elif i in UPPER_CONSONANT_LIST:
            i = random.choice(UPPER_CONSONANT_LIST)
        elif i in DIGIT_LIST:
            i = random.choice(DIGIT_LIST)
        new_string = new_string + i
    return new_string


def read_file(file, columns, outfilename=None):
    # Prepare the output file:
    outfilename = ""
    print(outfilename)
    if outfilename == "":
        outfilename = file.name + str("-bak.csv")

    # Outfile is going to be where we write the file to.
    outfile = (open(str(outfilename), "w"))
    csv_writer = csv.writer(outfile, delimiter=',', lineterminator='\n')

    # Open the file to obfuscate
    with open(str(file.name), newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        # Next just moves it on one row (to take out the header row)

        rowcount = 0  # keep a count of which row we are on
        # Iterate over the rows  in the csv file
        for row in csv_reader:
            # Iterate through all the columns, but if a column matches something in columns,
            # then it should be obfuscated
            newrow = [] # an array to hold our new row as we read the columns.
            if rowcount != 0: # if this is zero, then we are at the header
                # Iterate over the columns in the row keeping columncount as a counter
                columncount = 0
                for column in row:
                    newcell = "" # This will hold the contents of the new cell
                    if str(columncount) in columns: # Check if this is one of the files that needs obfuscaton:
                        for i in (column): # Loop through each character and change it
                            i = obfuscate(i) # This is the character being passed to obfuscate and returned
                            newcell = newcell + i # Collect all the random characters in newcell:

                        newrow.append(newcell) # Append the newcell to the new row
                    else:  # This column is not obfuscated
                        newrow.append(column) # Append the newcell to the new row
                    columncount = columncount + 1
            # If the cell doesn't need obfuscating, then just carry on
            else:
                # This must be the header as this is row 0, so lets add it to the new outfile:
                csv_writer.writerow(row)

            # OK - now we will increase our rowcount by one.
            rowcount = rowcount + 1
            # And write the newrow to the file:
            csv_writer.writerow(newrow)
    # We've finished all the files - so close the file:
    outfile.close()


def open_file(filename):
    file = open(filename)
    return file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", required=True, help="Which file do you want to read in?", dest="infile")
    parser.add_argument("-o", "--outfile", help="Which file do you want to write out to?")
    parser.add_argument("-r", "--rows", required=True, help="Which rows do you want to be obfuscated (in ascending"
                                                            " order)?", dest="rows", nargs='+')
    args = parser.parse_args()

    file = open_file(args.infile)
    # print("Args: ", args.infile)
    # print("file opened successfully.")
    read_file(file, args.rows, args.outfile)
    file.close()


if __name__ == '__main__':
    main()
