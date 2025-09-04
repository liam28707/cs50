import itertools
import random
import copy


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (
            len(self.cells) == self.count
        ):  # If number of cells is the same as is the count of mines then all cells are mines.
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (
            self.count == 0
        ):  # If there are no neighbouring mines then it means that the particular cells is safe
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if (
            cell in self.cells
        ):  # self.cells has a count value and unless it is 0 there is a mine,
            # so when count is decremented then it shows a mine is found
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if (
            cell in self.cells
        ):  # If the cell is in the set, remove it to mark it as safe.
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # print("Adding knowledge for cell:", cell)

        self.moves_made.add(
            cell
        )  # Marking the cell in which a move has been made and adding to it
        self.mark_safe(cell)  # mark the cell safe and add it to the knowledge base

        """ADD SENTENCE TO KNOELEDGE BASE"""
        # Set for neighboring cells
        neighbour = set()

        # Looping through adjacent cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbour_x = cell[0] + i
                neighbour_y = cell[1] + j
                adj = (neighbour_x, neighbour_y)
                if adj in self.mines:
                    count -= 1
                elif self.valid(neighbour_x, neighbour_y) and self.unclicked(adj):
                    neighbour.add(adj)
        new_sent = Sentence(neighbour, count)
        # print("Adding new sentence to knowledge base:", new_sent)
        if new_sent not in self.knowledge:
            self.knowledge.append(new_sent)

        """ MARKING ADDITIONAL CELLS AS SAFE OR A MINE IF IT CAN BE INFERRED"""
        while True:
            sentences_to_remove = []
            for sentence in self.knowledge:
                cells_copy = sentence.cells.copy()
                if sentence.count == len(cells_copy):
                    for cell in cells_copy:
                        self.mark_mine(cell)
                    sentences_to_remove.append(sentence)
                elif sentence.count == 0:
                    for cell in cells_copy:
                        self.mark_safe(cell)
                    sentences_to_remove.append(sentence)
            for sentence in sentences_to_remove:
                self.knowledge.remove(sentence)
            if len(sentences_to_remove) == 0:
                break

        """ ADDING NEW SENTENCES TO KNOWLEDGE BASE IF IT CAN BE INFERRED """
        new_sentences = []
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence1 = self.knowledge[i]
                sentence2 = self.knowledge[j]

                # if sentence1 is a subset of sentence2
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count

                    # Form new sentence
                    new_sentence = Sentence(new_cells, new_count)

                    if new_sentence not in self.knowledge:
                        new_sentences.append(new_sentence)
        self.knowledge.extend(new_sentences)
        # if new_sentences:
        #  print("Adding new sentences to knowledge base:", new_sentences)

    # Function to see if cell is a valid cell
    def valid(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    # Function for non-explored cell
    def unclicked(self, cell):
        x, y = cell
        if self.valid(x, y) and cell not in self.mines and cell not in self.safes:
            return True
        return False

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes - self.moves_made:
            return cell
        return None  # If no safe move exists

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = set()  # Total number of moves possible
        for i in range(8):
            for j in range(8):
                moves.add((i, j))

        # Find all safe moves
        valid_moves = moves - self.moves_made - self.mines
        if valid_moves:
            # get random safe move
            rand_move = random.choice(list(valid_moves))
            return rand_move
        # If there arent any safe moves, find all mines that can be flagged
        flag_mines = set()
        for sentence in self.knowledge:
            if sentence.count == len(sentence.cells):
                for cell in sentence.cells:
                    flag_mines.add(cell)
        # Flag a random mine
        if flag_mines:
            return random.choice(list(flag_mines))
        # If no safe moves or mines to be flagged
        return None
