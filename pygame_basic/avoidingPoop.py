import pygame

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
background = pygame.image.load("C:\\Pygame\\pygame_basic\\background.png")

# 캐릭터 불러오기
character = pygame.image.load("C:\\Pygame\\pygame_basic\\character.png")
character_size = character.get_rect().size # 캐릭터의 크기를 불러옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width/2)
character_y_pos = screen_height - character_height

# 이동할 좌표
to_x = 0

# 이동 속도
character_speen = 10

# 적 (enemy) 캐릭터
enemy = pygame.image.load("C:\\Pygame\\pygame_basic\\enemy.png")
enemy_size = enemy.get_rect().size # 캐릭터의 크기를 불러옴
enemy_width = enemy_size[0] # 캐릭터의 가로 크기
enemy_height = enemy_size[1] # 캐릭터의 세로 크기
enemy_x_pos = 0
enemy_y_pos = screen_height - enemy_height

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
            
        if event.type == pygame.KEYDOWN: # 방향키 누르면 움직인다.
            if event.key == pygame.K_LEFT:
                to_x-=character_speen
            if event.key == pygame.K_RIGHT:
                to_x+=character_speen
        
        if event.type == pygame.KEYUP: # 방향키 때면 멈춘다.
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x=0

          
    # 최종 캐릭터 위치 설정      
    character_x_pos+=to_x
    
    # 최종 캐릭터 위치 경계값 설정 
    if character_x_pos<0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        
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
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    
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
pygame.time.delay(2000)


# pygame 종료
pygame.quit()


