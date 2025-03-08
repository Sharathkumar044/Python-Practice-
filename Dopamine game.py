import pygame
import random
import math
import sys
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dopamine Boost Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 105, 180),  # Hot Pink
    (50, 205, 50),    # Lime Green
    (30, 144, 255),   # Dodger Blue
    (255, 215, 0),    # Gold
    (138, 43, 226),   # Blue Violet
    (255, 127, 80),   # Coral
    (0, 255, 255),    # Cyan
]

# Game variables
score = 0
particles = []
bubbles = []
combo = 0
combo_timer = 0
last_spawn = 0
spawn_rate = 1000  # milliseconds
level = 1

# Sound effects
try:
    pop_sound = mixer.Sound('pop.wav')  # You can create or download this sound
    reward_sound = mixer.Sound('reward.wav')  # You can create or download this sound
    # Default to system sounds if files are missing
except:
    pop_sound = None
    reward_sound = None

# Font
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 15)
        self.speed = random.uniform(2, 8)
        self.angle = random.uniform(0, math.pi * 2)
        self.lifetime = random.randint(20, 40)
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.size = max(0, self.size - 0.2)
        return self.lifetime > 0 and self.size > 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class Bubble:
    def __init__(self):
        self.size = random.randint(30, 70)
        self.x = random.randint(self.size, WIDTH - self.size)
        self.y = random.randint(self.size, HEIGHT - self.size)
        self.color = random.choice(COLORS)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)
        self.pulse_speed = random.uniform(0.05, 0.1)
        self.pulse_size = 0
        self.points = self.size // 5
    
    def update(self):
        # Move
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x - self.size < 0 or self.x + self.size > WIDTH:
            self.speed_x *= -1
        if self.y - self.size < 0 or self.y + self.size > HEIGHT:
            self.speed_y *= -1
        
        # Pulsing effect
        self.pulse_size = 5 * math.sin(pygame.time.get_ticks() * self.pulse_speed * 0.01)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size + self.pulse_size))
        # Draw highlight
        highlight_pos = (int(self.x - self.size/3), int(self.y - self.size/3))
        highlight_size = self.size/4
        pygame.draw.circle(surface, (255, 255, 255, 128), highlight_pos, int(highlight_size))
    
    def contains_point(self, point):
        return math.dist((self.x, self.y), point) <= self.size

def create_particles(x, y, color, count=20):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def spawn_bubble():
    bubbles.append(Bubble())

def draw_glow(surface, position, radius, color, intensity=50):
    glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    for i in range(intensity):
        alpha = int(255 - i * (255 / intensity))
        current_radius = int(radius - i * (radius / intensity))
        pygame.draw.circle(glow_surf, (*color, alpha), (radius, radius), current_radius)
    
    surface.blit(glow_surf, (position[0] - radius, position[1] - radius), special_flags=pygame.BLEND_RGBA_ADD)

# Game loop
clock = pygame.time.Clock()
running = True

# Start with a few bubbles
for _ in range(5):
    spawn_bubble()

while running:
    current_time = pygame.time.get_ticks()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            hit = False
            
            for i, bubble in enumerate(bubbles):
                if bubble.contains_point(pos):
                    # Add to score
                    bubble_score = bubble.points * (combo + 1)
                    score += bubble_score
                    
                    # Create particles
                    create_particles(bubble.x, bubble.y, bubble.color, count=30)
                    
                    # Play sound
                    if pop_sound:
                        pop_sound.play()
                    
                    # Update combo
                    combo += 1
                    combo_timer = current_time + 2000  # 2 seconds to maintain combo
                    
                    # Remove bubble
                    bubbles.pop(i)
                    
                    # Add new bubble if we popped one
                    if random.random() < 0.7:  # 70% chance
                        spawn_bubble()
                    
                    # Level up
                    if score >= level * 500:
                        level += 1
                        spawn_rate = max(300, spawn_rate - 100)  # Speed up spawning
                        
                        # Play reward sound
                        if reward_sound:
                            reward_sound.play()
                    
                    hit = True
                    break
            
            # Reset combo if missed
            if not hit:
                combo = 0
    
    # Check combo timer
    if combo > 0 and current_time > combo_timer:
        combo = 0
    
    # Update particles
    particles = [p for p in particles if p.update()]
    
    # Update bubbles
    for bubble in bubbles:
        bubble.update()
    
    # Spawn new bubbles over time
    if current_time - last_spawn > spawn_rate:
        if len(bubbles) < 10 + level:  # More bubbles at higher levels
            spawn_bubble()
            last_spawn = current_time
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw particles
    for particle in particles:
        particle.draw(screen)
    
    # Draw bubbles with glow
    for bubble in bubbles:
        draw_glow(screen, (int(bubble.x), int(bubble.y)), int(bubble.size * 1.5), bubble.color, intensity=30)
        bubble.draw(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Draw level
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (20, 60))
    
    # Draw combo
    if combo > 1:
        combo_text = font.render(f"Combo: x{combo}", True, (255, 215, 0))
        screen.blit(combo_text, (WIDTH - 150, 20))
        
        # Show combo timer
        remaining = max(0, (combo_timer - current_time) / 2000)
        pygame.draw.rect(screen, (255, 215, 0), (WIDTH - 150, 60, 130 * remaining, 10))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()