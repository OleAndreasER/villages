#!/bin/python3
import pygame
from library.graphics import drawWorld, drawUI, drag, changeZoom, rightClick, leftClick
from library.gamelogic import endTurn

width = 1920
height = 1080

fps = 60

isDragging = False

def main():
    global isDragging
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Villages")
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    isDragging = True
                    leftClick(win, event.pos)
                elif event.button == 4: #wheelup
                    changeZoom(1, event.pos)
                elif event.button == 5: #wheeldown
                    changeZoom(-1, event.pos)
                elif event.button == 2:
                    endTurn()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    isDragging = False 
                elif event.button == 3:
                    rightClick(win, pos)

            elif event.type == pygame.MOUSEMOTION:
                if isDragging:
                    drag(event.rel)

        drawWorld(win)
        drawUI(win)
        pygame.display.update()


if __name__ == "__main__":
    main()
