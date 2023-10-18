import sys
import os
import re 

# given a string of text, replace all instances of snake_case naming with camelCase
def snake_to_camel(line: str) -> str:
    new_line = [] # a list of words in the original string, with all snake_case names replaced with camelCase
    for i in line.split(' '):
        # check if the word is snake_case, and replace with it camelCase if so
        if re.match('[A-z0-9(\'"[.]*([a-z0-9]+_)+[a-z0-9]+[(\'")[\],A-z0-9.]*', i):
            word_list = i.split('_')
            camel = word_list[0] + ''.join(map(lambda x: x.capitalize(), word_list[1:]))
            new_line.append(camel)
        else:
            new_line.append(i)
    return ' '.join(new_line)

# given a string of text, replace all instances of camelCase naming with snake_case 
def camel_to_snake(line: str) -> str:
    new_line = [] # a list of words in the original string, with all camelCase names replaced with snake_case
    for i in line.split(' '):
        # check if the word is camelCase, and replace with it snake if so
        if re.match('[A-z0-9(\'"[.]*[a-z]+([A-Z][a-z0-9]+)+[(\'")[\],A-z0-9.]*', i):
            # split the camelCase word into it's component words (capital letters serve as delimiters and have their own index)
            split_name = re.split('([ABCDEFGHIJKLMNOPQRSTUVWXYZ])', i)
            # append all all capital letters to their respective words, and make them lowercase
            word_list = [split_name[0]]
            for i in range(1, len(split_name)):
                # check if the index is a word or a capital letter (all words have an even numbered index)
                if i % 2 == 0:
                    word_list.append(split_name[i-1].lower()+split_name[i])
            # convert the list of words to a snake_case name, and append it to the new line
            new_line.append('_'.join(word_list))
        else:
            new_line.append(i)
    return ' '.join(new_line)

# ensure a file was provided
if len(sys.argv) < 3:
    print('Please provide an opperation, and at least one file to convert')
    sys.exit(1)
# get the user's intended function
match sys.argv[1]:
    case 's2c':
        replacement_function = snake_to_camel
    case 'c2s':
        replacement_function = camel_to_snake
    case _:
        print('Invalid opperation. Must be:\ns2c: snake_case to camelCase\nc2s: camelCase to snake_case')


for file_path in sys.argv[2:]:
    # ensure the provided file exists
    if not os.path.exists(file_path):
        print('The provided file was not found')
        sys.exit(1)
    # read the file's original lines
    with open(file_path, 'r') as f:
        lines = f.read().split('\n')
    # run the replacement function on each line of the file, and overwrite the file with the converted lines
    lines = list(map(replacement_function, lines))
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'All names converted in "{file_path}"')
