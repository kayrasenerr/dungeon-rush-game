import sys
import pygame
import random
windowsize = windowwidth, windowheight = 1200, 760

WHITE = 255, 255, 255
FPS=60

pygame.init()
screen = pygame.display.set_mode(windowsize) 

class Game:
    def __init__(self):
        self._background = pygame.image.load("notebook\\project\\backgroundb.png")
        self._highscore=0
        self._score = 0
        self._shooted_knives = []
        self._foods_in_map = []
        self._enemy_list = []
        self._player = None
        self._enemy = None
        self._enemy_image_right = pygame.image.load("notebook\\project\\enemyright.png")
        self._enemy_image_left = pygame.image.load("notebook\\project\\enemyleft.png")

    def render(self):
        def draw_bg():
            screen.blit(self._background, (0, 0))
        
        def draw_player():
            screen.blit(self._player._player_image, self._player.here_is_position())

        def draw_food():
            screen.blit(food.here_is_image(), food.here_is_position())
        
        def draw_enemy():
            screen.blit(enemy.here_is_image(), enemy.here_is_position())
        
        def draw_knife():
            screen.blit(knife.here_is_image(), knife.here_is_position())

        draw_bg()

        for food in self._foods_in_map:
            draw_food()
            
        for enemy in self._enemy_list:
            draw_enemy()

        for knife in self._shooted_knives:
            draw_knife()

        draw_player()

        self._healthbar.update_bar()
        self._player.show_knife_count()
        self.show_score()
        pygame.display.flip()

    def create(self):
        self._player = Player()
        self._healthbar=Healthbar(self._player)
        self._enemy =Enemy(self._player._last_direction)  
        self._enemy_list.append(self._enemy)  

    def play(self):
        self.create()
        self._game_over = False
        clock = pygame.time.Clock()
        clock.tick(FPS) 

        while self._game_over is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self._player.handle_input()
            self._player.swing_sword()
            self._player.update()
            for enemy in self._enemy_list:
                enemy.update()

            if self._player.shoot_knife():
                knife = Knife(x=self._player._position[0]+30,y= self._player._position[1]+10,direction= self._player._last_direction)
                def append_to_shooted_knives():
                    self._shooted_knives.append(knife)
                append_to_shooted_knives()
            self.move_knives()
            self.handle_collisions()

            if self.should_generate_food():
                food = Food()
                self._foods_in_map.append(food)

            def generate_enemy(self):
                enemy = Enemy(player_last_direction=self._player._last_direction)  
                self._enemy_list.append(enemy)

            if self.should_generate_enemy():
                generate_enemy(self)
            
            self.render()
            if not self._player.is_alive():
                self._game_over = True
                game_over_screen = GameOverScreen(self._score)
                while self._game_over is True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.reset_game()  
                    game_over_screen.render()
                    pygame.display.flip()

            self.render()
            clock.tick(FPS)
                         
    def reset_game(self):
        if self._score > self._highscore:
            self._highscore=self._score 
        self._score = 0
        self._shooted_knives = []
        self._foods_in_map = []
        self._enemy_list = []
        self._player = None
        self._game_over = False
        self.create()

    def move_knives(self):
        for knife in self._shooted_knives:
            knife.update()

    def handle_collisions(self):
        for enemy in self._enemy_list:
            if enemy.collides_with(self._player):
                self._player.handle_enemy_collision(enemy)
                
            if self._player.swing_sword():    
                if self._player._last_direction=="left":
                    if 0<(self._player._position[0]-enemy._position[0])<=100 and abs(self._player._position[1]-enemy._position[1])<30:
                        self._enemy_list.remove(enemy)
                        self._score += 1
                        if self._score % 5==0:
                            self._player.get_knife()
                if self._player._last_direction=="right":
                    if 0<(enemy._position[0]-self._player._position[0])<=100 and abs(self._player._position[1]-enemy._position[1])<30:
                        self._enemy_list.remove(enemy)
                        self._score += 1
                        if self._score % 5==0:
                            self._player.get_knife()

        for food in self._foods_in_map:
            if food.collides_with(self._player):
                self._player.eat_food()
                food.is_eaten()
                self._foods_in_map.remove(food)

        for enemy in self._enemy_list:
            for knife in self._shooted_knives:
                if knife.collides_with(enemy):
                    self._enemy_list.remove(enemy)
                    self._score += 1  # Increment the score by one point
                    if self._score % 5==0:
                        self._player.get_knife()
                    self._shooted_knives.remove(knife)
                    
        self._shooted_knives = [knife for knife in self._shooted_knives if not knife.is_dead()]
        self._enemy_list = [enemy for enemy in self._enemy_list if enemy.is_alive()]

    def should_generate_food(self):
        return random.random() < 0.001

    def should_generate_enemy(self):
        return random.random() < 0.02

    def generate_food(self):
        food = Food()
        self._foods_in_map.append(food)

    def show_score(self):
        self._font = pygame.font.Font(None, 30)
        self._score_text = self._font.render(f"Score: {str(self._score)}", True, (255, 255, 255))
        screen.blit(self._score_text, (windowwidth-200, 20))
        if self._score>self._highscore:
            self._highscore=self._score
        self._font = pygame.font.Font(None, 30)
        self._score_text = self._font.render(f"Highscore: {str(self._highscore)}", True, (255, 255, 255))
        screen.blit(self._score_text, (windowwidth-200, 60))

class Entity:
    def __init__(self):
        self._position = [0, 0]
        self._last_direction="right"

    def collides_with(self, other_entity):
        return pygame.Rect(self._position[0], self._position[1], 32, 32).colliderect(
            pygame.Rect(other_entity.here_is_position()[0], other_entity.here_is_position()[1], 32, 32))

    def is_alive(self):
        return self._health>0

    def here_is_position(self):
        return self._position

class Player(Entity):
    def __init__(self):
        super().__init__()
        self._position=[0,650]
        self._player_image = pygame.image.load("notebook\\project\\right.png")
        self._health = 100
        self._knife_count = 5
        self._jump_start_pos = 0
        self._fall_start_pos = 0
        self._is_jumping = False
        self._is_falling = False
        self._jump_height = 145 
        self._jump_speed = 7 
        self._fall_speed = 7 
        self._jump_cooldown = 600  
        self._knife_cooldown = 800 
        self._invincibility_cooldown = 600
        self._swing_cooldown = 300
        self._last_jump_time = 0
        self._last_knife_time = 0
        self._last_swing_time = 0
        self._last_damage_time = 0
        self._knive_per_unit_score=2

    def handle_input(self):
        def move_left():
            self._position[0] -= 5
            self._last_direction = "left"
        def move_right():
            self._position[0] += 5
            self._last_direction = "right"
        def jump_up():
            self._jump_start_pos = self._position[1]
            self._last_jump_time = current_time
        def jump_down():
            self._fall_start_pos = self._position[1]

        self._keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if not self._is_jumping and not self._is_falling:
            if self._keys[pygame.K_UP] and current_time - self._last_jump_time >= self._jump_cooldown and self._position[1]>100:
                self._is_jumping = True
                jump_up()   
            elif self._keys[pygame.K_DOWN] and self._position[1]<600:
                self._is_falling = True
                jump_down()
                
        if self._is_jumping:
            if self._position[1] > self._jump_start_pos - self._jump_height:
                self._position[1] -= self._jump_speed
            else:
                self._is_jumping = False

        if self._is_falling:
            if self._position[1] < self._fall_start_pos + self._jump_height:
                self._position[1] += self._fall_speed
            else:
                self._is_falling = False

        if self._keys[pygame.K_LEFT] and self._position[0]>0:
            move_left()
        if self._keys[pygame.K_RIGHT] and self._position[0]<1150:
            move_right()

    def draw(self, path):
        self._player_image=pygame.image.load(path)

    def swing_sword(self):
        if self._keys[pygame.K_SPACE] and pygame.time.get_ticks()-self._last_knife_time>self._knife_cooldown:
            self._last_swing_time=pygame.time.get_ticks()
            if self._last_direction=="right":
                self.draw("notebook\\project\\right_attack.png")
            else:
                self.draw("notebook\\project\\left_attack.png")
            return True
        else:
            return False
            
    def shoot_knife(self):
        if self._keys[pygame.K_LSHIFT] and pygame.time.get_ticks()-self._last_knife_time>self._knife_cooldown and self._knife_count>0:
            self._knife_count-=1
            self._last_knife_time=pygame.time.get_ticks()
            return True
        else:
            return False

    def update(self):
        if pygame.time.get_ticks()>self._last_swing_time+self._swing_cooldown:
            if self._last_direction=="left":
                self.draw("notebook\\project\\left.png")
            else:
                self.draw("notebook\\project\\right.png")

    def handle_enemy_collision(self, enemy):
        if pygame.time.get_ticks() - self._last_damage_time > self._invincibility_cooldown:
            self._health -= enemy.here_is_damage()
            self._last_damage_time=pygame.time.get_ticks()

    def decrease_knife_count(self):
        self._knife_count -= 1

    def should_shoot_knife(self):
        self._keys = pygame.key.get_pressed()
        return self._keys[pygame.K_SPACE]

    def is_alive(self):
        return self._health > 0
    
    def eat_food(self):
        if self._health<=50:
            self._health+=50
        else:
            self._health=100

    def here_is_max_health(self):
        return 100
    
    def here_is_health(self):
        return self._health
    
    def show_knife_count(self):
        self._font = pygame.font.Font(None, 30)
        self._score_text = self._font.render(f"Knives: {str(self._knife_count)}", True, (255, 255, 255))
        screen.blit(self._score_text, (50, 50))
    
    def get_knife(self):
        self._knife_count+=self._knive_per_unit_score

class Enemy(Entity):
    def __init__(self, player_last_direction="right"):
        super().__init__()
        self._health = 1
        self._enemy_image_right = pygame.image.load("notebook\\project\\enemyright.png")
        self._enemy_image_left = pygame.image.load("notebook\\project\\enemyleft.png")
        self._enemy_image = self._enemy_image_right if player_last_direction == "right" else self._enemy_image_left
        self._position = [random.randint(1, 10) * 100, 650 - random.randint(0, 4) * 150]
        self._enemy_damage=25
    def update(self):
        player_position = self.here_is_player_position()  
        enemy_position = self.here_is_position()

        def update_to_left(self):
            enemy_position[0] -= 2 
            self._enemy_image = self._enemy_image_left 
        def update_to_right(self):
            enemy_position[0] += 2 
            self._enemy_image = self._enemy_image_right 

        if player_position[0] < enemy_position[0]:
            update_to_left(self)
        else:
            update_to_right(self)

        self._position = enemy_position  

    def here_is_player_position(self):
        return game_manager._game._player.here_is_position()

    def handle_knife_collision(self, knife):
        self._health -= knife.here_is_damage()

    def is_alive(self):
        return self._health > 0

    def here_is_damage(self):
        return self._enemy_damage

    def here_is_image(self):
        return self._enemy_image


class Knife(Entity):
    def __init__(self, x, y, direction):
        super().__init__()
        self._position = [x, y]
        self._image = pygame.image.load("notebook\\project\\knife.png")
        self._direction = direction
        self._speed = 10 
        self._damage=50
    
    def knife_to_right(self):
        self._position[0] += self._speed

    def knife_to_left(self):
        self._position[0] -= self._speed

    def update(self):
        if self._direction == "right":
            self.knife_to_right()
        elif self._direction == "left":
            self.knife_to_left()

    def is_dead(self):
        return False
    
    def here_is_image(self):
        return self._image
   
    def here_is_damage(self):
        return self._damage
    
    def collides_with(self, entity):
        return super().collides_with(entity)

class Food(Enemy):
    def __init__(self):
        super().__init__()
        self._food_image = pygame.image.load("notebook\\project\\food.png")
        self._position = [random.randint(1, 10) * 100, 680 - random.randint(0, 4) * 150]
        self._is_eaten = False

    def is_eaten(self):
        return self._is_eaten
    
    def here_is_image(self):
        return self._food_image

class Healthbar:
    def __init__(self, player):
        self._player = player
        self._x = 10  
        self._y = 10  
        self._width = 200  
        self._height = 20  
        self._max_health = player.here_is_max_health()  

    def update_bar(self):
        health_percentage = self._player.here_is_health() / self._max_health
        fill_width = int(self._width * health_percentage)

        pygame.draw.rect(screen, WHITE, (self._x, self._y, self._width, self._height), 2)

        pygame.draw.rect(screen, (255, 0, 0), (self._x, self._y, fill_width, self._height))
        self._font = pygame.font.Font(None, 20)
        self._score_text = self._font.render(f"Health: {str(self._player.here_is_health())}", True, (255, 255, 255))
        screen.blit(self._score_text, (self._x+10,self._y+5))
        
class GameOverScreen:
    def __init__(self, score):
        self._score = score
        self._font = pygame.font.Font(None, 50)
        self._text_color = WHITE
        self._game_over_text = self._font.render("Game Over", True, self._text_color)
        self._score_text = self._font.render(f"Score: {self._score}", True, self._text_color)
        self._play_again_text = self._font.render("Press SPACE to play again", True, self._text_color)

    def render(self):
        screen.blit(self._game_over_text, (windowwidth // 2 - self._game_over_text.get_width() // 2, 200))
        screen.blit(self._score_text, (windowwidth // 2 - self._score_text.get_width() // 2, 300))
        screen.blit(self._play_again_text, (windowwidth // 2 - self._play_again_text.get_width() // 2, 400))
        pygame.display.flip()

    def handle_input(self):
        self._keys = pygame.key.get_pressed()
        if self._keys[pygame.K_SPACE]:
            game_manager._game.reset_game()
            return True
        return False

class GameManager:
    def __init__(self):
        self._game = Game()

    def start(self):
        self._game.play()

if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.start()