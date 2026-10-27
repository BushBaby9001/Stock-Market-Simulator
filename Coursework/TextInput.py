import pygame
from Button import Button


class TextInput(Button):

    '''
    uses box.drawBox and box.drawText to display
    uses button.interaction to check for mouse hover/click detection
    then if the button is clicked and continuously hovered over, textinput.input is run, reading input from the user
    when the user presses enter, the text is then validated. If it is correct then it passes as a parameter into the function you want to run.
    '''

    def __init__(self, screen, rect, boxcolour, font, textsize, text, textcolour, hovercolour, clickcolour, usertext="", border_radius=20):
        super().__init__(screen, rect, boxcolour, font, textsize, text, textcolour, hovercolour, clickcolour, border_radius)
        self.usertext = usertext

    def input(self, event, function, length=100, datatype=None):
        if self.active: # if the box is clicked
            if event.type == pygame.KEYDOWN: # if a (specific) key is pressed

                if event.key == pygame.K_BACKSPACE:
                    # when backspace is pressed, usertext is set to usertext, but minus the last character
                    self.usertext = self.usertext[:-1]

                if event.key == pygame.K_RETURN:
                    # enter pressed, validate input then (if correct) pass to the function you want
                    validateduserinput = self.inputValidation(self.usertext, length, datatype)
                    if validateduserinput != None:
                        function(validateduserinput)
                    self.usertext = self.text

            if event.type == pygame.TEXTINPUT:
                # adds user text input to the userinput string
                self.usertext += event.text

            # self.text is what is used in box.drawText to actually display the text, so its easier to just set this to usertext, then reset later
            self.text = self.usertext # updates text in box to show what the user has typed
            self.drawText() # updates text in text box

        else:
            # for text input later, to display the original "click here to input text type text on a text box, and stopping typing into the box when not clicked.
            self.text = self.originaltext

    def inputValidation(self, userinput, length=100, datatype=None):
        #self.text = "" # resets the text when enter is pressed, resetting the text box
        inputlen = len(userinput)

        if not userinput.strip():
            print("invalid input - must not be whitespace")
            return None

        if inputlen == 0 or inputlen > length: # input is longer than the specified length value
            print("invalid input - invalid length")
            return None

        if datatype == "int": # for specific data types --- maybe add more validation for different data types if needed.
            try:
                return int(userinput)
            except ValueError:
                print("invalid input - wrong type")
                return None

        if datatype == "str":
            return str(userinput)

        return userinput
