import pygame
import psycopg2
import random

pygame.init()

conn = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password="Muhammed4ever"
)
current = conn.cursor()


current.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        game_count INT DEFAULT 0
    );
""")
conn.commit()

current.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        level INT
    );
""")
conn.commit()


WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 10


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def generate_walls_for_level(level):
    """
    Уровень 1: Нет стен.
    Уровень 2: Появляется горизонтальный ряд стен.
    Уровень 3: Дополнительно добавляются вертикальные стены.
    Если уровень >3, ограничиваем до 3.
    """
    if level < 2:
        return []
    if level > 3:
        level = 3
    if level == 2:
        walls = []
      
        for i in range(200, 300, CELL):
            walls.append((i, 200))
        return walls
    if level == 3:
        walls = []
     
        for i in range(200, 300, CELL):
            walls.append((i, 200))
    
        for j in range(180, 280, CELL):
            walls.append((300, j))
        return walls


def get_user():
    username = input("Введите ваш никнейм: ")
    current.execute("SELECT id, game_count FROM users WHERE username = %s", (username,))
    user = current.fetchone()
    if user:
        user_id, game_count = user
       
        current.execute("UPDATE users SET game_count = game_count + 1 WHERE id = %s", (user_id,))
        conn.commit()
        print(f"Добро пожаловать, {username}! Вы запустили игру {game_count + 1} раз(а).")
        return user_id, username
    else:
        current.execute(
            "INSERT INTO users (username, game_count) VALUES (%s, 1) RETURNING id",
            (username,),
        )
        user_id = current.fetchone()[0]
        conn.commit()
        print(f"Пользователь {username} зарегистрирован. Это ваша первая игра.")
        return user_id, username


def generate_food(snake, wall):
    while True:
        x = random.randint(0, WIDTH // CELL - 1) * CELL
        y = random.randint(0, HEIGHT // CELL - 1) * CELL
        if (x, y) not in snake and (x, y) not in wall:
            return (x, y)


def save_game(username, level):
   
    current.execute("INSERT INTO user_score (username, level) VALUES (%s, %s)", (username, level))
    conn.commit()
    print(f"Результат сохранён: {username} достиг уровня {level}")


def main():
    user_id, username = get_user()
   
    level = 1

    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = [(60, 60)]
    dx, dy = CELL, 0
    current_walls = generate_walls_for_level(level)
    food = generate_food(snake, current_walls)
    paused = False

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL, 0
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        print("Игра поставлена на паузу.")
                    else:
                        print("Игра возобновлена.")
        
        if paused:
            continue

       
        new_head = ((snake[-1][0] + dx) % WIDTH, (snake[-1][1] + dy) % HEIGHT)
        
       
        if new_head in snake or new_head in current_walls:
            print(f"Game Over! Вы достигли уровня: {level}")
            save_game(username, level)
            running = False
            break
        
        snake.append(new_head)
        
        if new_head == food:
            
            food = generate_food(snake, current_walls)
            
            if (len(snake) - 1) % 5 == 0:
                level += 1
                if level > 3:
                    level = 3
                current_walls = generate_walls_for_level(level)
                print(f"Переход на уровень {level}")
        else:
            snake.pop(0)
        
        screen.fill(BLACK)
        for wall in current_walls:
            pygame.draw.rect(screen, WHITE, (*wall, CELL, CELL))
        pygame.draw.rect(screen, RED, (*food, CELL, CELL))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))
        
        pygame.display.flip()
    
    pygame.quit()

main()