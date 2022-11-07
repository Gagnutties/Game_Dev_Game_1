import pygame
import random

class Fighter():
    def __init__(self, posx, posy, name, max_hp, strength, potions):
        self.name = name
        self.posx = posx
        self.posy = posy

        self.max_hp = max_hp
        self.hp = max_hp

        self.strength = strength
        self.start_potions = potions
        self.potions = potions

        self.alive = True

        self.animation_list = []
        self.frame_index = 0
        self.action = 0#0:Idle 1:attack 2:dead 3:hurt

        self.update_time = pygame.time.get_ticks()
        
        #####################LOAD ALL ANIMATION IMAGES########################################
        #Image Loader Idle
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'Game_Dev_Class_RPG_Tut-main/{self.name}/Idle/{i}.png')
            if self.name == 'Hero':
                img = pygame.transform.scale(img,(img.get_width()*1.2, img.get_height()*1.2))
            else:
                img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Image Loader Attack
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'Game_Dev_Class_RPG_Tut-main/{self.name}/Attack/{i}.png')
            if self.name == 'Hero':
                img = pygame.transform.scale(img,(img.get_width()*1.2, img.get_height()*1.2))
            else:
                img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Image Loader Death
        temp_list = []
        for i in range(9):
            img = pygame.image.load(f'Game_Dev_Class_RPG_Tut-main/{self.name}/Death/{i}.png')
            if self.name == 'Hero':
                img = pygame.transform.scale(img,(img.get_width()*1.2, img.get_height()*1.2))
            else:
                img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Image Loader Hurt
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Game_Dev_Class_RPG_Tut-main/{self.name}/Hurt/{i}.png')
            if self.name == 'Hero':
                img = pygame.transform.scale(img,(img.get_width()*1.2, img.get_height()*1.2))
            else:
                img = pygame.transform.scale(img,(img.get_width()*3, img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        ##########################################################################################


        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (posx,posy)



    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.idle()


    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target, damage_text_group, font):
        rand = random.randint(-5,5)
        damage = self.strength+rand
        target.hp -= damage
        target.hurt()
        # check if dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), (255,0,0), font)
        damage_text_group.add(damage_text)
        #attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self, window):
        window.blit(self.image, self.rect)

class HealthBar():#HEALTHBAR FOR CHARACTERS
    def __init__(self, screen, color, x, y, hp, max_hp):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    
    def draw(self, hp): #DRAWS BOXES TO REPRESENT HEALTH POINTS
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.screen, (0,255,0), (self.x, self.y, 150*ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete
        self.counter += 1
        if self.counter > 30:
            self.kill()



