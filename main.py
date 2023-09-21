import pygame as pg;
from random import randint;
from typing import List, Tuple;

class Game:
    def __init__(self, width:int, height:int, gridsXY:int):
        self.w:int = width;
        self.h:int = height;

        self.grids:int = gridsXY;
        self.gridSize:int;
        self.gridSize = (width/gridsXY, height/gridsXY);

        self.window = pg.display.set_mode((width, height));

        self.snakeDirection:Tuple[int,int] = (0,0);
        self.snakeLength:int = 0;

        self.snake:List[pg.Rect] = [pg.Rect(
            int(gridsXY/2)*self.gridSize[0],
            int(gridsXY/2)*self.gridSize[1],
            self.gridSize[0], self.gridSize[1])];
        
        self.food:pg.Rect = self.new_food();

        self.running:bool = False;
        self.clock:pg.time.Clock;
        self.clock = pg.time.Clock();
    
    def reset(self, gridsXY:int) -> None:
        self.snakeLength = 0;
        self.snake = [pg.Rect(
            int(gridsXY/2)*self.gridSize[0],
            int(gridsXY/2)*self.gridSize[1],
            self.gridSize[0], self.gridSize[1])];

    def mainLoop(self, FPS:int) -> None:
        self.running = True;
        while self.running:
            self.window.fill((0,0,0));
            self.events();
            self.move();
            self.draw();
            pg.display.update();
            self.clock.tick(FPS);

    def new_food(self) -> pg.Rect:
        pos:pg.Rect = pg.Rect(
            randint(0,self.grids-1)*self.gridSize[0],
            randint(0,self.grids-1)*self.gridSize[1],
            self.gridSize[0], self.gridSize[1]);
        
        if pos in self.snake:
            return self.new_food();
        return pos;

    def draw(self) -> None:
        pg.draw.rect(self.window, (255,0,0), self.food);
        for tail in self.snake:
            pg.draw.rect(self.window, (0,255,0), tail);

    def move(self) -> None:
        self.snake.append(pg.Rect(
            self.snake[self.snakeLength].x+self.snakeDirection[0],
            self.snake[self.snakeLength].y+self.snakeDirection[1],
            self.gridSize[0], self.gridSize[1]));
        
        self.snake.pop(0);

        if self.snake[self.snakeLength] == self.food:
            self.snake.append(self.snake[self.snakeLength]);
            self.snakeLength += 1;
            self.food = self.new_food();
            return;

        if self.snake[self.snakeLength].x < 0:
            self.reset(self.grids);
            return;
        if self.snake[self.snakeLength].x > self.w:
            self.reset(self.grids);
            return;
        if self.snake[self.snakeLength].y < 0:
            self.reset(self.grids);
            return;
        if self.snake[self.snakeLength].y > self.h:
            self.reset(self.grids);
            return;
        
        if self.snakeLength != 0:
            if self.snake[self.snakeLength] in self.snake[:self.snakeLength-1:]:
                self.reset(self.grids);
                return;

    def events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); exit(42);
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit(); exit(42);
                if event.key == pg.K_w:
                    if self.snakeDirection[1] == 0:
                        self.snakeDirection = (0, -self.gridSize[1]);
                    return;
                if event.key == pg.K_a:
                    if self.snakeDirection[0] == 0:
                        self.snakeDirection = (-self.gridSize[0], 0);
                    return;
                if event.key == pg.K_s:
                    if self.snakeDirection[1] == 0:
                        self.snakeDirection = (0, self.gridSize[1]);
                    return;
                if event.key == pg.K_d:
                    if self.snakeDirection[0] == 0:
                        self.snakeDirection = (self.gridSize[0], 0);
                    return;

if __name__ == "__main__":
    game = Game(500, 500, 20);
    game.mainLoop(10);
