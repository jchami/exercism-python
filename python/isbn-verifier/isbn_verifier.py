def verify(isbn):
    checksum = 0
    isbn = isbn.replace('-', '')
    if len(isbn) != 10:
        return False
    for i in range(0, 10):
        if isbn[i] not in '0123456789X':
            return False
        elif isbn[i] == 'X':
            checksum += 10
        else:
            checksum += (10 - i) * int(isbn[i])
    return checksum % 11 == 0
