import pygame
import yfinance as yf
import numpy as np

pygame.init()


global_periods = ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
global_intervals = ("1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo")




class Box:

    def __init__(self, screen, rect, boxcolour, font, textsize, text, textcolour, border_radius=20):
        # set the variables
        self.screen = screen
        self.rect = pygame.Rect(rect) # make into a Rect object to make drawing and getting centre easier
        self.boxcolour = boxcolour
        self.font = pygame.font.SysFont(font, textsize) # pygame font initialisation
        self.text = text
        self.textcolour = textcolour
        self.border_radius = border_radius

    def draw(self):
        self.drawBox()
        self.drawText()

    def drawBox(self):
        # draws a rectangle on the screen, with the correct colour, at the rect position with the correct border radius
        pygame.draw.rect(self.screen, self.boxcolour, self.rect, border_radius=self.border_radius)

    def drawText(self):

        text_render = self.font.render(self.text, True, self.textcolour) # render text
        centre = text_render.get_rect(center=self.rect.center) # get the centre of the box to get a position for the text to sit centred in the box

        self.screen.blit(text_render, centre) # draw the text on top of the box

    def updateText(self, text): # workaround for changing text in the period and interval buttons
        self.text = text




class Button(Box):

    def __init__(self, screen, rect, boxcolour, font, textsize, text, textcolour, hovercolour, clickcolour, border_radius=20):
        super().__init__(screen, rect, boxcolour, font, textsize, text, textcolour, border_radius)
        self.hovercolour = hovercolour
        self.clickcolour = clickcolour
        self.originalboxcolour = boxcolour
        #self.originaltext = text
        self.active = False # added to check if the box is currently being hovered over/ clicked (for text input later)


    def interaction(self, mousepos, event, function):
        if self.rect.collidepoint(mousepos):
            self.boxcolour = self.hovercolour
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.boxcolour = self.clickcolour
                try:
                    self.active = True
                    function()
                except TypeError: # stops from trying to call NoneType
                    pass

        else:
            self.boxcolour = self.originalboxcolour

            # for text input later, to display the original "click here to input text type text on a text box, and stopping typing into the box when not clicked.
            #self.text = self.originaltext
            self.active = False






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


    def inputValidation(self, userinput, length=100, datatype=None):
        self.usertext = "" # resets the usertext when enter is pressed, resetting the text box
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










class Data:

    # sets initial values for initial text on buttons
    def __init__(self, period="1y", interval="1wk"): # first setup for before a stock has been input
        self.period = period
        self.interval = interval
        self.period_pointer = global_periods.index(period)
        self.interval_pointer = global_intervals.index(interval)

    # ******* potentially change set_period and set_interval to be one function by passing period or interval as a parameter to change whats updated.
    # changes period by incrementing a pointer in an array
    def set_period(self):
        self.period_pointer = (self.period_pointer + 1) % len(global_periods)    # increments pointer and also resets the pointer to 0 if it goes past the length of the tuple

        self.period = global_periods[self.period_pointer] # setting period to be the index

    # changes interval by incrementing a pointer in an array
    def set_interval(self):
        self.interval_pointer = (self.interval_pointer + 1) % len(global_intervals)    # increments pointer and also resets the pointer to 0 if it goes past the length of the tuple

        self.interval = global_intervals[self.interval_pointer]
        #print(self.interval) for debugging

    # sets the stock and runs the get_data function
    def initialise(self, stock):
        self.stock = stock

        self.get_data()
        #self.print_data() #use for debugging, comment out later

    # uses yfinance to retrieve data based on user set stock, period and interval
    def get_data(self):

        try: # tries to gather data for a stock - works if stock ticker is valid, returns error if not
            ticker = yf.Ticker(self.stock) # wont return an error if an incorrect ticker name is used, so the next line is added too
            data = ticker.history(period=self.period, interval=self.interval) # gathers data from the ticker object
        except:
            return "invalid stock ticker"

        self.date = data.index
        self.open = data["Open"].values # values formats to array
        self.close = data["Close"].values
        self.high = data["High"].values
        self.low = data["Low"].values
        self.stockname = self.stock
        self.volume = data["Volume"].values
        self.dividends = data["Dividends"].values



    # prints data for debugging purposes - same idea can probably be used for formatting the data
    def print_data(self):
            for i in range(len(self.date)): # each set of data should be the same length
                print(f"{self.stockname} {i} {self.date[i]} -- ",
                      f"High: {round(self.high[i], 2)} ",
                      f"Low: {round(self.low[i], 2)} ",   # also round is used to round the data to the nearest 1p (for ease of use)
                      f"Open: {round(self.open[i], 2)} ",
                      f"Close: {round(self.low[i], 2)}")


class Graph:

    def __init__(self, screen, rect, data, first_loaded_frame, frame_timer):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.first_loaded_frame = first_loaded_frame
        self.frame_timer = frame_timer
        self.num_items = 1
        self.data = data
        self.data_min = min(self.data.low)
        self.data_max = max(self.data.high)
        range = self.data_max - self.data_min
        margin = range * 0.1
        self.data_min -= margin
        self.data_max += margin

        self.min_price_box = Box(self.screen, (910, 540, 50, 20), (0,0,0), "consolas", 20, f"${np.round(self.data_min, 2)}", (255,255,255))
        self.max_price_box = Box(self.screen, (910, 140, 50, 20), (0,0,0), "consolas", 20, f"${np.round(self.data_max, 2)}", (255,255,255))

        self.stock_price = self.data.open[1] # stock price based on the closing price for each data index - more variation than open, but less random like high/low

        self.stats_background = Box(self.screen, (100, 562.5, 800, 145), (0, 255, 0), "david", 40, "", (0, 0, 0))
        self.open_display_box = Box(self.screen, (110, 575, 253.3, 50), (255, 255, 255), "david", 40, "Open Display", (0, 0, 0))
        self.close_display_box = Box(self.screen, (110, 645, 253.3, 50), (255, 255, 255), "david", 40, "Close Display", (0, 0, 0))
        self.high_display_box = Box(self.screen, (373.3, 575, 253.3, 50), (255, 255, 255), "david", 40, "High Display", (0, 0, 0))
        self.low_display_box = Box(self.screen, (373.3, 645, 253.3, 50), (255, 255, 255), "david", 40, "Low Display", (0, 0, 0))
        self.volume_display_box = Box(self.screen, (636.6, 575, 253.3, 50), (255, 255, 255), "david", 40, "Volume Display", (0, 0, 0))
        self.dividends_display_box = Box(self.screen, (636.6, 645, 253.3, 50), (255, 255, 255), "david", 40, "Dividends Display", (0, 0, 0))


    def data_to_screen(self, data_value):
        normalised_y = ((data_value - self.data_min) / (self.data_max - self.data_min))
        normalised_y = 1.0 - normalised_y
        screen_y = self.rect.y + (normalised_y * self.rect.height)
        return screen_y

    def draw(self, current_frame):
        normalised_current_frame = current_frame - self.first_loaded_frame
        if normalised_current_frame % self.frame_timer == 0:
            self.num_items = min(int(normalised_current_frame / self.frame_timer) + 1, len(self.data.low))
        graph_width = self.rect.width
        candle_margin = 2
        candle_spacing = np.trunc(graph_width / self.num_items)
        candle_width = np.trunc(candle_spacing - candle_margin)

        bg_colour = (5, 70, 120)
        pygame.draw.rect(self.screen, bg_colour, self.rect) # adds a background colour to the graph rect

        for i in range(self.num_items):
            x  = np.trunc(self.rect.left + (candle_spacing * i))

            #pygame.draw.rect(self.screen, (0,0,255), (x, self.rect.y, candle_width, self.rect.height)) # background of candles - shows spacing between candles

            open_y = self.data_to_screen(self.data.open[i])
            close_y = self.data_to_screen(self.data.close[i])
            high_y = self.data_to_screen(self.data.high[i])
            low_y = self.data_to_screen(self.data.low[i])

            mid_x = x + (candle_width / 2)

            if self.data.close[i] >= self.data.open[i]:
                candle_colour = (0, 220, 32)
            else:
                candle_colour = (255, 64, 0)

            pygame.draw.line(self.screen, candle_colour, (mid_x, low_y), (mid_x , high_y), width=2) # high-low line

            candle_height = max(1, close_y - open_y) # ensures the candle height isnt too small to see

            pygame.draw.rect(self.screen, candle_colour, (x, open_y, candle_width, candle_height)) # open-close box

            self.min_price_box.draw()
            self.max_price_box.draw()

            self.stats_background.draw()
            self.open_display_box.draw()
            self.open_display_box.updateText(f"Open: {np.round(self.data.open[self.num_items - 1], 2)}") # could have put all of this in a for loop but i added the boxes at different times so didnt work out in practice
            self.close_display_box.draw()
            self.close_display_box.updateText(f"Close: {np.round(self.data.close[self.num_items - 1], 2)}")
            self.high_display_box.draw()
            self.high_display_box.updateText(f"High: {np.round(self.data.high[self.num_items - 1], 2)}")
            self.low_display_box.draw()
            self.low_display_box.updateText(f"Low: {np.round(self.data.low[self.num_items - 1], 2)}")
            self.volume_display_box.draw()
            self.volume_display_box.updateText(f"Vol (k): {self.data.volume[self.num_items - 1] / 1000}") # /1000 allows text to fit in the box even with high volumes
            self.dividends_display_box.draw()
            self.dividends_display_box.updateText(f"Dividends: {self.data.dividends[self.num_items - 1]}") # probably a useless metric but i have space for 6 boxes - ask stakeholders for feedback

            self.stock_price = np.round(self.data.open[self.num_items - 1], 2)


class StockMarketSimulator:

    def __init__(self, resolution, framerate):

        # initialise screen, resolution and framerate
        self.WIDTH, self.HEIGHT = resolution
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.current_frame = 0

    def init_simulator(self):

        # instantiating classes

        self.data = Data()

        self.button_buy = Button(self.screen, (1000, 50, 200, 50), (255, 255, 255), "david", 40, "BUY STOCKS", (0, 255, 0), (180, 180, 180), (0, 255, 0))
        self.button_sell = Button(self.screen, (1000, 110, 200, 50), (255, 255, 255), "david", 40, "SELL STOCKS", (255, 0, 0), (180, 180, 180), (255, 0, 0))


        self.stock_name_input = TextInput(self.screen, (100, 50, 200, 50), (255, 255, 255), "david", 40, "INPUT TEXT", (0, 0, 0), (180, 180, 180), (255, 0, 0), border_radius=0)
        self.stock_period = Button(self.screen, (1000, 410, 200, 50), (255, 255, 255), "david", 40, f"Period = {self.data.period}", (0, 0, 255), (180, 180, 180), (255, 0, 0))
        self.stock_interval = Button(self.screen, (1000, 470, 200, 50), (255, 255, 255), "david", 40, f"Interval = {self.data.interval}", (0, 0, 255), (180, 180, 180), (255, 0, 0))


        self.graph = None

    # temporary function to ensure buttons function are working.
    def testthing(self):
        print(self.graph.stock_price)

    def load_graph(self, stock):
        self.data.initialise(stock)
        self.graph = Graph(self.screen,  (100, 150, 800, 400), self.data, self.current_frame, 30)

    def set_period(self):
        self.data.set_period()
        self.stock_period.updateText(f"Period = {self.data.period}")

    def set_interval(self):
        self.data.set_interval()
        self.stock_interval.updateText(f"Interval = {self.data.interval}")

    def run(self):

        run = True
        while run: # main loop
            self.current_frame += 1

            mousepos = pygame.mouse.get_pos()

            for event in pygame.event.get(): # get events
                if event.type == pygame.QUIT: # if the X is pressed on the window, close program
                    run = False

                self.button_buy.interaction(mousepos, event, self.testthing)  # interactions have to go in event space
                self.button_sell.interaction(mousepos, event, self.testthing)

                self.stock_name_input.interaction(mousepos, event, self.stock_name_input.input(event, self.load_graph, 5, "string"))
                self.stock_period.interaction(mousepos, event, self.set_period)
                self.stock_interval.interaction(mousepos, event, self.set_interval)

            keys = pygame.key.get_pressed() # listen to keystrokes
            if keys[pygame.K_ESCAPE]: # if esc pressed, close program
                run = False

            self.screen.fill((0,0,0)) # start of every frame - clear screen

            self.button_buy.draw()
            self.button_sell.draw()

            self.stock_name_input.draw()

            self.stock_period.draw()
            self.stock_interval.draw()

            if self.graph:
                self.graph.draw(self.current_frame)


            pygame.display.flip() # end of every frame - update screen
            self.clock.tick(self.framerate) # cap framerate




# initialise simulator object and run
simulator = StockMarketSimulator((1280, 720), 30)
simulator.init_simulator()
simulator.run()

pygame.quit()


'''
goated:
https://www.examreferencelanguage.co.uk/?code=%5B%7B%22name%22%3A%22code%22%2C%22content%22%3A%22class+graph%3A%5Cn%5Cn%5Ctdef+__init__%28self%29%3A%5Cn%5Ct%5Ctself.car+%3D+10%5Cn%5Cnendclass%5Cn%22%7D%5D&a-level=
'''