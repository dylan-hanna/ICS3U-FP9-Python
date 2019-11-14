#!/usr/bin/env python3

# Created by: Dylan Hanna
# Created on: Nov 2019
# This program is the "Space Alien" game
#   for CircuitPython

import ugame
import stage
import time
import random
import board
import neopixel

import constants

# LED
PIXEL_PIN = board.NEOPIXEL  # pin that the NeoPixel is connected to
ORDER = neopixel.RGB   # pixel color channel order
COLOR_one= (0, 255, 0) # color to blink
COLOR_two = (255, 0, 0)
CLEAR = (0, 0, 0)      # clear (or second color)
pixel = neopixel.NeoPixel(PIXEL_PIN, 5, pixel_order=ORDER)
DELAY = 0.25


def splash_scene():
    # this function is the splash scene game loop

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, 160, 120)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic

        # Wait for 1 seconds
        time.sleep(1.0)
        menu_scene()

        # redraw sprite list

def menu_scene():
    # this function is a scene

    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # used this program to split the iamge into tile: https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # a list of sprites
    sprites = []

    # add text objects
    text = []

    text1 = stage.Text(width=29, height=14, font=None, palette=constants.NEW_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None, palette=constants.NEW_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = text + sprites + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic
        keys = ugame.buttons.get_pressed()
        #print(keys)

        if keys & ugame.K_START != 0:  # Start button
            game_scene()
            #break

        # redraw sprite list
def game_scene():
    # this function keeps the information of the buttons
    a_button_pressed = constants.button_state["button_up"]
    b_button_pressed = constants.button_state["button_up"]
    start_button_pressed = constants.button_state["button_up"]
    select_button_pressed = constants.button_state["button_up"]
    # LED
    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    boom_sound = open("boom.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    #
    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # a list of sprites that will be updated every frame
    sprites = []
    
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_1, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_X)
        lasers.append(a_single_laser)

    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
                        int(constants.SCREEN_Y - constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2))
    sprites.append(ship) # Insert at the top of the sprite list

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = sprites + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)
        # A button to fire
        if keys & ugame.K_X != 0:
            if a_button_pressed == constants.button_state["button_up"]:
                a_button_pressed = constants.button_state["button_just_pressed"]
            elif a_button_pressed == constants.button_state["button_just_pressed"]:
                a_button_pressed = constants.button_state["button_still_pressed"]
        else:
            a_button_pressed = constants.button_state["button_up"]

        # update game logic

        # move ship right
        if keys & ugame.K_RIGHT != 0:
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)

        # move ship left
        if keys & ugame.K_LEFT != 0:
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)

        # play sound if A is pressed
        if a_button_pressed == constants.button_state["button_just_pressed"]:
            # fire a laser, if we have enough power
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    pixel[0] = COLOR_two
                    pixel[1] = COLOR_two
                    pixel[2] = COLOR_two
                    pixel[3] = COLOR_two
                    pixel[4] = COLOR_two
                    time.sleep(DELAY)
                    pixel[0] = CLEAR
                    pixel[1] = CLEAR
                    pixel[2] = CLEAR
                    pixel[3] = CLEAR
                    pixel[4] = CLEAR
                    sound.stop()
                    sound.play(pew_sound)
                    break
        # each frame move the lasers, that have been fired, up
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x, lasers[laser_number].y - constants.LASER_SPEED)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)



        # redraw sprite list
        game.render_sprites(sprites)
        game.tick()  # wait until refresh rate finishes

if __name__ == "__main__":
    menu_scene()