import sys
import os
import re 


# regex constants
CAMEL_REGEX = '\\b[a-z]+[A-Z][a-zA-Z]*\\b'
PASCAL_REGEX ='\\b[A-Z][a-zA-Z]*\\b'
SNAKE_REGEX = '\\b[a-z]+_[a-z_]+\\b'

# takes a camelCase or PascalCase string, and returns all of its component words, for example myVar and MyVar would both return ['my', 'var']
def split_upper(string: str):
    split_string = re.split('([ABCDEFGHIJKLMNOPQRSTUVWXYZ])', string)
    word_list = []
    # determine if the string is PascalCase or camelCase, and start the word list with the first full word acordingly, and remove the first word from split_string
    if string[0].isupper():
        word_list.append(split_string[0]+split_string[1])
        del split_string[:2]
    else:
        print(split_string)
        word_list.append(split_string[0])
        del split_string[0]
    # iterate through the split string and append words to the word list
    for i in range(len(split_string)):
        # check if the index is a word or a capital letter (all words have an even numbered index)
        if i % 2 == 1:
            word_list.append(split_string[i-1].lower()+split_string[i])
    return word_list
    
# checks if a string contains snake_case names, and returns its component words if so
def parse_snake(string: str):
    if re.match(SNAKE_REGEX, string):
        return string.split('_')
    else:
        return None

# checks if a string contains camelCase names and returns its component words if so 
def parse_camel(string: str):
    if re.match(CAMEL_REGEX, string):
        return split_upper(string)
    else: 
        return None

# checks if a string contains PascalCase names and returns its component words if so
def parse_pascal(string: str):
    if re.match(PASCAL_REGEX, string):
        return split_upper(string)
    else: 
        return None

# takes a list of words and creates a camelCase name out of them
def generate_camel(word_list: list[str]):
    return word_list[0].lower() + ''.join(map(lambda x: x.capitalize(), word_list[1:]))

# takes a list of words and creates a snake_case name out of them
def generate_snake(word_list: list[str]):
    return '_'.join(map(str.lower, word_list))

# takes a list of words and creates a PascalCase name out of them
def genrate_pascal(word_list: list[str]):
    return ''.join(map(lambda x: x.capitalize()))


# replaces all instances of a particular naming convention with another in a given string
def replace_names(string: str, name_parser: 'function', name_gen: 'function'):
    word_list = []
    for i in string.split(' '):
        words = name_parser(i)
        if words:
            word_list.append(name_gen(words))
        else:
            word_list.append(i)

    return ' '.join(word_list)

# ensure an opperation at least one file was provided
if len(sys.argv) < 3:
    print('Please provide an opperation, and at least one file to convert')
    sys.exit(1)
# get the user's intended functions 
opperation = sys.argv[1].lower().strip()
# validate the specified opperation
if not re.match('^[cps]2[cps]$', opperation):
    print('Please provide an opperation in the following format: ["c" (camel) or "p" (pascal) or "s" (snake)]2["c" (camel) or "p" (pascal) or "s" (snake)]')
    sys.exit(1)
# determine the user's prefered name parsing and name generation functions from the opperation
name_parser_char, name_gen_char = opperation.split('2')
match name_parser_char:
    case 'c':
        name_parser = parse_camel
    case 'p':
        name_parser = parse_pascal
    case 's':
        name_parser = parse_snake
match name_gen_char:
    case 'c':
        name_gen = generate_camel
    case 'p':
        name_gen = generate_pascal
    case 's':
        name_gen = generate_snake

# run the specified parser and name generator to replace names in the provided file(s)
for i in sys.argv[2:]:
    if not os.path.exists(i):
        print(f'The file "{i}" could not be found.' )
        continue
    # read the file and replace names 
    with open(i) as f:
        # create an array of lines from the file
        lines = f.read().split('\n')
    # run the replacement function for each line, and write the result of each to output to be written to the file
    output = '\n'.join(map(lambda l: replace_names(l, name_parser, name_gen), lines))
    # overwrite the file with it's new contents
    with open(i, 'w') as f:
        f.write(output)
    print(f'All names have been updated in "{i}"')
        

