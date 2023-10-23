import sys
import os
import re 


# regex constants
CAMEL_REGEX = '\\b[a-z]+[A-Z][a-zA-Z]*\\b'
SNAKE_REGEX = '\\b[a-z]+_[a-z_]+\\b'

# checks if a string contains snake_case names, and returns its component words if so
def parse_snake(string: str):
    if re.match(SNAKE_REGEX, string):
        return string.split('_')
    else:
        return None

# checks if a string contains camelCase names and returns its component words if so
def parse_camel(string: str):
    if re.match(CAMEL_REGEX, string):
        split_name = re.split('([ABCDEFGHIJKLMNOPQRSTUVWXYZ])', string)
        word_list = [split_name[0]]
        for i in range(1, len(split_name)):
            # check if the index is a word or a capital letter (all words have an even numbered index)
            if i % 2 == 0:
                word_list.append(split_name[i-1].lower()+split_name[i])
        return word_list
    else: 
        return None

# takes a list of words and creates a camelCase name out of them
def generate_camel(word_list: list[str]):
    return word_list[0].lower() + ''.join(map(lambda x: x.capitalize(), word_list[1:]))

# takes a list of words and creates a snake_case name out of them
def generate_snake(word_list: list[str]):
    return '_'.join(map(str.lower, word_list))

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

# ensure a file was provided
if len(sys.argv) < 3:
    print('Please provide an opperation, and at least one file to convert')
    sys.exit(1)
# get the user's intended function
match sys.argv[1]:
    case 's2c':
        name_parser = parse_snake
        name_gen = generate_camel
    case 'c2s':
        name_parser = parse_camel
        name_gen = generate_snake
    case _:
        print('Invalid opperation. Must be:\ns2c: snake_case to camelCase\nc2s: camelCase to snake_case')
        sys.exit(1)

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
        

