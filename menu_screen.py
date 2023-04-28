import time
import pygame
pygame.init()
HEIGHT = 800
WIDTH = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class TextInputBox:
    def __init__(self, x, y, width, label):
        self.label = label
        self.rect = pygame.Rect(x, y, width, FONT_SIZE*1.5)
        self.color = GRAY
        self.text = ""
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GREEN if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = GRAY
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        text_surface = self.font.render(self.text, True, BLACK)
        width = max(self.rect.w, text_surface.get_width()+10)
        self.rect.w = width
        return text_surface

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        label_surface = self.font.render(self.label, True, BLACK)
        surface.blit(label_surface, (self.rect.x - label_surface.get_width() - 10, self.rect.y + 5))
        surface.blit(self.update(), (self.rect.x+5, self.rect.y+5))


def write_text():
    texts = []
    # Set up the title text
    title_font = pygame.font.SysFont(None, 36)
    title_text = title_font.render("Welcome to Rumor Spreading!", True, BLACK)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    texts.append((title_text, title_text_rect))

    # Set up the explanation
    text_font = pygame.font.SysFont(None, 24)
    explanation_text1 = text_font.render("Please enter values as follows:", True, BLACK)
    explanation_text_rect1 = title_text.get_rect(center=(WIDTH // 2.5, 100))
    texts.append((explanation_text1, explanation_text_rect1))

    explanation_text2 = text_font.render("1. 'population_density' is a float number between 0 and 1, ", True, BLACK)
    explanation_text_rect2 = title_text.get_rect(center=(WIDTH // 2.5, 130))
    texts.append((explanation_text2, explanation_text_rect2))

    explanation_text3 = text_font.render("which represents the proportion of people in the population.", True, BLACK)
    explanation_text_rect4 = title_text.get_rect(center=(WIDTH // 2.4, 150))
    texts.append((explanation_text3, explanation_text_rect4))

    explanation_text3 = text_font.render("2. 's1', 's2', 's3', and 's4' are float numbers between 0 and 1,", True, BLACK)
    explanation_text_rect3 = title_text.get_rect(center=(WIDTH // 2.5, 170))
    texts.append((explanation_text3, explanation_text_rect3))

    explanation_text3 = text_font.render(" which represent the level of skepticism.", True, BLACK)
    explanation_text_rect3 = title_text.get_rect(center=(WIDTH // 2.4, 190))
    texts.append((explanation_text3, explanation_text_rect3))

    explanation_text4 = text_font.render("- The sum of the values must be 1.", True, BLACK)
    explanation_text_rect4 = title_text.get_rect(center=(WIDTH // 2.4, 210))
    texts.append((explanation_text4, explanation_text_rect4))

    explanation_text5 = text_font.render("3. 'generation' is an integer that represents the duration during", True, BLACK)
    explanation_text_rect5 = title_text.get_rect(center=(WIDTH // 2.5, 230))
    texts.append((explanation_text5, explanation_text_rect5))

    explanation_text5 = text_font.render(" which a person cannot spread a rumor.", True, BLACK)
    explanation_text_rect5 = title_text.get_rect(center=(WIDTH // 2.4, 250))
    texts.append((explanation_text5, explanation_text_rect5))

    return texts


def validate_inputs(inputs):
    # Check that p_population_density is between 0 and 1
    try:
        p_population_density = float(inputs[0])
        p_s1 = float(inputs[1])
        p_s2 = float(inputs[2])
        p_s3 = float(inputs[3])
        p_s4 = float(inputs[4])
        l_generation = int(inputs[5])
        mode = inputs[6]
    except ValueError:
        return False
    if not 0 <= p_population_density and p_s1 and p_s2 and p_s3 and p_s4 <= 1:
        return False
    if p_s1 + p_s2 + p_s3 + p_s4 != 1:
        return False

    if not l_generation > 0:
        return False
    if mode not in ["slow", "fast", "default"]:
        return False

    return True


def run_menu_screen():
    input_boxes = []
    x = 300
    y = 260
    labels = ["p - population_density:", "p - s1:", "p - s2:", "p - s3:", "p - s4:", "l - generation:", "mode:"]
    for i in range(7):
        input_box = TextInputBox(x, y, 150, label=labels[i])
        input_boxes.append(input_box)
        y += 70

    # Create "Next" button
    next_button_rect = pygame.Rect(WIDTH - 110, HEIGHT - 60, 100, 50)
    next_button_color = GRAY

    # Set up window and clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    # Get values from input boxes and do something with them
                    values = [box.text for box in input_boxes]
                    # Validate inputs
                    if not validate_inputs(values):
                        # Show error message
                        error_font = pygame.font.SysFont(None, FONT_SIZE)
                        error_text = error_font.render("Invalid input values!", True, RED)
                        screen.blit(error_text, (WIDTH // 1.5, 400))
                        pygame.display.update()
                        time.sleep(0.5)
                        continue
                    # Inputs are valid, do something with them
                    # Clean up
                    # pygame.quit()
                    return values

        # Update screen
        screen.fill(WHITE)

        for tuples in write_text():
            screen.blit(tuples[0], tuples[1])

        for box in input_boxes:
            box.draw(screen)
        pygame.draw.rect(screen, next_button_color, next_button_rect)
        next_button_font = pygame.font.SysFont(None, FONT_SIZE)
        next_button_text = next_button_font.render("Next", True, BLACK)
        screen.blit(next_button_text, (next_button_rect.x + 25, next_button_rect.y + 10))
        pygame.display.update()

        # Limit frame rate
        clock.tick(30)

    # Clean up
    pygame.quit()
