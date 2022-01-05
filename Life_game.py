""" Описание задачи:
Правила игры «Жизнь» достаточно простые:
1) «Жизнь» разыгрывается на бесконечном клеточном поле.
2) У каждой клетки 8 соседних клеток.
3) В каждой клетке может жить существо.
4) Существо с двумя или тремя соседями выживает в следующем поколении, иначе погибает от одиночества или перенаселённости.
5) В пустой клетке с тремя соседями в следующем поколении рождается существо.

Требования к коду:
1) Код необходимо предоставить в виде github репозитория.
2) Игра и все её составляющие (поле, клетки) должны быть реализованы в виде отдельных модулей (классов).
3) Классы должны быть реализованы в соотвтетствии с принципами Объектно Ориентированного Программирования.
4) Программа должна быть реализована на языке Python3 и запускаться на любом устройстве с Windows,
Linux, MacOS в виде .py скрипта или в консоли, или в графическом интерфейсе, на ваше усмотрение.
"""
import random
import pygame


class Cell:
    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        self.life = life
        self.neighbours = 0

    def cell_count_neighbours(self):
        '''
        считаем кол-во соседей для одной ячейки.
        Если она на границе, считаем, что за границей соседей у нее нет.
        '''
        kol = 0
        for i in range(max(0, self.x - 1), min(Area.count_x-1, self.x + 1) + 1):  # клетка слева и справа
            for j in range(max(0, self.y - 1), min(Area.count_y-1, self.y + 1) + 1):  # клетка снизу и сверху
                if i != self.x or j != self.y:
                    kol += int(Area.cells[i][j].life)
        self.neighbours = kol
        return kol

    def cell_area_rule(self):
        '''
        правила игры
        '''
        if self.life == False and self.neighbours == 3:
            self.life = True
        elif self.life == True and (self.neighbours == 3 or self.neighbours == 2):
            self.life = True
        else:
            self.life = False



class Area:
    cells = []  # чтобы увидеть переменные в классе Cell
    count_x = 0
    count_y = 0

    def __init__(self, count_x, count_y):
        Area.count_x = count_x
        Area.count_y = count_y
        # заполняем матрицу случайными 0/1
        for i in range(count_x):
            line = []
            for j in range(count_y):
                line.append(Cell(i, j, random.randint(0, 1)))
            Area.cells.append(line)

    def count_neighbours(self):
        '''
        для каждой ячейки поля считаем соседей
        '''
        for i in Area.cells:
            for j in i:
                j.cell_count_neighbours()

    def area_rule(self):
        '''
        для каждой ячейки поля выполняем правила игры
        '''
        for i in Area.cells:
            for j in i:
                j.cell_area_rule()


class Game:
    def __init__(self, width, height, count_w, count_h):
        self.width = width
        self.height = height
        self.cell_size_w = width // count_w
        self.cell_size_h = height // count_h
        self.screen = pygame.display.set_mode([width, height])
        self.cells = Area(count_w, count_h)


    def draw_rect(self):
        '''
        закрашиваем ячейки с существами и рисум сетку
        '''
        for cell_list in self.cells.cells:
            for item in cell_list:
                x = item.x
                y = item.y
                if item.life:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     [x * self.cell_size_w,
                                      y * self.cell_size_h,
                                      self.cell_size_w, self.cell_size_h])

        for x in range(0, self.width, self.cell_size_w):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size_h):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        running = True
        while running:
            for event in pygame.event.get():
                # держим окно открытым, пока не нажмем "закрыть"
                if event.type == pygame.QUIT:
                    running = False
            self.cells.count_neighbours()
            self.cells.area_rule()
            self.screen.fill(pygame.Color('white'))
            self.draw_rect()  # закрашиваем ячейки
            pygame.display.flip()  # обновляем поле
            clock.tick(10)
        pygame.quit()


def main():
    game = Game(440, 440, 20, 20)
    game.run()

if __name__ == "__main__":
    main()
