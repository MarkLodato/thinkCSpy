import os

def get_screens():
    f = open('cheeseshopscreens.txt', 'r')
    text = f.read()
    f.close()
    return text.split('+++')


def show(screen):
    os.system('clear')
    choice = raw_input(screen)
    if choice:
        return choice[0].upper()
    return "<Enter>" 


def cheeses_str(cheeses):
    cheeses_list = '' 
    for i in range(len(cheeses)):
        cheeses_list += '\t%d. %s\n' % (i+1, cheeses[i])
    return cheeses_list


def list_cheeses(cheeses):
    os.system('clear')
    print '\n\n'
    print cheeses_str(cheeses)
    raw_input('\n\nPress <enter> to continue...')


def add_cheese(cheeses):
    os.system('clear')
    cheeses.append(raw_input("\n\nEnter name of new cheese: "))
    cheeses.sort()


def delete_cheese(cheeses):
    os.system('clear')
    print '\n\n'
    print cheeses_str(cheeses)
    choice = input('\n\nWhich cheese would you like to delete? ')
    if choice in range(len(cheeses)):
        cheeses.remove(cheeses[choice])


def save_cheeses(cheeses):
    f = open('cheeselist.txt', 'w')
    for cheese in cheeses:
        f.write(cheese + '\n')
    f.close()


def load_cheeses():
    try:
        f = open('cheeselist.txt', 'r')
        text = f.read() 
        cheeses = text.split()
        f.close()
    except:
        cheeses = []
    return cheeses


def run():
    cheeses = load_cheeses() 
    screens = get_screens()
    show(screens[0])

    while True:
        choice = show(screens[1].rstrip() + ' ')

        while choice not in ['L', 'A', 'D', 'S', 'Q']:
            show(screens[-1] % choice)
            choice = show(screens[1].rstrip() + ' ')

        if choice == 'Q':
            save_cheeses(cheeses)
            break

        choices = {'L': list_cheeses,
                   'A': add_cheese,
                   'D': delete_cheese,
                   'S': save_cheeses}

        choices[choice](cheeses)


if __name__ == '__main__':
    run()
