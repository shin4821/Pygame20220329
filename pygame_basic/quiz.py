import pygame
import random


""" Quiz) 하늘에서 떨어지는 똥 피하기 게임을 만드시오

[게임 조건]
1. 캐릭터는 화면 가장 아래에 위치, 좌우로만 이동 가능
2. 똥은 화면 가장 위에서 떨어짐. x 좌표는 매번 랜덤으로 설정
3. 캐릭터가 똥을 피하면 다음 똥이 다시 떨어짐
4. 캐릭터가 똥과 충돌하면 게임 종료
5. FPS는 30으로 고정

[게임 이미지]
1. 배경: 640 * 480 (세로 가로) - background.png
2. 캐릭터: 70 * 70 - character.png
3. 똥: 70 * 70 - enemy.png """


#############################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 640 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Avoiding Poop Game")

# FPS
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("C:\\Pygame\\pygame_basic\\design-space-paper-textured-background.jpg")

# 캐릭터 불러오기
character = pygame.image.load("C:\\Pygame\\pygame_basic\\docCharacter1.png")
character_size = character.get_rect().size # 캐릭터의 크기를 불러옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width/2)
character_y_pos = screen_height - character_height

# 수정1 : 기존의 character_to_x 를 왼쪽 방향, 오른쪽 방향 변수 2개로 나눔
to_x_left = 0
to_x_right = 0

# 이동 속도
character_speed = 10

# 적 (enemy) 캐릭터
enemy = pygame.image.load("C:\Pygame\pygame_basic\poopCharacter1.png")
enemy_size = enemy.get_rect().size # 캐릭터의 크기를 불러옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = random.randint(0, screen_width - character_width)
enemy_y_pos = 0
enemy_speed = 10

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 10

# 시작 시간
start_ticks = pygame.time.get_ticks() # 시작 tick을 받아옴
#############################################################

# 이벤트 루프
running = True
while running:
    # FPS 설정
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 닫기 버튼 누르면 닫힌다.
            running = False
            
        if event.type == pygame.KEYDOWN: # 수정2 : 키를 누를 때 LEFT, RIGHT 에 따라 서로 다른 변수의 값 조정
            if event.key == pygame.K_LEFT:
                to_x_left-=character_speed
            if event.key == pygame.K_RIGHT:
                to_x_right+=character_speed
        
        if event.type == pygame.KEYUP: # 수정3 : 키에서 손을 뗄 때 LEFT, RIGHT 를 각각 처리
            if event.key == pygame.K_LEFT:
                to_x_left = 0            
            elif event.key == pygame.K_RIGHT:
                to_x_right = 0

          
    # 최종 캐릭터 위치 설정      
    character_x_pos+=to_x_left + to_x_right
    
    # 최종 캐릭터 위치 경계값 설정 
    if character_x_pos<0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
    # 똥 캐릭터 위치 설정
    enemy_y_pos += enemy_speed    
    
    # 똥 떨어지면 다시 떨어지도록 설정
    if enemy_y_pos > screen_height :
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width - character_width)
    
    
    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos
    
    
    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요.")
        running = False
        
        
    screen.blit(background, (0,0)) # 배경화면 그리기
    screen.blit(character, (character_x_pos,character_y_pos)) # 캐릭터 위치 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 똥 위치 그리기
    
    # 타이머 집어 넣기, 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과시간(ms)을 1000으로 나누어서 초(s)단위로 표시 
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255)) # 시간, True, 글자색상
    screen.blit(timer, (10, 10))
    
    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False
    
    
    pygame.display.update() # 배경화면 계속 업데이트 (필수로 해줘야함)

# 잠시 대기
#pygame.time.delay(2000)

# pygame 종료
pygame.quit()


