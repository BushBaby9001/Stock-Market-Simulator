import pygame
import numpy as np
from Box import Box
from Button import Button
from TextInput import TextInput
from Data import Data
from Graph import Graph
from Account import Account

global_stocks = []

class StockMarketSimulator:

    def __init__(self, resolution, framerate):

        # initialise variables
        self.WIDTH, self.HEIGHT = resolution
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.current_frame = 0
        self.stock_pointer = 0
        self.money = 10000.00
        self.volume = "1"
        self.volume_array = ["1", "10", "100", "max"]
        self.volume_pointer = 0

        pygame.mixer.music.load("MotivationalStockTradingMusic.mp3") #load music
        pygame.mixer.music.play(100, 0.0) # play music - loop 100 times

    def init_simulator(self):

        # initialising window title and icon

        pygame.display.set_caption("Stock Market Simulator")
        pygame.display.set_icon(pygame.image.load("StockMarketSim.png"))

        # instantiating classes

        self.data = Data()
        self.account = Account()

        self.money_display = Box(self.screen, (925, 50, 275, 50), (255, 255, 255), "david", 40, "MONEY", (0, 0, 0))

        self.button_buy = Button(self.screen, (1000, 150, 200, 50), (255, 255, 255), "david", 40, "BUY STOCKS", (0, 255, 0), (180, 180, 180), (0, 255, 0))
        self.button_sell = Button(self.screen, (1000, 220, 200, 50), (255, 255, 255), "david", 40, "SELL STOCKS", (255, 0, 0), (180, 180, 180), (255, 0, 0))
        self.button_change_volume = Button(self.screen, (1000, 290, 200, 50), (255, 255, 255), "david", 40, "VOLUME", (0, 0, 255), (180, 180, 180), (255, 0, 0))

        self.stock_name_input = TextInput(self.screen, (100, 50, 200, 50), (255, 255, 255), "david", 40, "LOAD STOCK", (0, 0, 0), (180, 180, 180), (255, 0, 0))
        self.button_change_stock = Button(self.screen, (325, 50, 350, 50), (255, 255, 255), "david", 40, "STOCK", (0, 0, 0), (180, 180, 180), (0, 255, 0))
        self.shares_display = Box(self.screen, (700, 50, 200, 50), (255, 255, 255), "david", 40, "SHARES", (0, 0, 0))
        self.portfolio_worth_display = Button(self.screen, (1000, 360, 200, 50), (255, 255, 255), "david", 40, "WORTH", (0, 0, 255), (180, 180, 180), (255, 0, 0))

        self.button_account = Button(self.screen, (1000, 430, 200, 50), (255, 255, 255), "david", 40, "ACCOUNT", (0, 0, 0), (180, 180, 180), (255, 0, 0))

        self.stock_period = Button(self.screen, (1000, 575, 200, 50), (255, 255, 255), "david", 40, f"Period = {self.data.period}", (0, 0, 255), (180, 180, 180), (255, 0, 0))
        self.stock_interval = Button(self.screen, (1000, 645, 200, 50), (255, 255, 255), "david", 40, f"Interval = {self.data.interval}", (0, 0, 255), (180, 180, 180), (255, 0, 0))

        self.graph = None

    def buy_stocks(self):
        self.money = np.round(self.graph.buy(self.money, self.volume), 2) # runs buy function, rounding the amount to the nearest 1p

    def sell_stocks(self):
        self.money = np.round(self.graph.sell(self.money, self.volume), 2)

    def set_volume(self):
        self.volume_pointer = (self.volume_pointer + 1) % len(self.volume_array) # every time set_volume is run, increment the pointer but if it is at the end of the list then reset it
        self.volume = self.volume_array[self.volume_pointer] # setting index

    def change_stock(self):
        if not global_stocks: # if no graphs have been loaded yet
            print("no stocks loaded")
        else:
            self.stock_pointer = (self.stock_pointer + 1) % len(global_stocks) # same code as switching through volume
            self.graph = global_stocks[self.stock_pointer]

    def load_graph(self, stock):
        try:
            self.data = Data(period=self.data.period, interval=self.data.interval) # initialise a new data object every time a new graph is loaded - keeps data separate from other graphs
            self.data.initialise(stock) # initialise the stock
            self.graph = Graph(self.screen, (100,150,800,400), self.data, self.current_frame, (30 * (self.framerate / 60))) # initialise the graph using gathered data. Time between candlesticks is normalised
            global_stocks.append(self.graph) # add to a list so user can swap between stocks

        except:
            return

    def set_period(self): # this and the interval one just link to data class functions and update button text
        self.data.set_period()
        self.stock_period.updateText(f"Period = {self.data.period}")

    def set_interval(self):
        self.data.set_interval()
        self.stock_interval.updateText(f"Interval = {self.data.interval}")

    def get_portfolio_worth(self): # for every graph in the graph list, add the stocks owned * current price = total stock worth
        total_worth = 0
        for stock in global_stocks:
            total_worth += stock.worth
        return total_worth

    def access_account(self):
        money = np.round((self.get_portfolio_worth() + self.money), 2) # adds all stock worth and cash
        username = input("Input Username: ") # gets data as console inputs
        password = input("Input Password: ")
        mode = input("Save or Load: ")
        data = self.account.accessAccount(username, password, mode, money) # performs account creation / save / load
        if data: # if data is loaded, it will return saved money - otherwise nothing will be returned.
            self.money = data

    def run(self):

        run = True
        while run: # main loop
            self.current_frame += 1 # frame counter

            mousepos = pygame.mouse.get_pos()

            for event in pygame.event.get(): # get events
                if event.type == pygame.QUIT: # if the X is pressed on the window, close program
                    run = False

                # interactions have to go in event space - entire functions are passed in, allowing them to be run
                self.button_buy.interaction(mousepos, event, self.buy_stocks)
                self.button_sell.interaction(mousepos, event, self.sell_stocks)
                self.button_change_volume.interaction(mousepos, event, self.set_volume)

                self.button_change_stock.interaction(mousepos, event, self.change_stock)
            
                self.stock_name_input.interaction(mousepos, event, self.stock_name_input.input(event, self.load_graph, 5, "string"))

                self.button_account.interaction(mousepos, event, self.access_account)

                self.stock_period.interaction(mousepos, event, self.set_period)
                self.stock_interval.interaction(mousepos, event, self.set_interval)

            keys = pygame.key.get_pressed() # listen to keystrokes
            if keys[pygame.K_ESCAPE]: # if esc pressed, close program
                run = False

            self.screen.fill((0,0,0)) # start of every frame - clear screen


            #draw and update boxes, graphs, text, etc. Some only draws if a graph has been loaded
            self.stock_name_input.draw()

            self.stock_period.draw()
            self.stock_interval.draw()

            if self.graph: # if a graph has been loaded
                self.graph.draw(self.current_frame)

                self.button_buy.draw()
                self.button_sell.draw()

                self.button_change_volume.updateText(f"VOLUME: {self.volume}")
                self.button_change_volume.draw()

                self.button_change_stock.updateText(f"STOCK LOADED: {self.graph.data.stockname}")
                self.button_change_stock.draw()

                self.shares_display.updateText(f"SHARES: {self.graph.shares}")
                self.shares_display.draw()

                self.money_display.updateText(f"MONEY: {self.money}")
                self.money_display.draw()

                total_money = np.round(self.get_portfolio_worth(), 2)
                self.portfolio_worth_display.updateText(f"{total_money}")
                self.portfolio_worth_display.draw()


                self.button_account.draw()


            pygame.display.flip() # end of every frame - update screen
            self.clock.tick(self.framerate) # cap framerate