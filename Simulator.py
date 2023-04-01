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
    matrix = []
    for r in range(rows):
        row = []
        for col in range(cols):
            row.append(None)
        matrix.append(row)
    return matrix


def spread_rumor(person_position, matrix):
    row = person_position[0]
    column = person_position[1]
    if matrix[row][column].state == NON_INFECTED:
        matrix[row][column].state = INFECTED
        return 1
    return 0


class Person:
    def __init__(self, level_of_skepticism, position, state):
        self.level_of_skepticism = level_of_skepticism
        self.state = state
        self.position = position
        self.colors = [(0, 255, 0), (255, 0, 0)]  # green, red
        self.stop_spreading = 0
        self.generation = 0
        self.move_set = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.original_level_of_skepticism = level_of_skepticism
        self.rumors_counter = 0

    def render(self, win, distance):
        # the color of the cell depending on the state of the cell
        if self.state == INFECTED:
            color = self.colors[1]
        else:
            color = self.colors[0]
        y, x = self.position
        size = WIDTH // 200
        pygame.draw.rect(win, color, (x * distance, y * distance + EXTENSION_FOR_TEXT, size, size))

    def get_moves(self):
        # calculate moves for the cell based on its location and move set
        r, c = self.position
        moves = []
        for row, col in self.move_set:
            moves.append(((r + row) % ROWS, (c + col) % COLS))
        return moves

    def update(self):
        if self.stop_spreading > 0:
            self.stop_spreading -= 1


class Simulation:
    def __init__(self, parameters):
        self.rows = ROWS
        self.cols = COLS
        self.generation = 0
        self.infected_persons = 0
        self.matrix = create_matrix(self.rows, self.cols)
        self.p_population_density = parameters.get("p_population_density")
        self.number_of_persons = int(ROWS * COLS * self.p_population_density)
        self.p_s1 = parameters.get("p_s1")
        self.p_s2 = parameters.get("p_s2")
        self.p_s3 = parameters.get("p_s3")
        self.p_s4 = parameters.get("p_s4")
        self.l_generation = parameters.get("l_generation")
        self.name = parameters.get("name")
        self.persons = []
        self.info = []
        self.init_simulation()

    def create_person(self, position, p_type, state):
        row = position // self.rows
        col = position % self.cols
        person = Person(p_type, (row, col), state)
        self.matrix[row][col] = person
        self.persons.append(person)

    def init_simulation(self):
        # getting random numbers to represent the place in the matrix the cell get
        cells_pos = random.sample(range(self.rows * self.cols), self.number_of_persons)
        probabilities = [self.p_s1, self.p_s2, self.p_s3, self.p_s4]
        random_person = random.choice(cells_pos)
        for position in cells_pos:
            type_of_person = random.choices(range(1, 5), weights=probabilities)[0]
            if position == random_person:
                # spreading person
                self.create_person(position, type_of_person, INFECTED)
                self.infected_persons += 1
            else:
                self.create_person(position, type_of_person, NON_INFECTED)

    def simulate(self, win, large_font, small_font):
        run = True
        while run:
            # making sure the simulation not run to fast
            time.sleep(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            self.render(win, large_font, small_font)
            self.update()
            if self.generation > 100:
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
            person.render(win, WIDTH // self.cols)
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
            valid_moves = self.get_valid_moves(person.get_moves())
            for valid_move in valid_moves:
                row = valid_move[0]
                column = valid_move[1]
                current_person = self.matrix[row][column]
                current_person.rumors_counter += 1
                if current_person.rumors_counter == 2:
                    current_person.level_of_skepticism = max(1, current_person.level_of_skepticism - 1)

            for valid_move in valid_moves:
                person_type = person.level_of_skepticism
                if person_type == 1 and person.stop_spreading == 0:
                    infected_num += spread_rumor(valid_move, self.matrix)
                    person.stop_spreading = self.l_generation
                elif person_type == 2 and person.stop_spreading == 0:
                    random_number = random.randint(1, 3)
                    if random_number == 1:
                        infected_num += spread_rumor(valid_move, self.matrix)
                        person.stop_spreading = self.l_generation
                elif person_type == 3 and person.stop_spreading == 0:
                    random_number = random.randint(1, 3)
                    if random_number == 1 or random_number == 2:
                        infected_num += spread_rumor(valid_move, self.matrix)
                        person.stop_spreading = self.l_generation
            person.update()
        self.infected_persons += infected_num
        self.generation += 1
        self.info.append(infected_num)
        # restart number of rumors counter to 0 after each generation.
        for person in self.persons:
            person.level_of_skepticism = person.original_level_of_skepticism
            person.rumors_counter = 0
