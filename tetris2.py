import sys
from math import sqrt
from random import randint
import pygame
from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_DOWN,K_SPACE,K_0
from block_data import BLOCK_DATA
import pip

class Block:
    def __init__(self,count):
        self.turn = randint(0,3)
        self.type = BLOCK_DATA[randint(0,6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos= randint(2,8-self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL

    def update(self,count):
        erased = 0
        if is_overlapped(self.xpos,self.ypos+1,self.turn):
            # for y_offset in range(BLOCK.size):
            #     for x_offset in range(BLOCK.size):
            #         if 0 <= self.xpos+x_offset < WIDTH and 0 <= self.ypos+y_offset < HEIGHT:
            #             val = BLOCK.data[y_offset*BLOCK.size + x_offset]
            #             if val != 0:
            #                 FIELD[self.ypos+y_offset][self.xpos+x_offset] = val
            # ブロックがフィールド上にあるかどうかを確認し、フィールドに値を代入する
          
          #修正後
            for i in range(BLOCK.size * BLOCK.size):
                x_offset = i % BLOCK.size
                y_offset = i // BLOCK.size
                x_pos = self.xpos + x_offset
                y_pos = self.ypos + y_offset
                # フィールドの範囲内かを確認
                if 0 <= x_pos < WIDTH and 0 <= y_pos < HEIGHT:
                    val = BLOCK.data[i]
                    if val != 0:
                        FIELD[y_pos][x_pos] = val

            erased = erase_line()
            go_next_block(count)

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos+=1
        return erased

    def draw(self):
        """ ブロックを描画する """
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and 0 <= xpos + self.xpos < WIDTH and val != 0:
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24))
                
def erase_line():
    erased = 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            del FIELD[ypos]
            FIELD.insert(0, [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8])
        else:
            ypos -= 1
    return erased

def is_game_over():
    """ ゲームオーバーか否か """
    # filled = 0
    # for i in FIELD[0]:
    #     if i != 0:
    #         filled += 1
    # return filled > 2   # 2 = 左右の壁
    flag = False
    for i in FIELD[0][1:WIDTH-1]:
        if i != 0:
            flag = True
    return flag

def go_next_block(count):
    """ 次のブロックに切り替える """
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)

def is_overlapped(xpos, ypos, turn):
    """ ブロックが壁や他のブロックと重なっているかどうか """
    data = BLOCK.type[turn]
    if any(data[y_offset * BLOCK.size + x_offset] != 0 and FIELD[ypos + y_offset][xpos + x_offset] != 0
       for y_offset in range(BLOCK.size) for x_offset in range(BLOCK.size)
       if 0 <= xpos + x_offset < WIDTH and 0 <= ypos + y_offset < HEIGHT):
            return True
    return False

    # for y_offset in range(BLOCK.size):
    #     for x_offset in range(BLOCK.size):
    #         if 0 <= xpos+x_offset < WIDTH and \
    #             0 <= ypos+y_offset < HEIGHT:
    #             if data[y_offset*BLOCK.size + x_offset] != 0 and \
    #                 FIELD[ypos+y_offset][xpos+x_offset] != 0:
    #                 return True
    # return False


pygame.init()
pygame.key.set_repeat(30,30)
SURFACE = pygame.display.set_mode([700,700])
FPSCLOCK = pygame.time.Clock()
#WIDTH = 12
WIDTH = 16
HEIGHT = 22
INTERVAL = 40
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255),(0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NEXT_BLOCK = None
HOLD_BLOCK = None

def main():
    global INTERVAL,HOLD_BLOCK,BLOCK,NEXT_BLOCK
    count = 0
    score = 0
    game_over = False
    ishold = False
    smallfont = pygame.font.SysFont(None,36)
    largefont = pygame.font.SysFont(None,72)
    message_over = largefont.render("GAME OVER!!",True, (0, 255, 225))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)
    go_next_block(INTERVAL)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0 or xpos == WIDTH - 1 else 0
    #FIELD = [[8 if xpos == 0 or xpos == WIDTH - 1 else 0 for xpos in range(WIDTH)] for ypos in range(HEIGHT)]
    FIELD[ypos][xpos]
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 8

    keyleft = False
    keyright = False
    keydown = False
    keyspace = False
    while True:
        key = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key

        game_over = is_game_over()
        if not game_over:
            count+=5
            if count % 1000 == 0:
                INTERVAL = max(1,INTERVAL-2)
            
            if BLOCK is None:
                # ブロックがない場合、次のブロックを取得
                BLOCK = NEXT_BLOCK if NEXT_BLOCK is not None else Block(count)
                NEXT_BLOCK = Block(count)

            erased = BLOCK.update(count)
            if erased > 0:
                score += (2 ** erased) * 100

            next_x, next_y, next_t = BLOCK.xpos, BLOCK.ypos, BLOCK.turn
            keys = pygame.key.get_pressed()
            # if keys[K_0] and not ishold: #ホールドしてないとき
            #     if HOLD_BLOCK is None:
            #         BLOCK,HOLD_BLOCK = NEXT_BLOCK,BLOCK if NEXT_BLOCK is not None else Block(count)
            #         go_next_block(count)
            #     BLOCK.xpos,BLOCK.ypos = randint(2,8-BLOCK.size),1-BLOCK.size
            #     ishold=True
            # elif keys[K_0] and ishold:
            #     BLOCK,NEXT_BLOCK = HOLD_BLOCK,BLOCK
            #     HOLD_BLOCK = None
            #     ishold = False
            if keys[K_0]:
                if HOLD_BLOCK is None and not ishold: #ホールドしてない
                    HOLD_BLOCK = BLOCK
                    go_next_block(count)
                    #BLOCK = NEXT_BLOCK if NEXT_BLOCK is not None else Block(count)
                    ishold=True
                    
                elif HOLD_BLOCK is not None and ishold: #ホールドしている
                    NEXT_BLOCK = BLOCK
                    BLOCK = HOLD_BLOCK
                    HOLD_BLOCK = None
                    ishold = False
                BLOCK.xpos,BLOCK.ypos = randint(2,8-BLOCK.size),1-BLOCK.size
            if keys[K_SPACE]:
                if not keyspace:
                    keyspace = True
                    next_t = (next_t + 1) % 4
                else:
                    keyspace = False
            if keys[K_LEFT]:
                if not keyleft:
                    keyleft = True
                    next_x -= 1
                else:
                    keyleft = False
            if keys[K_RIGHT]:
                if not keyright:
                    keyright = True
                    next_x += 1
                else:
                    keyright = False
            if keys[K_DOWN]:
                if not keydown:
                    keydown = True
                    next_y += 1
                else:
                    keydown = False
            # if key== K_0 and  not ishold:
            #     if HOLD_BLOCK is None:
            #         BLOCK = NEXT_BLOCK if NEXT_BLOCK is not None else Block(count)
            #         go_next_block(count)
            #     else:
            #         HOLD_BLOCK,BLOCK = BLOCK,HOLD_BLOCK
            #     BLOCK.xpos,BLOCK.ypos = randint(2,8-BLOCK.size),1-BLOCK.size
            #     ishold=True
            # elif key == K_SPACE:
            #     next_t = (next_t + 1) % 4
            # elif key == K_RIGHT:
            #     next_x += 1
            # elif key == K_LEFT:
            #     next_x -= 1
            # elif key == K_DOWN:
            #     next_y += 1

            if not is_overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]
        else:
            ishold=False

        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT): #ゲームフィールド
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val],(xpos*25 + 25, ypos*25 + 25, 24, 24))
        BLOCK.draw()

        #ホールドブロックの描画
        if HOLD_BLOCK is not None:
            for ypos in range(HOLD_BLOCK.size):
                for xpos in range(HOLD_BLOCK.size):
                    val = HOLD_BLOCK.data[xpos + ypos * HOLD_BLOCK.size]
                    pygame.draw.rect(SURFACE, COLORS[val], (xpos * 25 + 500, ypos * 25 + 350, 24, 24))
        hold_block = str("holdblock").zfill(6)
        text_image = smallfont.render(hold_block,True,(0,255,255))
        SURFACE.blit(text_image,(500,300))

        # 次のブロックの描画
        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos*NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val],(xpos*25 + 500, ypos*25 + 180, 24, 24))
        next_block = str("nextblock").zfill(6)
        text_image = smallfont.render(next_block,True,(0,255,255))
        SURFACE.blit(text_image,(500,120))

        # スコアの描画
        score_str = str(score).zfill(6)
        score_image = smallfont.render(score_str,True, (0, 255, 0))
        SURFACE.blit(score_image, (500, 30))

        import os
        japanese_font = os.path.join(pygame.font.get_default_font(), "C:/Users/hatot/.vscode/pygames/tetris/msmincho.ttc")
        smallfont = pygame.font.Font(japanese_font, 20)
        largefont = pygame.font.Font(japanese_font, 72)

        execption = str("  操作説明").zfill(6)
        text_image1 = smallfont.render(execption,True,(0,255,255))
        SURFACE.blit(text_image1,(500,450))

        execption2 = str("十字キーの左右で移動").zfill(6)
        text_image2 = smallfont.render(execption2,True,(0,255,255))
        SURFACE.blit(text_image2,(500,500))

        execption3 = str("下で落下速度上昇").zfill(6)
        text_image3 = smallfont.render(execption3,True,(0,255,255))
        SURFACE.blit(text_image3,(500,550))

        execption4 = str("スペースキーで回転").zfill(6)
        text_image4 = smallfont.render(execption4,True,(0,255,255))
        SURFACE.blit(text_image4,(500,600))

        execption5 = str("0キーでホールド").zfill(6)
        text_image5 = smallfont.render(execption5,True,(0,255,255))
        SURFACE.blit(text_image5,(500,650))

        if game_over:
            SURFACE.blit(message_over, message_rect)

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()