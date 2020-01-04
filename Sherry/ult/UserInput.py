def get_input_username():
    result = ''
    flag = True
    while flag:
        temp = input()
        if temp == '$b':
            return None
        if 0 < len(temp) <= 100:
            result = temp
            flag = False
        elif len(temp) == 0:
            print('The user name must be at least one character! Please enter again. (Or enter $b to leave.)')
        elif len(temp) > 100:
            print('The user name must be under 100 character! Please enter again. (Or enter $b to leave.)')

    return result


def get_input_lucky_num():
    result = ''
    flag = True
    while flag:
        temp = input()
        if temp == '$b':
            return None
        if 0 < len(temp) <= 100:
            result = temp
            flag = False
        elif len(temp) == 0:
            print('The lucky number must be at least one character! Please enter again. (Or enter $b to leave.)')
        elif len(temp) > 100:
            print('The lucky number must be under 100 character! Please enter again. (Or enter $b to leave.)')

    return result


def get_input_comment():
    result = ''
    flag = True
    while flag:
        temp = input()
        if temp == '$b':
            return None

        if 0 < len(temp) <= 3000:
            result = temp
            flag = False

        elif len(temp) == 0:
            print('The comment in BCMB must be at least one character! Please enter again. (Or enter $b to leave.)')

        elif len(temp) > 3000:
            print('The comment in BCMB must be under 3000 character! Please enter again. (Or enter $b to leave.)')

    return result


def get_input_siuk():
    result = ''
    flag = True
    while flag:
        temp = input()
        if temp == '$b':
            return None
        if len(temp) == 32:
            result = temp
            flag = False
        else:
            print('The form of the input key is invalid, please try again. (Or enter $b to leave.)')
    return result
