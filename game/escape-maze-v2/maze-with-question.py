import tkinter as tk
from tkinter import ttk
import pygame
import random
import heapq
import threading
import time
import sys
import os
import math
import json

class QuestionSystem:
    def __init__(self):
        # Programming questions pool
        self.questions = [
            {
                "question": "In Python, what does the 'len()' function do?",
                "options": {
                    "A": "Returns the number of items in an object",
                    "B": "Converts string to integer", 
                    "C": "Calculates the sum of all items",
                    "D": "Reverses a string"
                },
                "correct_answer": "A",
                "direction_map": {
                    "A": "left",
                    "B": "right", 
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Python"
            },
            {
                "question": "What does CSS stand for?",
                "options": {
                    "A": "Computer Style Sheets",
                    "B": "Creative Style Sheets",
                    "C": "Cascading Style Sheets", 
                    "D": "Colorful Style Sheets"
                },
                "correct_answer": "C",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward", 
                    "D": "backward"
                },
                "category": "Web Dev"
            },
            {
                "question": "In JavaScript, which method adds an element to the end of an array?",
                "options": {
                    "A": "append()",
                    "B": "push()",
                    "C": "add()",
                    "D": "insert()"
                },
                "correct_answer": "B",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "JavaScript"
            },
            {
                "question": "What does SQL stand for?",
                "options": {
                    "A": "Structured Query Language",
                    "B": "Simple Query Language",
                    "C": "Standard Query Language", 
                    "D": "System Query Language"
                },
                "correct_answer": "A",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Database"
            },
            {
                "question": "In Python, what keyword is used to define a function?",
                "options": {
                    "A": "function",
                    "B": "def",
                    "C": "define",
                    "D": "func"
                },
                "correct_answer": "B",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward", 
                    "D": "backward"
                },
                "category": "Python"
            },
            {
                "question": "What does AI stand for?",
                "options": {
                    "A": "Artificial Intelligence",
                    "B": "Automated Intelligence",
                    "C": "Advanced Intelligence",
                    "D": "Applied Intelligence"
                },
                "correct_answer": "A", 
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "AI"
            },
            {
                "question": "In machine learning, what does 'overfitting' mean?",
                "options": {
                    "A": "Model performs well on training data but poorly on new data",
                    "B": "Model has too many parameters",
                    "C": "Model training takes too long",
                    "D": "Model uses too much memory"
                },
                "correct_answer": "A",
                "direction_map": {
                    "A": "left", 
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Machine Learning"
            },
            {
                "question": "What does HTTP stand for?",
                "options": {
                    "A": "HyperText Transfer Protocol",
                    "B": "HyperText Transmission Protocol",
                    "C": "HyperText Transport Protocol",
                    "D": "HyperText Transfer Process"
                },
                "correct_answer": "A",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Web Dev"
            },
            {
                "question": "In Python, which data structure is ordered and changeable?",
                "options": {
                    "A": "tuple",
                    "B": "set",
                    "C": "list",
                    "D": "dictionary"
                },
                "correct_answer": "C",
                "direction_map": {
                    "A": "left",
                    "B": "right", 
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Python"
            },
            {
                "question": "What does API stand for?",
                "options": {
                    "A": "Application Programming Interface",
                    "B": "Automated Programming Interface",
                    "C": "Advanced Programming Interface",
                    "D": "Applied Programming Interface"
                },
                "correct_answer": "A",
                "direction_map": {
                    "A": "left",
                    "B": "right",
                    "C": "forward",
                    "D": "backward"
                },
                "category": "Programming"
            }
        ]
        
    def get_random_question(self):
        """Get a random question from the pool"""
        return random.choice(self.questions)

class MazeGame:
    def __init__(self):
        # Game state
        self.maze = []
        self.width = 0
        self.height = 0
        self.cell_size = 32  # Increased default cell size for zoomed view
        self.player_x = 0
        self.player_y = 0
        self.solution_path = []
        self.show_solution = False
        self.generating = False
        self.game_running = False
        
        # Camera system
        self.camera_x = 0
        self.camera_y = 0
        self.viewport_width = 950
        self.viewport_height = 600
        
        # Lighting system
        self.lighting_enabled = True
        self.light_radius = 200
        self.darkness_color = (0, 0, 0, 255)  # RGBA - semi-transparent black
        self.light_fade = 1.5  # Controls smooth gradient spread
        self.light_overlay = None
        self.light_surface = None
        
        # Minimap system
        self.minimap_expanded = False
        self.minimap_rect = None
        self.expanded_minimap_rect = None
        
        # FOG OF WAR CONFIGURATION
        self.VISIBILITY_RADIUS_MINIMAP = 300  # How far around player is revealed on minimap (in pixels)
        self.FADE_SOFTNESS = 1.8  # Controls gradient smoothness (higher = softer transition)
        self.FOG_COLOR = (20, 20, 20)  # Color of unexplored areas (dark gray)
        self.VISIBLE_TILE_OPACITY = 255  # Full brightness for currently visible area
        self.EXPLORED_TILE_OPACITY = 120  # Dimmer for previously explored areas
        self.UNEXPLORED_TILE_OPACITY = 15  # Nearly black for unexplored areas
        
        # Fog of war system
        self.explored_map = None  # Stores exploration data as 2D array of opacity values
        self.fog_surface = None  # Surface for rendering fog overlay
        self.visibility_surface = None  # Pre-rendered visibility gradient
        
        # Focus management
        self.pygame_focused = False
        
        # Pygame vars
        self.pygame_surface = None
        self.game_canvas = None
        self.clock = None
        
        # QUESTION SYSTEM
        self.question_system = QuestionSystem()
        self.visited_junctions = set()  # Track visited junctions
        self.question_active = False  # Flag to pause movement during questions
        self.question_modal = None  # Modal window for questions
        self.current_question = None  # Currently displayed question
        self.allowed_direction = None  # Direction player is allowed to move after answering
        self.question_timer = None  # Timer for question timeout
        self.previous_position = (0, 0)  # Track where player came from
        self.questions_enabled = True  # Debug flag to disable questions
        
        # Initialize UI
        self.setup_ui()
        self.init_pygame()
        
    def setup_ui(self):
        """Setup main Tkinter window with split layout"""
        self.root = tk.Tk()
        self.root.title("Advanced Maze Game")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Bind global key events to the root window
        self.root.bind('<Key>', self.handle_tkinter_key_event)
        self.root.focus_set()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel (Controls) - 300px width
        self.setup_control_panel(main_frame)
        
        # Right panel (Game Area) - 980px width
        self.setup_game_panel(main_frame)
        
    def setup_control_panel(self, parent):
        """Setup left control panel"""
        control_frame = tk.Frame(parent, bg='#34495e', relief='ridge', bd=2)
        control_frame.pack(side='left', fill='y', padx=(0, 10))
        control_frame.configure(width=300)
        control_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(control_frame, text="🧩 MAZE CONTROL", 
                              font=('Arial', 16, 'bold'), 
                              fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=20)
        
        # Generate button
        self.generate_btn = tk.Button(control_frame, 
                                     text="🎲 Generate Maze",
                                     command=self.generate_maze_clicked,
                                     font=('Arial', 12, 'bold'),
                                     bg='#3498db', fg='white',
                                     relief='raised', bd=3,
                                     width=20, height=2)
        self.generate_btn.pack(pady=10)
        
        # Solve button
        self.solve_btn = tk.Button(control_frame,
                                  text="🧠 Solve Maze",
                                  command=self.solve_maze_clicked,
                                  font=('Arial', 12, 'bold'),
                                  bg='#2ecc71', fg='white',
                                  relief='raised', bd=3,
                                  width=20, height=2,
                                  state='disabled')
        self.solve_btn.pack(pady=10)
        
        # Reset button
        self.reset_btn = tk.Button(control_frame,
                                  text="🔄 Reset Player",
                                  command=self.reset_player_clicked,
                                  font=('Arial', 12, 'bold'),
                                  bg='#f39c12', fg='white',
                                  relief='raised', bd=3,
                                  width=20, height=2,
                                  state='disabled')
        self.reset_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(control_frame,
                                    text="Ready to generate maze...",
                                    font=('Arial', 10),
                                    fg='#ecf0f1', bg='#34495e',
                                    wraplength=280, justify='center')
        self.status_label.pack(pady=20)
        
        # Settings frame
        settings_frame = tk.LabelFrame(control_frame, text="Settings", 
                                      font=('Arial', 10, 'bold'),
                                      fg='#ecf0f1', bg='#34495e')
        settings_frame.pack(pady=20, padx=10, fill='x')
        
        # Maze size input
        tk.Label(settings_frame, text="Maze Width:", 
                font=('Arial', 9), fg='#ecf0f1', bg='#34495e').pack()
        
        self.width_var = tk.StringVar(value="25")
        self.width_entry = tk.Entry(settings_frame, textvariable=self.width_var,
                              width=10, justify='center')
        self.width_entry.pack(pady=2)
        
        # Bind focus events to entry widgets
        self.width_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.width_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        tk.Label(settings_frame, text="Maze Height:", 
                font=('Arial', 9), fg='#ecf0f1', bg='#34495e').pack()
        
        self.height_var = tk.StringVar(value="25")
        self.height_entry = tk.Entry(settings_frame, textvariable=self.height_var,
                               width=10, justify='center')
        self.height_entry.pack(pady=2)
        
        # Bind focus events to entry widgets
        self.height_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.height_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        tk.Label(settings_frame, text="(5-100, camera follows player)", 
                font=('Arial', 8), fg='#bdc3c7', bg='#34495e').pack(pady=2)
        
        # Instructions
        instructions = tk.Label(control_frame,
                               text="🎮 Controls:\nWASD or Arrow Keys\nL - Toggle Lighting\n\n🔴 Player (Camera Center)\n🟢 Goal\n🔵 Start\n🟡 Solution Path\n\n📍 Click minimap to expand\n🕯️ Dynamic lighting enabled\n🌫️ Fog of War minimap\n\n🧠 NEW: Programming Questions\nat junctions test your knowledge!\n\n❓ Answer correctly to choose\nyour path direction!",
                               font=('Arial', 9),
                               fg='#bdc3c7', bg='#34495e',
                               justify='left')
        instructions.pack(side='bottom', pady=20)
        
    def setup_game_panel(self, parent):
        """Setup right game panel"""
        self.game_frame = tk.Frame(parent, bg='#2c3e50', relief='ridge', bd=2)
        self.game_frame.pack(side='right', fill='both', expand=True)
        
        # Game title
        game_title = tk.Label(self.game_frame, text="🎯 Escape Program", 
                             font=('Arial', 14, 'bold'),
                             fg='#ecf0f1', bg='#2c3e50')
        game_title.pack(pady=10)
        
        # Pygame container with fixed dimensions
        self.pygame_container = tk.Frame(self.game_frame, bg='black', relief='sunken', bd=3)
        self.pygame_container.pack(padx=20, pady=10)
        
        # Set fixed size for the pygame container
        self.pygame_container.configure(width=950, height=600)
        self.pygame_container.pack_propagate(False)
        
        # Make pygame container focusable and bind click events
        self.pygame_container.focus_set()
        self.pygame_container.bind('<Button-1>', self.on_pygame_click)
        
        # Minimap will be created later
        self.minimap_canvas = None
        
    def on_entry_focus_in(self, event):
        """Called when entry widget gains focus"""
        self.pygame_focused = False
        
    def on_entry_focus_out(self, event):
        """Called when entry widget loses focus"""
        self.ensure_game_focus()
        
    def on_pygame_click(self, event):
        """Called when pygame area is clicked"""
        # Check if click is on minimap
        if self.minimap_rect and self.minimap_rect.collidepoint(event.x, event.y):
            self.toggle_minimap()
            return
            
        # Check if click is on expanded minimap close button
        if self.minimap_expanded and self.expanded_minimap_rect:
            # Close button area (top-right of expanded minimap)
            close_x = self.expanded_minimap_rect.right - 30
            close_y = self.expanded_minimap_rect.top
            if (close_x <= event.x <= close_x + 25 and 
                close_y <= event.y <= close_y + 25):
                self.toggle_minimap()
                return
        
        self.ensure_game_focus()
        
    def toggle_minimap(self):
        """Toggle between normal and expanded minimap"""
        self.minimap_expanded = not self.minimap_expanded
        if self.minimap_expanded:
            self.status_label.config(text="Expanded minimap view\nClick close button to return")
        else:
            self.status_label.config(text="Camera following player\nUse WASD to move")
        
    def init_pygame(self):
        """Initialize pygame in the tkinter window"""
        # Set pygame window position
        os.environ['SDL_WINDOWID'] = str(self.pygame_container.winfo_id())
        
        # Initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # Start game loop
        self.root.after(100, self.setup_pygame_surface)
        
    def setup_pygame_surface(self):
        """Setup pygame surface after container is ready"""
        try:
            # Wait for container to be properly mapped
            self.pygame_container.update()
            
            # Create pygame display
            self.pygame_surface = pygame.display.set_mode((950, 600))
            pygame.display.set_caption("Maze Game - Camera View")
            
            # Initialize lighting surfaces
            self.init_lighting_system()
            
            # Fill with welcome screen
            self.pygame_surface.fill((40, 40, 40))
            font = pygame.font.Font(None, 48)
            text = font.render("Generate a maze to start!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(475, 300))
            self.pygame_surface.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 32)
            text2 = font_small.render("Camera will follow your player", True, (200, 200, 200))
            text2_rect = text2.get_rect(center=(475, 350))
            self.pygame_surface.blit(text2, text2_rect)
            
            text3 = font_small.render("Press L to toggle lighting", True, (150, 150, 255))
            text3_rect = text3.get_rect(center=(475, 380))
            self.pygame_surface.blit(text3, text3_rect)
            
            text4 = font_small.render("Programming Questions at Junctions!", True, (255, 200, 100))
            text4_rect = text4.get_rect(center=(475, 410))
            self.pygame_surface.blit(text4, text4_rect)
            
            pygame.display.flip()
            
            # Start game loop
            self.game_running = True
            self.game_loop()
            
            # Set initial focus
            self.ensure_game_focus()
            
        except Exception as e:
            print(f"Pygame setup error: {e}")
            self.root.after(100, self.setup_pygame_surface)
    
    def ensure_game_focus(self):
        """Ensure the game has focus for key events"""
        # Clear focus from entry widgets
        self.width_entry.selection_clear()
        self.height_entry.selection_clear()
        
        # Set focus to root window for key capture
        self.root.focus_set()
        self.pygame_focused = True
        
        # Force update
        self.root.update_idletasks()
        
    def update_camera(self):
        """Update camera position to follow player"""
        if not self.maze:
            return
            
        # Center camera on player
        self.camera_x = self.player_x - self.viewport_width // 2
        self.camera_y = self.player_y - self.viewport_height // 2
        
        # Keep camera within maze bounds
        max_camera_x = self.width * self.cell_size - self.viewport_width
        max_camera_y = self.height * self.cell_size - self.viewport_height
        
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
        self.camera_y = max(0, min(self.camera_y, max_camera_y))
    
    def get_grid_pos(self, x, y):
        """Convert pixel position to grid coordinates"""
        return x // self.cell_size, y // self.cell_size
    
    def is_junction(self, grid_x, grid_y):
        """Check if current position is a junction (more than 2 open paths)"""
        if not self.maze or grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return False
            
        if self.maze[grid_y][grid_x] == '#':  # Wall
            return False
            
        # Check all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
        open_paths = 0
        
        for dx, dy in directions:
            nx, ny = grid_x + dx, grid_y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.maze[ny][nx] == ' '):
                open_paths += 1
        
        # Junction if more than 2 open paths
        return open_paths > 2
    
    def show_question_modal(self):
        """Display question modal and pause game"""
        if self.question_modal:
            return  # Modal already exists
            
        self.question_active = True
        self.current_question = self.question_system.get_random_question()
        
        # Create modal window
        self.question_modal = tk.Toplevel(self.root)
        self.question_modal.title("Programming Junction")
        self.question_modal.geometry("600x400")
        self.question_modal.configure(bg='#2c3e50')
        self.question_modal.transient(self.root)
        self.question_modal.grab_set()
        
        # Center the modal
        self.question_modal.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 340,
            self.root.winfo_rooty() + 160
        ))
        
        # Title
        title_label = tk.Label(self.question_modal, 
                              text="🧠 Programming Junction Challenge",
                              font=('Arial', 18, 'bold'),
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Question text
        question_frame = tk.Frame(self.question_modal, bg='#34495e', relief='raised', bd=2)
        question_frame.pack(pady=10, padx=20, fill='x')
        
        question_label = tk.Label(question_frame, 
                                 text=self.current_question['question'],
                                 font=('Arial', 14, 'bold'),
                                 fg='#ecf0f1', bg='#34495e',
                                 wraplength=550, justify='center')
        question_label.pack(pady=15)
        
        # Category label
        category_label = tk.Label(question_frame,
                                 text=f"Category: {self.current_question['category']}",
                                 font=('Arial', 10, 'italic'),
                                 fg='#bdc3c7', bg='#34495e')
        category_label.pack(pady=(0, 10))
        
        # Answer buttons
        self.answer_var = tk.StringVar()
        buttons_frame = tk.Frame(self.question_modal, bg='#2c3e50')
        buttons_frame.pack(pady=20, expand=True)
        
        # Create answer buttons
        button_colors = {'A': '#e74c3c', 'B': '#3498db', 'C': '#2ecc71', 'D': '#f39c12'}
        
        for option, text in self.current_question['options'].items():
            btn = tk.Radiobutton(buttons_frame,
                               text=f"{option}. {text}",
                               variable=self.answer_var,
                               value=option,
                               font=('Arial', 12),
                               bg=button_colors[option],
                               fg='white',
                               selectcolor='#34495e',
                               relief='raised',
                               bd=3,
                               wraplength=500,
                               justify='left')
            btn.pack(pady=5, padx=20, fill='x')
        
        # Submit button
        submit_btn = tk.Button(self.question_modal,
                              text="Submit Answer",
                              command=self.submit_answer,
                              font=('Arial', 14, 'bold'),
                              bg='#9b59b6', fg='white',
                              relief='raised', bd=3,
                              width=20, height=2)
        submit_btn.pack(pady=20)
        
        # Timer label
        self.timer_label = tk.Label(self.question_modal,
                                   text="Time remaining: 15 seconds",
                                   font=('Arial', 12),
                                   fg='#e67e22', bg='#2c3e50')
        self.timer_label.pack(pady=10)
        
        # Start countdown timer
        self.question_time_left = 15
        self.update_timer()
        
        # Direction mapping info
        direction_info = tk.Label(self.question_modal,
                                 text="Your answer determines your allowed direction:\nA=Left, B=Right, C=Forward, D=Backward",
                                 font=('Arial', 10),
                                 fg='#95a5a6', bg='#2c3e50',
                                 justify='center')
        direction_info.pack(side='bottom', pady=10)
        
    def update_timer(self):
        """Update question timer"""
        if not self.question_modal or not self.question_active:
            return
            
        if self.question_time_left > 0:
            self.timer_label.config(text=f"Time remaining: {self.question_time_left} seconds")
            self.question_time_left -= 1
            self.question_timer = self.root.after(1000, self.update_timer)
        else:
            # Time's up - auto-submit or close modal
            self.timer_label.config(text="Time's up!", fg='#e74c3c')
            self.root.after(2000, self.close_question_modal)
    
    def submit_answer(self):
        """Handle answer submission"""
        selected_answer = self.answer_var.get()
        if not selected_answer:
            return
            
        # Cancel timer
        if self.question_timer:
            self.root.after_cancel(self.question_timer)
        
        # Get direction mapping
        direction_map = self.current_question['direction_map']
        self.allowed_direction = direction_map[selected_answer]
        
        # Check if answer is correct
        is_correct = selected_answer == self.current_question['correct_answer']
        
        # Show result
        result_text = f"{'✅ Correct!' if is_correct else '❌ Wrong!'}\n"
        result_text += f"You can move: {self.allowed_direction.upper()}"
        
        result_label = tk.Label(self.question_modal,
                               text=result_text,
                               font=('Arial', 14, 'bold'),
                               fg='#2ecc71' if is_correct else '#e74c3c',
                               bg='#2c3e50')
        result_label.pack(pady=10)
        
        # Close modal after showing result
        self.root.after(2000, self.close_question_modal)
    
    def close_question_modal(self):
        """Close question modal and resume game"""
        if self.question_modal:
            self.question_modal.destroy()
            self.question_modal = None
            
        if self.question_timer:
            self.root.after_cancel(self.question_timer)
            self.question_timer = None
            
        self.question_active = False
        self.ensure_game_focus()
        
        # Show direction hint on game screen
        if self.allowed_direction:
            self.status_label.config(text=f"Junction answered!\nYou can move: {self.allowed_direction.upper()}\nOther directions blocked!")
            # Clear allowed direction after some time
            self.root.after(5000, lambda: self.status_label.config(text="Navigate the maze\nAnswer questions at junctions"))
        else:
            self.status_label.config(text="No answer given\nMovement restricted!")
            
    def handle_tkinter_key_event(self, event):
        """Handle key events from Tkinter and forward to game logic"""
        # Handle lighting toggle
        if event.keysym in ['l', 'L']:
            self.toggle_lighting()
            return "break"
            
        # Only handle keys if pygame is focused and maze exists and no question active
        if (not self.pygame_focused or not self.maze or self.show_solution or 
            self.minimap_expanded or self.question_active):
            # Allow ESC to close expanded minimap
            if event.keysym == 'Escape' and self.minimap_expanded:
                self.toggle_minimap()
            return
            
        # Store previous position
        old_x, old_y = self.player_x, self.player_y
        
        # Map tkinter key events to movement
        moved = False
        new_x, new_y = self.player_x, self.player_y
        direction_attempted = None
        
        if event.keysym in ['Left', 'a', 'A']:
            new_x = max(0, self.player_x - self.cell_size)
            direction_attempted = 'left'
        elif event.keysym in ['Right', 'd', 'D']:
            new_x = min((self.width - 1) * self.cell_size, self.player_x + self.cell_size)
            direction_attempted = 'right'
        elif event.keysym in ['Up', 'w', 'W']:
            new_y = max(0, self.player_y - self.cell_size)
            direction_attempted = 'forward'
        elif event.keysym in ['Down', 's', 'S']:
            new_y = min((self.height - 1) * self.cell_size, self.player_y + self.cell_size)
            direction_attempted = 'backward'
        
        # Check if movement is valid (not hitting walls)
        if direction_attempted and self.can_move_to(new_x, new_y):
            # Check if we're at a junction and need to restrict movement
            current_grid_x, current_grid_y = self.get_grid_pos(self.player_x, self.player_y)
            
            # If we have an allowed direction restriction, check it
            if (self.allowed_direction and 
                self.allowed_direction != direction_attempted and
                self.is_junction(current_grid_x, current_grid_y)):
                # Movement blocked - show message
                self.status_label.config(text=f"❌ Direction blocked!\nYou can only move: {self.allowed_direction.upper()}")
                return "break"
            
            # Valid movement
            self.player_x = new_x
            self.player_y = new_y
            moved = True
            
            # Clear allowed direction restriction after successful move
            if self.allowed_direction:
                self.allowed_direction = None
            
            # Update camera to follow player
            self.update_camera()
            
            # Update fog of war when player moves
            self.update_fog_of_war()
            
            # Check for junctions AFTER moving
            if self.questions_enabled and moved:
                new_grid_x, new_grid_y = self.get_grid_pos(self.player_x, self.player_y)
                junction_key = (new_grid_x, new_grid_y)
                
                # Check if we're at a new junction we haven't visited
                if (self.is_junction(new_grid_x, new_grid_y) and 
                    junction_key not in self.visited_junctions):
                    
                    # Add to visited junctions
                    self.visited_junctions.add(junction_key)
                    
                    # Show question modal
                    self.root.after(500, self.show_question_modal)  # Small delay for smooth experience
        
        # Check win condition after movement
        if moved:
            player_grid_x = self.player_x // self.cell_size
            player_grid_y = self.player_y // self.cell_size
            if player_grid_x == 1 and player_grid_y == 1:
                self.status_label.config(text="🎉 Congratulations!\nYou solved the maze!\nGreat programming knowledge!")
        
        # Prevent event from propagating to entry widgets
        if moved or direction_attempted:
            return "break"
    
    def game_loop(self):
        """Main game loop"""
        if not self.game_running:
            return
            
        # Handle pygame events (mainly for cleanup and window management)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                return
                
        # Render game
        self.render_game()
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
        
    def can_move_to(self, x, y):
        """Check if player can move to position"""
        margin = 1
        
        # Check all corners of the player rectangle
        positions_to_check = [
            (x + margin, y + margin),
            (x + self.cell_size - margin, y + margin),
            (x + margin, y + self.cell_size - margin),
            (x + self.cell_size - margin, y + self.cell_size - margin),
            (x + self.cell_size//2, y + self.cell_size//2)  # Center
        ]
        
        for px, py in positions_to_check:
            col = int(px // self.cell_size)
            row = int(py // self.cell_size)
            
            if (col < 0 or col >= self.width or 
                row < 0 or row >= self.height or 
                self.maze[row][col] == '#'):
                return False
        return True
        
    def render_game(self):
        """Render the game with camera system"""
        if not self.pygame_surface:
            return
            
        self.pygame_surface.fill((40, 40, 40))
        
        if self.maze:
            # Calculate visible range based on camera position
            start_col = max(0, int(self.camera_x // self.cell_size) - 1)
            end_col = min(self.width, int((self.camera_x + self.viewport_width) // self.cell_size) + 2)
            start_row = max(0, int(self.camera_y // self.cell_size) - 1)
            end_row = min(self.height, int((self.camera_y + self.viewport_height) // self.cell_size) + 2)
            
            # Draw maze (only visible portion)
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    # Calculate screen position
                    screen_x = col * self.cell_size - self.camera_x
                    screen_y = row * self.cell_size - self.camera_y
                    
                    # Skip if outside viewport
                    if (screen_x + self.cell_size < 0 or screen_x > self.viewport_width or
                        screen_y + self.cell_size < 0 or screen_y > self.viewport_height):
                        continue
                    
                    if self.maze[row][col] == '#':
                        pygame.draw.rect(self.pygame_surface, (255, 255, 255),
                                       (screen_x, screen_y, self.cell_size, self.cell_size))
                    else:
                        # Color code junctions differently
                        if self.is_junction(col, row):
                            # Highlight junctions with a subtle purple tint
                            if (col, row) in self.visited_junctions:
                                # Visited junction - darker purple
                                pygame.draw.rect(self.pygame_surface, (80, 60, 100),
                                               (screen_x, screen_y, self.cell_size, self.cell_size))
                            else:
                                # Unvisited junction - brighter purple
                                pygame.draw.rect(self.pygame_surface, (100, 80, 120),
                                               (screen_x, screen_y, self.cell_size, self.cell_size))
                        else:
                            # Normal path
                            pygame.draw.rect(self.pygame_surface, (60, 60, 60),
                                           (screen_x, screen_y, self.cell_size, self.cell_size))
            
            # Draw solution path if visible
            if self.show_solution and self.solution_path:
                for col, row in self.solution_path:
                    screen_x = col * self.cell_size - self.camera_x
                    screen_y = row * self.cell_size - self.camera_y
                    
                    # Only draw if visible
                    if (0 <= screen_x <= self.viewport_width - self.cell_size and
                        0 <= screen_y <= self.viewport_height - self.cell_size):
                        pygame.draw.rect(self.pygame_surface, (255, 255, 0),
                                       (screen_x + 4, screen_y + 4, self.cell_size - 8, self.cell_size - 8))
            
            # Draw start and goal
            start_screen_x = (self.width - 2) * self.cell_size - self.camera_x
            start_screen_y = (self.height - 2) * self.cell_size - self.camera_y
            if (0 <= start_screen_x <= self.viewport_width - self.cell_size and
                0 <= start_screen_y <= self.viewport_height - self.cell_size):
                pygame.draw.rect(self.pygame_surface, (0, 0, 255),
                               (start_screen_x + 2, start_screen_y + 2, self.cell_size - 4, self.cell_size - 4))
            
            goal_screen_x = 1 * self.cell_size - self.camera_x
            goal_screen_y = 1 * self.cell_size - self.camera_y
            if (0 <= goal_screen_x <= self.viewport_width - self.cell_size and
                0 <= goal_screen_y <= self.viewport_height - self.cell_size):
                pygame.draw.rect(self.pygame_surface, (0, 255, 0),
                               (goal_screen_x + 2, goal_screen_y + 2, self.cell_size - 4, self.cell_size - 4))
            
            # Draw player (always centered when camera follows)
            if not self.show_solution:
                player_screen_x = self.player_x - self.camera_x
                player_screen_y = self.player_y - self.camera_y
                pygame.draw.rect(self.pygame_surface, (255, 0, 0),
                               (player_screen_x + 1, player_screen_y + 1, 
                                self.cell_size - 2, self.cell_size - 2))
            
            # Draw junction indicators on visible junctions
            current_grid_x, current_grid_y = self.get_grid_pos(self.player_x, self.player_y)
            for row in range(start_row, end_row):
                for col in range(start_col, end_col):
                    if self.is_junction(col, row):
                        screen_x = col * self.cell_size - self.camera_x
                        screen_y = row * self.cell_size - self.camera_y
                        
                        if (0 <= screen_x <= self.viewport_width - self.cell_size and
                            0 <= screen_y <= self.viewport_height - self.cell_size):
                            
                            # Draw question mark for unvisited junctions
                            if (col, row) not in self.visited_junctions:
                                center_x = screen_x + self.cell_size // 2
                                center_y = screen_y + self.cell_size // 2
                                
                                # Draw question mark
                                font = pygame.font.Font(None, max(16, self.cell_size // 2))
                                text = font.render("?", True, (255, 255, 0))
                                text_rect = text.get_rect(center=(center_x, center_y))
                                self.pygame_surface.blit(text, text_rect)
            
            # Apply lighting effect if enabled
            if self.lighting_enabled:
                player_screen_x = self.player_x - self.camera_x
                player_screen_y = self.player_y - self.camera_y
                player_center = (player_screen_x + self.cell_size // 2, 
                               player_screen_y + self.cell_size // 2)
                self.draw_light_overlay(self.pygame_surface, player_center)
            
            # Draw minimap with fog of war
            self.render_minimap()
        
        pygame.display.flip()
        
    def init_fog_of_war(self):
        """Initialize fog of war system for new maze"""
        if not self.maze:
            return
            
        # Initialize explored map - all areas start as unexplored (low opacity)
        self.explored_map = [[self.UNEXPLORED_TILE_OPACITY for _ in range(self.width)] 
                           for _ in range(self.height)]
        
        # Create fog surface for rendering
        # Size based on largest possible minimap
        max_minimap_size = max(600, 120)  # Accommodate both compact and expanded
        self.fog_surface = pygame.Surface((max_minimap_size, max_minimap_size), pygame.SRCALPHA)
        
        # Create visibility gradient surface
        visibility_diameter = int(self.VISIBILITY_RADIUS_MINIMAP * 2 * self.FADE_SOFTNESS)
        self.visibility_surface = pygame.Surface((visibility_diameter, visibility_diameter), pygame.SRCALPHA)
        self.create_visibility_gradient()
        
        # Update initial position
        self.update_fog_of_war()
    
    def create_visibility_gradient(self):
        """Create a radial gradient for minimap visibility"""
        if not self.visibility_surface:
            return
            
        visibility_diameter = int(self.VISIBILITY_RADIUS_MINIMAP * 2 * self.FADE_SOFTNESS)
        center = visibility_diameter // 2
        
        # Clear the surface
        self.visibility_surface.fill((0, 0, 0, 0))
        
        # Create radial gradient from center outward
        for radius in range(int(self.VISIBILITY_RADIUS_MINIMAP * self.FADE_SOFTNESS), 0, -1):
            # Calculate opacity based on distance from center
            if radius <= self.VISIBILITY_RADIUS_MINIMAP:
                # Full visibility in the center
                opacity = self.VISIBLE_TILE_OPACITY
            else:
                # Fade out gradually
                fade_distance = radius - self.VISIBILITY_RADIUS_MINIMAP
                max_fade_distance = self.VISIBILITY_RADIUS_MINIMAP * (self.FADE_SOFTNESS - 1)
                fade_factor = 1.0 - (fade_distance / max_fade_distance)
                opacity = int(self.EXPLORED_TILE_OPACITY * fade_factor)
            
            # Draw circle with calculated opacity
            color = (255, 255, 255, opacity)
            if opacity > 0:
                pygame.draw.circle(self.visibility_surface, color, (center, center), radius)
    
    def update_fog_of_war(self):
        """Update explored areas based on player position"""
        if not self.maze or not self.explored_map:
            return
            
        # Convert player position to grid coordinates
        player_grid_x = self.player_x // self.cell_size
        player_grid_y = self.player_y // self.cell_size
        
        # Calculate visibility radius in grid cells
        visibility_grid_radius = max(1, int(self.VISIBILITY_RADIUS_MINIMAP / max(self.cell_size, 1)))
        
        # Update exploration for areas within visibility radius
        for dy in range(-visibility_grid_radius, visibility_grid_radius + 1):
            for dx in range(-visibility_grid_radius, visibility_grid_radius + 1):
                grid_x = player_grid_x + dx
                grid_y = player_grid_y + dy
                
                # Check bounds
                if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                    # Calculate distance from player
                    distance = math.sqrt(dx * dx + dy * dy) * max(self.cell_size, 1)
                    
                    if distance <= self.VISIBILITY_RADIUS_MINIMAP:
                        # Currently visible area
                        opacity = self.VISIBLE_TILE_OPACITY
                    elif distance <= self.VISIBILITY_RADIUS_MINIMAP * self.FADE_SOFTNESS:
                        # Fade zone - becomes explored
                        fade_distance = distance - self.VISIBILITY_RADIUS_MINIMAP
                        max_fade_distance = self.VISIBILITY_RADIUS_MINIMAP * (self.FADE_SOFTNESS - 1)
                        fade_factor = 1.0 - (fade_distance / max_fade_distance)
                        opacity = int(self.EXPLORED_TILE_OPACITY * fade_factor)
                    else:
                        # Keep current exploration level (don't reduce visibility)
                        opacity = self.explored_map[grid_y][grid_x]
                    
                    # Update only if new opacity is higher (more visible)
                    self.explored_map[grid_y][grid_x] = max(self.explored_map[grid_y][grid_x], opacity)
    
    def render_minimap(self):
        """Render minimap overlay with fog of war"""
        if not self.maze:
            return
            
        if self.minimap_expanded:
            self.render_expanded_minimap()
        else:
            self.render_compact_minimap()
    
    def render_compact_minimap(self):
        """Render small minimap in corner with fog of war"""
        # Minimap configuration
        minimap_size = 120
        minimap_x = self.viewport_width - minimap_size - 70
        minimap_y = 15
        
        # Store minimap rect for click detection
        self.minimap_rect = pygame.Rect(minimap_x, minimap_y, minimap_size, minimap_size)
        
        # Draw minimap background
        pygame.draw.rect(self.pygame_surface, (20, 20, 20), self.minimap_rect)
        pygame.draw.rect(self.pygame_surface, (100, 100, 100), self.minimap_rect, 2)
        
        # Calculate minimap scale
        scale_x = (minimap_size - 10) / (self.width * self.cell_size)
        scale_y = (minimap_size - 10) / (self.height * self.cell_size)
        scale = min(scale_x, scale_y)
        
        # Draw maze on minimap with fog of war
        for row in range(self.height):
            for col in range(self.width):
                mini_x = minimap_x + 5 + col * self.cell_size * scale
                mini_y = minimap_y + 5 + row * self.cell_size * scale
                mini_size = max(1, int(self.cell_size * scale))
                
                # Get exploration opacity for this tile
                if self.explored_map:
                    tile_opacity = self.explored_map[row][col]
                else:
                    tile_opacity = self.UNEXPLORED_TILE_OPACITY
                
                # Draw based on exploration and maze structure
                if tile_opacity <= self.UNEXPLORED_TILE_OPACITY:
                    # Unexplored - draw fog
                    color = self.FOG_COLOR
                elif self.maze[row][col] == '#':
                    # Explored wall
                    base_color = 200
                    alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                    color_value = int(base_color * alpha_factor)
                    color = (color_value, color_value, color_value)
                else:
                    # Explored path - highlight junctions
                    if self.is_junction(col, row):
                        if (col, row) in self.visited_junctions:
                            # Visited junction - purple
                            base_color = (80, 60, 100)
                        else:
                            # Unvisited junction - bright purple
                            base_color = (120, 100, 140)
                        alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                        color = tuple(int(c * alpha_factor) for c in base_color)
                    else:
                        # Normal path
                        base_color = 60
                        alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                        color_value = int(base_color * alpha_factor)
                        color = (color_value, color_value, color_value)
                
                pygame.draw.rect(self.pygame_surface, color,
                               (mini_x, mini_y, mini_size, mini_size))
        
        # Draw player on minimap (only if explored)
        player_grid_x = self.player_x // self.cell_size
        player_grid_y = self.player_y // self.cell_size
        if (self.explored_map and 0 <= player_grid_x < self.width and 0 <= player_grid_y < self.height and
            self.explored_map[player_grid_y][player_grid_x] > self.UNEXPLORED_TILE_OPACITY):
            player_mini_x = minimap_x + 5 + (self.player_x * scale)
            player_mini_y = minimap_y + 5 + (self.player_y * scale)
            player_mini_size = max(2, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (255, 0, 0),
                           (player_mini_x, player_mini_y, player_mini_size, player_mini_size))
        
        # Draw camera viewport on minimap (only if area is explored)
        viewport_mini_x = minimap_x + 5 + (self.camera_x * scale)
        viewport_mini_y = minimap_y + 5 + (self.camera_y * scale)
        viewport_mini_w = self.viewport_width * scale
        viewport_mini_h = self.viewport_height * scale
        pygame.draw.rect(self.pygame_surface, (0, 255, 255),
                       (viewport_mini_x, viewport_mini_y, viewport_mini_w, viewport_mini_h), 1)
        
        # Draw goal and start on minimap (only if explored)
        if (self.explored_map and self.explored_map[1][1] > self.UNEXPLORED_TILE_OPACITY):
            goal_mini_x = minimap_x + 5 + (1 * self.cell_size * scale)
            goal_mini_y = minimap_y + 5 + (1 * self.cell_size * scale)
            player_mini_size = max(2, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (0, 255, 0),
                           (goal_mini_x, goal_mini_y, player_mini_size, player_mini_size))
        
        if (self.explored_map and self.height >= 2 and self.width >= 2 and 
            self.explored_map[self.height-2][self.width-2] > self.UNEXPLORED_TILE_OPACITY):
            start_mini_x = minimap_x + 5 + ((self.width - 2) * self.cell_size * scale)
            start_mini_y = minimap_y + 5 + ((self.height - 2) * self.cell_size * scale)
            player_mini_size = max(2, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (0, 0, 255),
                           (start_mini_x, start_mini_y, player_mini_size, player_mini_size))
        
    def render_expanded_minimap(self):
        """Render full-size minimap overlay with fog of war"""
        # Expanded minimap takes most of the screen
        expanded_size = min(self.viewport_width - 100, self.viewport_height - 100)
        expanded_x = (self.viewport_width - expanded_size) // 2
        expanded_y = (self.viewport_height - expanded_size) // 2
        
        # Store expanded minimap rect
        self.expanded_minimap_rect = pygame.Rect(expanded_x, expanded_y, expanded_size, expanded_size)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.viewport_width, self.viewport_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.pygame_surface.blit(overlay, (0, 0))
        
        # Draw expanded minimap background
        pygame.draw.rect(self.pygame_surface, (30, 30, 30), self.expanded_minimap_rect)
        pygame.draw.rect(self.pygame_surface, (150, 150, 150), self.expanded_minimap_rect, 3)
        
        # Calculate scale for expanded minimap
        scale_x = (expanded_size - 20) / (self.width * self.cell_size)
        scale_y = (expanded_size - 20) / (self.height * self.cell_size)
        scale = min(scale_x, scale_y)
        
        # Draw maze on expanded minimap with fog of war and junction highlights
        for row in range(self.height):
            for col in range(self.width):
                mini_x = expanded_x + 10 + col * self.cell_size * scale
                mini_y = expanded_y + 10 + row * self.cell_size * scale
                mini_size = max(1, int(self.cell_size * scale))
                
                # Get exploration opacity for this tile
                if self.explored_map:
                    tile_opacity = self.explored_map[row][col]
                else:
                    tile_opacity = self.UNEXPLORED_TILE_OPACITY
                
                # Draw based on exploration and maze structure
                if tile_opacity <= self.UNEXPLORED_TILE_OPACITY:
                    # Unexplored - draw fog
                    color = self.FOG_COLOR
                elif self.maze[row][col] == '#':
                    # Explored wall
                    base_color = 200
                    alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                    color_value = int(base_color * alpha_factor)
                    color = (color_value, color_value, color_value)
                else:
                    # Explored path - highlight junctions
                    if self.is_junction(col, row):
                        if (col, row) in self.visited_junctions:
                            # Visited junction - purple
                            base_color = (80, 60, 100)
                        else:
                            # Unvisited junction - bright purple
                            base_color = (120, 100, 140)
                        alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                        color = tuple(int(c * alpha_factor) for c in base_color)
                    else:
                        # Normal path
                        base_color = 60
                        alpha_factor = tile_opacity / self.VISIBLE_TILE_OPACITY
                        color_value = int(base_color * alpha_factor)
                        color = (color_value, color_value, color_value)
                
                pygame.draw.rect(self.pygame_surface, color,
                               (mini_x, mini_y, mini_size, mini_size))
        
        # Draw solution path if visible and explored
        if self.show_solution and self.solution_path:
            for col, row in self.solution_path:
                if (self.explored_map and 0 <= row < self.height and 0 <= col < self.width and
                    self.explored_map[row][col] > self.UNEXPLORED_TILE_OPACITY):
                    mini_x = expanded_x + 10 + col * self.cell_size * scale
                    mini_y = expanded_y + 10 + row * self.cell_size * scale
                    mini_size = max(1, int(self.cell_size * scale))
                    pygame.draw.rect(self.pygame_surface, (255, 255, 0),
                                   (mini_x + 1, mini_y + 1, mini_size - 2, mini_size - 2))
        
        # Draw player on expanded minimap (only if explored)
        player_grid_x = self.player_x // self.cell_size
        player_grid_y = self.player_y // self.cell_size
        if (self.explored_map and 0 <= player_grid_x < self.width and 0 <= player_grid_y < self.height and
            self.explored_map[player_grid_y][player_grid_x] > self.UNEXPLORED_TILE_OPACITY):
            player_mini_x = expanded_x + 10 + (self.player_x * scale)
            player_mini_y = expanded_y + 10 + (self.player_y * scale)
            player_mini_size = max(3, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (255, 0, 0),
                           (player_mini_x, player_mini_y, player_mini_size, player_mini_size))
        
        # Draw camera viewport on expanded minimap
        viewport_mini_x = expanded_x + 10 + (self.camera_x * scale)
        viewport_mini_y = expanded_y + 10 + (self.camera_y * scale)
        viewport_mini_w = self.viewport_width * scale
        viewport_mini_h = self.viewport_height * scale
        pygame.draw.rect(self.pygame_surface, (0, 255, 255),
                       (viewport_mini_x, viewport_mini_y, viewport_mini_w, viewport_mini_h), 2)
        
        # Draw goal and start on expanded minimap (only if explored)
        if (self.explored_map and self.explored_map[1][1] > self.UNEXPLORED_TILE_OPACITY):
            goal_mini_x = expanded_x + 10 + (1 * self.cell_size * scale)
            goal_mini_y = expanded_y + 10 + (1 * self.cell_size * scale)
            player_mini_size = max(3, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (0, 255, 0),
                           (goal_mini_x, goal_mini_y, player_mini_size, player_mini_size))
        
        if (self.explored_map and self.height >= 2 and self.width >= 2 and 
            self.explored_map[self.height-2][self.width-2] > self.UNEXPLORED_TILE_OPACITY):
            start_mini_x = expanded_x + 10 + ((self.width - 2) * self.cell_size * scale)
            start_mini_y = expanded_y + 10 + ((self.height - 2) * self.cell_size * scale)
            player_mini_size = max(3, int(self.cell_size * scale))
            pygame.draw.rect(self.pygame_surface, (0, 0, 255),
                           (start_mini_x, start_mini_y, player_mini_size, player_mini_size))
        
        # Draw close button
        close_x = self.expanded_minimap_rect.right - 30
        close_y = self.expanded_minimap_rect.top
        pygame.draw.rect(self.pygame_surface, (200, 50, 50), (close_x, close_y, 25, 25))
        
        # Draw X for close button
        font = pygame.font.Font(None, 20)
        close_text = font.render("X", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=(close_x + 12, close_y + 12))
        self.pygame_surface.blit(close_text, close_rect)
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instruction = font.render("Click X to close | ESC to close | Purple = Junctions | Questions at unvisited junctions", True, (255, 255, 255))
        inst_rect = instruction.get_rect(center=(self.viewport_width // 2, expanded_y - 25))
        self.pygame_surface.blit(instruction, inst_rect)
        
    def init_lighting_system(self):
        """Initialize lighting system surfaces"""
        # Create overlay surface for darkness
        self.light_overlay = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
        
        # Create light surface for the radial gradient
        light_diameter = int(self.light_radius * 2 * self.light_fade)
        self.light_surface = pygame.Surface((light_diameter, light_diameter), pygame.SRCALPHA)
        
        # Pre-render the radial gradient light
        self.create_light_gradient()
        
    def create_light_gradient(self):
        """Create a radial gradient for the light effect"""
        if not self.light_surface:
            return
            
        light_diameter = int(self.light_radius * 2 * self.light_fade)
        center = light_diameter // 2
        
        # Clear the surface
        self.light_surface.fill((0, 0, 0, 0))
        
        # Create radial gradient
        for radius in range(int(self.light_radius * self.light_fade), 0, -1):
            # Calculate alpha based on distance from center
            if radius <= self.light_radius:
                # Full brightness in the center
                alpha = 255
            else:
                # Fade out gradually
                fade_distance = radius - self.light_radius
                max_fade_distance = self.light_radius * (self.light_fade - 1)
                alpha = max(0, 255 - int(255 * fade_distance / max_fade_distance))
            
            # Draw circle with calculated alpha
            color = (255, 255, 255, alpha)
            if alpha > 0:
                pygame.draw.circle(self.light_surface, color, (center, center), radius)
    
    def draw_light_overlay(self, surface, light_center):
        """Draw the lighting overlay effect"""
        if not self.lighting_enabled or not self.light_overlay or not self.light_surface:
            return
        
        # Fill overlay with darkness
        self.light_overlay.fill(self.darkness_color)
        
        # Calculate light position on overlay
        light_diameter = int(self.light_radius * 2 * self.light_fade)
        light_x = light_center[0] - light_diameter // 2
        light_y = light_center[1] - light_diameter // 2
        
        # Subtract (blend) the light from the darkness using BLEND_RGBA_SUB
        self.light_overlay.blit(self.light_surface, (light_x, light_y), 
                              special_flags=pygame.BLEND_RGBA_SUB)
        
        # Apply the overlay to the main surface
        surface.blit(self.light_overlay, (0, 0))
    
    def toggle_lighting(self):
        """Toggle lighting system on/off"""
        self.lighting_enabled = not self.lighting_enabled
        
        if self.lighting_enabled:
            self.status_label.config(text="🕯️ Lighting enabled\nUse WASD to move")
            # Recreate lighting surfaces if needed
            if not self.light_overlay or not self.light_surface:
                self.init_lighting_system()
        else:
            self.status_label.config(text="💡 Lighting disabled\nUse WASD to move")
    
    def update_light_settings(self, radius=None, darkness_alpha=None, fade=None):
        """Update lighting settings and recreate surfaces if needed"""
        settings_changed = False
        
        if radius is not None and radius != self.light_radius:
            self.light_radius = radius
            settings_changed = True
            
        if darkness_alpha is not None:
            self.darkness_color = (self.darkness_color[0], self.darkness_color[1], 
                                 self.darkness_color[2], darkness_alpha)
            
        if fade is not None and fade != self.light_fade:
            self.light_fade = fade
            settings_changed = True
        
        # Recreate light surface if radius or fade changed
        if settings_changed and self.lighting_enabled:
            light_diameter = int(self.light_radius * 2 * self.light_fade)
            self.light_surface = pygame.Surface((light_diameter, light_diameter), pygame.SRCALPHA)
            self.create_light_gradient()
        
    def generate_maze_clicked(self):
        """Handle generate maze button click"""
        self.ensure_game_focus()
        self.generate_maze_threaded()
        
    def solve_maze_clicked(self):
        """Handle solve maze button click"""
        self.ensure_game_focus()
        self.solve_maze()
        
    def reset_player_clicked(self):
        """Handle reset player button click"""
        self.ensure_game_focus()
        self.reset_player()
        
    def generate_maze_threaded(self):
        """Start maze generation in separate thread"""
        if self.generating:
            return
            
        # Validate input
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width < 5 or width > 100 or height < 5 or height > 100:
                self.status_label.config(text="Error: Size must be\nbetween 5 and 100")
                return
        except ValueError:
            self.status_label.config(text="Error: Please enter\nvalid numbers")
            return
            
        self.generating = True
        self.generate_btn.config(state='disabled')
        self.solve_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.status_label.config(text="Generating maze...")
        
        # Start generation thread
        thread = threading.Thread(target=self.generate_maze, args=(width, height), daemon=True)
        thread.start()
        
    def generate_maze(self, w, h):
        """Generate maze using Prim's algorithm"""
        try:
            self.width, self.height = w, h
            if self.width % 2 == 0: self.width += 1
            if self.height % 2 == 0: self.height += 1
            
            # Calculate optimal cell size for camera view
            # Make cells larger for better zoomed experience
            min_cell_size = 16
            max_cell_size = 48
            
            # Calculate based on viewport size
            optimal_width_cell = self.viewport_width // (self.width // 3)  # Show about 1/3 of maze width
            optimal_height_cell = self.viewport_height // (self.height // 3)  # Show about 1/3 of maze height
            
            self.cell_size = max(min_cell_size, min(max_cell_size, min(optimal_width_cell, optimal_height_cell)))
            
            # Initialize maze
            self.maze = [['#' for _ in range(self.width)] for _ in range(self.height)]
            
            # Prim's algorithm
            start_x = random.randint(1, self.width // 2) * 2 - 1
            start_y = random.randint(1, self.height // 2) * 2 - 1
            self.maze[start_y][start_x] = ' '
            walls = [(start_x, start_y)]
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            
            while walls:
                x, y = random.choice(walls)
                walls.remove((x, y))
                random.shuffle(directions)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and 
                        self.maze[ny][nx] == '#'):
                        self.maze[(y + ny) // 2][(x + nx) // 2] = ' '
                        self.maze[ny][nx] = ' '
                        walls.append((nx, ny))
                        
                # Update status periodically
                if len(walls) % 10 == 0:
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"Generating maze...\n{len(walls)} walls remaining"))
            
            # Ensure start and end are open
            self.maze[self.height-2][self.width-2] = ' '  # Start (bottom-right)
            self.maze[1][1] = ' '  # Goal (top-left)
            
            # Set player position at start
            self.player_x = (self.width - 2) * self.cell_size
            self.player_y = (self.height - 2) * self.cell_size
            
            # Initialize camera to follow player
            self.update_camera()
            
            # Update UI
            self.root.after(0, self.maze_generated)
            
        except Exception as e:
            print(f"Maze generation error: {e}")
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {e}"))
            
    def maze_generated(self):
        """Called when maze generation is complete"""
        self.generating = False
        self.show_solution = False
        self.minimap_expanded = False
        self.generate_btn.config(state='normal')
        self.solve_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        
        # Reset question system for new maze
        self.visited_junctions.clear()
        self.question_active = False
        self.allowed_direction = None
        if self.question_modal:
            self.question_modal.destroy()
            self.question_modal = None
        
        self.status_label.config(text="Maze generated!\n🧠 Programming questions\nat junctions!\nUse WASD to move\nPress L for lighting")
        
        # Initialize/update lighting system for new maze
        if self.pygame_surface:
            self.init_lighting_system()
        
        # Initialize fog of war system
        self.init_fog_of_war()
        
        # Ensure game focus is set with a small delay
        self.root.after(200, self.ensure_game_focus)
        
    def solve_maze(self):
        """Solve maze using A* algorithm"""
        if not self.maze:
            return
            
        self.status_label.config(text="Solving maze...")
        
        # A* algorithm
        start = (self.width - 2, self.height - 2)
        goal = (1, 1)
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        queue = [(0, start)]
        g_cost = {start: 0}
        parents = {start: None}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            _, current = heapq.heappop(queue)
            
            if current == goal:
                break
                
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                nx, ny = neighbor
                
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.maze[ny][nx] == ' '):
                    new_g = g_cost[current] + 1
                    
                    if neighbor not in g_cost or new_g < g_cost[neighbor]:
                        g_cost[neighbor] = new_g
                        f = new_g + heuristic(neighbor, goal)
                        heapq.heappush(queue, (f, neighbor))
                        parents[neighbor] = current
        
        # Build solution path
        self.solution_path = []
        current = goal
        while current is not None:
            self.solution_path.append(current)
            current = parents.get(current)
        
        self.show_solution = True
        self.status_label.config(text="Maze solved!\nYellow path shows solution\nClick minimap to see junctions\n🧠 Questions disabled in solve mode")
        
    def reset_player(self):
        """Reset player to start position and clear exploration"""
        if self.maze:
            self.player_x = (self.width - 2) * self.cell_size
            self.player_y = (self.height - 2) * self.cell_size
            self.show_solution = False
            self.minimap_expanded = False
            
            # Reset question system
            self.visited_junctions.clear()
            self.question_active = False
            self.allowed_direction = None
            if self.question_modal:
                self.question_modal.destroy()
                self.question_modal = None
            
            # Update camera to follow player
            self.update_camera()
            
            # Reset fog of war - clear all exploration
            self.init_fog_of_war()
            
            self.status_label.config(text="Player reset!\nJunctions reset!\nExploration cleared!\n🧠 Questions reactivated!")
            
            # Ensure focus after reset
            self.root.after(100, self.ensure_game_focus)
            
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        self.game_running = False
        
        # Close question modal if open
        if self.question_modal:
            try:
                self.question_modal.destroy()
            except:
                pass
                
        # Cancel any timers
        if self.question_timer:
            try:
                self.root.after_cancel(self.question_timer)
            except:
                pass
                
        try:
            pygame.quit()
        except:
            pass
        self.root.destroy()

# Run the game
if __name__ == "__main__":
    game = MazeGame()
    game.run()