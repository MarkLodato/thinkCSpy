from World import *
from filters import *

# a Palindrome object is a kind of Gui
class Palindrome(Gui):

    # the __init__ function is called when we create a Palindrome
    def __init__(self):
        Gui.__init__(self)
        self.setup()
        self.mainloop()

    # create the widgets that make up the GUI
    def setup(self):
        # text entry
        self.entry = self.en()
        # label
        self.label = self.la()
        # frame
        self.fr()
        # two buttons
        self.bu(LEFT, text='Check', command=self.check_palindrome)
        self.bu(LEFT, text='Quit', command=self.quit)
        # end of frame
        self.endfr()

    # this is the function that gets called when the user presses
    # the Check button
    def check_palindrome(self):
        # get the contents of the text entry
        word = self.entry.get()
        # check the word
        if is_palindrome(word):
            text = 'Yes! %s is a palindrome.' % word
        else:            
            text = '%s is not a palindrome.' % word
        # change the contents of the label
        self.label.configure(text=text)


# The following is a standard idiom for including test code
# in a module.  It is not executed if the module is imported.
if __name__ == '__main__':
    Palindrome()
