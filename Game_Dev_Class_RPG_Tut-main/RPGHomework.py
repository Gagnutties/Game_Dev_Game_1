"""
Author: Dylan Smith
Created: Oct. 31, 2022
"""
import pygame
import Characters
import button
pygame.init()

clock = pygame.time.Clock()
fps = 60


###################SET UP WINDOW##############
bottom_panel = 150
screensize = width, height = 800, 400+bottom_panel
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Underground Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90

attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

#define fonts
font = pygame.font.SysFont('Papyrus', 26)

#define colors
red = (255,0,0)
green = (0,255,0)




################INITIALIZE IMAGES#################
background_img = pygame.image.load("Game_Dev_Class_RPG_Tut-main/Backgrounds/Background.png").convert_alpha()
foreground_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Backgrounds/Foreground.png').convert_alpha()
panel_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Backgrounds/Panel.png').convert_alpha()

sword_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Icons/sword.png').convert_alpha()
potion_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Icons/potion.png').convert_alpha()

victory_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Icons/defeat.png').convert_alpha()
restart_img = pygame.image.load('Game_Dev_Class_RPG_Tut-main/Icons/restart.png').convert_alpha()

####################DRAW THE STUFF##################
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_panel():
    screen.blit(panel_img, (0, 400))
        #show knight stats
    draw_text(f'{wizard.name} HP: {wizard.hp}', font, red, 100, height - bottom_panel+10)
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.hp}', font, red, 500, (height - bottom_panel+10)+ count * 60)


damage_text_group = pygame.sprite.Group()



###############CREATE PLAYERS AND NPCS###############
wizard = Characters.Fighter(230, 300, 'Hero', 30, 15, 3)
bandit1 = Characters.Fighter(550, 310, 'Bandit', 20, 6, 1)
bandit2 = Characters.Fighter(700, 290, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

wizard_health_bar = Characters.HealthBar(screen, red, 100, height-bottom_panel+40, wizard.hp, wizard.max_hp)
bandit1_health_bar = Characters.HealthBar(screen, red, 550, height-bottom_panel+40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = Characters.HealthBar(screen, red, 550, height-bottom_panel+100, bandit2.hp, bandit2.max_hp)

####################BUTTONS###################
potion_button = button.Button(screen, 100, height-bottom_panel+70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

################INITIALIZE LOOP###############
on=True
while on:
    clock.tick(fps)
    
    #DRAW BACKGROUND
    screen.blit(background_img, (0,0))
    
    #DRAW PANEL
    draw_panel()
    wizard_health_bar.draw(wizard.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #UPDATE AND DRAW CHARACTERS
    wizard.update()
    wizard.draw(screen)
    #wizard.draw()
    for b in bandit_list:
        b.update()
        b.draw(screen)
    
    damage_text_group.update()
    damage_text_group.draw(screen)


    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None


    #mouse is visible
    pygame.mouse.set_visible(True)

    #GETS POSITION OF MOUSE AND PUTS SWORD OVER IT
    pos = pygame.mouse.get_pos()
    for count, b in enumerate(bandit_list):
        if b.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            screen.blit(sword_img, pos)
            #IF CLICKED ON AREA THEN ATTACK AND TARGET
            if clicked == True and b.alive == True:
                
                attack = True
                
                target = bandit_list[count]

    if potion_button.draw():
        potion = True

    draw_text(str(wizard.potions), font, red, 150, height - bottom_panel+70)
    if game_over == 0:
        #CONTROL OF PLAYER
        if wizard.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    if attack == True and target != None:
                        wizard.attack(target, damage_text_group, font)
                        current_fighter += 1
                        action_cooldown = 0
                    if potion == True:
                        if wizard.potions > 0:
                            if wizard.max_hp - wizard.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = wizard.max_hp-wizard.hp
                            wizard.hp += heal_amount
                            wizard.potions -= 1
                            damage_text = Characters.DamageText(wizard.rect.centerx, wizard.rect.y, str(heal_amount), green, font)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        #ENEMY AI TO ATTACK DURING THEIR TURN
        for count, b in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if b.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #bandit  healing
                        if (b.hp/b.max_hp)< 0.5 and b.potions > 0:
                            if b.max_hp - b.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = b.max_hp-b.hp
                            b.hp += heal_amount
                            b.potions -= 1
                            damage_text = Characters.DamageText(b.rect.centerx, b.rect.y, str(heal_amount), green, font)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        #attack
                        else:
                            b.attack(wizard, damage_text_group, font)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1
        clicked = False
        #IF EVERYONE HAS WENT THEN BACK TO WIZARD
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all bandits dead
    alive_bandits = 0
    for b in bandit_list:
        if b.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1


    #check if game is over
    if game_over!=0:
        if game_over==1:
            screen.blit(victory_img, (250, 50))
        if game_over==-1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            wizard.reset()
            for b in bandit_list:
                b.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0




    #CREATES FOREGROUND IMAGE AND PLACES IT ABOVE EVERYTHING
    screen.blit(foreground_img, (0,0))


    #EVENT LISTENER FOR QUIT AND FOR ON CLICK WILL CHANGE CLICKED TO TRUE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
#        else:
#            clicked = False

    #UPDATE DISPLAY
    pygame.display.update()
#WHEN LOOP EXIT
pygame.quit()