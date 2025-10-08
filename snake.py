import tkinter as tk
import random
WIDTH = 400
HEIGHT = 400
score = 0
game_over = False
cell_size = 10
delay = 100
root = tk.Tk()
root.title('Змейка / Счёт: 0')
root.resizable(False, False)
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg='black',
    highlightthickness=0)
canvas.pack()
def create_snake():
    max_x = (WIDTH//cell_size) - 3
    max_y = (HEIGHT//cell_size) - 3
    x = random.randint(0, max_x) * cell_size
    y = random.randint(0, max_y) * cell_size
    return [(x,y),(x-cell_size,y),(x-2*cell_size,y)]
snake = create_snake()
direction = 'Right'
directions = ['Right','Left','Up','Down']

def create_food():
    while True:
        x = random.randint(0, (WIDTH - cell_size) // cell_size) * cell_size
        y = random.randint(0, (HEIGHT - cell_size) // cell_size) * cell_size
        if (x,y) not in snake:
            return (x,y)
food = create_food()
def draw_food():
    canvas.create_rectangle(
        food[0], food[1],
        food[0] + cell_size,
        food[1] + cell_size,
        fill='red'
    )
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
        segment[0], segment[1],
        segment[0]+cell_size,
        segment[1]+cell_size,
        fill = 'green',
        outline = 'black'
    )

def move_snake():
    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - cell_size)
    elif direction == "Down":
        new_head = (head_x, head_y + cell_size)
    elif direction == "Left":
        new_head = (head_x - cell_size, head_y)
    elif direction == "Right":
        new_head = (head_x + cell_size, head_y)

    snake.insert(0,new_head)
    if not check_food_collusion():
        snake.pop()

def on_key_press(event):
    global direction
    key = event.keysym
    if key in directions:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key

root.bind("<KeyPress>", on_key_press)

def check_food_collusion():
    global snake,score,food
    if food == snake[0]:
        score += 1
        food = create_food()
        return True
    return False
def update_title():
    root.title(f' Змейка / Счёт: {score}')

def check_wall_collusion():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT
    )

def check_snake_collusion():
    return snake[0] in snake[1:]

def end_game():
    global game_over
    game_over = True
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
    text='Game Over!',
    font=('Arial', 20, 'bold'),
    fill='red')

def restart_game():
    global snake, direction, game_over, food, score
    snake = create_snake()
    direction = 'Right'
    food = create_food()
    score = 0
    game_over = False
    canvas.delete('all')
    draw_food()
    draw_snake()
    update_title()
    root.after(delay, game_loop)


def on_key_press(event):
    global direction, game_over
    key = event.keysym
    if key in directions and not game_over:
        if (key == "Up" and direction != "Down" or
        key == "Down" and direction != "Up" or
        key == "Left" and direction != "Right" or
        key == "Right" and direction != "Left"):
            direction = key
    elif key == 'space' and game_over:
        restart_game()

root.bind("<KeyPress>", on_key_press)


def game_loop():
    global snake, food, score
    if game_over:
        return
    move_snake()
    if check_wall_collusion() or check_snake_collusion():
        end_game()
        return
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(delay, game_loop)


draw_food()
draw_snake()
root.after(delay, game_loop)
root.mainloop()