from colorama import Fore, Back
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
from colorama import init
import unicodedata
import re

# Spacing for strings
spacing = '                                                                                ' + Back.RESET + Fore.RESET

# SCRIPT NOTES
logo = Fore.RED + '                    ..     \n' + \
       Fore.RED + '                 .::.      ' + Fore.RESET + '___   ___   ___   ___   ___ \n' + \
       Fore.RED + '               .:::.       ' + Fore.RESET + '  /  |       | |   |   |    \n' + \
       Fore.RED + '             .::::         ' + Fore.RESET + ' +    -+-    + |   +    -+- \n' + \
       Fore.RED + '               .:::.       ' + Fore.RESET + '/        |   | |   |       |\n' + \
       Fore.RED + '              .:::.        ' + Fore.RESET + '---   ---   ---   ---   --- \n' + \
       Fore.RED + '            .::.     \n' + \
       Fore.RED + '           .:          ' + Fore.RESET + '                   Marian Bodnar\n\n'

title = Back.WHITE + Fore.BLACK + \
        '>> PYTHON SCRIPT 1.0- Konverzia SAP.txt dat do .csv'
title = title + spacing[len(title):] + '\n\n'

note = Back.YELLOW + Fore.BLACK + 'UPOZORNENIE !' + Back.RESET + Fore.RESET + \
       '\n1. TXT subor sa musi nachadzat v priecinku so scriptom.' + \
       '\n2. Prvy stlpec v tabulke musi obsahovat cisla (INTEGER).' + \
       '\n3. Riadok pre popis pocitat od 1.' + \
       '\n4. Podporovane kodovanie: ' + Back.YELLOW + Fore.BLACK + 'ANSI' + Back.RESET + Fore.RESET + \
       '\n5. Znak oddelovaca nachadzajuci sa v datach bude zameneny za medzeru.' + \
       '\n6. Popis stlpcov bude modifikovany pre podporu -SQLite import csv-\n\n'

user = Back.WHITE + Fore.BLACK + \
       '>> VSTUPNE DATA'
user = user + spacing[len(user):]

working = Back.WHITE + Fore.BLACK + \
          '>> SPRACOVANIE'
working = working + spacing[len(working):]

escape = Back.YELLOW + Fore.BLACK + '>> PRESS ANY KEY FOR ESCAPE...'
escape = escape + spacing[len(escape):]

# Input values
input_file_name = ''
output_file_name = ''
description_line = 0
separator = ','
# DATA
cleaned_file = []


# Remove diacritics
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


# Clean up DATA
def clean_up(file_name):
    global cleaned_file
    record_counter = 0

    print('>> READING DATA:', end='')
    try:
        ff = open(file_name, mode="r", encoding='ANSI')
        lines = ff.readlines()
        # records = int(len(lines) / 10)
        # sandokan = records

        for line in lines:
            # Catch description line
            if record_counter == description_line:
                # Cut First character
                line = line[1:]
                # Cut Last 2 characters
                line = line[:-2]
                # Replace all characters like separator
                line = line.replace(separator, ' ')
                #  Split line
                tmp_line = line.split('|')
                line = ''
                for word in tmp_line:
                    # Remove diacritics
                    word = strip_accents(word)
                    # Remove not allowed Characters
                    cut_word = re.findall(r"[\w']+", word)
                    # Capitalize first character and add
                    word = ''
                    for text in cut_word:
                        text = text[0].upper() + text[1:]
                        word = word + text
                    # Add words to one line with separator
                    line = line + word + separator
                # Append to description to the list
                cleaned_file.append(line[:-1] + '\n')
            record_counter += 1

            # if records == record_counter:
            #     print(Back.WHITE + ' ' + Back.RESET, end='')
            #     records += sandokan

            if line[0] != '|' or ord(line[3]) < 47 or ord(line[3]) > 58:
                continue
            else:
                # remove characters
                line = line.replace(separator, ' ')
                # Cut first character
                line = line[1:]
                # Cut last 2 characters
                line = line[:-2]
                # Split line
                tmp_line = line.split('|')
                # Remove whitespaces
                line = ''
                for word in tmp_line:
                    word = word.strip()
                    line = line + word + separator
                # Append line to data
                cleaned_file.append(line[:-1] + '\n')
        ff.close()
    except:
        print('\t\t\t\t' + Back.RED + Fore.BLACK + 'FAILED    ' + Fore.RESET + Back.RESET)
        return False
    else:
        print('\t\t\t\t' + Back.GREEN + Fore.BLACK + 'PASSED    ' + Fore.RESET + Back.RESET)
        print('>> ALL RECORDS: ' + '\t\t\t\t' + str(record_counter))
        print('>> CLEAN RECORDS: ' + '\t\t\t\t' + str(len(cleaned_file)))
        return True


# Write raw data to the new file
def write_csv(cleaned_data):
    print('>> WRITING DATA:', end='')
    try:
        w_csv = open(output_file_name + '.csv', 'a', encoding='ANSI')
        for line in cleaned_data:
            w_csv.write(line)
        w_csv.close()
    except:
        print('\t\t\t\t' + Back.RED + Fore.BLACK + 'FAILED    ' + Fore.RESET + Back.RESET)
        return False
    else:
        print('\t\t\t\t' + Back.GREEN + Fore.BLACK + 'PASSED    ' + Fore.RESET + Back.RESET)
        return True


if __name__ == '__main__':
    # Rape windows console with colors
    init()

    # Print Console
    print(logo)
    print(title)
    print(note)
    print(user)

    # USER input
    input_file_name = input('>> VSTUP - NAZOV SUBORU + .txt:  ')
    if input_file_name.find('.txt') != -1:
        description_line = input('>> CISLO RIADKU PRE POPIS:  ')
        if len(description_line) == 1 and 48 <= ord(description_line) <= 57:
            description_line = int(int(description_line) - 1)
            output_file_name = input('>> VYSTUP - NAZOV SUBORU:  ')
            separator = input('>> ZNAK ODDELOVACA:  ')
            # RUN SCRIPT
            print(working)
            if clean_up(input_file_name):
                pass
                if write_csv(cleaned_file):

                    nothing = input(escape)
                else:
                    nothing = input(escape)
            else:
                nothing = input(escape)
        else:
            print(Fore.RED + '>> CHYBA !' + Fore.RESET + '  Nespravne zadane cislo riadku 0-9.')
            nothing = input(escape)
    else:
        print(Fore.RED + '>> CHYBA !' + Fore.RESET + '  Nespravne zadany vstupny subor.')
        nothing = input(escape)
