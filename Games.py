import os
import zipfile

# Define the complete folder structure and files as requested in Phase 1
project_structure = {
    "requirements.txt": "pygame-ce>=2.5.0\n",
    "setup.bat": """@echo off
echo [Studio] Initializing Shadow Village Environment...
python -m venv venv
call venv\\Scripts\\activate
pip install -r requirements.txt
echo [Studio] Environment setup complete.
pause
""",
    "launcher.bat": """@echo off
echo [Studio] Launching Shadow Village...
call venv\\Scripts\\activate
python main.py
pause
""",
    "run.sh": """#!/bin/bash
echo "[Studio] Launching Shadow Village..."
source venv/bin/activate
python3 main.py
""",
    "main.py": """from core.engine import GameEngine

if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
""",
    "config/__init__.py": "",
    "config/constants.py": """import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "Shadow Village"

COLOR_DARK_BG = (15, 15, 25)
COLOR_PANEL_BG = (30, 30, 45)
COLOR_TEXT_LIGHT = (240, 240, 255)
COLOR_TEXT_MUTED = (140, 140, 160)
COLOR_AMBER = (235, 140, 40)
COLOR_RED = (220, 60, 60)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SAVE_DIR = os.path.join(BASE_DIR, "saves")
""",
    "config/settings.py": """class GameSettings:
    def __init__(self):
        self.master_volume = 0.8
        self.sfx_volume = 0.9
        self.music_volume = 0.7
        self.fullscreen = False
        self.vsync = True
        self.show_fps = True
        self.lighting_enabled = True
        self.particles_enabled = True

    def to_dict(self):
        return {
            "master_volume": self.master_volume,
            "sfx_volume": self.sfx_volume,
            "music_volume": self.music_volume,
            "fullscreen": self.fullscreen,
            "vsync": self.vsync,
            "show_fps": self.show_fps,
            "lighting_enabled": self.lighting_enabled,
            "particles_enabled": self.particles_enabled
        }

    def load_from_dict(self, data):
        self.master_volume = data.get("master_volume", self.master_volume)
        self.sfx_volume = data.get("sfx_volume", self.sfx_volume)
        self.music_volume = data.get("music_volume", self.music_volume)
        self.fullscreen = data.get("fullscreen", self.fullscreen)
        self.vsync = data.get("vsync", self.vsync)
        self.show_fps = data.get("show_fps", self.show_fps)
        self.lighting_enabled = data.get("lighting_enabled", self.lighting_enabled)
        self.particles_enabled = data.get("particles_enabled", self.particles_enabled)
""",
    "core/__init__.py": "",
    "core/engine.py": """import pygame
import sys
import random
import math
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, COLOR_DARK_BG
from config.settings import GameSettings
from core.managers.asset import AssetManager
from core.managers.sound import SoundManager
from core.managers.save import SaveManager
from core.managers.scene import SceneManager, BaseScene
from core.managers.camera import Camera
from core.managers.collision import CollisionManager
from core.managers.animation import AnimationManager
from core.managers.sprite import SpriteManager
from core.managers.lighting import LightingManager, LightSource
from core.managers.particle import ParticleManager
from core.managers.weather import WeatherManager

class MockMenuScene(BaseScene):
    def __init__(self, engine):
        super().__init__(engine)
        self.font = self.engine.asset_mgr.get_font("Arial", 24)
        self.engine.lighting_mgr.clear_lights()
        self.engine.lighting_mgr.add_light(LightSource((400, 300), 250, (255, 180, 100), 200))
        self.engine.lighting_mgr.add_light(LightSource((800, 450), 180, (100, 150, 255), 180))
        self.engine.weather_mgr.set_weather("rain", 0.6)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.engine.sound_mgr.play_sfx("click.wav", frequency=580, duration=0.08)
                if event.key == pygame.K_w:
                    self.engine.weather_mgr.set_weather("fog" if self.engine.weather_mgr.weather_type == "rain" else "rain")

    def update(self, dt):
        mx, my = pygame.mouse.get_pos()
        world_mouse = pygame.Vector2(mx, my) + self.engine.camera.offset
        if pygame.mouse.get_pressed()[0]:
            for _ in range(2):
                self.engine.particle_mgr.emit(
                    pos=world_mouse,
                    velocity=(random.uniform(-2, 2), random.uniform(-4, -1)),
                    color=(235, 140, 40),
                    lifetime=0.8,
                    size=4
                )
        self.engine.particle_mgr.update(dt)
        self.engine.weather_mgr.update(dt)

    def draw(self, surface):
        surface.fill(COLOR_DARK_BG)
        title_surf = self.font.render("SHADOW VILLAGE - Engine Live [Phase 1]", True, (240, 240, 255))
        prompt_surf = self.font.render("Press SPACE for SFX Sync | Drag Mouse for Particles | Press W to toggle Weather", True, (160, 160, 180))
        surface.blit(title_surf, (50, 50))
        surface.blit(prompt_surf, (50, 100))
        self.engine.particle_mgr.draw(surface, self.engine.camera)
        self.engine.lighting_mgr.render_lighting(surface, self.engine.camera)
        self.engine.weather_mgr.draw(surface)

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = GameSettings()
        flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=self.settings.vsync)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.Clock()
        self.running = True

        self.asset_mgr = AssetManager()
        self.sound_mgr = SoundManager(self.settings)
        self.save_mgr = SaveManager()
        self.scene_mgr = SceneManager()
        self.camera = Camera(2000, 2000)
        self.collision_mgr = CollisionManager()
        self.animation_mgr = AnimationManager()
        self.sprite_mgr = SpriteManager()
        self.lighting_mgr = LightingManager(self.settings)
        self.particle_mgr = ParticleManager(self.settings)
        self.weather_mgr = WeatherManager(self.settings)

        self.scene_mgr.change_scene("boot_test", MockMenuScene(self))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            self.scene_mgr.handle_events(events)
            self.scene_mgr.update(dt)
            self.scene_mgr.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
""",
    "core/managers/__init__.py": "",
    "core/managers/asset.py": """import pygame
import os
from config.constants import ASSETS_DIR

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.fonts = {}
        self._create_directories()

    def _create_directories(self):
        os.makedirs(os.path.join(ASSETS_DIR, "sprites", "characters"), exist_ok=True)
        os.makedirs(os.path.join(ASSETS_DIR, "sprites", "environment"), exist_ok=True)
        os.makedirs(os.path.join(ASSETS_DIR, "sprites", "interface"), exist_ok=True)
        os.makedirs(os.path.join(ASSETS_DIR, "audio", "ambience"), exist_ok=True)
        os.makedirs(os.path.join(ASSETS_DIR, "audio", "sfx"), exist_ok=True)
        os.makedirs(os.path.join(ASSETS_DIR, "fonts"), exist_ok=True)

    def get_sprite(self, path, width=32, height=32, color=(255, 0, 255)):
        full_path = os.path.join(ASSETS_DIR, "sprites", path)
        if full_path in self.sprites:
            return self.sprites[full_path]
        if os.path.exists(full_path):
            surface = pygame.image.load(full_path).convert_alpha()
            self.sprites[full_path] = surface
            return surface
        else:
            fallback = pygame.Surface((width, height), pygame.SRCALPHA)
            fallback.fill(color)
            self.sprites[full_path] = fallback
            return fallback

    def get_font(self, name, size):
        key = f"{name}_{size}"
        if key in self.fonts:
            return self.fonts[key]
        full_path = os.path.join(ASSETS_DIR, "fonts", name)
        if os.path.exists(full_path):
            font = pygame.font.Font(full_path, size)
        else:
            font = pygame.font.SysFont("Arial", size)
        self.fonts[key] = font
        return font
""",
    "core/managers/sound.py": """import pygame
import os
import array
import math
from config.constants import ASSETS_DIR

class SoundManager:
    def __init__(self, settings):
        self.settings = settings
        self.sounds = {}
        self.current_music_path = None

    def play_sfx(self, path, frequency=440, duration=0.1):
        full_path = os.path.join(ASSETS_DIR, "audio", "sfx", path)
        volume = self.settings.sfx_volume * self.settings.master_volume

        if full_path in self.sounds:
            sound = self.sounds[full_path]
            sound.set_volume(volume)
            sound.play()
            return

        if os.path.exists(full_path):
            sound = pygame.mixer.Sound(full_path)
        else:
            sample_rate = 44100
            n_samples = int(sample_rate * duration)
            buf = array.array('h', [0] * n_samples)
            for i in range(n_samples):
                t = float(i) / sample_rate
                buf[i] = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * frequency * t))
            sound = pygame.mixer.Sound(buffer=buf)

        self.sounds[full_path] = sound
        sound.set_volume(volume)
        sound.play()

    def play_ambience(self, path, loop=True):
        full_path = os.path.join(ASSETS_DIR, "audio", "ambience", path)
        volume = self.settings.music_volume * self.settings.master_volume
        if os.path.exists(full_path):
            if self.current_music_path != full_path:
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music_path = full_path

    def stop_all(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.current_music_path = None
""",
    "core/managers/save.py": """import json
import os
from config.constants import SAVE_DIR

class SaveManager:
    def __init__(self):
        os.makedirs(SAVE_DIR, exist_ok=True)

    def save_slot(self, slot_id, data):
        filepath = os.path.join(SAVE_DIR, f"slot_{slot_id}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load_slot(self, slot_id):
        filepath = os.path.join(SAVE_DIR, f"slot_{slot_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            return json.load(f)

    def delete_slot(self, slot_id):
        filepath = os.path.join(SAVE_DIR, f"slot_{slot_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
""",
    "core/managers/scene.py": """class BaseScene:
    def __init__(self, engine):
        self.engine = engine
    def handle_events(self, events):
        pass
    def update(self, dt):
        pass
    def draw(self, surface):
        pass

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.scenes = {}
    def change_scene(self, scene_name, scene_instance):
        self.scenes[scene_name] = scene_instance
        self.current_scene = self.scenes[scene_name]
    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)
    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)
    def draw(self, surface):
        if self.current_scene:
            self.current_scene.draw(surface)
""",
    "core/managers/camera.py": """import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, map_width, map_height):
        self.offset = pygame.Vector2(0, 0)
        self.map_width = map_width
        self.map_height = map_height

    def look_at(self, target_vector):
        x = target_vector.x - int(SCREEN_WIDTH / 2)
        y = target_vector.y - int(SCREEN_HEIGHT / 2)
        x = max(0, min(x, self.map_width - SCREEN_WIDTH))
        y = max(0, min(y, self.map_height - SCREEN_HEIGHT))
        self.offset.x = x
        self.offset.y = y

    def apply(self, rect_or_vector):
        if isinstance(rect_or_vector, pygame.Rect):
            return rect_or_vector.move(-self.offset.x, -self.offset.y)
        elif isinstance(rect_or_vector, (pygame.Vector2, tuple, list)):
            return pygame.Vector2(rect_or_vector) - self.offset
        return rect_or_vector
""",
    "core/managers/collision.py": """import pygame

class CollisionManager:
    def __init__(self):
        self.colliders = []
    def clear(self):
        self.colliders.clear()
    def add_collider(self, rect):
        self.colliders.append(rect)
    def check_xy_collisions(self, entity_rect, movement_vector):
        entity_rect.x += movement_vector.x
        for wall in self.colliders:
            if entity_rect.colliderect(wall):
                if movement_vector.x > 0:
                    entity_rect.right = wall.left
                if movement_vector.x < 0:
                    entity_rect.left = wall.right
                movement_vector.x = 0
        entity_rect.y += movement_vector.y
        for wall in self.colliders:
            if entity_rect.colliderect(wall):
                if movement_vector.y > 0:
                    entity_rect.bottom = wall.top
                if movement_vector.y < 0:
                    entity_rect.top = wall.bottom
                movement_vector.y = 0
        return movement_vector
""",
    "core/managers/animation.py": """class AnimationManager:
    def __init__(self):
        self.animations = {}
    def register_state(self, state_name, frames, frame_duration=0.1):
        self.animations[state_name] = {"frames": frames, "duration": frame_duration}
    def get_frame(self, state_name, elapsed_time, loop=True):
        if state_name not in self.animations:
            return None
        anim = self.animations[state_name]
        frames = anim["frames"]
        total_frames = len(frames)
        if total_frames == 0:
            return None
        frame_idx = int(elapsed_time / anim["duration"])
        if loop:
            frame_idx = frame_idx % total_frames
        else:
            frame_idx = min(frame_idx, total_frames - 1)
        return frames[frame_idx]
""",
    "core/managers/sprite.py": """import pygame

class SpriteManager:
    def __init__(self):
        self.render_layers = {"background": [], "shadows": [], "entities": [], "lighting": [], "ui": []}
    def clear_layers(self):
        for layer in self.render_layers:
            self.render_layers[layer].clear()
    def add_to_layer(self, layer_name, drawable):
        if layer_name in self.render_layers:
            self.render_layers[layer_name].append(drawable)
    def draw_layer(self, layer_name, surface, camera=None):
        if layer_name not in self.render_layers:
            return
        if layer_name == "entities":
            self.render_layers[layer_name].sort(key=lambda item: item.rect.bottom)
        for item in self.render_layers[layer_name]:
            item.draw(surface, camera)
""",
    "core/managers/lighting.py": """import pygame
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class LightSource:
    def __init__(self, position, radius, color=(255, 200, 120), intensity=255):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.color = color
        self.intensity = intensity
        self.surface = self._create_light_mask()

    def _create_light_mask(self):
        mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        for r in range(self.radius, 0, -2):
            alpha = int((1.0 - (r / self.radius)) * self.intensity)
            pygame.draw.circle(mask, (*self.color, alpha), (self.radius, self.radius), r)
        return mask

class LightingManager:
    def __init__(self, settings):
        self.settings = settings
        self.ambient_color = [40, 40, 60, 255]
        self.light_sources = []
        self.light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def set_ambient(self, r, g, b, alpha=255):
        self.ambient_color = [r, g, b, alpha]
    def add_light(self, light_source):
        self.light_sources.append(light_source)
    def clear_lights(self):
        self.light_sources.clear()
    def render_lighting(self, target_surface, camera):
        if not self.settings.lighting_enabled:
            return
        self.light_mask.fill(self.ambient_color)
        for light in self.light_sources:
            screen_pos = camera.apply(light.position)
            render_rect = light.surface.get_rect(center=screen_pos)
            self.light_mask.blit(light.surface, render_rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)
        target_surface.blit(self.light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
""",
    "core/managers/particle.py": """import pygame

class Particle:
    def __init__(self, pos, velocity, color, lifetime, size=3):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size

    def update(self, dt):
        self.pos += self.velocity * dt * 60.0
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, surface, camera):
        screen_pos = camera.apply(self.pos)
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        alpha = max(0, min(alpha, 255))
        p_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(p_surf, p_surf.get_rect(center=screen_pos).topleft)

class ParticleManager:
    def __init__(self, settings):
        self.settings = settings
        self.particles = []
    def emit(self, pos, velocity, color, lifetime, size=3):
        if not self.settings.particles_enabled:
            return
        self.particles.append(Particle(pos, velocity, color, lifetime, size))
    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
    def draw(self, surface, camera):
        for p in self.particles:
            p.draw(surface, camera)
""",
    "core/managers/weather.py": """import pygame
import random
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class WeatherManager:
    def __init__(self, settings):
        self.settings = settings
        self.weather_type = "clear"
        self.intensity = 0.0
        self.drops = []
        self._init_weather()

    def _init_weather(self):
        self.drops = [[random.randint(0, SCREEN_WIDTH), random.randint(-SCREEN_HEIGHT, 0)] for _ in range(200)]

    def set_weather(self, weather_type, intensity=0.5):
        self.weather_type = weather_type
        self.intensity = max(0.0, min(intensity, 1.0))

    def update(self, dt):
        if self.weather_type == "rain":
            speed = 700 * dt
            for drop in self.drops:
                drop[1] += speed
                drop[0] -= speed * 0.2
                if drop[1] > SCREEN_HEIGHT:
                    drop[1] = random.randint(-50, 0)
                    drop[0] = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        if self.weather_type == "rain":
            for drop in self.drops:
                pygame.draw.line(surface, (100, 120, 160, 150), (drop[0], drop[1]), (drop[0] - 2, drop[1] + 10), 1)
        elif self.weather_type == "fog":
            fog_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fog_surf.fill((200, 200, 220, int(40 * self.intensity)))
            surface.blit(fog_surf, (0, 0))
""",
    "README.md": """# Shadow Village - Phase 1

Architecture Phase Complete.
To install dependencies, run `setup.bat`.
To launch the game framework, run `launcher.bat` or `run.sh`.
"""
}

zip_filename = "shadow_village_phase1.zip"

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filepath, content in project_structure.items():
        # Ensure directories exist in structure
        zipf.writestr(os.path.join("shadow_village", filepath), content)
    
    # Pre-create asset empty sub-directories explicitly in zip entry table
    empty_dirs = [
        "shadow_village/assets/sprites/characters/",
        "shadow_village/assets/sprites/environment/",
        "shadow_village/assets/sprites/interface/",
        "shadow_village/assets/audio/ambience/",
        "shadow_village/assets/audio/sfx/",
        "shadow_village/assets/fonts/",
        "shadow_village/saves/"
    ]
    for d in empty_dirs:
        zinfo = zipfile.ZipInfo(d)
        zipf.writestr(zinfo, '')

print(f"Zip created successfully: {zip_filename}")