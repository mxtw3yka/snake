import tkinter as tk
import random
WIDTH = 400
HEIGHT = 400
score = 0
max_score = 0
game_over = False
game_paused = False
cell_size = 10
delay = 100
root = tk.Tk()
root.title('Змейка / Счёт: 0')
root.resizable(False, False)
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg='green',
    highlightthickness=0)
canvas.pack()
def create_snake():
    max_x = (WIDTH//cell_size) - 3
    max_y = (HEIGHT//cell_size) - 3
    x = random.randint(0, max_x) * cell_size
    y = random.randint(0, max_y) * cell_size
    return [(x,y),(x-cell_size,y),(x-2*cell_size,y)]
snake = create_snake()
direction = 'd'
directions = ['d','a','w','s']

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
        fill = 'darkgreen',
        outline = 'black'
    )

def move_snake():
    head_x, head_y = snake[0]

    if direction == "w":
        new_head = (head_x, head_y - cell_size)
    elif direction == "s":
        new_head = (head_x, head_y + cell_size)
    elif direction == "a":
        new_head = (head_x - cell_size, head_y)
    elif direction == "d":
        new_head = (head_x + cell_size, head_y)

    snake.insert(0,new_head)
    if not check_food_collusion():
        snake.pop()

def on_key_press(event):
    global direction
    key = event.keysym
    if key in directions:
        if (key == "w" and direction != "s" or
            key == "s" and direction != "w" or
            key == "a" and direction != "d" or
            key == "d" and direction != "a"):
            direction = key

root.bind("<KeyPress>", on_key_press)

def check_food_collusion():
    global snake,score,food, delay
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
    global game_over, max_score
    game_over = True
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
    text=f'Счёт {score}\nMax: {max_score}\nGame Over!',
    font=('Arial', 20, 'bold'),
    fill='black')

def restart_game():
    global snake, direction, game_over, food, score, max_score
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

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        show_pause_menu()
    else:
        hide_pause_menu()


def show_pause_menu():
    pause_overlay = tk.Canvas(
        root,
        width=WIDTH,
        height=HEIGHT,
        bg='green',
        highlightthickness=0
    )
    pause_overlay.place(x=0, y=0)
    pause_overlay.configure(bg='green', highlightbackground='green')
    pause_overlay.configure(highlightbackground='green')

    pause_overlay.create_text(
        WIDTH // 2,
        HEIGHT // 2-30,
        text='ПАУЗА',
        fill='white'
    )
    continue_btn = tk.Button(
        root,
        text='Press (ESC) to continue',
        command=toggle_pause,
        bg='lightgreen',

    )
    continue_btn.place(x=WIDTH//2-60, y=HEIGHT//2+10)

    restart_btn = tk.Button(
        root,
        text='Restart Game',
        command=restart_game,
        bg='lightgreen',
    )
    restart_btn.place(x=WIDTH//2-60, y=HEIGHT//2+50)
    root.pause_overlay = pause_overlay
    root.continue_btn = continue_btn
    root.restart_btn = restart_btn
def hide_pause_menu():
    if hasattr(root, 'pause_overlay'):
        root.pause_overlay.destroy()
    if hasattr(root, 'continue_btn'):
        root.continue_btn.destroy()
    if hasattr(root, 'restart_btn'):
        root.restart_btn.destroy()


def on_key_press(event):
    global direction, game_over, game_paused
    key = event.keysym
    if key in directions and not game_over:
        if (key == "w" and direction != "s" or
        key == "s" and direction != "w" or
        key == "a" and direction != "d" or
        key == "d" and direction != "a"):
            direction = key
    elif key == 'space' and game_over:
        restart_game()
    elif key == 'Escape':
        toggle_pause()
        return

root.bind("<KeyPress>", on_key_press)


def game_loop():
    global snake, food, score, max_score
    if game_over or game_paused:
        root.after(delay, game_loop)
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