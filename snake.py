import pygame
import time
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)
green = (41,240,26)
red = (201, 18, 18)
yellow = (239,250,32)

dis_width = 800
dis_height = 600

#loading sound traks
start_sound=pygame.mixer.Sound("game_sound.mp3")
direction_sound=pygame.mixer.Sound("direction.mp3")
bite_sound=pygame.mixer.Sound("bite.mp3")
game_over_sound=pygame.mixer.Sound("game_over.mp3")
game_bite_itself=pygame.mixer.Sound("snake_skin_bite.wav")
dis = pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("Snake game")

clock = pygame.time.Clock()

snake_block = 10


font_style = pygame.font.SysFont("calibri",25)
score_font = pygame.font.SysFont("comicsans",34)
# print(pygame.font.get_fonts())

def show_rules():
    rule_msg = font_style.render("Welcome to Snake Game!", True, yellow)
    dis.blit(rule_msg, [dis_width/12, dis_height/4])
    
    rule_msg2 = font_style.render("1. Eat the red food to grow.", True, yellow)
    dis.blit(rule_msg2, [dis_width/12, dis_height/4 + 30])
    
    rule_msg3 = font_style.render("2. Colliding with wall would end the game", True, yellow)
    dis.blit(rule_msg3, [dis_width/12, dis_height/4 + 60])
    
    rule_msg3 = font_style.render("3. You got 3 lives", True, yellow)
    dis.blit(rule_msg3, [dis_width/12, dis_height/4 + 90])

    rule_msg4 = font_style.render("4. Colliding with yourself would lose your size ,", True, yellow)
    dis.blit(rule_msg4, [dis_width/12, dis_height/4 + 120])
    
    rule_msg=font_style.render("    1 live and your score by 2 points",True, yellow)
    dis.blit(rule_msg, [dis_width/12, dis_height/4 + 150])

    rule_msg3 = font_style.render("5. Press any key to start the game!!", True, yellow)
    dis.blit(rule_msg3, [dis_width/12, dis_height/4 + 180])

    pygame.display.update()
    pygame.time.wait(1000)  # Display rules for 1 second

    # Wait for a key press to start the game
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False
                break

def my_score(score,lives):
    value = score_font.render("Score: "+str(score),True,yellow)
    dis.blit(value, [0,0])

    # Display remaining lives
    life_msg = font_style.render("Lives: " + str(lives), True, yellow)
    dis.blit(life_msg, [dis_width - 100, 0])

def message(msg,color):
    mssg = font_style.render(msg,True,color)
    dis.blit(mssg,[dis_width//6, dis_height//2])


def my_snake(snake_block,snake_list):
    for x in snake_list:
        pygame.draw.rect(dis,green,[x[0],x[1],snake_block,snake_block])



def main_game():
    start_sound.play()
    show_rules()
    # pygame.time.delay(5000)  # Delay for 5000 milliseconds (5 seconds)
    start_sound.fadeout(2000)
    
    game_over = False
    game_close = False


    x1 = dis_width/2
    y1 = dis_height/2

    x1_change = 0
    y1_change = 0

    snake_list =[]
    length_snake = 1
    snake_speed = 8
    lives=3
    score=0

    foodx = round(random.randrange(0,dis_width- snake_block)/10.0)*10.0
    foody = round(random.randrange(0,dis_height-snake_block)/10.0)*10.0

    while not game_over:
        # for event in pygame.event.get():
        #     if event.type==pygame.QUIT:
        #         game_over=True
        while game_close == True:
            dis.fill(white)
            message("You lost! press p to play again q to quit",red)
            my_score(score,lives)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        lives=3
                        game_over=False
                        game_close=False
                        main_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change>0:
                        continue
                    x1_change = -snake_block
                    y1_change = 0
                    direction_sound.play()

                elif event.key == pygame.K_RIGHT:
                    if x1_change<0:
                        continue
                    x1_change = snake_block
                    y1_change = 0
                    direction_sound.play()

                elif event.key == pygame.K_UP:
                    if y1_change>0:
                        continue
                    x1_change = 0
                    y1_change = -snake_block
                    direction_sound.play()

                elif event.key == pygame.K_DOWN:
                    if y1_change<0:
                        continue
                    x1_change = 0
                    y1_change = snake_block
                    direction_sound.play()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
            game_over_sound.play()

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)

        pygame.draw.rect(dis,red, [foodx,foody,snake_block,snake_block] )
        snake_size = []
        snake_size.append(x1)
        snake_size.append(y1)
        snake_list.append(snake_size)
        # Check for collision with own body and decrease length and lives
        collision_idx=None
        if(length_snake>1):
            for idx, segment in enumerate(snake_list[:-1]):  # Exclude the head from the check
                if segment == [x1, y1]:
                    lives =lives-1
                    score=score-2
                    print(lives)
                    collision_idx=idx
                    break

        # Decrease snake size till the place it bit itself
        if collision_idx is not None:
            game_bite_itself.play()
            del snake_list[collision_idx+1:]
            length_snake=len(snake_list)
                
        if lives == 0:
            game_close = True
            game_over_sound.play()

        if len(snake_list) > length_snake:
            del snake_list[0]

        my_snake(snake_block,snake_list)
        my_score(score,lives)

        pygame.display.update()


        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width-snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height-snake_block) / 10.0) * 10.0
            length_snake +=1
            score+=1
            bite_sound.play()


            #Increase speed at specific lengths
            if score>=10 and score<20:
                snake_speed=10
            elif score>=20 and score<30:
                snake_speed=15
            elif score>=30 and score<40:
                snake_speed=18
            elif score>=40:
                snake_speed=22
        my_score(score,lives)


        clock.tick(snake_speed)

    game_over_sound.play()
    pygame.quit()
    quit()

main_game()