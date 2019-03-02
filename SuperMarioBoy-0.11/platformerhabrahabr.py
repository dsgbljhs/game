import pygame
# from pygame import *
# from player import *
# from blocks import *
import player
import blocks

# Объявляем переменные
WIN_WIDTH = 900  # Ширина создаваемого окна
WIN_HEIGHT = 700  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = player.Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    level = [
        "--------------------------------------------------",
        "-         ** ---               -    ---          -",
        "-     -      ---               -    ---          -",
        "---  --- ---              -    -    ---          -",
        "-    - - ---              -    *    ---          -",
        "-  - -   ---             --                      -",
        "-  - --- ---        --   --                      -",
        "-- -   - ---*  -   ---  ---  -   ---   ------    -",
        "-- --- - ---*  -   ---  ---  -    --     *       -",
        "--     -      ---   -   ---  -    ---            -",
        "--     -            -   ---  -   *--             -",
        "--   ---   --    ----  ---- --   *--             -",
        "--     *   -- --    -  ---- --   *--  -------  ---",
        "-----  -  --- ---  --  ---- --*  *--  -------  ---",
        "--     -   -- --   -   -    ----      -------  ---",
        "--     -   -- --   - --     ----           *   ---",
        "--- --*@@- -- --  -- --             -      - -----",
        "-        -    -- --  -              -*     - -----",
        "-        -   *@*  -  -      ----------    --   ---",
        "--------------    -  ---    -------  -   --      -",
        "----------        -  ---    -------  -  -----    -",
        "-        -----    -  ---   ------        ------  -",
        "-             ------       ------ P --------*    -",
        "-                    **    --------          -* --",
        "--------------------------------------------------"
    ]
    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = blocks.Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = blocks.BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "@":
                bs = blocks.BlockDi(x, y)
                entities.add(bs)
                platforms.append(bs)
            if col == "P":
                pr = blocks.Princess(x, y)
                print(x, y)
                entities.add(pr)
                platforms.append(pr)

            x += blocks.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += blocks.PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * blocks.PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * blocks.PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                raise SystemExit
                "QUIT"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True

            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        # entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
