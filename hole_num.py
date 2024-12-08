import pygame
import random
import os
import sys
import button

# Initialize Pygame
pygame.init()

# Set up pygame display window
pygame.display.set_caption("Math Puzzle Game")
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# *VARIABLES
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)

# Images
HOLE_ONE = pygame.image.load(os.path.join("assets/images", "character-one.png"))
HOLE_ONE = pygame.transform.scale(HOLE_ONE, (30 * 2, 30 * 2))

HOLE_TWO = pygame.image.load(os.path.join("assets/images", "character-two.png"))
HOLE_TWO = pygame.transform.scale(HOLE_TWO, (30 * 2, 30 * 2))

HOLE_THREE = pygame.image.load(os.path.join("assets/images", "character-three.png"))
HOLE_THREE = pygame.transform.scale(HOLE_THREE, (30 * 2, 30 * 2))

HOLE_FOUR = pygame.image.load(os.path.join("assets/images", "character-four.png"))
HOLE_FOUR = pygame.transform.scale(HOLE_FOUR, (30 * 2, 30 * 2))

BG = pygame.image.load(os.path.join("assets/images", "background.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

MAIN_MENU = pygame.image.load(os.path.join("assets/images", "menu.png"))
MAIN_MENU = pygame.transform.scale(MAIN_MENU, (SCREEN_WIDTH, SCREEN_HEIGHT))

PLAY_BTN = pygame.image.load(os.path.join("assets/images", "play_btn.png"))
QUIT_BTN = pygame.image.load(os.path.join("assets/images", "quit_btn.png"))
MENU_BTN = pygame.image.load(os.path.join("assets/images", "menu_btn.png"))
AGAIN_BTN = pygame.image.load(os.path.join("assets/images", "again_btn.png"))

GAMEOVER_SCREEN = pygame.image.load(os.path.join("assets/images", "gameover.png"))
GAMEOVER_SCREEN = pygame.transform.scale(GAMEOVER_SCREEN, (SCREEN_WIDTH, SCREEN_HEIGHT))

OUT_TIME_SCREEN = pygame.image.load(os.path.join("assets/images", "out_time.png"))
OUT_TIME_SCREEN = pygame.transform.scale(OUT_TIME_SCREEN, (SCREEN_WIDTH, SCREEN_HEIGHT))

CHOOSE_CHARACTER = pygame.image.load(os.path.join("assets/images", "choose_hole.png"))
CHOOSE_CHARACTER = pygame.transform.scale(CHOOSE_CHARACTER, (SCREEN_WIDTH, SCREEN_HEIGHT))

play_btn = button.Button(370, 250, PLAY_BTN, 0.5)
quit_btn = button.Button(370, 400, QUIT_BTN, 0.5)

again_btn = button.Button(440, 350, AGAIN_BTN, 0.4)
menu_btn = button.Button(240, 450, MENU_BTN, 0.4)

character_one = button.Button(200, 350, HOLE_ONE, 2)
character_two = button.Button(400, 350, HOLE_TWO, 2)
character_three = button.Button(600, 350, HOLE_THREE, 2)
character_four = button.Button(800, 350, HOLE_FOUR, 2)

hole_selected = HOLE_ONE

# Fonts
font_large = pygame.font.SysFont("Helvetica", 72)
font_small = pygame.font.SysFont("Helvetica", 36)

# Game Global Variables
pointsLevel = [10, 20, 30, 40, 50]
playerPoints = 0
hole_size = 30
hole_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
scattered_numbers = []
collected_numbers = ["", ""]
lives = 3
level = 1
operations = ["+", "-", "×", "÷"]
current_operation = "+"
target_result = 10
timer = 30  # Seconds
start_time = 0
# Game Loop
running = True
game_over = False
speed = 0

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  SCREEN.blit(img, (x, y))

def mainMenu():
        while True:
          pygame.event.get()
          
          keys = pygame.key.get_pressed()
          for event in pygame.event.get():
            if event.type == keys[pygame.QUIT]:
                pygame.quit()
                sys.exit()
            if event.type == keys[pygame.KEYDOWN]:
                if event.key == keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
          
          SCREEN.fill([255, 255, 255])
          SCREEN.blit(MAIN_MENU, (0, 0))

          if play_btn.draw(SCREEN):
            chooseCharacter()
            
          if quit_btn.draw(SCREEN):
              pygame.quit()
              sys.exit()

          pygame.display.update()

def chooseCharacter():
    global  hole_selected
    
    while True:
        pygame.event.get()
        SCREEN.fill([255, 255, 255])
        SCREEN.blit(CHOOSE_CHARACTER, (0, 0))
        
        if character_one.draw(SCREEN):
            hole_selected = HOLE_ONE
            game()
            
        if character_two.draw(SCREEN):
            hole_selected = HOLE_TWO
            game()
            
        if character_three.draw(SCREEN):
            hole_selected = HOLE_THREE
            game()
            
        if character_four.draw(SCREEN):
            hole_selected = HOLE_FOUR
            game()
        
        pygame.display.update()

          
# Generate math problem
def generate_math_problem():
    global scattered_numbers, collected_numbers, target_result, current_operation, timer, start_time, speed

    # Select operation
    current_operation = random.choice(operations)

    if current_operation == "+":
        n1 = random.randint(1, 10 * level)
        n2 = random.randint(1, 10 * level)
        target_result = n1 + n2
    elif current_operation == "-":
        n1 = random.randint(5, 15 * level)
        n2 = random.randint(1, n1)
        target_result = n1 - n2
    elif current_operation == "×":
        n1 = random.randint(1, 5 * level)
        n2 = random.randint(1, 5 * level)
        target_result = n1 * n2
    elif current_operation == "÷":
        n2 = random.randint(1, 5 * level)
        target_result = random.randint(1, 5 * level)
        n1 = target_result * n2

    correct_numbers = [n1, n2]
    
    distractors = [random.randint(1, 20 * level) for _ in range(10)]
    scattered_numbers = [
        (
            random.randint(50, SCREEN_WIDTH - 50),  # x position
            random.randint(50, SCREEN_HEIGHT - 200),  # y position
            n,  # number value
            n in correct_numbers,  # is it a correct number?
            random.uniform(-2, 2) * speed,  # x velocity
            random.uniform(-2, 2)  * speed # y velocity
        )
        for n in correct_numbers + distractors
    ]
    
    for i in range(len(scattered_numbers)):
        x, y, n, is_correct, vx, vy = scattered_numbers[i]

        # Update position
        x += vx 
        y += vy

        # Check for boundary collisions and reverse velocity if necessary
        if x <= 0 or x >= SCREEN_WIDTH:
            vx = -vx
        if y <= 0 or y >= SCREEN_HEIGHT - 200:
            vy = -vy

        # Update the scattered_numbers list
        scattered_numbers[i] = (x, y, n, is_correct, vx, vy)
        
    for x, y, n, is_correct, _, _ in scattered_numbers:
        # Replace with your rendering code, e.g., draw a circle or number
        pygame.draw.circle(SCREEN, (255, 255, 255), (int(x), int(y)), 20)
        text = font_small.render(str(n), True, (0, 0, 0))
        SCREEN.blit(text, (int(x) - text.get_width() // 2, int(y) - text.get_height() // 2))
    
    collected_numbers = ["_", "_"]
    timer = max(10, 30 - level)  # Timer decreases slightly as levels increase
    start_time = pygame.time.get_ticks()  # Reset level start time

# Check if the hole collects a number
def check_collision():
    global collected_numbers, lives
    hole_rect = pygame.Rect(hole_pos[0] - hole_size, hole_pos[1] - hole_size, 2 * hole_size, 2 * hole_size)
    for number in scattered_numbers[:]:
        number_rect = pygame.Rect(number[0] - 20, number[1] - 20, 40, 40)
        if hole_rect.colliderect(number_rect):
            scattered_numbers.remove(number)
            if number[3]:  # Correct number
                if "_" in collected_numbers:
                    collected_numbers[collected_numbers.index("_")] = str(number[2])
            else:  # Incorrect number
                lives -= 1
                if lives == 0:
                    return False  # Game over
    return True  # Continue playing

# Check if the equation is complete
def is_equation_complete():
    if "_" in collected_numbers:  # Check if both numbers are collected
        return False
    try:
        n1, n2 = int(collected_numbers[0]), int(collected_numbers[1])
        if current_operation == "+":
            return n1 + n2 == target_result
        elif current_operation == "-":
            return n1 - n2 == target_result
        elif current_operation == "×":
            return n1 * n2 == target_result
        elif current_operation == "÷":
            return n2 != 0 and n1 // n2 == target_result
    except ValueError:
        return False  # Ensure no crash due to invalid values
    return False

    
def update_scattered_numbers(scattered_numbers, screen_width, screen_height):
    updated_numbers = []

    for x, y, n, is_correct, vx, vy in scattered_numbers:
        # Update position
        x += vx
        y += vy

        # Check for boundary collisions and reverse velocity if necessary
        if x <= 0 or x >= screen_width:
            vx = -vx
        if y <= 0 or y >= screen_height - 200:  # Assuming 200 is a reserved area
            vy = -vy

        # Append the updated number to the list
        updated_numbers.append((x, y, n, is_correct, vx, vy))

    return updated_numbers

# Reset game
def go_to_mainmenu():
    global lives, level, game_over, speed
    lives = 3
    level = 1
    game_over = False
    speed = 0
    mainMenu()
    
def reset_game():
    global lives, level, game_over, speed
    lives = 3
    level = 1
    game_over = False
    speed = 0
    game()

# Next level
def next_level():
    global level, speed
    level += 1
    speed += 1.5
    generate_math_problem()
    
def gamOverScreen():
    global lives, speed
    # Display Game Over Screen
    SCREEN.fill([255, 255, 255])
    SCREEN.blit(GAMEOVER_SCREEN, (0, 0))
    
    draw_text('Press R, To Play Again', font_small, (0, 0, 0), 400, 350)
    draw_text('Press M, To Main Menu', font_small, (0, 0, 0), 400, 450)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
    if keys[pygame.K_m]:
        go_to_mainmenu()
    speed = 0

    pygame.display.flip()
    
def outOfTimeScreen():
    global lives, speed
    # Display Game Over Screen
    SCREEN.fill([255, 255, 255])
    SCREEN.blit(OUT_TIME_SCREEN, (0, 0))
    
    draw_text('Press R, To Play Again', font_small, (0, 0, 0), 400, 350)
    draw_text('Press M, To Main Menu', font_small, (0, 0, 0), 400, 450)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
    if keys[pygame.K_m]:
        go_to_mainmenu()
    speed = 0
    pygame.display.flip()
    
def draw_popup(message):
    # Create a semi-transparent surface for the popup
    popup_width = 700
    popup_height = 250
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((0, 0, 0, 200))  # Black background with transparency

    # Calculate the popup position
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2

    # Render the message text
    text = font_small.render(message, True, WHITE)
    text_x = (popup_width - text.get_width()) // 2
    text_y = (popup_height - text.get_height()) // 2

    # Blit the text onto the popup surface
    popup_surface.blit(text, (text_x, text_y))

    # Draw the popup on the main screen
    SCREEN.blit(popup_surface, (popup_x, popup_y))

def nextLevelScreen():
    draw_popup("Level Complete! Press N for Next Level")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_n]:
        next_level()


          
def game():
    global game_over, lives, scattered_numbers, speed, hole_selected

    generate_math_problem()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Move the hole with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                hole_pos[0] -= 7
            if keys[pygame.K_RIGHT]:
                hole_pos[0] += 7
            if keys[pygame.K_UP]:
                hole_pos[1] -= 7
            if keys[pygame.K_DOWN]:
                hole_pos[1] += 7

            # Check for collisions with numbers
            if not check_collision():
                game_over = True

            # Calculate time remaining
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            time_left = max(0, timer - elapsed_time)
            if time_left == 0:
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    generate_math_problem()

            # Draw everything
            SCREEN.fill([255, 255, 255])
            SCREEN.blit(BG, (0, 0))

            # Draw the hole
            SCREEN.blit(hole_selected, (hole_pos[0] - hole_size, hole_pos[1] - hole_size))

            # Update logic
            scattered_numbers = update_scattered_numbers(scattered_numbers, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Rendering logic
            for x, y, n, is_correct, _, _ in scattered_numbers:
                text = font_small.render(str(n), True, (0, 0, 0))
                SCREEN.blit(text, (int(x) - text.get_width() // 2, int(y) - text.get_height() // 2))

            # Display the math equation
            equation_display = f"{collected_numbers[0]} {current_operation} {collected_numbers[1]} = {target_result}"
            equation_text = font_large.render(equation_display, True, WHITE)
            SCREEN.blit(equation_text, (SCREEN_WIDTH // 2 - equation_text.get_width() // 2, SCREEN_HEIGHT - 100))

            # Display lives, level, and timer
            lives_text = font_small.render(f"Lives: {lives}", True, WHITE)
            level_text = font_small.render(f"Level: {level}", True, WHITE)
            timer_text = font_small.render(f"Time: {time_left}s", True, WHITE)
            SCREEN.blit(lives_text, (10, 10))
            SCREEN.blit(level_text, (10, 50))
            SCREEN.blit(timer_text, (10, 90))

            # Check win condition
            if is_equation_complete():
                nextLevelScreen()
                
        else:
            if lives == 0:
                gamOverScreen()
            elif time_left == 0 and lives == 0:
                outOfTimeScreen()

        # Update the display
        pygame.display.flip()
        pygame.time.delay(30)
    


mainMenu()

pygame.quit()