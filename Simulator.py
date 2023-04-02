import random
import time
import pygame
HEIGHT = 800
WIDTH = 600
ROWS = 100
COLS = 100
WHITE = (255, 255, 255)
HEADERS = [("Non Infected", (0, 255, 0)), ("Infected", (255, 0, 0))]
EXTENSION_FOR_TEXT = 100
INFECTED = "Infected"
NON_INFECTED = "Non Infected"


def create_matrix(rows, cols):
    """Create a matrix of the specified size with all elements initialized to None.

    Args:
        rows (int): The number of rows in the matrix.
        cols (int): The number of columns in the matrix.

    Returns:
        list: A two-dimensional list representing the matrix.

    """
    matrix = []
    for r in range(rows):
        row = []
        for col in range(cols):
            row.append(None)
        matrix.append(row)
    return matrix


def spread_rumor(person_position, matrix):
    """
    Spreads a rumor to a person in the given position of the matrix.

    Args:
        person_position (tuple): A tuple containing the row and column indexes of the person to spread the rumor to.
        matrix (list): A 2D list of Person objects representing the population.

    Returns:
        int: 1 if the person in the given position was successfully infected, 0 otherwise.
    """
    row = person_position[0]
    column = person_position[1]
    if matrix[row][column].state == NON_INFECTED:
        matrix[row][column].state = INFECTED
        return 1
    return 0


class Person:
    def __init__(self, skepticism_level, position, state):
        """
        Initializes a Person object.

        Args:
            level_of_skepticism (int): The initial level of skepticism of the person.
            position (tuple): The (y, x) position of the person on the screen.
            state (int): The initial state of the person (either susceptible, infected, or recovered).
        """
        self.skepticism_level = skepticism_level
        self.state = state
        self.position = position
        self.color_infected = (255, 0, 0)
        self.color_not_infected = (0, 255, 0)
        self.stop_spreading_duration = 0
        self.generation = 0
        self.move_set = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.original_skepticism_level = skepticism_level
        self.rumors_counter = 0

    def draw(self, surface, distance):
        """
        Draw the person on the given surface.

        Args:
            surface: pygame.Surface object to draw the person on
            distance: distance between each person on the surface
        """
        if self.state == INFECTED:
            color = self.color_infected
        else:
            color = self.color_not_infected
        y, x = self.position
        size = WIDTH // 200
        pygame.draw.rect(surface, color, (x * distance, y * distance + EXTENSION_FOR_TEXT, size, size))

    def get_adjacent_positions(self):
        """
        Get the adjacent positions of the person based on their current position and move set.

        Returns:
            A list of adjacent positions (tuples).
        """
        r, c = self.position
        moves = []
        for row, col in self.move_set:
            moves.append(((r + row) % ROWS, (c + col) % COLS))
        return moves

    def update(self):
        """
        Update the state of the person. If the person is currently in the "stop_spreading" state,
        decrement the duration of the state. Otherwise, do nothing.
        """
        if self.stop_spreading_duration > 0:
            self.stop_spreading_duration -= 1


class Simulation:
    def __init__(self, parameters):
        self.rows = ROWS
        self.cols = COLS
        self.generation = 0
        self.infected_persons = 0
        self.matrix = create_matrix(self.rows, self.cols)
        self.p_population_density = parameters.get("p_population_density")
        self.num_persons = int(ROWS * COLS * self.p_population_density)
        self.p_s1 = parameters.get("p_s1")
        self.p_s2 = parameters.get("p_s2")
        self.p_s3 = parameters.get("p_s3")
        self.p_s4 = parameters.get("p_s4")
        self.l_generation = parameters.get("l_generation")
        self.name = parameters.get("name")
        self.persons = []
        self.info = []
        self.init_simulation()

    def add_person(self, position, p_type, state):
        """
        Adds a new Person to the matrix at the given position with the given
        level of skepticism and state.
        """
        row = position // self.rows
        col = position % self.cols
        person = Person(p_type, (row, col), state)
        self.matrix[row][col] = person
        self.persons.append(person)

    def init_simulation(self):
        # getting random numbers to represent the place in the matrix the cell get
        cells_pos = random.sample(range(self.rows * self.cols), self.num_persons)
        probabilities = [self.p_s1, self.p_s2, self.p_s3, self.p_s4]
        random_person = random.choice(cells_pos)
        for position in cells_pos:
            type_of_person = random.choices(range(1, 5), weights=probabilities)[0]
            if position == random_person:
                # spreading person
                self.add_person(position, type_of_person, INFECTED)
                self.infected_persons += 1
            else:
                self.add_person(position, type_of_person, NON_INFECTED)

    def simulate(self, win, large_font, small_font):
        run = True
        while run:
            # making sure the simulation not run to fast
            time.sleep(0.2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            self.render(win, large_font, small_font)
            self.update()
            if self.generation > 170:
                run = False
        return self.info

    def render(self, win, large_font, small_font):
        # rendering the screen with white color
        pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT))
        # render simulation name
        simulation_name_text = large_font.render("Simulation Name : " + self.name, 1, (100, 100, 100))
        win.blit(simulation_name_text, ((WIDTH - simulation_name_text.get_width()) // 2, 0))
        # how spaces is the headers for each other
        different = 40
        x = 0
        # blit legend to the window
        for text, color in HEADERS:
            text_box = large_font.render(text, 1, color)
            win.blit(text_box, (x + different, EXTENSION_FOR_TEXT // 2))
            x += different + text_box.get_width()
        # blit generation number to window
        gen_text = large_font.render(f"Generation number : {self.generation}", 1, (100, 100, 100))
        win.blit(gen_text, ((WIDTH - gen_text.get_width()) // 2, EXTENSION_FOR_TEXT + 200 * (WIDTH // 200)))
        # blit the parameters to the window
        parameters = "population_density: %s, s1: %s, s2: %s, s3: %s, s4: %s L: %s" % \
                     (self.p_population_density, self.p_s1, self.p_s2, self.p_s3, self.p_s4, self.l_generation)
        parameters_text = small_font.render(parameters, 1, (100, 100, 100))
        win.blit(parameters_text, ((WIDTH - parameters_text.get_width()) // 2, HEIGHT - 50))
        # rendering each cell into the window
        for person in self.persons:
            person.draw(win, WIDTH // self.cols)
        pygame.display.update()

    def get_valid_moves(self, moves):
        valid = []
        for move in moves:
            row, col = move
            # if it is not None it is mean there is person there.
            if self.matrix[row][col] is not None:
                valid.append(move)
        return valid

    def update(self):
        infected_num = 0
        # creating new empty matrix for the new generation
        for person in self.persons:
            if person.state == NON_INFECTED:
                continue
            # gets all the valid moves the cell can go
            valid_moves = self.get_valid_moves(person.get_adjacent_positions())
            for valid_move in valid_moves:
                row = valid_move[0]
                column = valid_move[1]
                current_person = self.matrix[row][column]
                current_person.rumors_counter += 1
                if current_person.rumors_counter == 2:
                    current_person.skepticism_level = max(1, current_person.skepticism_level - 1)

            for valid_move in valid_moves:
                person_type = person.skepticism_level
                if person_type == 1 and person.stop_spreading_duration == 0:
                    infected_num += spread_rumor(valid_move, self.matrix)
                    person.stop_spreading_duration = self.l_generation
                elif person_type == 2 and person.stop_spreading_duration == 0:
                    random_number = random.randint(1, 3)
                    if random_number == 1:
                        infected_num += spread_rumor(valid_move, self.matrix)
                        person.stop_spreading_duration = self.l_generation
                elif person_type == 3 and person.stop_spreading_duration == 0:
                    random_number = random.randint(1, 3)
                    if random_number == 1 or random_number == 2:
                        infected_num += spread_rumor(valid_move, self.matrix)
                        person.stop_spreading_duration = self.l_generation
            person.update()
        self.infected_persons += infected_num
        self.generation += 1
        self.info.append(infected_num)
        # restart number of rumors counter to 0 after each generation.
        for person in self.persons:
            person.skepticism_level = person.original_skepticism_level
            person.rumors_counter = 0
