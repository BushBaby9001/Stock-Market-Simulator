import pygame
import numpy as np
from Box import Box

class Graph:

    def __init__(self, screen, rect, data, first_loaded_frame, frame_timer):
        #setting variables - should be self explanatory
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

        # initialising min/max box objects
        self.min_price_box = Box(self.screen, (910, 540, 50, 20), (0,0,0), "consolas", 20, f"${np.round(self.data_min, 2)}", (255,255,255))
        self.max_price_box = Box(self.screen, (910, 140, 50, 20), (0,0,0), "consolas", 20, f"${np.round(self.data_max, 2)}", (255,255,255))

        self.stock_price = self.data.open[1] # stock price based on the closing price for each data index - more variation than open, but less random like high/low
        self.shares = 0
        self.worth = 0

        # initialising additional display box objects
        self.stats_background = Box(self.screen, (100, 562.5, 800, 145), (0, 255, 0), "david", 40, "", (0, 0, 0))
        self.open_display_box = Box(self.screen, (110, 575, 253.3, 50), (255, 255, 255), "david", 40, "Open Display", (0, 0, 0))
        self.close_display_box = Box(self.screen, (110, 645, 253.3, 50), (255, 255, 255), "david", 40, "Close Display", (0, 0, 0))
        self.high_display_box = Box(self.screen, (373.3, 575, 253.3, 50), (255, 255, 255), "david", 40, "High Display", (0, 0, 0))
        self.low_display_box = Box(self.screen, (373.3, 645, 253.3, 50), (255, 255, 255), "david", 40, "Low Display", (0, 0, 0))
        self.volume_display_box = Box(self.screen, (636.6, 575, 253.3, 50), (255, 255, 255), "david", 40, "Volume Display", (0, 0, 0))
        self.dividends_display_box = Box(self.screen, (636.6, 645, 253.3, 50), (255, 255, 255), "david", 40, "Dividends Display", (0, 0, 0))


    def data_to_screen(self, data_value): # takes the straight data value and converts it into coordinates on the screen
        normalised_y = ((data_value - self.data_min) / (self.data_max - self.data_min))
        normalised_y = 1.0 - normalised_y
        screen_y = self.rect.y + (normalised_y * self.rect.height)
        return screen_y

    def draw(self, current_frame):
        normalised_current_frame = current_frame - self.first_loaded_frame # starts counting from frame 0 instead of some random frame
        if normalised_current_frame % self.frame_timer == 0:
            self.num_items = min(int(normalised_current_frame / self.frame_timer) + 1, len(self.data.low)) # adds another candlestick to the list if enough time (frames) has passed
        graph_width = self.rect.width
        candle_margin = 2
        candle_spacing = np.trunc(graph_width / self.num_items) # spacing calculations - has to be to nearest pixel, so leaves space at right of graph sometimes
        candle_width = np.trunc(candle_spacing - candle_margin)

        bg_colour = (5, 70, 120)
        pygame.draw.rect(self.screen, bg_colour, self.rect) # adds a background colour to the graph rect

        for i in range(self.num_items):
            x  = np.trunc(self.rect.left + (candle_spacing * i))

            #pygame.draw.rect(self.screen, (0,0,255), (x, self.rect.y, candle_width, self.rect.height)) # background of candles - shows spacing between candles

            open_y = self.data_to_screen(self.data.open[i]) # getting the data values for the current candlestick
            close_y = self.data_to_screen(self.data.close[i])
            high_y = self.data_to_screen(self.data.high[i])
            low_y = self.data_to_screen(self.data.low[i])

            mid_x = x + (candle_width / 2)

            if self.data.close[i] >= self.data.open[i]: # checking if price is increasing / decreasing to decide colour (green/red)
                candle_colour = (0, 220, 32)
            else:
                candle_colour = (255, 64, 0)

            pygame.draw.line(self.screen, candle_colour, (mid_x, low_y), (mid_x , high_y), width=2) # high-low line

            candle_height = max(1, close_y - open_y) # ensures the candle height isnt too small to see

            pygame.draw.rect(self.screen, candle_colour, (x, open_y, candle_width, candle_height)) # open-close box

            # drawing all of the boxes initialised earlier. Updates text as well to display current data
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
            self.worth = self.shares * self.stock_price # for portfolio worth

    def buy(self, money, volume): # if you have enough money to buy stock price * volume then buy it. otherwise you cant
        if volume == "max":
            volume = money // self.stock_price
            price = volume * self.stock_price
        else:
            price = self.stock_price * int(volume)

        if money >= price:
            self.shares += int(volume)
            money -= price
        return money

    def sell(self, money, volume): # same logic for buying but for selling.
        if volume == "max":
            volume = self.shares

        volume = int(volume)
        revenue = self.stock_price * volume

        if self.shares >= volume:
            self.shares -= volume
            money += revenue
        return money