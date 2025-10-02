import pygame
import math
import time
import random
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()
pygame.mixer.init()

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    HOW_TO_PLAY = "how_to_play"

class Difficulty(Enum):
    EASY = {"speed": 8, "obstacles": 3, "name": "Easy"}
    MEDIUM = {"speed": 12, "obstacles": 6, "name": "Medium"}
    HARD = {"speed": 16, "obstacles": 10, "name": "Hard"}

class PowerUpType(Enum):
    SLOW_TIME = {"color": (0, 191, 255), "duration": 3000, "name": "Slow Time"}
    SHRINK = {"color": (255, 165, 0), "duration": 5000, "name": "Shrink"}
    BONUS_POINTS = {"color": (255, 215, 0), "duration": 0, "name": "Bonus Points"}

@dataclass
class Position:
    x: float
    y: float
    
    def to_grid(self, block_size: int) -> Tuple[int, int]:
        return (int(self.x // block_size), int(self.y // block_size))

class Theme:
    def __init__(self, dark_mode: bool = False):
        if dark_mode:
            self.bg_color = (25, 25, 25)
            self.snake_color = (100, 200, 100)
            self.food_color = (255, 100, 100)
            self.text_color = (255, 255, 255)
            self.ui_bg = (40, 40, 40)
            self.button_color = (60, 60, 60)
            self.button_hover = (80, 80, 80)
            self.obstacle_color = (150, 150, 150)
        else:
            self.bg_color = (114, 183, 106)
            self.snake_color = (26, 115, 232)
            self.food_color = (233, 67, 37)
            self.text_color = (255, 255, 255)
            self.ui_bg = (50, 50, 50, 180)
            self.button_color = (70, 130, 180)
            self.button_hover = (100, 149, 237)
            self.obstacle_color = (139, 69, 19)

class PowerUp:
    def __init__(self, x: int, y: int, power_type: PowerUpType, block_size: int):
        self.x = x
        self.y = y
        self.type = power_type
        self.block_size = block_size
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10000  # 10 seconds
        
    def draw(self, screen, theme):
        color = self.type.value["color"]
        # Pulsing effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
        size_offset = int(pulse * 5)
        
        pygame.draw.rect(screen, color, 
                        [self.x * self.block_size - size_offset//2, 
                         self.y * self.block_size - size_offset//2, 
                         self.block_size + size_offset, 
                         self.block_size + size_offset])
        
        # Draw power-up symbol
        center_x = self.x * self.block_size + self.block_size // 2
        center_y = self.y * self.block_size + self.block_size // 2
        
        if self.type == PowerUpType.SLOW_TIME:
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 5)
        elif self.type == PowerUpType.SHRINK:
            pygame.draw.polygon(screen, (255, 255, 255), 
                              [(center_x-5, center_y+5), (center_x+5, center_y+5), (center_x, center_y-5)])
        elif self.type == PowerUpType.BONUS_POINTS:
            pygame.draw.polygon(screen, (255, 255, 255),
                              [(center_x, center_y-6), (center_x-4, center_y+2), 
                               (center_x+4, center_y+2)])
    
    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

class Snake:
    def __init__(self, start_x: float, start_y: float, block_size: int):
        self.block_size = block_size
        self.segments = [
            Position(start_x - 2 * block_size, start_y),
            Position(start_x - block_size, start_y),
            Position(start_x, start_y)
        ]
        self.direction = Position(1, 0)
        self.next_direction = Position(1, 0)
        self.speed = 200.0  # pixels per second
        self.move_timer = 0
        self.move_interval = 1000 / 10  # 10 moves per second initially
        self.growing = False
        self.skin = 0  # Current skin index
        
    def update(self, delta_time: float):
        self.move_timer += delta_time
        
        if self.move_timer >= self.move_interval:
            # Update direction
            if (self.next_direction.x != -self.direction.x or 
                self.next_direction.y != -self.direction.y):
                self.direction = self.next_direction
            
            # Move snake
            head = self.segments[-1]
            new_head = Position(
                head.x + self.direction.x * self.block_size,
                head.y + self.direction.y * self.block_size
            )
            self.segments.append(new_head)
            
            if not self.growing:
                self.segments.pop(0)
            else:
                self.growing = False
                
            self.move_timer = 0
    
    def set_direction(self, direction: Position):
        # Prevent moving into itself
        if len(self.segments) > 1:
            if (direction.x != -self.direction.x or direction.y != -self.direction.y):
                self.next_direction = direction
        else:
            self.next_direction = direction
    
    def grow(self):
        self.growing = True
    
    def shrink(self):
        if len(self.segments) > 3:
            self.segments.pop(0)
    
    def set_speed(self, speed: float):
        self.move_interval = 1000 / speed
    
    def check_self_collision(self) -> bool:
        head = self.segments[-1]
        return any(segment.x == head.x and segment.y == head.y 
                  for segment in self.segments[:-1])
    
    def check_wall_collision(self, width: int, height: int) -> bool:
        head = self.segments[-1]
        return (head.x < 0 or head.x >= width or 
                head.y < 0 or head.y >= height)
    
    def check_obstacle_collision(self, obstacles: List[Tuple[int, int]]) -> bool:
        head = self.segments[-1]
        grid_pos = head.to_grid(self.block_size)
        return grid_pos in obstacles
    
    def draw(self, screen, theme):
        # Snake skins
        snake_colors = [
            theme.snake_color,  # Default
            (255, 100, 255),    # Pink
            (100, 255, 100),    # Bright Green
            (255, 255, 100),    # Yellow
            (100, 100, 255),    # Blue
        ]
        
        color = snake_colors[self.skin % len(snake_colors)]
        
        for i, segment in enumerate(self.segments):
            # Head is slightly larger
            size_offset = 3 if i == len(self.segments) - 1 else 0
            
            pygame.draw.rect(screen, color, 
                           [segment.x - size_offset//2, segment.y - size_offset//2, 
                            self.block_size + size_offset, self.block_size + size_offset])
            
            # Add eyes to head
            if i == len(self.segments) - 1:
                eye_offset = 5
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (int(segment.x + eye_offset), int(segment.y + eye_offset)), 2)
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (int(segment.x + self.block_size - eye_offset), 
                                  int(segment.y + eye_offset)), 2)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        
    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        return False
    
    def draw(self, screen, theme):
        color = theme.button_hover if self.hovered else theme.button_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, theme.text_color, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, theme.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        
        # Create simple sound effects
        try:
            # You can replace these with actual sound files
            self.create_beep_sound("eat", 800, 0.1)
            self.create_beep_sound("game_over", 300, 0.5)
            self.create_beep_sound("pause", 600, 0.1)
            self.create_beep_sound("powerup", 1000, 0.2)
        except:
            # If sound creation fails, disable sounds
            pass
    
    def create_beep_sound(self, name: str, frequency: int, duration: float):
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr.append([int(wave), int(wave)])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
        self.sounds[name] = sound
    
    def play_sound(self, name: str):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass
    
    def play_background_music(self):
        # You can add background music file here
        pass

class GameData:
    def __init__(self):
        self.high_score = 0
        self.unlocked_skins = [0]  # Start with default skin unlocked
        self.dark_mode = False
        self.load_data()
    
    def load_data(self):
        try:
            with open("game_data.json", "r") as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
                self.unlocked_skins = data.get("unlocked_skins", [0])
                self.dark_mode = data.get("dark_mode", False)
        except:
            pass
    
    def save_data(self):
        data = {
            "high_score": self.high_score,
            "unlocked_skins": self.unlocked_skins,
            "dark_mode": self.dark_mode
        }
        try:
            with open("game_data.json", "w") as f:
                json.dump(data, f)
        except:
            pass
    
    def unlock_skin(self, skin_id: int):
        if skin_id not in self.unlocked_skins:
            self.unlocked_skins.append(skin_id)
            self.save_data()
            return True
        return False

class EnhancedSnakeGame:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.GAME_WIDTH = 640
        self.GAME_HEIGHT = 480
        self.BLOCK_SIZE = 20
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
                                              pygame.RESIZABLE)
        pygame.display.set_caption("Enhanced Snake Game")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.game_data = GameData()
        self.theme = Theme(self.game_data.dark_mode)
        self.sound_manager = SoundManager()
        
        self.state = GameState.MENU
        self.difficulty = Difficulty.MEDIUM
        
        # Game variables
        self.snake = None
        self.food_pos = Position(0, 0)
        self.score = 0
        self.obstacles = []
        self.power_ups = []
        self.active_power_ups = {}
        
        # Timing
        self.last_time = pygame.time.get_ticks()
        self.power_up_spawn_timer = 0
        
        self.create_ui_elements()
        
    def create_ui_elements(self):
        # Menu buttons
        button_width, button_height = 200, 50
        center_x = self.SCREEN_WIDTH // 2 - button_width // 2
        
        self.menu_buttons = {
            "start": Button(center_x, 200, button_width, button_height, "Start Game", self.font),
            "how_to_play": Button(center_x, 270, button_width, button_height, "How to Play", self.font),
            "difficulty": Button(center_x, 340, button_width, button_height, 
                               f"Difficulty: {self.difficulty.value['name']}", self.font),
            "dark_mode": Button(center_x, 410, button_width, button_height, 
                              f"Theme: {'Dark' if self.game_data.dark_mode else 'Light'}", self.font),
            "exit": Button(center_x, 480, button_width, button_height, "Exit", self.font)
        }
        
        # Game over buttons
        self.game_over_buttons = {
            "restart": Button(center_x, 350, button_width, button_height, "Play Again", self.font),
            "menu": Button(center_x, 420, button_width, button_height, "Main Menu", self.font)
        }
        
        # How to play button
        self.how_to_play_button = Button(center_x, 500, button_width, button_height, "Back", self.font)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.VIDEORESIZE:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.size
                self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
                                                      pygame.RESIZABLE)
                self.create_ui_elements()
            
            elif self.state == GameState.MENU:
                self.handle_menu_events(event)
                
            elif self.state == GameState.PLAYING:
                self.handle_game_events(event)
                
            elif self.state == GameState.PAUSED:
                self.handle_pause_events(event)
                
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events(event)
                
            elif self.state == GameState.HOW_TO_PLAY:
                if self.how_to_play_button.handle_event(event):
                    self.state = GameState.MENU
        
        return True
    
    def handle_menu_events(self, event):
        if self.menu_buttons["start"].handle_event(event):
            self.start_new_game()
        elif self.menu_buttons["how_to_play"].handle_event(event):
            self.state = GameState.HOW_TO_PLAY
        elif self.menu_buttons["difficulty"].handle_event(event):
            self.cycle_difficulty()
        elif self.menu_buttons["dark_mode"].handle_event(event):
            self.toggle_dark_mode()
        elif self.menu_buttons["exit"].handle_event(event):
            return False
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = GameState.PAUSED
                self.sound_manager.play_sound("pause")
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.snake.set_direction(Position(-1, 0))
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.snake.set_direction(Position(1, 0))
            elif event.key in [pygame.K_UP, pygame.K_w]:
                self.snake.set_direction(Position(0, -1))
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.snake.set_direction(Position(0, 1))
            elif event.key == pygame.K_SPACE:
                self.cycle_snake_skin()
    
    def handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                self.state = GameState.PLAYING
                self.sound_manager.play_sound("pause")
            elif event.key == pygame.K_r:
                self.start_new_game()
            elif event.key == pygame.K_m:
                self.state = GameState.MENU
    
    def handle_game_over_events(self, event):
        if self.game_over_buttons["restart"].handle_event(event):
            self.start_new_game()
        elif self.game_over_buttons["menu"].handle_event(event):
            self.state = GameState.MENU
    
    def cycle_difficulty(self):
        difficulties = list(Difficulty)
        current_index = difficulties.index(self.difficulty)
        self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
        self.menu_buttons["difficulty"].text = f"Difficulty: {self.difficulty.value['name']}"
    
    def toggle_dark_mode(self):
        self.game_data.dark_mode = not self.game_data.dark_mode
        self.theme = Theme(self.game_data.dark_mode)
        self.game_data.save_data()
        self.menu_buttons["dark_mode"].text = f"Theme: {'Dark' if self.game_data.dark_mode else 'Light'}"
    
    def cycle_snake_skin(self):
        if self.snake:
            available_skins = [skin for skin in self.game_data.unlocked_skins]
            current_index = available_skins.index(self.snake.skin) if self.snake.skin in available_skins else 0
            self.snake.skin = available_skins[(current_index + 1) % len(available_skins)]
    
    def start_new_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        
        # Initialize snake
        start_x = self.GAME_WIDTH // 2
        start_y = self.GAME_HEIGHT // 2
        self.snake = Snake(start_x, start_y, self.BLOCK_SIZE)
        self.snake.set_speed(self.difficulty.value["speed"])
        
        # Generate obstacles
        self.generate_obstacles()
        
        # Generate food
        self.generate_food()
        
        # Reset power-ups
        self.power_ups.clear()
        self.active_power_ups.clear()
        self.power_up_spawn_timer = 0
    
    def generate_obstacles(self):
        self.obstacles = []
        obstacle_count = self.difficulty.value["obstacles"]
        
        for _ in range(obstacle_count):
            while True:
                x = random.randint(0, self.GAME_WIDTH // self.BLOCK_SIZE - 1)
                y = random.randint(0, self.GAME_HEIGHT // self.BLOCK_SIZE - 1)
                
                # Make sure obstacle doesn't spawn on snake or food
                if (x, y) not in [(int(seg.x // self.BLOCK_SIZE), int(seg.y // self.BLOCK_SIZE)) 
                                  for seg in self.snake.segments]:
                    self.obstacles.append((x, y))
                    break
    
    def generate_food(self):
        while True:
            x = random.randint(0, self.GAME_WIDTH // self.BLOCK_SIZE - 1)
            y = random.randint(0, self.GAME_HEIGHT // self.BLOCK_SIZE - 1)
            
            # Make sure food doesn't spawn on snake or obstacles
            snake_positions = [(int(seg.x // self.BLOCK_SIZE), int(seg.y // self.BLOCK_SIZE)) 
                              for seg in self.snake.segments]
            
            if (x, y) not in snake_positions and (x, y) not in self.obstacles:
                self.food_pos = Position(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE)
                break
    
    def spawn_power_up(self):
        if len(self.power_ups) < 2:  # Max 2 power-ups at once
            while True:
                x = random.randint(0, self.GAME_WIDTH // self.BLOCK_SIZE - 1)
                y = random.randint(0, self.GAME_HEIGHT // self.BLOCK_SIZE - 1)
                
                # Check if position is free
                snake_positions = [(int(seg.x // self.BLOCK_SIZE), int(seg.y // self.BLOCK_SIZE)) 
                                  for seg in self.snake.segments]
                food_pos = (int(self.food_pos.x // self.BLOCK_SIZE), int(self.food_pos.y // self.BLOCK_SIZE))
                
                if ((x, y) not in snake_positions and (x, y) not in self.obstacles and 
                    (x, y) != food_pos):
                    power_type = random.choice(list(PowerUpType))
                    self.power_ups.append(PowerUp(x, y, power_type, self.BLOCK_SIZE))
                    break
    
    def apply_power_up(self, power_up: PowerUp):
        current_time = pygame.time.get_ticks()
        
        if power_up.type == PowerUpType.SLOW_TIME:
            self.snake.set_speed(self.difficulty.value["speed"] * 0.5)
            self.active_power_ups["slow_time"] = current_time + power_up.type.value["duration"]
            
        elif power_up.type == PowerUpType.SHRINK:
            self.snake.shrink()
            self.active_power_ups["shrink"] = current_time + power_up.type.value["duration"]
            
        elif power_up.type == PowerUpType.BONUS_POINTS:
            self.score += 5
            # Check for skin unlocks
            if self.score >= 20 and 1 not in self.game_data.unlocked_skins:
                self.game_data.unlock_skin(1)
            elif self.score >= 50 and 2 not in self.game_data.unlocked_skins:
                self.game_data.unlock_skin(2)
        
        self.sound_manager.play_sound("powerup")
    
    def update_power_ups(self):
        current_time = pygame.time.get_ticks()
        
        # Remove expired power-ups from world
        self.power_ups = [pu for pu in self.power_ups if not pu.is_expired()]
        
        # Check active power-up expiration
        expired_effects = []
        for effect, end_time in self.active_power_ups.items():
            if current_time > end_time:
                expired_effects.append(effect)
        
        for effect in expired_effects:
            del self.active_power_ups[effect]
            if effect == "slow_time":
                self.snake.set_speed(self.difficulty.value["speed"])
    
    def update_game(self, delta_time: float):
        if self.state != GameState.PLAYING:
            return
        
        # Update snake
        self.snake.update(delta_time)
        
        # Check collisions
        if (self.snake.check_wall_collision(self.GAME_WIDTH, self.GAME_HEIGHT) or 
            self.snake.check_self_collision() or 
            self.snake.check_obstacle_collision(self.obstacles)):
            self.game_over()
            return
        
        # Check food collision
        head = self.snake.segments[-1]
        if (int(head.x) == int(self.food_pos.x) and int(head.y) == int(self.food_pos.y)):
            self.snake.grow()
            self.score += 1
            self.sound_manager.play_sound("eat")
            
            if self.score > self.game_data.high_score:
                self.game_data.high_score = self.score
                self.game_data.save_data()
            
            self.generate_food()
            
            # Increase speed slightly
            current_speed = self.difficulty.value["speed"] + (self.score // 5)
            if "slow_time" not in self.active_power_ups:
                self.snake.set_speed(min(current_speed, 25))
        
        # Check power-up collisions
        head_grid = (int(head.x // self.BLOCK_SIZE), int(head.y // self.BLOCK_SIZE))
        for power_up in self.power_ups[:]:
            if head_grid == (power_up.x, power_up.y):
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)
        
        # Spawn power-ups
        self.power_up_spawn_timer += delta_time
        if self.power_up_spawn_timer > 15000:  # Every 15 seconds
            self.spawn_power_up()
            self.power_up_spawn_timer = 0
        
        # Update power-ups
        self.update_power_ups()
    
    def game_over(self):
        self.state = GameState.GAME_OVER
        self.sound_manager.play_sound("game_over")
    
    def draw_game_field(self):
        # Calculate centering offset
        offset_x = (self.SCREEN_WIDTH - self.GAME_WIDTH) // 2
        offset_y = (self.SCREEN_HEIGHT - self.GAME_HEIGHT) // 2
        
        # Draw game background
        game_rect = pygame.Rect(offset_x, offset_y, self.GAME_WIDTH, self.GAME_HEIGHT)
        pygame.draw.rect(self.screen, self.theme.bg_color, game_rect)
        pygame.draw.rect(self.screen, self.theme.text_color, game_rect, 2)
        
        # Set up clipping for game area
        old_clip = self.screen.get_clip()
        self.screen.set_clip(game_rect)
        
        # Draw obstacles
        for obs_x, obs_y in self.obstacles:
            pygame.draw.rect(self.screen, self.theme.obstacle_color,
                           [offset_x + obs_x * self.BLOCK_SIZE, 
                            offset_y + obs_y * self.BLOCK_SIZE,
                            self.BLOCK_SIZE, self.BLOCK_SIZE])
        
        # Draw food with pulsing effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
        food_size = self.BLOCK_SIZE + int(pulse * 4)
        food_offset = (self.BLOCK_SIZE - food_size) // 2
        
        pygame.draw.rect(self.screen, self.theme.food_color,
                        [offset_x + self.food_pos.x + food_offset,
                         offset_y + self.food_pos.y + food_offset,
                         food_size, food_size])
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen, self.theme)
        
        # Draw snake (adjust positions for centering)
        if self.snake:
            # Temporarily adjust snake positions
            original_positions = [(seg.x, seg.y) for seg in self.snake.segments]
            for seg in self.snake.segments:
                seg.x += offset_x
                seg.y += offset_y
            
            self.snake.draw(self.screen, self.theme)
            
            # Restore original positions
            for i, (x, y) in enumerate(original_positions):
                self.snake.segments[i].x = x
                self.snake.segments[i].y = y
        
        # Restore clipping
        self.screen.set_clip(old_clip)
    
    def draw_ui(self):
        if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw overlay UI
            ui_height = 60
            ui_surface = pygame.Surface((self.SCREEN_WIDTH, ui_height))
            ui_surface.set_alpha(180)
            ui_surface.fill(self.theme.ui_bg[:3] if len(self.theme.ui_bg) == 3 else (40, 40, 40))
            self.screen.blit(ui_surface, (0, 0))
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, self.theme.text_color)
            self.screen.blit(score_text, (20, 15))
            
            # Draw high score
            high_score_text = self.font.render(f"High Score: {self.game_data.high_score}", True, self.theme.text_color)
            high_score_rect = high_score_text.get_rect()
            high_score_rect.topright = (self.SCREEN_WIDTH - 20, 15)
            self.screen.blit(high_score_text, high_score_rect)
            
            # Draw speed level
            speed_level = (self.score // 5) + 1
            speed_text = self.small_font.render(f"Speed Level: {speed_level}", True, self.theme.text_color)
            speed_rect = speed_text.get_rect()
            speed_rect.center = (self.SCREEN_WIDTH // 2, 20)
            self.screen.blit(speed_text, speed_rect)
            
            # Draw active power-ups
            y_offset = 35
            for effect in self.active_power_ups.keys():
                effect_text = self.small_font.render(f"Active: {effect.replace('_', ' ').title()}", 
                                                   True, (255, 255, 0))
                effect_rect = effect_text.get_rect()
                effect_rect.center = (self.SCREEN_WIDTH // 2, y_offset)
                self.screen.blit(effect_text, effect_rect)
                y_offset += 20
    
    def draw_menu(self):
        self.screen.fill(self.theme.bg_color)
        
        # Title
        title_text = pygame.font.Font(None, 72).render("Enhanced Snake", True, self.theme.text_color)
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("A Modern Snake Game Experience", True, self.theme.text_color)
        subtitle_rect = subtitle_text.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for button in self.menu_buttons.values():
            button.draw(self.screen, self.theme)
        
        # Draw high score
        high_score_text = self.small_font.render(f"Current High Score: {self.game_data.high_score}", 
                                                True, self.theme.text_color)
        high_score_rect = high_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 550))
        self.screen.blit(high_score_text, high_score_rect)
    
    def draw_pause_screen(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = pygame.font.Font(None, 72).render("PAUSED", True, self.theme.text_color)
        pause_rect = pause_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw controls
        controls = [
            "P or ESC - Resume",
            "R - Restart",
            "M - Main Menu"
        ]
        
        y_offset = 0
        for control in controls:
            control_text = self.font.render(control, True, self.theme.text_color)
            control_rect = control_text.get_rect(center=(self.SCREEN_WIDTH // 2, 
                                               self.SCREEN_HEIGHT // 2 + y_offset))
            self.screen.blit(control_text, control_rect)
            y_offset += 40
    
    def draw_game_over_screen(self):
        self.screen.fill(self.theme.bg_color)
        
        # Title
        game_over_text = pygame.font.Font(None, 72).render("Game Over", True, self.theme.text_color)
        game_over_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, self.theme.text_color)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # High score
        high_score_text = self.font.render(f"High Score: {self.game_data.high_score}", True, self.theme.text_color)
        high_score_rect = high_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 260))
        self.screen.blit(high_score_text, high_score_rect)
        
        # New high score message
        if self.score == self.game_data.high_score and self.score > 0:
            new_high_text = self.font.render("NEW HIGH SCORE!", True, (255, 215, 0))
            new_high_rect = new_high_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300))
            self.screen.blit(new_high_text, new_high_rect)
        
        # Draw buttons
        for button in self.game_over_buttons.values():
            button.draw(self.screen, self.theme)
    
    def draw_how_to_play(self):
        self.screen.fill(self.theme.bg_color)
        
        # Title
        title_text = pygame.font.Font(None, 48).render("How to Play", True, self.theme.text_color)
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "🐍 Use WASD or Arrow Keys to move the snake",
            "🍎 Eat food to grow and increase your score",
            "⚡ Collect power-ups for special abilities:",
            "   • Blue: Slow Time - Reduces snake speed temporarily",
            "   • Orange: Shrink - Removes one segment from snake",
            "   • Gold: Bonus Points - Gives extra points",
            "🚧 Avoid walls, obstacles, and your own tail",
            "⏸️ Press P or ESC to pause the game",
            "🎨 Press SPACE during game to cycle snake skins",
            "🏆 Unlock new skins by reaching high scores!",
            "",
            "Difficulty Levels:",
            "• Easy: Slow speed, few obstacles",
            "• Medium: Normal speed, some obstacles", 
            "• Hard: Fast speed, many obstacles"
        ]
        
        y_start = 120
        for i, instruction in enumerate(instructions):
            if instruction.startswith("🐍") or instruction.startswith("Difficulty"):
                color = (100, 255, 100)  # Green for main points
            elif instruction.startswith("   •"):
                color = (255, 255, 100)  # Yellow for sub-points
            else:
                color = self.theme.text_color
                
            text = self.small_font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_start + i * 25))
            self.screen.blit(text, text_rect)
        
        # Back button
        self.how_to_play_button.draw(self.screen, self.theme)
    
    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.screen.fill((20, 20, 20))  # Dark background around game field
            self.draw_game_field()
            self.draw_ui()
        elif self.state == GameState.PAUSED:
            self.screen.fill((20, 20, 20))
            self.draw_game_field()
            self.draw_ui()
            self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen()
        elif self.state == GameState.HOW_TO_PLAY:
            self.draw_how_to_play()
    
    def run(self):
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_time
            self.last_time = current_time
            
            running = self.handle_events()
            self.update_game(delta_time)
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    game = EnhancedSnakeGame()
    game.run()

if __name__ == "__main__":
    main()