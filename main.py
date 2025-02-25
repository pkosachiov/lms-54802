#импортирование всех библиотек
import pygame
import os

class Board:
    # создание поля
    def __init__(self, board):
        self.board = load_world('./world.txt')
        self.width = len(self.board[0])
        self.height = len(self.board)
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    #обработка игровой карты
    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                image = pygame.transform.scale(load_image(self.board[i][j].img), (self.cell_size, self.cell_size))
                screen.blit(image, (j*self.cell_size + self.left, i*self.cell_size + self.top))

    #функция для перемещения вниз
    def move_up(self, x, y):
        if y-1 >= 0 and board.board[y-1][x].name != 'wall':
            board.board[y-1][x], board.board[y][x] = board.board[y][x], board.board[y-1][x]

    #функция для перемещения вверх
    def move_down(self, x, y):
        if y+1 < board.height and board.board[y+1][x].name != 'wall':
            board.board[y+1][x], board.board[y][x] = board.board[y][x], board.board[y+1][x]

    #функция для перемещения вправо
    def move_right(self, x, y):
        if x+1 < board.width and board.board[y][x+1].name != 'wall':
            board.board[y][x+1], board.board[y][x] = board.board[y][x], board.board[y][x+1]

    #функция для перемещения влево
    def move_left(self, x, y):
        if x-1 >= 0 and board.board[y][x-1].name != 'wall':
            board.board[y][x-1], board.board[y][x] = board.board[y][x], board.board[y][x-1]

#класс с клетками
class map_cell:
#имя в дебаге, имя в игре, обозначение на карте, шанс выпадения
    def __init__(self, name, game_name, img):
        self.name = name
        self.game_name = game_name
        self.img = img

#все клетки
all_cell = {
        'wall': ('стена', './imgs/wall.png'),
        'floor': ('пол', './imgs/floor.png'),
        'player': ('игрок', './imgs/player.png')
        }

#функция для загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        return None
    image = pygame.image.load(fullname)
    return image

def players_cell():
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j].name == 'player':
                return j, i

def recover_cell(insciption):
    if insciption == 'f':
        return(map_cell('floor', *all_cell['floor']))
    elif insciption == 'w':
        return(map_cell('wall', *all_cell['wall']))
    elif insciption == 'p':
        return(map_cell('player', *all_cell['player']))

#считывание мира из файла
def load_world(path_world):
    world = []
    with open(path_world, 'r') as f:
        file_map = f.readlines()
    for i in range(len(file_map)):
        world.append([])
        for j in file_map[i][:-1]:
            world[i].append(recover_cell(j))
    return(world)


size = width, height = 10, 10

deaftul_map = []

board = Board(deaftul_map)

end_game = False

#инициальзация шрифта
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

#инициальзация экрана
pygame.init()
pygame.display.set_caption('main')
#высота и ширина карты
screen = pygame.display.set_mode(list(map(lambda x: x*board.cell_size, size)))

screen.fill((0, 0, 0))

running = True
fps = 60
clock = pygame.time.Clock()

epilog = True

#начальный экран
while epilog:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True
            running = False
            epilog = False
        elif event.type == pygame.KEYDOWN:
            epilog = False
    image = pygame.transform.scale(load_image("./imgs/fon.jpg"), (board.height*board.cell_size, board.width*board.cell_size))
    screen.blit(image, (0, 0, 0, 0))
    pygame.display.flip()

while running:

    while not end_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    board.move_down(*players_cell())
                if event.key == pygame.K_w:
                    board.move_up(*players_cell())
                if event.key == pygame.K_a:
                    board.move_left(*players_cell())
                if event.key == pygame.K_d:
                    board.move_right(*players_cell())

        #вывод карты с игроком
        board.render(screen)

        #загрузка экрана
        clock.tick(fps)
        pygame.display.flip()

pygame.quit()
