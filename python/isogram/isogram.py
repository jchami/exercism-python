def is_isogram(string):
    aux_string = ''
    for letter in string.lower():
        if letter in aux_string and letter.isalnum():
            return False
        else:
            aux_string += letter
    return True
