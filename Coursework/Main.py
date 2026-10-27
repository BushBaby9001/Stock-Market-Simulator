import pygame
from StockMarketSimulator import StockMarketSimulator


pygame.init()

# initialise simulator object and run
simulator = StockMarketSimulator((1280, 720), 30)
simulator.init_simulator()
simulator.run()

pygame.quit()
