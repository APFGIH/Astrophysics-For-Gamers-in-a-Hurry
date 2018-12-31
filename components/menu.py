"""
This file contains all the UI elements of the game. This includes buttons, text boxes and complete menus.

Main UI Developer: Henry Tu & Syed Safwaan
"""

# RAHCRAFT
# COPYRIGHT 2017 (C) RAHMISH EMPIRE, MINISTRY OF RAHCRAFT DEVELOPMENT
# DEVELOPED BY RYAN ZHANG, HENRY TU, SYED SAFWAAN

# menu.py
# UI elements

from pygame import *
import json
import components.mehdi as meh

# Loads standard UI elements (Button states)
button_hover = image.load("textures/menu/button_hover.png")
button_pressed = image.load("textures/menu/button_pressed.png")
button_idle = image.load("textures/menu/button_idle.png")

# Button class
class Button:
    # Creates a button given size, function, and label
    def __init__(self, x, y, w, h, func, text):

        """ Initializes the button instance. """

        self.rect = Rect(x, y, w, h)  # Creates rect
        self.text = text  # Button Label
        self.func = func  # Function after button is clicked

        # Button textures
        self.hover_img = transform.scale(button_hover, (w, h))
        self.press_img = transform.scale(button_pressed, (w, h))
        self.idle_img = transform.scale(button_idle, (w, h))

    # Mouse hover
    def highlight(self, surf):

        """ Highlights the button. """

        surf.blit(self.hover_img, self.rect)

    # Mouse click
    def mouse_down(self, surf):

        """ Emphasizes botton on mouse click. """

        surf.blit(self.press_img, self.rect)

    # Mouse not on button
    def idle(self, surf):
        surf.blit(self.idle_img, self.rect)

    # Update button state
    def update(self, surf, mx, my, m_press, size, release):

        # Button in contact with cursor
        if self.rect.collidepoint(mx, my):

            # Mouse button down
            if m_press[0]:
                self.mouse_down(surf)

            # Mouse released over button
            elif release:
                # Click cursor
                mouse.set_cursor(*cursors.tri_left)

                # Click sound
                meh.load_sound(['sound/random/click.ogg'])

                # Executes function
                return self.func

            else:
                # Highlight button
                self.highlight(surf)
        else:
            # Draw idle button
            self.idle(surf)

        # Draws button text
        text_surf = meh.text(self.text, size)
        surf.blit(text_surf, meh.center(*self.rect, text_surf.get_width(), text_surf.get_height()))


# Slider with range from 0-100
class Slider:
    def __init__(self, x, y, w, h, position, text):

        # Creates properties
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.pos = position

        # Tectures
        self.texture = {'hover': transform.scale(button_hover, (20, h - 3)),
                        'idle': transform.scale(button_idle, (20, h - 3))}

    # Update slider
    def update(self, surf, mx, my, m_press, size, release):

        # Outline slider
        draw.rect(surf, (0, 0, 0), self.rect)
        draw.rect(surf, (200, 200, 200), self.rect, 1)

        # Mouse is over slider
        if self.rect.collidepoint(mx, my):

            # Change mouse state
            mouse_state = 'hover'

            # Mouse is mouse is down, update cursor position
            if m_press[0]:
                self.pos = (mx - self.rect.x) / self.rect.w

            # Play click sound
            if release:
                meh.load_sound(['sound/random/click.ogg'])

        else:
            # Change mouse state
            mouse_state = 'idle'

        # Draws indicator
        surf.blit(self.texture[mouse_state], (
            self.rect.x + min(max(self.pos, ((self.texture[mouse_state].get_width() + 2) // 2) / self.rect.w),
                              1 - ((self.texture[mouse_state].get_width() + 3) // 2) / self.rect.w) * self.rect.w -
            self.texture[mouse_state].get_width() // 2, self.rect.y + 1))

        # Draws label
        text_surf = meh.text(self.text, size)
        surf.blit(text_surf, meh.center(*self.rect, text_surf.get_width(), text_surf.get_height()))


# Toggle button
class Toggle:
    def __init__(self, x, y, w, h, state, text):

        # Properties
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.state = state

        # Texture
        self.texture = {'idle': transform.scale(button_idle, (w, h)),
                        'press': transform.scale(button_pressed, (w, h))}

    # Draws button
    def draw_button(self, surf, type, size):

        # Dras texture depending on button state
        surf.blit(self.texture[type], (self.rect.x, self.rect.y))

        # Button label
        text_surf = meh.text(self.text, size)
        surf.blit(text_surf, meh.center(*self.rect, text_surf.get_width(), text_surf.get_height()))

    # Updates button
    def update(self, surf, mx, my, m_press, size, release):

        # If mouse click
        if self.rect.collidepoint(mx, my) and release:
            # Update cursor
            mouse.set_cursor(*cursors.tri_left)

            # Click sound
            meh.load_sound(['sound/random/click.ogg'])

            # Toggle state
            self.state = not self.state

        # Draw texture based on state
        if self.state:
            self.draw_button(surf, 'press', size)
        else:
            self.draw_button(surf, 'idle', size)


# Sliding switch
class Switch:
    def __init__(self, x, y, w, h, state, text):

        # Button properies
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.state = state

        # Slider position an direction
        self.slider_x = 0
        self.slider_v = 0

        slider_w = self.rect.w // 2 - 5
        slider_h = self.rect.h - 6

        # Texture
        self.texture = {'hover': transform.scale(button_hover, (slider_w, slider_h)),
                        'idle': transform.scale(button_idle, (slider_w, slider_h))}

    # Draw button
    def draw_button(self, surf, offset, type, size):

        # Draw outline
        draw.rect(surf, (200, 200, 200), self.rect)
        draw.rect(surf, (20, 20, 20), (self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, self.rect.h - 4))

        # Draw slider
        surf.blit(self.texture[type], (self.rect.x + 3 + offset, self.rect.y + 3))

        # Draws label
        text_surf = meh.text(self.text, size)
        surf.blit(text_surf, meh.center(self.rect.x + 3 + offset, self.rect.y + 3, *self.texture['idle'].get_size(), \
                                        text_surf.get_width(), text_surf.get_height()))

    # Move button on
    def turn_on(self):
        self.state = True
        self.slider_v = 15  # Changes velocity

    # Move button off
    def turn_off(self):
        self.state = False
        self.slider_v = -15  # Changes velocity

    # Updates button
    def update(self, surf, mx, my, m_press, size, release):
        # Moves slider
        self.slider_x += self.slider_v

        # Stops slider from flying off
        if self.slider_x <= 0 or self.slider_x > self.rect.w // 2:
            self.slider_v = 0

        if self.slider_x < 0:
            self.slider_x = 0

        elif self.slider_x > self.rect.w // 2:
            self.slider_x = self.rect.w // 2

        # Mouse hovers over switch
        if self.rect.collidepoint(mx, my):

            # Mouse click
            if release:

                # Change mouse cursor
                mouse.set_cursor(*cursors.tri_left)

                # Click sound
                meh.load_sound(['sound/random/click.ogg'])

                # Toggle state
                if self.state:
                    self.turn_off()
                else:
                    self.turn_on()

            else:
                # Button hover
                self.draw_button(surf, self.slider_x, 'hover', size)

        else:
            # Button idle
            self.draw_button(surf, self.slider_x, 'idle', size)


# Hover cursor
click_cursor = ["      ..                ",
                "     .XX.               ",
                "     .XX.               ",
                "     .XX.               ",
                "     .XX.               ",
                "     .XX.               ",
                "     .XX...             ",
                "     .XX.XX...          ",
                "     .XX.XX.XX.         ",
                "     .XX.XX.XX...       ",
                "     .XX.XX.XX.XX.      ",
                "     .XX.XX.XX.XX.      ",
                "...  .XX.XX.XX.XX.      ",
                ".XX...XXXXXXXXXXX.      ",
                ".XXXX.XXXXXXXXXXX.      ",
                " .XXX.XXXXXXXXXXX.      ",
                "  .XXXXXXXXXXXXXX.      ",
                "  .XXXXXXXXXXXXXX.      ",
                "   .XXXXXXXXXXXXX.      ",
                "    .XXXXXXXXXXX.       ",
                "    .XXXXXXXXXXX.       ",
                "     .XXXXXXXXX.        ",
                "     .XXXXXXXXX.        ",
                "     ...........        "]
# Compile cursor
click_cursor_data = ((24, 24), (7, 1), *cursors.compile(click_cursor))


# Class to format buttons given their row
class Menu:
    def __init__(self, button_param, x, y, w, h, ):

        # Gets the number of rows based on the largest row value
        row_num = max([button_row for button_row, *trash in button_param])

        # Width of all buttons
        group_w = 400

        # Height of group is height of button * number of buttons - padding
        group_h = row_num * 50 - 10

        # Location of button 'group' on canvas
        group_x = x + w // 2 - group_w // 2
        group_y = y + h // 2 - group_h // 2

        # List of button parameters
        self.button_list = []

        # Organize buttons in list based on row number
        sorted_button_param = [[button for button in button_param if button[0] == row] for row in range(row_num + 1)]

        # Creates button object from params in button list
        for button_row in range(len(sorted_button_param)):

            # If there is a button on the row
            if sorted_button_param[button_row]:

                # Button width based on number of buttons sharing the row
                b_w = int(group_w / len(sorted_button_param[button_row]) - 10)

                # Button height
                b_h = 40

                # Button Y coordinate relative to group orgin
                b_y = group_y + ((b_h + 10) * button_row)

                # Construct individual buttons on each row
                for button_index in range(len(sorted_button_param[button_row])):
                    b_x = group_x + ((b_w + 10) * button_index)  # Button X Location relative to group origin

                    func = sorted_button_param[button_row][button_index][1]  # Button function
                    text = sorted_button_param[button_row][button_index][2]  # Button label

                    # Creates button object
                    self.button_list.append(Button(b_x, b_y, b_w, b_h, func, text))

    # Update button group
    def update(self, surf, release, mx, my, m_press):
        hover_over_button = False  # Cursor state

        # Updates each button
        for button in self.button_list:
            nav_update = button.update(surf, mx, my, m_press, 15, release)

            # If button returns function, execute
            if nav_update is not None:
                return nav_update

            # If hover over button
            if button.rect.collidepoint(mx, my):
                hover_over_button = True

        # Change cursor
        if hover_over_button:
            mouse.set_cursor(*click_cursor_data)

        else:
            mouse.set_cursor(*cursors.tri_left)


# Textfield
class TextBox:
    def __init__(self, x, y, w, h, label):

        # Intitializes properties
        self.rect = Rect(x, y, w, h)

        # Contents of field
        self.content = ""

        # Label on textbox
        self.font = font.Font("fonts/UndertaleSans.ttf", 14)
        self.label = self.font.render(label, True, (255, 255, 255))
        self.name = label

        # Width of a single character to determine max char count
        self.charwidth = self.font.render("X", True, (255, 255, 255)).get_width()

        # Legal characters
        self.allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'A', 'Y', 'Z', '0', '1', '2', '3', '4',
                        '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
                        '/', ' ', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', "'",
                        "'"]

    # Draw the textbox
    def draw(self, surf, selected):

        # Draw label
        surf.blit(self.label, (self.rect.x, self.rect.y - self.label.get_height() - 2))

        # Draw the text box
        draw.rect(surf, (0, 0, 0), self.rect)
        draw.rect(surf, (151, 151, 151), self.rect, 2)

        # Draw stars if field is password
        # Otherwise, draw field content
        if 'Password' in self.name:
            text = '*' * len(self.content)
        else:
            text = self.content

        surf.blit(self.font.render(text, True, (255, 255, 255)), (self.rect.x + 10, self.rect.y + 15))

        # Draw highlight if field is selected
        if selected == self.name:
            draw.rect(surf, (255, 255, 255), self.rect, 2)

    # Updates field
    def update(self, e):

        # If key down
        if e and e.type == KEYDOWN:

            # If key is valid, add to field content
            if e.unicode in self.allowed and len(self.content) < self.rect.w // self.charwidth - 1:
                self.content += e.unicode

            # Delete character
            elif e.key == K_BACKSPACE:
                try:
                    self.content = self.content[:-1]
                except IndexError:
                    pass

        return self.content


# Large button for displaying servers
class ServerButton:
    def __init__(self, x, y, w, h, title, host, port, motd, strength):

        # Button properties
        self.rect = Rect(x, y, w, h)
        self.title = title
        self.host = host
        self.port = port
        self.motd = motd
        self.strength = strength

        # List of hardcoded servers that should be kept intact
        self.do_not_destroy = ['Rahmish Imperial', 'Localhost']

    # Draws the button outline
    def draw_button(self, surf, inner, outer):
        draw.rect(surf, outer, self.rect)
        draw.rect(surf, inner, (self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, self.rect.h - 4))

    # Button states
    # Button highlight
    def highlight(self, surf):
        self.draw_button(surf, (40, 40, 40), (250, 250, 250))

    # Button pressed
    def mouse_down(self, surf):
        self.draw_button(surf, (10, 10, 10), (250, 250, 250))

    # Button idle
    def idle(self, surf):
        self.draw_button(surf, (20, 20, 20), (250, 250, 250))

    # Update button state
    def update(self, surf, mx, my, m_press, release, right_release, size):

        # If cursor in contact with button
        if self.rect.collidepoint(mx, my):

            # If mouse is down
            if m_press[0]:
                self.mouse_down(surf)

            # If mouse is released and not on 'menu strip'
            elif release and my < size[1] - 80:
                # Change mouse cursor
                mouse.set_cursor(*cursors.tri_left)

                # Play click sound
                meh.load_sound(['sound/random/click.ogg'])

                # Start the game function
                return ['game', self.host, self.port]

            # If right click (Delete server)
            elif right_release and my < size[1] - 80:

                # If button is not on do not destroy list
                if self.title not in self.do_not_destroy:
                    return ['remove', self.title, self.host, self.port]
                else:
                    return ['remove fail']

            else:
                # Button is being hovered
                self.highlight(surf)
        else:
            # Button is sitting idle
            self.idle(surf)

        # Server title
        title_text_surf = meh.text(self.title, 20)
        surf.blit(title_text_surf, (self.rect.x + 10, self.rect.y + 10))

        # Server ip and port
        connection_text_surf = meh.text("%s:%i" % (self.host, self.port), 15)
        surf.blit(connection_text_surf, (self.rect.x + 10, self.rect.y + 50))

        # Server MOTD
        motd_text_surf = meh.text("%s" % (self.motd), 12)
        surf.blit(motd_text_surf, (self.rect.x + 10, self.rect.y + 34))

        # Special tag if server is verified to be Rahmish
        if self.host == 'mehmish.com':
            special_text_surf = meh.text("Verified Rahmish Server", 12)
            surf.blit(special_text_surf,
                      (self.rect.x + self.rect.w - special_text_surf.get_width() - 10, self.rect.y + 50))

        # Calculates signal strength based on ping
        signal_strength = self.strength // 100

        # *Signal bars are in reverse strength (5+ [Worse case], 1 [Best case])*

        # Draws 5 bars
        for bar in range(5):

            # Only fill in bars below bar #
            if bar >= signal_strength:

                # If signal is below 3 bars, bars are yellow
                if signal_strength > 2:
                    colour = (200, 255, 0)
                else:
                    colour = (0, 255, 0)
            else:
                colour = (100, 100, 100)

            # Draws bar
            draw.rect(surf, colour, (self.rect.x + self.rect.w - 10 - bar * 5, self.rect.y + 25, 3, - 15 + bar * 2))

            # If there is no signal, draw crss
            if signal_strength >= 5:
                draw.line(surf, (255, 0, 0), (self.rect.x + self.rect.w - 30, self.rect.y + 10),
                          (self.rect.x + self.rect.w - 15, self.rect.y + 25), 4)
                draw.line(surf, (255, 0, 0), (self.rect.x + self.rect.w - 30, self.rect.y + 25),
                          (self.rect.x + self.rect.w - 15, self.rect.y + 10), 4)


# Menu class, but for server buttons
class ScrollingMenu:
    def __init__(self, button_param, x, y, w):
        # button_list <row>, <func>, <title>, <host>, <port>

        #Width of button group
        group_w = 400

        #Location of button group on canvas
        group_x = x + w // 2 - group_w // 2
        group_y = 50

        # Button list
        self.button_list = []

        # Create button object based on params in button list
        for button_index in range(len(button_param)):
            row, title, host, port, motd, strength = button_param[button_index]
            port, strength = int(port), int(strength)

            # Extracts button params from list
            button_x = group_x
            button_y = group_y + row * 80

            # Creates object
            self.button_list.append(
                ServerButton(button_x, button_y, 400, 75, title, host, port, motd, strength))

    # Updates entire group
    def update(self, surf, release, right_release, mx, my, m_press, y_offset, size):

        # Updates cursor
        click_cursor_data = ((24, 24), (7, 1), *cursors.compile(click_cursor))

        # Resets cursor state
        hover_over_button = False

        # Update buttons
        for button in self.button_list:

            # Update the button
            nav_update = button.update(surf, mx, my, m_press, release, right_release, size)

            # Update button Y location if necessary based on scroll
            button.rect.y = y_offset + self.button_list.index(button) * (button.rect.h + 5)

            # If button is clicked, run function
            if nav_update is not None:
                return nav_update

            # If cursor over button
            if button.rect.collidepoint(mx, my):
                hover_over_button = True

        # Change cursor state
        if hover_over_button:
            mouse.set_cursor(*click_cursor_data)

        else:
            mouse.set_cursor(*cursors.tri_left)


class Inventory:
    def __init__(self, w,
                 h):  # Init function declares all of the variables and loads all of the graphics. w and h are the width and height of the screen
        self.graphic = image.load('textures/gui/inventory.png')  # Loads the inventory graphic
        self.x, self.y = w // 2 - self.graphic.get_width() // 2, h // 2 - self.graphic.get_height() // 2  # Calculates the location of where the menu graphics should be placed
        self.w, self.h = w, h  # Keeping the width and height as a backup
        self.highlight = Surface((32, 32))  # Creating a highlight to give user feedback
        self.highlight.fill((255, 255, 255))
        self.highlight.set_alpha(150)
        self.holding = [0, 0]  # The current item that the user is holding. The default is 0,0 or air/nothing

        self.recipes = json.load(open(
            "data/tucrafting.json"))  # Loads the crafting recipes stored in a json format for easy edits and recipe adding

        self.crafting_grid = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]  # Creates an empty crafting grid for crafting
        self.result = [0, 0]  # The results of the crafting

    def recipe_check(
            self):  # This function is used to lookup the recipe. If the recipe exists, the function sets the result to the item that corresponds to the recipe
        current_recipe = [self.crafting_grid[x][y][0] for x in range(2) for y in range(
            2)]  # Using list comprehension to generate a flattened list of whats currently on the crafting grid
        current_recipe = " ".join(
            list(map(str, current_recipe)))  # Converting the crafting grid to a string. This is used for lookup later

        if current_recipe in self.recipes:  # If the recipe exists in the json
            self.resulting_item = [self.recipes[current_recipe]['result'], self.recipes[current_recipe][
                'quantity']]  # Setting the correct result and amount crafted
        else:
            self.resulting_item = [0, 0]  # Crafting recipe does not exist. revert to default values

    # Crafting function takes an item library which store the basic information of all of the blocks and items. This will be used for item stacking. It subtracts one from every single item on the crafting grid and
    # puts the item in to self.holding if the recipe exists
    def craft(self, item_lib):
        if self.resulting_item != [0, 0]:  # If the recipe is confirmed to exist
            if self.holding[0] == 0:  # If the player is holding nothing
                self.holding = self.resulting_item  # Gives the player the crafted item

            elif self.holding[0] == self.resulting_item[0] and self.holding[1] + self.resulting_item[1] <= \
                    item_lib[self.holding[0]][
                        -1]:  # If the player is holding the same item as the result and when crafted results in less than one stack,
                # Add items to the item current holding
                self.holding[1] += self.resulting_item[1]

            for x in range(
                    len(self.crafting_grid)):  # Loop through all of the spots in the crafting grid using a nested loop
                for y in range(2):
                    if self.crafting_grid[x][y][0] != 0:  # If the specific part of the crafting grid is not empty
                        if self.crafting_grid[x][y][
                            1] == 1:  # If there are only one item left in that spot on the crafting grid.
                            self.crafting_grid[x][y] = [0, 0]  # Reset spot to default values
                        else:  # If there are more than one item on the spot
                            self.crafting_grid[x][y][1] -= 1  # Remove one item

    # Calculates stacking based on the number of items in the slot and the number of item holding. This is a function because other inventories also require this
    # and by doing so allows for modular code development to prevent repetition
    def check_stacking(self, item, item_lib):
        if self.holding[0] != item[0] or item[1] == item_lib[item[0]][
            -1]:  # If the item holding does not stack to the one in the item slot becuase the two items are different
            previous_holding = self.holding[
                               :]  # Make a temporary variable to switch the item currently being in hand with the one in item slot
            self.holding = item[:]  # Changes the item that is in hand to the one in item slot
            return previous_holding

        else:  # If the items are the same
            calculate_stack = item_lib[item[0]][-1] - self.holding[1] - item[
                1]  # Calculates how much item is required for a full stack
            amount_holding = self.holding[1]

            if calculate_stack >= 0:  # If the item can be stacked
                self.holding = [0, 0]
                return [item[0], item[1] + amount_holding]
            else:  # If full stack
                self.holding = [item[0], abs(calculate_stack)]  # Switch the the stacks.
                return [item[0], item_lib[item[0]][-1]]

    # Add one item to the inventory slot
    def single_add(self, inv, item_lib):
        if self.holding[0] != 0 and inv[1] < item_lib[self.holding[0]][-1]:  # If the item can stack
            if self.holding[0] == inv[0] or inv[
                0] == 0:  # If the item in the inventory and the one in hand are the same
                inv[0] = self.holding[0]  # Set the item just in case
                self.holding[1] -= 1  # Subtract one from hand and add one to slot
                inv[1] += 1

        elif self.holding[0] == 0:  # If the user is not holding anything, get half of stack of items
            half = inv[1] // 2  # Gets half of the item in the slot

            self.holding = [inv[0], half]
            inv[1] -= half

        if self.holding[1] == 0:  # If the items in hand are all gone, set to default value
            self.holding = [0, 0]

        return inv

    def update(self, surf, mx, my, m_press, l_click, r_click, inventory, hotbar,
               item_lib):  # Renders the inventory along with all of the items and the crafting grid
        surf.blit(self.graphic, (self.x, self.y))

        for row in range(len(inventory)):  # Nested loops render the multi-dimensional lists
            for item in range(len(inventory[row])):
                if inventory[row][item][1] != 0:  # If there are items in the slot
                    surf.blit(item_lib[inventory[row][item][0]][1], (
                        self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))  # Render icon for the item/block
                    surf.blit(meh.text(str(inventory[row][item][1]), 10), (
                        self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))  # Render the text for the item

                if Rect((self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32)).collidepoint(mx,
                                                                                                 my):  # Collision detection for user feedback and selection
                    surf.blit(self.highlight, (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    if l_click:  # If left mouse button has been pressed, check the stacking
                        inventory[row][item] = self.check_stacking(inventory[row][item][:], item_lib)
                    elif r_click:
                        inventory[row][item] = self.single_add(inventory[row][item][:],
                                                               item_lib)  # Adds single block or get half

        for item in range(len(hotbar)):  # Same as above but with hotbar
            if hotbar[item][1] != 0:
                surf.blit(item_lib[hotbar[item][0]][1], (self.x + 16 + item * 36, self.y + 283, 32, 32))
                surf.blit(meh.text(str(hotbar[item][1]), 10), (self.x + 16 + item * 36, self.y + 283, 32, 32))

            if Rect((self.x + 16 + item * 36, self.y + 283, 32, 32)).collidepoint(mx, my):
                surf.blit(self.highlight, (self.x + 16 + item * 36, self.y + 283, 32, 32))

                if l_click:
                    hotbar[item] = self.check_stacking(hotbar[item][:], item_lib)
                elif r_click:
                    hotbar[item] = self.single_add(hotbar[item][:], item_lib)

        for row in range(len(self.crafting_grid)):  # Same as above but with crafting grid
            for item in range(len(self.crafting_grid[row])):
                if self.crafting_grid[row][item][1] != 0:
                    surf.blit(item_lib[self.crafting_grid[row][item][0]][1],
                              (self.w // 2 + 19 + 36 * item, self.h // 2 - 130 + 36 * row, 32, 32))
                    surf.blit(meh.text(str(self.crafting_grid[row][item][1]), 10),
                              (self.w // 2 + 19 + 36 * item, self.h // 2 - 130 + 36 * row, 32, 32))

                if Rect((self.w // 2 + 19 + 36 * item, self.h // 2 - 130 + 36 * row, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.w // 2 + 19 + 36 * item, self.h // 2 - 130 + 36 * row, 32, 32))
                    if l_click:
                        self.crafting_grid[row][item] = self.check_stacking(self.crafting_grid[row][item][:], item_lib)
                    elif r_click:
                        self.crafting_grid[row][item] = self.single_add(self.crafting_grid[row][item][:], item_lib)

        self.recipe_check()  # Check if the recipe if possible

        if self.resulting_item[0] != 0:  # I f the recipe is possible
            surf.blit(item_lib[self.resulting_item[0]][1], (self.w // 2 + 131, self.h // 2 - 110, 32, 32))
            surf.blit(meh.text(str(self.resulting_item[1]), 10), (self.w // 2 + 131, self.h // 2 - 110, 32, 32))

            if Rect((self.w // 2 + 131, self.h // 2 - 110, 32, 32)).collidepoint(mx,
                                                                                 my) and l_click:  # If the player wants the craft
                self.craft(item_lib)

        if self.holding[0] > 0:  # Blits the item that is in had if there is an item
            surf.blit(item_lib[self.holding[0]][1], (mx - 10, my - 10))  # Blits the number of items in hand
            surf.blit(meh.text(str(self.holding[1]), 10), (mx - 10, my - 10))


'''
The Crafting class contains the crafting bench screen graphics and all of the functions in it.
'''


class Crafting:
    def __init__(self, w,
                 h):  # Init function declares all of the variables and loads all of the graphics. w and h are the width and height of the screen
        self.graphic = image.load('textures/gui/crafting_table.png').convert_alpha()  # Loads the inventory graphic
        self.x, self.y = w // 2 - self.graphic.get_width() // 2, h // 2 - self.graphic.get_height() // 2
        self.w, self.h = w, h
        self.highlight = Surface((32, 32))
        self.highlight.fill((255, 255, 255))
        self.highlight.set_alpha(150)
        self.holding = [0, 0]

        self.crafting_grid = [[[0, 0] for _ in range(3)] for __ in
                              range(3)]  # Creates an empty crafting grid for crafting
        self.recipes = json.load(open('data/crafting.json'))

        meh.mehprint(self.recipes)  # Small printing function for debugging

        self.resulting_item = [0, 0]  # The results of the crafting

    def recipe_check(self):  # Same as the one in inventory class but with a 3x3 crafting grid
        current_recipe = [self.crafting_grid[x][y][0] for x in range(3) for y in range(3)]
        current_recipe = " ".join(list(map(str, current_recipe)))
        if current_recipe in self.recipes:
            self.resulting_item = [self.recipes[current_recipe]['result'], self.recipes[current_recipe]['quantity']]

        else:
            self.resulting_item = [0, 0]

    def craft(self, item_lib):  # Same as the one in inventory class but with a 3x3 crafting grid
        if self.resulting_item != [0, 0]:
            if self.holding[0] == 0:
                self.holding = self.resulting_item

            elif self.holding[0] == self.resulting_item[0] and self.holding[1] + self.resulting_item[1] <= \
                    item_lib[self.holding[0]][-1]:
                self.holding[1] += self.resulting_item[1]

            for x in range(len(self.crafting_grid)):
                for y in range(3):
                    if self.crafting_grid[x][y][0] != 0:
                        if self.crafting_grid[x][y][1] == 1:
                            self.crafting_grid[x][y] = [0, 0]
                        else:
                            self.crafting_grid[x][y][1] -= 1

    def check_stacking(self, item, item_lib):  # Same as the one in inventory
        if self.holding[0] != item[0] or item[1] == item_lib[item[0]][-1]:
            previous_holding = self.holding[:]
            self.holding = item[:]
            return previous_holding
        else:
            calculate_stack = item_lib[item[0]][-1] - self.holding[1] - item[1]
            amount_holding = self.holding[1]

            if calculate_stack >= 0:
                self.holding = [0, 0]
                return [item[0], item[1] + amount_holding]
            else:
                self.holding = [item[0], abs(calculate_stack)]
                return [item[0], item_lib[item[0]][-1]]

    def single_add(self, inv, item_lib):  # S ame as the single_add function in inventory.py
        if self.holding[0] != 0 and inv[1] < item_lib[self.holding[0]][-1]:
            if self.holding[0] == inv[0] or inv[0] == 0:
                inv[0] = self.holding[0]
                self.holding[1] -= 1
                inv[1] += 1

        elif self.holding[0] == 0:
            half = inv[1] // 2

            self.holding = [inv[0], half]
            inv[1] -= half

        if self.holding[1] == 0:
            self.holding = [0, 0]

        return inv

    def update(self, surf, mx, my, m_press, l_click, r_click, inventory, hotbar,
               item_lib):  # Everything in this update function is the smae as the one in inventory class but with a 3x3 crafting grid instead
        surf.blit(self.graphic, (self.x, self.y))

        for row in range(len(inventory)):
            for item in range(len(inventory[row])):
                if inventory[row][item][1] != 0:
                    surf.blit(item_lib[inventory[row][item][0]][1],
                              (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    surf.blit(meh.text(str(inventory[row][item][1]), 10),
                              (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                if Rect((self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    if l_click:
                        inventory[row][item] = self.check_stacking(inventory[row][item][:], item_lib)
                    elif r_click:
                        inventory[row][item] = self.single_add(inventory[row][item][:], item_lib)

        for item in range(len(hotbar)):
            if hotbar[item][1] != 0:
                surf.blit(item_lib[hotbar[item][0]][1], (self.x + 16 + item * 36, self.y + 283, 32, 32))

                surf.blit(meh.text(str(hotbar[item][1]), 10), (self.x + 16 + item * 36, self.y + 283, 32, 32))

            if Rect((self.x + 16 + item * 36, self.y + 283, 32, 32)).collidepoint(mx, my):
                surf.blit(self.highlight, (self.x + 16 + item * 36, self.y + 283, 32, 32))

                if l_click:
                    hotbar[item] = self.check_stacking(hotbar[item][:], item_lib)
                elif r_click:
                    hotbar[item] = self.single_add(hotbar[item][:], item_lib)

        for row in range(len(self.crafting_grid)):
            for item in range(3):
                if self.crafting_grid[row][item][1] != 0:
                    surf.blit(item_lib[self.crafting_grid[row][item][0]][1],
                              (self.x + item * 36 + 60, self.y + 36 * row + 33, 32, 32))

                    surf.blit(meh.text(str(self.crafting_grid[row][item][1]), 10),
                              (self.x + item * 36 + 60, self.y + 36 * row + 33, 32, 32))

                if Rect((self.x + item * 36 + 60, self.y + 36 * row + 33, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.x + item * 36 + 60, self.y + 36 * row + 34, 32, 32))

                    if l_click:
                        self.crafting_grid[row][item] = self.check_stacking(self.crafting_grid[row][item][:], item_lib)
                    elif r_click:
                        self.crafting_grid[row][item] = self.single_add(self.crafting_grid[row][item][:], item_lib)

        self.recipe_check()

        if self.resulting_item[0] != 0 and self.resulting_item[1] != 0:
            surf.blit(item_lib[self.resulting_item[0]][1], (self.x + 247, self.y + 69))
            surf.blit(meh.text(str(self.resulting_item[1]), 10), (self.x + 247, self.y + 69))

        if Rect((self.x + 247, self.y + 69, 32, 32)).collidepoint(mx, my):
            if l_click:
                self.craft(item_lib)

        if self.holding[0] > 0:
            surf.blit(item_lib[self.holding[0]][1], (mx - 10, my - 10))
            surf.blit(meh.text(str(self.holding[1]), 10), (mx - 10, my - 10))


'''
The Chest class contains the chest screen graphics and all of the functions in it.
'''


class Chest:
    def __init__(self, w, h):
        self.graphic = image.load('textures/gui/small_chest.png').convert_alpha()  # Loads graphics

        self.x, self.y = w // 2 - self.graphic.get_width() // 2, h // 2 - self.graphic.get_height() // 2
        self.w, self.h = w, h

        self.highlight = Surface((32, 32))
        self.highlight.fill((255, 255, 255))
        self.highlight.set_alpha(150)
        self.item_slots = []
        self.holding = [0, 0]

    def check_stacking(self, item, item_lib):  # Generic crafting function for stacking
        if self.holding[0] != item[0] or item[1] == item_lib[item[0]][-1]:
            previous_holding = self.holding[:]
            self.holding = item[:]
            return previous_holding
        else:
            calculate_stack = item_lib[item[0]][-1] - self.holding[1] - item[1]
            amount_holding = self.holding[1]

            if calculate_stack >= 0:
                self.holding = [0, 0]
                return [item[0], item[1] + amount_holding]
            else:
                self.holding = [item[0], abs(calculate_stack)]
                return [item[0], item_lib[item[0]][-1]]

    def single_add(self, inv, item_lib):  # Generic function for adding one item and getting half of the items
        if self.holding[0] != 0 and inv[1] < item_lib[self.holding[0]][-1]:
            if self.holding[0] == inv[0] or inv[0] == 0:
                inv[0] = self.holding[0]
                self.holding[1] -= 1
                inv[1] += 1

        elif self.holding[0] == 0:
            half = inv[1] // 2

            self.holding = [inv[0], half]
            inv[1] -= half

        if self.holding[1] == 0:
            self.holding = [0, 0]

        return inv

    def update(self, surf, mx, my, m_press, l_click, r_click, inventory, hotbar, chest_inv,
               item_lib):  # Update function takes in the chest inventory from the server side. This way one chest object can be used for all chests on the server
        surf.blit(self.graphic, (self.x, self.y))
        changed = [0, 0]  # A changed var keeps in track of whats changed so it can be sent to the server

        for row in range(len(chest_inv)):  # Generic rendering function for rendering the contents of the chest
            for item in range(len(chest_inv[row])):
                if chest_inv[row][item][1] != 0:
                    surf.blit(item_lib[chest_inv[row][item][0]][1],
                              (self.x + 15 + item * 36, self.y + 36 + row * 36, 32, 32))

                    surf.blit(meh.text(str(chest_inv[row][item][1]), 10),
                              (self.x + 15 + item * 36, self.y + 36 + row * 36, 32, 32))

                if Rect((self.x + 15 + item * 36, self.y + 36 + row * 36, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.x + 15 + item * 36, self.y + 36 + row * 36, 32, 32))

                    if l_click:
                        chest_inv[row][item] = self.check_stacking(chest_inv[row][item][:], item_lib)
                        changed = [8, 'chest', row, item,
                                   chest_inv[row][item]]  # Outputs changes in a format readable by the server
                    elif r_click:
                        chest_inv[row][item] = self.single_add(chest_inv[row][item][:], item_lib)
                        changed = [8, 'chest', row, item, chest_inv[row][item]]

        for row in range(len(inventory)):
            for item in range(len(inventory[row])):
                if inventory[row][item][1] != 0:
                    surf.blit(item_lib[inventory[row][item][0]][1],
                              (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    surf.blit(meh.text(str(inventory[row][item][1]), 10),
                              (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                if Rect((self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    if l_click:
                        inventory[row][item] = self.check_stacking(inventory[row][item][:], item_lib)
                    elif r_click:
                        inventory[row][item] = self.single_add(inventory[row][item][:], item_lib)

        for item in range(len(hotbar)):
            if hotbar[item][1] != 0:
                surf.blit(item_lib[hotbar[item][0]][1], (self.x + 16 + item * 36, self.y + 283, 32, 32))

                surf.blit(meh.text(str(hotbar[item][1]), 10), (self.x + 16 + item * 36, self.y + 283, 32, 32))

            if Rect((self.x + 16 + item * 36, self.y + 283, 32, 32)).collidepoint(mx, my):
                surf.blit(self.highlight, (self.x + 16 + item * 36, self.y + 283, 32, 32))

                if l_click:
                    hotbar[item] = self.check_stacking(hotbar[item], item_lib)

        if self.holding[0] > 0:
            surf.blit(item_lib[self.holding[0]][1], (mx - 10, my - 10))

        return changed  # Returns the new change so it can be sent to the server for updates


'''
The Furnace class contains the furnace screen graphics and all of the functions in it.
'''


class Furnace:
    def __init__(self, w, h):

        self.graphic = image.load('textures/gui/furnace.png').convert_alpha()
        self.toggle_image = image.load('textures/gui/flame.png').convert_alpha()  # The flame for when fuel is burning
        self.progress = image.load('textures/gui/progress.png').convert_alpha()  # The progress bar for added effects

        self.fuel = json.load(
            open("data/smelting_time.json"))  # The fuel burn time. All times are obtained from minecraft wiki
        self.recipes = json.load(open("data/smelting.json"))  # Smelting recipes

        self.x, self.y = w // 2 - self.graphic.get_width() // 2, h // 2 - self.graphic.get_height() // 2
        self.w, self.h = w, h

        self.highlight = Surface((32, 32))
        self.highlight.fill((255, 255, 255))
        self.highlight.set_alpha(150)
        self.item_slots = []
        self.holding = [0, 0]

        self.SMELT_TIME = 10  # The default amount of time to smelt an item in Seconds

    def check_stacking(self, item, item_lib):  # Generic function to check stacking
        if self.holding[0] != item[0] or item[1] == item_lib[item[0]][-1]:
            previous_holding = self.holding[:]
            self.holding = item[:]
            return previous_holding
        else:
            calculate_stack = item_lib[item[0]][-1] - self.holding[1] - item[1]
            amount_holding = self.holding[1]

            if calculate_stack >= 0:
                self.holding = [0, 0]
                return [item[0], item[1] + amount_holding]
            else:
                self.holding = [item[0], abs(calculate_stack)]
                return [item[0], item_lib[item[0]][-1]]

    def single_add(self, inv, item_lib):  # Generic function to add one item or to get half of the items in slot
        if self.holding[0] != 0 and inv[1] < item_lib[self.holding[0]][-1]:
            if self.holding[0] == inv[0] or inv[0] == 0:
                inv[0] = self.holding[0]
                self.holding[1] -= 1
                inv[1] += 1

        elif self.holding[0] == 0:
            half = inv[1] // 2

            self.holding = [inv[0], half]
            inv[1] -= half

        if self.holding[1] == 0:
            self.holding = [0, 0]

        return inv

    def calculate(self, smelted, item_lib):  # Function used to calculate the amount of fuel
        max_smelt = 0  # The default value for the max amount of items that can be smelted
        fuel_burned = 0  # The amount of fuel to delete

        if str(smelted[0][0]) in self.recipes and str(smelted[1][
                                                          0]) in self.fuel:  # If the item can be smelted and the item placed in the fuel slot is a fuel
            if smelted[2][0] == 0 or smelted[2][0] == self.recipes[str(smelted[0][0])][
                'result']:  # If there is no item in the results slot or the result slot has the same item as the result of the recipe being smelted
                max_smelt = min((smelted[1][1] * self.fuel[str(smelted[1][0])]['duration']) // self.SMELT_TIME,
                                smelted[0][1], item_lib[smelted[0][0]][2] - smelted[2][
                                    1])  # Calculating the max amount of items that can be smelted at this time. it takes the min of how many items
                # can be burned with the amount of fuel provided, the amount of item that can be smelted, and the amount of tiems that can be stacked
                fuel_burned = smelted[1][1] - ((10 * (max_smelt - 1) // self.fuel[str(smelted[1][0])][
                    'duration']) + 1)  # Get the amount of fuel that will be burned

        return max_smelt, fuel_burned

    def update(self, surf, mx, my, m_press, l_click, r_click, inventory, hotbar, smelted,
               item_lib):  # Update function takes the smelted list requested from the server
        # smelted = item, fuel, result  The list is in this format
        if len(smelted) > 0:  # If the server responded
            surf.blit(self.graphic, (self.x, self.y))  # blit furnace graphics
            items_smelted, fuel_burned = self.calculate(smelted, item_lib)  # Gets the calculations done
            if items_smelted > 0:  # If the items provided can be smelted
                smelted[0][1] -= items_smelted  # Remove items form the items smelted
                smelted[1][1] = fuel_burned  # Remove The amount of fuel
                smelted[2][0] = self.recipes[str(smelted[0][0])]['result']  # Set the resulting type to the result
                smelted[2][1] += items_smelted  # Sets the number of items smelted

                for item in range(len(smelted)):  # Double check to make sure non of the items are at 0 or no item
                    if smelted[item][0] == 0 or smelted[item][1] == 0:  # Reset to default value
                        smelted[item] = [0, 0]

            if smelted[2][0] > 0:  # If there if items smelted, blit the fuel burn and progress bar for effects
                surf.blit(self.progress, (self.x + 158, self.y + 69))
                surf.blit(self.toggle_image, (self.x + 113, self.y + 72))

            if smelted[0][0] != 0 and smelted[0][1] != 0:  # Item slot has item, blit item
                surf.blit(item_lib[smelted[0][0]][1], (self.x + 112, self.y + 34, 32, 32))
                surf.blit(meh.text(str(int(smelted[0][1])), 10), (self.x + 112, self.y + 34, 32, 32))
            if Rect((self.x + 112, self.y + 34, 32, 32)).collidepoint(mx, my):  # feedback and slectiong
                surf.blit(self.highlight, (self.x + 112, self.y + 34, 32, 32))
                if l_click:  # Generic stacking function
                    smelted[0] = self.check_stacking(smelted[0], item_lib)
                elif r_click:
                    smelted[0] = self.single_add(smelted[0], item_lib)

            if smelted[1][0] != 0 and smelted[1][1] != 0:  # Same as above but with fuel
                surf.blit(item_lib[smelted[1][0]][1], (self.x + 112, self.y + 106, 32, 32))
                surf.blit(meh.text(str(smelted[1][1] - fuel_burned), 10), (self.x + 112, self.y + 106, 32, 32))
            if Rect((self.x + 112, self.y + 106, 32, 32)).collidepoint(mx, my):
                surf.blit(self.highlight, (self.x + 112, self.y + 106, 32, 32))
                if l_click:
                    smelted[1] = self.check_stacking(smelted[1], item_lib)
                elif r_click:
                    smelted[1] = self.single_add(smelted[1], item_lib)

            if smelted[2][1] > 0:  # If item is smelted
                surf.blit(item_lib[smelted[2][0]][1], (self.x + 232, self.y + 70, 32, 32))
                surf.blit(meh.text(str(smelted[2][1]), 10), (self.x + 232, self.y + 70, 32, 32))
            if Rect((self.x + 232, self.y + 70, 32, 32)).collidepoint(mx, my):
                surf.blit(self.highlight, (self.x + 232, self.y + 70, 32, 32))
                if l_click and (self.holding[0] == smelted[2][0] or self.holding[
                    0] == 0):  # If the user clicked on the item and retrieving the item is possible
                    hold_stack = item_lib[smelted[2][0]][2] - self.holding[
                        1]  # Gets the amount of items needed to complete a whole stack with the items in hand
                    if smelted[2][
                        1] <= hold_stack:  # If there are less or equal in smelted that can make hand items to full stack
                        self.holding[1] += smelted[2][
                            1]  # Add the number of items in the results slot to the holding slot
                        self.holding[0] = smelted[2][0]  # Change the item type in hand
                        smelted[2] = [0, 0]
                    else:  # More items are in the results of the furnace than it takes to complete a full stack
                        self.holding[1] += hold_stack  # Add the amount of
                        self.holding[0] = smelted[2][0]
                        smelted[2][1] -= hold_stack  # Subtract the retrieved items

            for row in range(len(inventory)):  # Generic rendering functions
                for item in range(len(inventory[row])):
                    if inventory[row][item][1] != 0:
                        surf.blit(item_lib[inventory[row][item][0]][1],
                                  (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                        surf.blit(meh.text(str(inventory[row][item][1]), 10),
                                  (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                    if Rect((self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32)).collidepoint(mx, my):
                        surf.blit(self.highlight, (self.x + 15 + item * 36, self.y + 168 + row * 36, 32, 32))

                        if l_click:
                            inventory[row][item] = self.check_stacking(inventory[row][item][:], item_lib)
                        elif r_click:
                            inventory[row][item] = self.single_add(inventory[row][item][:], item_lib)

            for item in range(len(hotbar)):
                if hotbar[item][1] != 0:
                    surf.blit(item_lib[hotbar[item][0]][1], (self.x + 16 + item * 36, self.y + 283, 32, 32))

                    surf.blit(meh.text(str(hotbar[item][1]), 10), (self.x + 16 + item * 36, self.y + 283, 32, 32))

                if Rect((self.x + 16 + item * 36, self.y + 283, 32, 32)).collidepoint(mx, my):
                    surf.blit(self.highlight, (self.x + 16 + item * 36, self.y + 283, 32, 32))

                    if l_click:
                        hotbar[item] = self.check_stacking(hotbar[item], item_lib)
                    elif r_click:
                        hotbar[item] = self.single_add(hotbar[item], item_lib)

            if self.holding[0] > 0:
                surf.blit(item_lib[self.holding[0]][1], (mx - 10, my - 10))
