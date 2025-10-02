import turtle
import random
import heapq
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import pygame
import sys
import time

# === GLOBALS ===
maze = []
player_x = player_y = 0
width = height = block_size = 0
player_size = 0
run_pygame = False
pygame_thread = None
auto_solving = False
solution_path = []
pygame_initialized = False

# === TURTLE SETUP ===
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Prim's Algorithm Maze")
maze_drawer = turtle.Turtle()
maze_drawer.speed(0)
maze_drawer.hideturtle()
maze_drawer.penup()
maze_drawer.color("white")
solver = turtle.Turtle()
solver.speed(0)
solver.hideturtle()
solver.penup()
solver.color("green")
screen.tracer(0, 0)

screen_width = screen.window_width()
screen_height = screen.window_height()

# === MAZE FUNCTIONS ===
def draw_wall(x, y, size):
    maze_drawer.goto(x, y)
    maze_drawer.pendown()
    for _ in range(4):
        maze_drawer.forward(size)
        maze_drawer.right(90)
    maze_drawer.penup()

def fill_path(x, y, size, scale_factor=0.8):
    solver.goto(x + size * (1 - scale_factor) / 2, y - size * (1 - scale_factor) / 2)
    solver.pendown()
    reduced_size = size * scale_factor
    solver.begin_fill()
    for _ in range(4):
        solver.forward(reduced_size)
        solver.right(90)
    solver.end_fill()
    solver.penup()

def prims_maze(w, h, bs):
    global maze, start_x, start_y, width, height, block_size
    width, height, block_size = w, h, bs
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    # Start from a random odd position
    start_x = random.randint(1, width // 2) * 2 - 1
    start_y = random.randint(1, height // 2) * 2 - 1
    maze[start_y][start_x] = ' '
    walls = [(start_x, start_y)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                maze[(y + ny) // 2][(x + nx) // 2] = ' '
                maze[ny][nx] = ' '
                walls.append((nx, ny))
    
    # Ensure start and end positions are open
    maze[height-2][width-2] = ' '  # Bottom-right (start)
    maze[1][1] = ' '               # Top-left (end)
    
    # Create paths to ensure connectivity
    for i in range(1, width-1):
        if maze[height-2][i] == '#' and maze[height-2][i-1] == ' ':
            maze[height-2][i] = ' '
            break
    for i in range(1, height-1):
        if maze[i][1] == '#' and maze[i-1][1] == ' ':
            maze[i][1] = ' '
            break
    
    maze_drawer.clear()
    for row in range(height):
        for col in range(width):
            if maze[row][col] == '#':
                x = -width * block_size // 2 + col * block_size
                y = height * block_size // 2 - row * block_size
                draw_wall(x, y, block_size)
    screen.update()

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_solve():
    global maze, block_size, solution_path
    width = len(maze[0])
    height = len(maze)
    start = (width - 2, height - 2)  # Bottom-right
    end = (1, 1)                     # Top-left
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    queue = []
    heapq.heappush(queue, (0, start))
    g_cost = {start: 0}
    parents = {start: None}
    
    while queue:
        _, current = heapq.heappop(queue)
        if current == end:
            break
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            nx, ny = neighbor
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == ' ':
                new_g = g_cost[current] + 1
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    f = new_g + heuristic(neighbor, end)
                    heapq.heappush(queue, (f, neighbor))
                    parents[neighbor] = current
    
    # Build solution path
    solution_path = []
    current = end
    while current is not None:
        solution_path.append(current)
        current = parents.get(current)
    solution_path.reverse()
    
    # Draw solution on turtle canvas
    current = end
    while current != start:
        if current in parents:
            x, y = current
            px = -width * block_size // 2 + x * block_size
            py = height * block_size // 2 - y * block_size
            fill_path(px, py, block_size)
            current = parents[current]
        else:
            break
    screen.update()

def is_valid_position(x, y, cell_size, margin=2):
    """Check if the position is valid with proper collision detection"""
    # Add margin to prevent clipping through walls
    left = x + margin
    right = x + cell_size - margin
    top = y + margin
    bottom = y + cell_size - margin
    
    # Convert to grid coordinates and check all corners
    positions_to_check = [
        (left, top), (right, top),
        (left, bottom), (right, bottom),
        (x + cell_size//2, y + cell_size//2)  # Center point
    ]
    
    for px, py in positions_to_check:
        col = int(px // cell_size)
        row = int(py // cell_size)
        
        # Check boundaries
        if col < 0 or col >= width or row < 0 or row >= height:
            return False
        
        # Check if any part touches a wall
        if maze[row][col] == '#':
            return False
    
    return True

def stop_pygame():
    """Safely stop pygame"""
    global run_pygame, pygame_thread
    print("Stopping pygame...")
    run_pygame = False
    
    if pygame_thread and pygame_thread.is_alive():
        print("Waiting for pygame thread to stop...")
        pygame_thread.join(timeout=3)
        if pygame_thread.is_alive():
            print("Warning: Pygame thread didn't stop gracefully")
        else:
            print("Pygame thread stopped successfully")
    
    # Force quit pygame display
    try:
        pygame.display.quit()
    except:
        pass

# === PYGAME PLAYER ===
def launch_player():
    global player_x, player_y, run_pygame, auto_solving, solution_path, pygame_initialized
    
    try:
        print(f"Launching pygame player for maze {width}x{height}")
        
        # Always reinitialize pygame for new window
        try:
            pygame.quit()
        except:
            pass
        
        pygame.init()
        pygame_initialized = True
        
        win_size = 600
        cell_size = min(win_size // width, win_size // height)
        cell_size = max(cell_size, 15)  # Minimum cell size
        
        win = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("Maze Player - Use WASD or Arrow Keys")
        
        player_color = (255, 0, 0)
        # Start at bottom-right position
        player_x = (width - 2) * cell_size
        player_y = (height - 2) * cell_size
        
        speed = 120  # Pixels per second
        auto_speed = 200
        clock = pygame.time.Clock()
        run_pygame = True
        
        # Auto-solving variables
        path_index = 0
        last_move_time = 0
        move_delay = 0.2
        
        print(f"Pygame window launched: {width}x{height}, cell_size: {cell_size}")

        while run_pygame:
            dt = clock.tick(60) / 1000.0
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_pygame = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset position
                        player_x = (width - 2) * cell_size
                        player_y = (height - 2) * cell_size
                        auto_solving = False

            if auto_solving and solution_path and len(solution_path) > 1:
                # Auto-solving mode
                if current_time - last_move_time > move_delay and path_index < len(solution_path) - 1:
                    path_index += 1
                    target_col, target_row = solution_path[path_index]
                    player_x = target_col * cell_size
                    player_y = target_row * cell_size
                    last_move_time = current_time
                    
                    # Check if reached the end
                    if path_index >= len(solution_path) - 1:
                        auto_solving = False
                        print("Maze solved!")
            else:
                # Manual control
                keys = pygame.key.get_pressed()
                move_x = move_y = 0
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: move_x = -1
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: move_x = 1
                if keys[pygame.K_UP] or keys[pygame.K_w]: move_y = -1
                if keys[pygame.K_DOWN] or keys[pygame.K_s]: move_y = 1

                # Calculate new position with smaller steps for better collision
                step_size = speed * dt
                new_x = player_x
                new_y = player_y
                
                # Move in X direction
                if move_x != 0:
                    test_x = player_x + move_x * step_size
                    if is_valid_position(test_x, player_y, cell_size):
                        new_x = test_x
                
                # Move in Y direction
                if move_y != 0:
                    test_y = player_y + move_y * step_size
                    if is_valid_position(new_x, test_y, cell_size):
                        new_y = test_y
                
                player_x = new_x
                player_y = new_y

            # Draw everything
            win.fill((0, 0, 0))
            
            # Draw maze walls
            for r in range(height):
                for c in range(width):
                    if maze[r][c] == '#':
                        pygame.draw.rect(win, (255, 255, 255), 
                                       (c * cell_size, r * cell_size, cell_size, cell_size))
            
            # Draw start and end markers
            end_rect = pygame.Rect(1 * cell_size + 2, 1 * cell_size + 2, 
                                 cell_size - 4, cell_size - 4)
            pygame.draw.rect(win, (0, 255, 0), end_rect)  # Green goal
            
            start_rect = pygame.Rect((width-2) * cell_size + 2, (height-2) * cell_size + 2, 
                                   cell_size - 4, cell_size - 4)
            pygame.draw.rect(win, (0, 0, 255), start_rect)  # Blue start
            
            # Draw player
            player_rect = pygame.Rect(int(player_x) + 1, int(player_y) + 1, 
                                    cell_size - 2, cell_size - 2)
            pygame.draw.rect(win, player_color, player_rect)
            
            # Check win condition
            player_grid_x = int((player_x + cell_size//2) // cell_size)
            player_grid_y = int((player_y + cell_size//2) // cell_size)
            if player_grid_x == 1 and player_grid_y == 1:
                # Draw win message
                font = pygame.font.Font(None, 36)
                text = font.render("YOU WIN! Press R to reset", True, (255, 255, 0))
                text_rect = text.get_rect(center=(width * cell_size // 2, height * cell_size // 2))
                win.blit(text, text_rect)
            
            pygame.display.flip()
            
    except Exception as e:
        print(f"Error in pygame: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Pygame loop ended")
        run_pygame = False
        try:
            pygame.display.quit()
        except:
            pass

# === TKINTER GUI ===
def setup_gui():
    global pygame_thread, run_pygame, auto_solving
    
    root = tk.Tk()
    root.title("Enhanced Maze Generator and Solver")
    root.geometry("350x400")
    root.resizable(True, True)

    def generate_action():
        global pygame_thread, run_pygame, auto_solving, maze
        
        print("Generate action started...")
        
        # Stop auto-solving
        auto_solving = False
        
        # Get dimensions
        w = simpledialog.askinteger("Width", "Maze width (5-51, odd recommended)", 
                                  minvalue=5, maxvalue=51, initialvalue=21)
        if w is None: 
            print("Width input cancelled")
            return
        
        h = simpledialog.askinteger("Height", "Maze height (5-51, odd recommended)", 
                                  minvalue=5, maxvalue=51, initialvalue=21)
        if h is None: 
            print("Height input cancelled")
            return
        
        print(f"Generating maze {w}x{h}...")
        
        # Stop previous pygame completely
        stop_pygame()
        
        # Wait a bit more for complete cleanup
        time.sleep(0.5)
        
        # Generate new maze
        bs = min(screen_width // (w + 2), screen_height // (h + 2))
        bs = max(bs, 10)
        
        solver.clear()
        prims_maze(w, h, bs)
        print("Maze generated successfully")
        
        # Start new pygame with more delay
        root.after(500, start_new_pygame)

    def start_new_pygame():
        global pygame_thread, run_pygame
        print("Starting new pygame...")
        
        if not maze:
            print("No maze available!")
            return
            
        run_pygame = True
        pygame_thread = threading.Thread(target=launch_player, daemon=False)
        pygame_thread.start()
        print("New pygame thread started")

    def solve_action():
        global auto_solving, solution_path
        if not maze:
            messagebox.showwarning("Warning", "Please generate a maze first!")
            return
            
        solver.clear()
        a_star_solve()
        
        if solution_path and len(solution_path) > 1:
            auto_solving = True
            print("Auto-solving started!")
        else:
            messagebox.showinfo("Info", "No solution found!")

    def reset_player():
        global player_x, player_y, auto_solving
        auto_solving = False
        if width > 0 and height > 0:
            cell_size = min(600 // width, 600 // height)
            player_x = (width - 2) * cell_size
            player_y = (height - 2) * cell_size

    def quit_application():
        global run_pygame
        print("Quitting application...")
        stop_pygame()
        try:
            pygame.quit()
        except:
            pass
        root.quit()
        root.destroy()

    # Create GUI elements
    title_label = tk.Label(root, text="Enhanced Maze Generator", 
                          font=('Arial', 14, 'bold'), fg='blue')
    title_label.pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(fill='both', padx=20, pady=5)
    
    tk.Button(button_frame, text="🎲 Generate New Maze", command=generate_action, 
              width=25, height=2, bg='lightblue', font=('Arial', 10, 'bold')).pack(pady=5)
    
    tk.Button(button_frame, text="🤖 Auto Solve Maze", command=solve_action, 
              width=25, height=2, bg='lightgreen', font=('Arial', 10, 'bold')).pack(pady=5)
    
    tk.Button(button_frame, text="🔄 Reset Player", command=reset_player, 
              width=25, height=2, bg='lightyellow', font=('Arial', 10, 'bold')).pack(pady=5)
    
    # Debug button
    def debug_pygame():
        print(f"Debug - run_pygame: {run_pygame}")
        print(f"Debug - pygame_thread alive: {pygame_thread.is_alive() if pygame_thread else 'None'}")
        print(f"Debug - maze size: {len(maze)}x{len(maze[0]) if maze else 0}")
        print(f"Debug - width x height: {width}x{height}")
        if not run_pygame and maze:
            print("Manually starting pygame...")
            start_new_pygame()
    
    tk.Button(button_frame, text="🔧 Debug/Force Start", command=debug_pygame, 
              width=25, height=1, bg='orange', font=('Arial', 9)).pack(pady=3)
    
    tk.Button(button_frame, text="❌ Quit", command=quit_application, 
              width=25, height=2, bg='lightcoral', font=('Arial', 10, 'bold')).pack(pady=5)
    
    # Instructions
    instruction_frame = tk.Frame(root, bg='lightgray', relief='ridge', bd=2)
    instruction_frame.pack(fill='x', padx=10, pady=5)
    
    instructions = tk.Label(instruction_frame, 
                           text="🎮 Controls: WASD or Arrow Keys\n" +
                                "🔴 Red = Player  🟢 Green = Goal  🔵 Blue = Start\n" +
                                "Press R in game to reset position",
                           font=('Arial', 8), justify='center', bg='lightgray')
    instructions.pack(pady=3)
    
    root.protocol("WM_DELETE_WINDOW", quit_application)
    root.mainloop()

# === MAIN ===
if __name__ == "__main__":
    try:
        setup_gui()
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        stop_pygame()
        pygame.quit()