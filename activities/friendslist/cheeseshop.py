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
    for cheese in cheeses:
        cheeses_list += '\t%s\n' % cheese
    return cheeses_list


def list_cheeses(cheeses):
    os.system('clear')
    print '\n\n'
    print cheeses_str(cheeses)
    raw_input('\n\nPress <enter> to continue...')


def add_cheese(cheeses):
    os.system('clear')
    cheeses.append(raw_input("\n\nEnter name of new cheese: "))


def delete_cheese(cheeses):
    pass


def save_cheeses(cheeses):
    pass


def run():
    cheeses = []
    screens = get_screens()
    show(screens[0])

    while True:
        choice = show(screens[1].rstrip() + ' ')

        while choice not in ['L', 'A', 'D', 'S', 'Q']:
            show(screens[-1] % choice)
            choice = show(screens[1].rstrip() + ' ')

        if choice == 'Q': break

        choices = {'L': list_cheeses,
                   'A': add_cheese,
                   'E': delete_cheese,
                   'S': save_cheeses}

        choices[choice](cheeses)


if __name__ == '__main__':
    run()
