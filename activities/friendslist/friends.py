import os
import string

def get_screens():
    f = open('fscreens.txt', 'r')
    text = f.read()
    f.close()
    return text.split('+++')


def show(screen):
    os.system('clear')
    choice = raw_input(screen)
    if choice:
        return choice[0].upper()
    return "<Enter>" 


def friends_str(friends):
    friends_list = '' 
    for i in range(len(friends)):
        friends_list += '\t%d. %s %s\n' % (i+1, friends[i][0], friends[i][1])
    return friends_list


def friend_str(friend, scr):
    return scr % (friend[0], friend[1], friend[2], friend[3],
                  friend[4], friend[5], friend[6], friend[7])


def list_friends(friends, fscr):
    os.system('clear')
    print '\n\n'
    print friends_str(friends)
    prompt = '\n\nFor which friend would you like to see details?\n'
    prompt += 'Enter the number of the friend or press <enter> for previous'
    prompt += ' menu: '
    choice = raw_input(prompt)
    while choice:
        choice = int(choice) - 1
        os.system('clear')
        print friend_str(friends[choice], fscr)
        raw_input("\nPress <enter> to continue...")
        os.system('clear')
        print '\n\n'
        print friends_str(friends)
        choice = raw_input(prompt)



def add_friend(friends):
    os.system('clear')
    friend = []
    friend.append(raw_input("\n\nEnter first name of new friend: "))
    friend.append(raw_input("\n\nEnter last name of new friend: "))
    friend.append(raw_input("\n\nEnter street address of new friend: "))
    friend.append(raw_input("\n\nEnter city where new friend lives: "))
    friend.append(raw_input("\n\nEnter state where new friend lives: "))
    friend.append(raw_input("\n\nEnter new friend's zip code: "))
    friend.append(raw_input("\n\nEnter new friend's phone number: "))
    friend.append(raw_input("\n\nEnter new friend's email address: "))
    friends.append(friend)
    friends.sort()


def edit_friend(friends):
    pass

def remove_friend(friends):
    os.system('clear')
    print '\n\n'
    print friends_str(friends)
    choice = input('\n\nWhich friend would you like to remove? ')
    choice -= 1
    if choice in range(len(friends)):
        friends.remove(friends[choice])


def save_friends(friends):
    f = open('friendlist.dat', 'w')
    for friend in friends:
        f.write(friend[0])
        for item in friend[1:]:
            f.write('; ' + item)
        f.write('\n')
    f.close()


def load_friends():
    friends = []
    try:
        f = open('friendlist.dat', 'r')
        raw_friends = f.readlines() 
        f.close()
        for friend in raw_friends:
            friends.append(friend.split(';'))
    except:
        pass

    for friend in friends:
        for i in range(len(friend)):
            friend[i] = friend[i].strip()

    return friends


def run():
    friends = load_friends() 
    screens = get_screens()
    show(screens[0])

    while True:
        choice = show(screens[1].rstrip() + ' ')

        while choice not in ['L', 'A', 'E', 'R', 'S', 'Q']:
            show(screens[-2] % choice)
            choice = show(screens[1].rstrip() + ' ')

        if choice == 'Q':
            save_friends(friends)
            break

        if choice == 'L':
            list_friends(friends, screens[-1])
        elif choice == 'A':
            add_friend(friends)
        elif choice == 'E':
            edit_friend(friends)
        elif choice == 'R':
            remove_friend(friends)
        else:
            save_friends(friends)


    save_friends(friends)


if __name__ == '__main__':
    run()
