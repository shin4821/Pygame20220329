import pygame
import os

""" Project) 오락실 Pang 게임 만들기

[게임조건]
1. 캐릭터는 화면 아래에 위치, 좌우로만 이동 가능
2. 스페이스를 누르면 무기를 쏘아 올림
3. 큰 공 1개가 나타나서 바운스
4. 무기에 닿으면 공은 작은 크기 2개로 분할, 가장 작은 크기의 공은 사라짐
5. 모든 공을 없애면 게임 종료 (성공)
6. 캐릭터는 공에 닿으면 게임 종료 (실패)
7. 시간 제한 99초 초과시 게임 종료 (실패)
8. FPS는 30으로 고정 (필요시 speed 값을 조정)

[게임 이미지]
1. 배경: 640 * 480 (가로 세로) - background.png
2. 무대: 640 * 50 - stage.png
3. 캐릭터: 60 * 33 - character.png
4. 무기: 20 * 430 - weapon.png
5. 공: 160 * 160, 80 * 80, 40 * 40, 20 * 20 - balloon1.png ~ balloon4.png """



############################################################
# 반드시 해야하는 것들
pygame.init()

# 화면크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 배경화면 설정
current_path = os.path.dirname(__file__) #현재 파일
images_path = os.path.join(current_path, "images")
background = pygame.image.load(os.path.join(images_path, "background.jpg"))
 
# 스테이지 설정
stage = pygame.image.load(os.path.join(images_path, "gamestage.jpg"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

stage_x_pos = 0
stage_y_pos = screen_height - stage_height

# 캐릭터 설정
character = pygame.image.load(os.path.join(images_path, "gameCharacter1.png"))

character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_height - character_height

character_speed = 10

to_x_right = 0
to_x_left = 0

# 무기 설정
weapon = pygame.image.load(os.path.join(images_path, "arrow1.png"))

weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기는 한 번에 여러번 발사 가능
weapons = []
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images=[
    pygame.image.load(os.path.join(images_path, "balloon1.png")),
    pygame.image.load(os.path.join(images_path, "balloon2.png")),
    pygame.image.load(os.path.join(images_path, "balloon3.png")),
    pygame.image.load(os.path.join(images_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls =[]

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x": 3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽으로
    "to_y":-6, # y축 이동방향,
    "init_spd_y" : ball_speed_y[0] # y 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1             
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_time = pygame.time.get_ticks() # 시작 시간 정의
game_result = "Game Over" # Time out, Mission Complete, Game Over


# 화면 타이틀 설정
pygame.display.set_caption("BounceBall Game")


# FPS
clock = pygame.time.Clock()

############################################################

running =  True
while running :
    dt = clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 키 눌렀을 때
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                to_x_right+=character_speed
            if event.key == pygame.K_LEFT:
                to_x_left-=character_speed
            if event.key == pygame.K_SPACE:          
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
                              
        # 키 땠을 때
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                to_x_right = 0
            if event.key == pygame.K_LEFT:
                to_x_left = 0
                         
    # 위치 정하기
    character_x_pos += to_x_right + to_x_left   
    
    
    # 위치 한계 정하기
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width   
    
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1]>0]
    
    # 공 위치 정하기
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        # 가로 벽에 부딛혔을 때 공 튕기는 효과
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1
            
        # 세로 위치, 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 튕기기 전 떨어질 때
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    
    # 4. 충돌 처리
    
    # 캐릭터 rect 정보 저장 
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    # 공 rect 정보 저장
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]
            
            # 무기 rect 정보 저장 
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos
            
            # 충돌할 경우, 무기는 없어지고 공은 둘로 쪼개어진다.
            if weapon_rect.colliderect(ball_rect):            
                weapon_to_remove = weapon_idx # 현재 무기 index값 넣어주기
                ball_to_remove = ball_idx # 현재 공 index값 넣어주기
                
                if ball_img_idx < 3: # 제일 작은 공이 아닌 경우,
                    
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    
                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    
                    
                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "to_x": -3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽으로
                        "to_y":-6, # y축 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })
                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "to_x": 3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽으로
                        "to_y":-6, # y축 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })
                 
                
                break
        else:
            continue
        break
    
    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    
    # 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls)==0:
        game_result = "Mission Complete"
        running = False
    
    
            
    # 5. 화면 그리기
    screen.blit(background, (0,0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
      screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
    
    screen.blit(stage, (stage_x_pos,stage_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer,  (10,10))
    
    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False 

    pygame.display.update()

# 게임 오버 메세지
msg = game_font.render(game_result, True, (255,255,0)) # 노란색
msg_rect = msg.get_rect(center =(int(screen_width / 2), int(screen_height /2)))
screen.blit(msg, msg_rect)

pygame.display.update()
pygame.time.delay(2000)


#파이게임종료
pygame.quit()
        
