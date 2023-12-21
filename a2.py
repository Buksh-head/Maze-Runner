from __future__ import annotations
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *


__author__ = "<Adnaan Buksh>, <47435568>"
__email__ = "<adnaan.buksh@uqconnect.edu.au>"
__version__ = 1.1


ZERO = 0
ONE = 1
TIME_TO_CHANGE = 5
NEW_LINE = '\n'
ENTITY = 'E'
NO_ITEM = "No item with that name!"
ITEMS_NAME = ['Water', 'Honey', 'Coin', 'Potion', 'Apple']
ITEMS = [WATER, HONEY, COIN, POTION, APPLE]
USABLE_NAME = ['Water', 'Honey', 'Potion', 'Apple']
USABLE = [WATER, HONEY, POTION, APPLE]
BLOCKS = [WALL, LAVA, COIN, DOOR, EMPTY]


def load_game(filename: str) -> list['Level']:
    """ Reads a game file and creates a list of all the levels in order.

    Parameters:
        filename: The path to the game file

    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels


class Tile:
    """Represents the floor for a (row, column) position.
    """
    def __init__(self):
        """All Class have an initializer which sets run as the Class is
           created, and the variables are assigned a value
        """
        self._is_blocking = False
        self._damage = ZERO
        self._id = ABSTRACT_TILE

    def is_blocking(self) -> bool:
        """Displays if the tile is occupiable

        Returns:
             bool: Returns true if user can move onto that position occupied,
                   default False
        """
        return self._is_blocking

    def damage(self) -> int:
        """Returns the damage done to a player if they step on this tile

        Returns:
            int: Amount of damage that block does, default = 0
        """
        return self._damage

    def get_id(self) -> str:
        """
        Returns:
            str: Returns the ID of the tile.
        """
        return self._id

    def __str__(self) -> str:
        """
        Returns:
            str: Returns of the ID of the tile, encapsulated in
                 quotation marks
        """
        return self._id

    def __repr__(self) -> str:
        """Returns the text that would be required to create a new
           instance of this class.

        Returns:
            str: Name of the Class
        """
        return f'{type(self).__name__}()'


class Wall(Tile):
    """
    Type of tile that inherits from Tile and redefined variables
    """
    def __init__(self):
        super().__init__()
        self._is_blocking = True
        self._id = WALL


class Empty(Tile):
    """
    Type of tile that inherits from Tile and redefined variables
    """
    def __init__(self):
        super().__init__()
        self._id = EMPTY


class Lava(Tile):
    """
    Type of tile that inherits from Tile and redefined variables
    """
    def __init__(self):
        super().__init__()
        self._damage = LAVA_DAMAGE
        self._id = LAVA


class Door(Tile):
    """
    Type of tile that inherits from Tile and redefined variables
    """
    def __init__(self):
        super().__init__()
        self._is_blocking = True
        self._id = DOOR

    def unlock(self):
        """Unlocks the door.
        """
        super().__init__()
        self._id = EMPTY


class Entity(object):
    """Provides base functionality for all entities in the game."""
    def __init__(self, position: tuple[int, int]) -> None:
        """
        Parameters:
            position (tuple[int, int]): Sets up this entity at the
                                        given (row, column) position.
        """
        self._position = position
        self._id = ENTITY

    def get_position(self) -> tuple[int, int]:
        """
        Returns:
            tuple[int, int]: Returns this entities (row, column) position.
        """
        return self._position

    def get_name(self) -> str:
        """
        Returns:
            str: Returns the name of the class to which this entity belongs.
        """
        return f'{type(self).__name__}'

    def get_id(self) -> str:
        """
        Returns:
            str: Returns the ID of this entity
        """
        return self._id

    def __str__(self) -> str:
        """Returns the string representation for this entity

        Returns:
            str: ID in quotation marks
        """
        return self._id

    def __repr__(self) -> str:
        """Returns the text that would be required to make a new
           instance of this class

        Returns:
            str: the name of the Class and position
        """
        return f'{type(self).__name__}({self._position})'


class DynamicEntity(Entity):
    """DynamicEntity is an abstract class which provides base functionality
       for special types of Entities that are dynamic

       Inherits functionality from Entity
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = DYNAMIC_ENTITY

    def set_position(self, new_position: tuple[int, int]) -> None:
        """Updates the DynamicEntity position
        """
        self._position = new_position


class Player(DynamicEntity):
    """Player is a DynamicEntity that is controlled by the user

       Inherits functionality from DynamicEntity
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = PLAYER
        self._hunger = ZERO
        self._thirst = ZERO
        self._health = MAX_HEALTH
        self._inventory = []
        self._player_inv = Inventory(self._inventory)

    def get_hunger(self) -> int:
        """
        Returns:
            int: Returns the players current hunger level
        """
        return self._hunger

    def get_thirst(self) -> int:
        """
        Returns:
            int: Returns the players current thirst level.
        """
        return self._thirst

    def get_health(self) -> int:
        """
        Returns:
            int: the players current Health level.
        """
        return self._health

    def change_hunger(self, amount: int) -> None:
        """Alters the players hunger level by the given amount.
        """
        self._hunger = self._hunger + amount
        # Alters players hunger to be between 0 and its max amount
        if self._hunger < ZERO:
            self._hunger = ZERO

        elif self._hunger > MAX_HUNGER:
            self._hunger = MAX_HUNGER

    def change_thirst(self, amount: int) -> None:
        """Alters the players thirst level by the given amount.
        """
        self._thirst = self._thirst + amount

        if self._thirst < ZERO:
            self._thirst = ZERO

        elif self._thirst > MAX_THIRST:
            self._thirst = MAX_THIRST

    def change_health(self, amount: int) -> None:
        """Alters the players health level by the given amount.
        """
        self._health = self._health + amount

        if self._health > MAX_HEALTH:
            self._health = MAX_HEALTH

        elif self._health < ZERO:
            self._health = ZERO

    def get_inventory(self) -> Inventory:
        """Returns the players Inventory instance.

        Returns:
            Inventory: Sets up the Inventory Class for the PLayer
        """
        return self._player_inv

    def add_item(self, item: Item) -> None:
        """Adds the given item to the players Inventory instance.
        """
        self._player_inv.add_item(item)


class Item(Entity):
    """Subclass of Entity which provides base functionality for all items
       in the game.

       Inherits functionality from Entity
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = ITEM

    def apply(self, player: Player) -> None:
        """Applies the items effect, if any, to the given player.

        Parameters:
            player (Player): The player that the item takes effect on

        Raises:
            NotImplementedError: If no effect is applied
                                 Else applies the change
        """
        raise NotImplementedError


class Potion(Item):
    """A potion is an item that increases the players HP

       Inherits functionality from Item
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = POTION

    def apply(self, player: Player) -> None:
        # Run the change health def in player Class
        player.change_health(POTION_AMOUNT)


class Coin(Item):
    """A coin is an item that has no effect when applied

       Inherits functionality from Item
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = COIN

    def apply(self, player: Player) -> None:
        return None


class Water(Item):
    """Water is an item that will decrease the players thirst

       Inherits functionality from Item
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = WATER

    def apply(self, player: Player) -> None:
        player.change_thirst(WATER_AMOUNT)


class Food(Item):
    """Method that decreases the players hunger

       Inherits functionality from Item
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = FOOD
        self._food_amount = 0

    def apply(self, player: Player) -> None:
        player.change_hunger(self._food_amount)


class Apple(Food):
    """Apple is a type of food that decreases the players hunger
       
       Inherits functionality from Food
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = APPLE
        self._food_amount = APPLE_AMOUNT


class Honey(Food):
    """Honey is a type of food that decreases the players hunger
       
       Inherits functionality from Food
    """
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self._id = HONEY
        self._food_amount = HONEY_AMOUNT


class Inventory:
    """An Inventory contains and manages a collection of items."""
    def __init__(self, initial_items: Optional[list[Item, ...]] = None) -> None:
        """
        Parameters:
            initial_items (Optional[list[Item, ...]]): Adds initial items to
                                                       players inventory
            Defaults to None.
        """
        self._inventory = {}

        if initial_items is not None:
            for items in initial_items:
                self.add_item(items)

    def add_item(self, item: Item) -> None:
        """Adds the given item to this inventories collection of items.

        Parameters:
            item (Item): Item collected
        """
        # Adds given item in a dictionary
        # First checks if item type is already in dictionary, then adds
        # otherwise adds to dictionary
        if item.get_name() in self._inventory.keys():
            # \ is used so the rest of the line can go to the next line
            # and not go pass the character limit
            self._inventory[item.get_name()] = \
                self._inventory[item.get_name()] + [item]

        else:
            self._inventory.update({item.get_name(): [item]})

    def get_items(self) -> dict[str, list[Item, ...]]:
        """
        Returns:
            dict[str, list[Item, ...]]: a dictionary mapping the names of all
                                        items in the inventory to lists
                                        containing each instance of the item
                                        with that name
        """
        return self._inventory

    def remove_item(self, item_name: str) -> Optional[Item]:
        """Removes and returns the first instance of the item from the inventory

        Parameters:
            item_name (str): item that need to be removed

        Returns:
            Optional[Item]: First instance of item_name from inventory
        """
        # removes the first instance of item from dictionary
        # then checks if the item type contains nothing
        # if it contains no iteam eg (Water(2,3)) item type is deleted
        if item_name in self._inventory:
            removed_item = self._inventory[item_name].pop(0)

            if len(self._inventory[item_name]) == 0:
                self._inventory.pop(item_name)

            return removed_item

    def __str__(self) -> str:
        """
        Returns:
            str: a string containing information about quantities 
                 of items available in the inventory
        """
        self._combined_inventory = []

        for items in self._inventory.keys():
            self._combined_inventory.append\
                (f'{items}: {len(self._inventory[items])}')

        return f"{NEW_LINE.join(self._combined_inventory)}"

    def __repr__(self) -> str:
        """Returns a string that could be used to construct a new
           instance of Inventory containing the same items

        Returns:
            str: Name of the Class with list of items in inventory 
        """
        return f'{type(self).__name__}(initial_items={self._inventory})'


class Maze:
    """A Maze instance represents the space in which a level takes place."""
    def __init__(self, dimensions: tuple[int, int]) -> None:
        """Sets up an empty maze of given dimensions

        Parameters:
            dimensions (tuple[int, int]): number of rows and columns
        """
        self._dimensions = dimensions
        self._row = dimensions[1]
        self._column = dimensions[0]
        self._new_row = []
        self._tile = []
        self._maze = []
        self._tiles = []
        # Sets up the classes
        self._wall = Wall()
        self._door = Door()
        self._lava = Lava()
        self._empty = Empty()

    def get_dimensions(self) -> tuple[int, int]:
        """
        Returns:
            tuple[int, int]: the (#rows, #columns) in the maze.
        """
        return self._dimensions

    def add_row(self, row: str) -> None:
        """Adds a row of tiles to the maze.

        Parameters:
            row (str): the row of the maze
        
        Precondition:
            addition of a row must not violate the maze dimensions.
        """
        self._tile = []

        # Checks if it violates dimensions
        # for each letter in given row the ID and Tile Type are
        # added in 2 lists
        if len(row) == self._row and len(self._maze) <= self._column:
            for char in row:
                if char == WALL:
                    self._new_row.append(self._wall.get_id())
                    self._tile.append(self._wall)

                elif char == DOOR:
                    self._new_row.append(self._door.get_id())
                    self._tile.append(self._door)

                elif char == LAVA:
                    self._new_row.append(self._lava.get_id())
                    self._tile.append(self._lava)

                else:
                    self._new_row.append(self._empty.get_id())
                    self._tile.append(self._empty)

        self._tiles.append(self._tile)
        self._maze.append(''.join(self._new_row))
        self._new_row.clear()

    def get_tiles(self) -> list[list[Tile]]:
        """
        Returns:
            list[list[Tile]]: Returns the Tile instances in this maze.
        """
        return self._tiles

    def unlock_door(self) -> None:
        """Unlocks any doors that exist in the maze
        """
        self._door.unlock()  # Updates the Door() Class
        count = ZERO

        # iterates through each row and changes the ID
        # representation to Empty

        for row in self._maze:
            if DOOR in row:
                self._maze[count] = row.replace(DOOR, EMPTY)

            count = count + ONE  # The number of the row

    def get_tile(self, position: tuple[int, int]) -> Tile:
        """Returns the Tile instance at the given position.

        Precondition:
            position (tuple[int, int]): given position (row, column)

        Returns:
            Tile: Type of Tile
        """
        return self._tiles[position[0]][position[1]]

    def __str__(self) -> str:
        """
        Returns:
            str: Returns the string representation of this maze
        """
        return NEW_LINE.join(self._maze)

    def __repr__(self) -> str:
        """Returns a string that could be copied and pasted to construct a
           new Maze instance with the same dimensions as this Maze instance

        Returns:
            str: Class name with its dimensions
        """
        return f'{type(self).__name__}({self._dimensions})'


class Level:
    """A Level instance keeps track of both the maze and the non-player
       entities placed on the maze for a single level."""
    def __init__(self, dimensions: tuple[int, int]) -> None:
        """Sets up a new level with empty maze using the given dimensions.

        Parameters:
            dimensions (tuple[int, int]): dimensions of the maze (row, column)
        """
        self._dimensions = dimensions
        self._row = dimensions[1]
        self._column = dimensions[0]
        self._items = {}
        self._has_coin = []
        self._row_count = ZERO
        self._start = None
        self._maze = Maze(self._dimensions)

    def get_maze(self) -> Maze:
        """
        Returns:
            Maze: Returns the Maze instance for this level.
        """
        return self._maze

    def attempt_unlock_door(self) -> None:
        """Unlocks the doors in the maze if there are no coins remaining.
        """
        # puts all the values from dictionary in a list
        # checks that list if it doesn't contain coin
        for item in self._items.values():
            self._has_coin.append(item.get_id())

        if COIN not in self._has_coin:
            self._maze.unlock_door()

        self._has_coin = []

    def add_row(self, row: str) -> None:
        """Adds the tiles and entities from the row to this level.

        Parameters:
            row (str): row of maze
        """
        column_num = ZERO

        # iterates through row and gets the entities and assigns it a class
        # the walls in the row are added using the def from the Maze class
        for char in row:
            position = self._row_count, column_num

            if char in ITEMS:
                self.add_entity(position, char)

            elif char == PLAYER:
                self.add_player_start(position)

            column_num = column_num + ONE

        self._row_count = self._row_count + ONE  # Keeps track of row
                                                 # in this maze
        self._maze.add_row(row)

    def add_entity(self, position: tuple[int, int], entity_id: str) -> None:
        """Adds a new entity to this level in the given position.

        Parameters:
            position (tuple[int, int]): (row, column) position on maze
            entity_id (str): item on maze to be collected
        """
        if entity_id == POTION:
            self._items[position] = Potion(position)

        elif entity_id == HONEY:
            self._items[position] = Honey(position)

        elif entity_id == APPLE:
            self._items[position] = Apple(position)

        elif entity_id == WATER:
            self._items[position] = Water(position)

        elif entity_id == COIN:
            self._items[position] = Coin(position)

    def get_dimensions(self) -> tuple[int, int]:
        """
        Returns:
            tuple[int, int]: Returns the (#rows, #columns) in the level maze.
        """
        return self._dimensions

    def get_items(self) -> dict[tuple[int, int], Item]:
        """
        Returns:
            dict[tuple[int, int], Item]: a mapping from position to the Item
                                         at that position for all items
                                         currently in this level.
        """
        return self._items

    def remove_item(self, position: tuple[int, int]) -> None:
        """Deletes the item from the given position

        Parameters:
            position (tuple[int, int]): Position (#rows, #columns) of item
            to be removed

        Precondition:
            There is an Item instance at the position
        """
        self._items.pop(position)

    def add_player_start(self, position: tuple[int, int]) -> None:
        """Adds the start position for the player in this level.

        Parameters:
            position (tuple[int, int]): Position (#rows, #columns) of player
            on maze
        """
        self._start = position

    def get_player_start(self) -> Optional[tuple[int, int]]:
        """
        Returns:
            Optional[tuple[int, int]]: Returns the starting position of
                                       the player for this level.
        """
        return self._start

    def __str__(self) -> str:
        """
        Returns:
            str: a string representation of this level.
        """
        return f'Maze: {Maze.__str__(self._maze)}\nItems: ' \
               f'{self._items}\nPlayer start: {self._start}'

    def __repr__(self) -> str:
        """Returns a string that could be copied and pasted to construct a
           new Level instance with the same dimensions as this Level instance.

        Returns:
            str: Name of the Class and its dimension
        """
        return f'{type(self).__name__}({self._dimensions})'


class Model:
    """Used to understand and mutate the game state. Keeps track of a Player,
       and multiple Level instances. Provides the interface through which the
        controller can request information about the game state, and request
        changes to the game state.
    """
    def __init__(self, game_file: str) -> None:
        """Sets up the model from the game file

        Parameters:
            game_file (str): contains game information
        """
        self._game_file = game_file
        self._levels = load_game(self._game_file)
        self._won = False
        self._lost = False
        self._level_up = False
        self._current_level = ZERO
        self._valid_move = ZERO
        self._max_level = len(self._levels) - ONE  # Compensates due to lists
                                                   # starting from zero
        # Gets players position from maze
        self._player = Player(Model.get_level(self).get_player_start())

    def has_won(self) -> bool:
        """ A game has been won if all the levels have been successfully
            completed

        Returns:
            bool: True if game has been won. Default False
        """
        return self._won

    def has_lost(self) -> bool:
        """
        Returns:
            bool: True if game has been lost. Default False
        """
        stats = list(self.get_player_stats())

        # Checks if stats are out of limit to end game
        if stats[0] <= ZERO or stats[1] >= MAX_HUNGER \
                or stats[2] >= MAX_THIRST:
            self._lost = True

        return self._lost

    def get_level(self) -> Level:
        """
        Returns:
            Level: the current level
        """
        return self._levels[self._current_level]

    def level_up(self) -> None:
        """Changes the level to the next level in the game.
           If no more levels remain, the player has won the game.
        """
        # Checks if current level is the last one and activates game won
        # Otherwise updates level and gets new player position
        if self._current_level == self._max_level:
            self._won = True

        else:
            self._current_level = self._current_level + ONE
            self._level_up = True
            start_pos = self.get_level().get_player_start()
            self._player.set_position(start_pos)

    def did_level_up(self) -> bool:
        """
        Returns:
            bool: True if player moved to next level on the previous turn.
                  Default False
        """
        return self._level_up

    def move_player(self, delta: tuple[int, int]) -> None:
        """Tries to move the player by the requested (row, column) change

        Parameters:
            delta (tuple[int, int]): Requested player movement
        """
        cur_pos = self._player.get_position()
        # current x, y pos plus movement x,y
        new_pos = (cur_pos[0] + delta[0],
                   cur_pos[1] + delta[1])

        # tries to get tile for the next position
        # if it is out of the scope of dimension
        # which can only happen when moving out of maze from door
        # activates level up

        try:
            self.get_current_maze().get_tile(new_pos)
            next_tile = self.get_current_maze().get_tile(new_pos)

            if not next_tile.is_blocking():
                self._player.set_position(new_pos)
                self._player.change_health(-ONE)
                self._player.change_health(-(next_tile.damage()))
                self._valid_move = self._valid_move + ONE
                self.get_level().attempt_unlock_door()

                if new_pos in Model.get_current_items(self):
                    Model.attempt_collect_item(self, new_pos)

                # every five moves updates thirst and hunger
                if self._valid_move == TIME_TO_CHANGE:
                    self._player.change_hunger(ONE)
                    self._player.change_thirst(ONE)
                    self._valid_move = ZERO
        except:
            self.level_up()

    def attempt_collect_item(self, position: tuple[int, int]) -> None:
        """Collects the item at the given position if one exists.

        Parameters:
            position (tuple[int, int]): (row, column) of player position
        """

        self._player.add_item(self.get_level().get_items().get(position))
        self.get_level().remove_item(position)
        self.get_level().attempt_unlock_door()

    def get_player(self) -> Player:
        """
        Returns:
            Player: Returns the player in the game, with its position
        """
        return self._player

    def get_player_stats(self) -> tuple[int, int, int]:
        """
        Returns:
            tuple[int, int, int]: Returns the players current stats
        """
        health = self._player.get_health()
        hunger = self._player.get_hunger()
        thirst = self._player.get_thirst()
        return health, hunger, thirst

    def get_player_inventory(self) -> Inventory:
        """
        Returns:
            Inventory: Returns the players inventory.
        """
        return self._player.get_inventory()

    def get_current_maze(self) -> Maze:
        """
        Returns:
            Maze: Returns the Maze for the current level.
        """
        return self.get_level().get_maze()

    def get_current_items(self) -> dict[tuple[int, int], Item]:
        """
        Returns:
            dict[tuple[int, int], Item]: a dictionary mapping tuple positions
                                         to the item that currently exists at
                                         that position on the maze.
        """
        return self.get_level().get_items()

    def __str__(self) -> str:
        """
        Returns:
            str: __repr__ in quotation marks
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns:
            str: the text required to construct a new instance of Model
                 with the same game file used to construct self
        """
        return f"{type(self).__name__}('{self._game_file}')"


class MazeRunner:
    def __init__(self, game_file: str, view: UserInterface) -> None:
        """Creates a new MazeRunner game with the given view and a new Model
           instantiated using the given game file.

        Parameters:
            game_file (str): contains game information
            view (UserInterface): Abstract class providing an interface
                                  for any MazeRunner View class.
        """
        self._model = Model(game_file)
        self._player_inv = self._model.get_player_inventory().get_items()
        self._finished = False
        self.display()
        self._view = view

    def display(self):
        """Gets the text display for the Game
        """
        TextInterface().draw(self._model.get_current_maze(),
                             self._model.get_current_items(),
                             self._model.get_player().get_position(),
                             self._model.get_player_inventory(),
                             self._model.get_player_stats())

    def play(self) -> None:
        """Executes the entire game until a win or loss occurs
        """
        # Loop continues till game lost or won
        while not self._finished:
            not_usable = True
            print()
            move = input("Enter a move: ")

            if 'i ' in move:  # Checks if move is "i xxxx"
                for item in USABLE_NAME:  # Checks if  "xxxx" part is an item
                    if item in move:  # Checks if item was in user input
                                      # Applies the item to the player
                        not_usable = False
                        if item in self._player_inv.keys():
                            item_pos = self._player_inv[item][0].get_position()

                            if item == USABLE_NAME[0]:
                                Water(item_pos).apply(self._model.get_player())

                            elif item == USABLE_NAME[1]:
                                Honey(item_pos).apply(self._model.get_player())

                            elif item == USABLE_NAME[2]:
                                Potion(item_pos).apply(self._model.get_player())

                            elif item == USABLE_NAME[3]:
                                Apple(item_pos).apply(self._model.get_player())

                            self._model.get_player_inventory().remove_item(item)

                        else:  # if item not in players inventory executes this
                            print(ITEM_UNAVAILABLE_MESSAGE)

                if not_usable:  # if Item not an real item
                    print()
                    print(NO_ITEM)
                    print()

                self.display()

            # if valid move updates player position
            # Checks if the game has been won or lost
            elif move in MOVE_DELTAS:
                self._model.move_player(MOVE_DELTAS[move])

                if self._model.has_lost() is True:
                    self._finished = True
                    print(LOSS_MESSAGE)
                    break

                elif self._model.has_won() is True:
                    self._finished = True
                    print(WIN_MESSAGE)
                    break

                self.display()


def main():
    """Gets game file from user and then sets up Maze runner class with
       given text file
    """
    given_file = input("Enter game file: ")
    MazeRunner(given_file, UserInterface()).play()


if __name__ == '__main__':
    main()
