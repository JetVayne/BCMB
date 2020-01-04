# ult first intro
def first_intro(bot_name: str):
    print('Welcome to BCMC ! I am ' + bot_name + ', your girl Friday.')
    print('Do you need anything from me?')
    print('1. Sign up\n' +
          '2. Sign in\n' +
          '3. Set key\n' +
          '4. Push comment\n' +
          '5. Get my comment\n' +
          '6. Get the rank\n' +
          '7. Get chain JSON\n' +
          '8. Chat with me\n' +
          'q. Exit BCMC\n'
          )


# ult recursive intro
def rs_intro(login_flag: bool, user_name: str, bot_name: str):
    if login_flag:
        print('Dear ' + user_name + ', Is there anything else I can help with?')
        print(bot_name + ' is at your service. :)')
        print('3. Set key\n' +
              '4. Push comment\n' +
              '5. Get my comment\n' +
              '6. Get the rank\n' +
              '7. Get chain JSON\n' +
              '8. Chat with me\n' +
              'q. Exit BCMC\n'
              )
    else:
        print('Is there anything else I can help with?')
        print('1. Sign up\n' +
              '2. Sign in\n' +
              '3. Set key\n' +
              '4. Push comment\n' +
              '5. Get my comment\n' +
              '6. Get the rank\n' +
              '7. Get chain JSON\n' +
              '8. Chat with me\n' +
              'q. Exit BCMC\n'
              )


def wrong_ft_intro_a():
    print('Oops, please type the right command code again to let me know. Please retry.')
    print('1. Sign up\n' +
          '2. Sign in\n' +
          '3. Set key\n' +
          '4. Push comment\n' +
          '5. Get my comment\n' +
          '6. Get the rank\n' +
          '7. Get chain JSON\n' +
          '8. Chat with me\n' +
          'q. Exit BCMC\n'
          )


def wrong_ft_intro_b():
    print('Oops, please type the right command code again to let me know. Please retry.')
    print('3. Set key\n' +
          '4. Push comment\n' +
          '5. Get my comment\n' +
          '6. Get the rank\n' +
          '7. Get chain JSON\n' +
          '8. Chat with me\n' +
          'q. Exit BCMC\n'
          )
