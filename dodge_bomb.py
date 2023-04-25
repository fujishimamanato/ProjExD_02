import time
import random
import sys

import pygame as pg

# 練習４
delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
        pg.K_w: (0, -2),
        pg.K_s: (0, +2),
        pg.K_a: (-2, 0),
        pg.K_d: (+2, 0)
        }



def check_dound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool,bool]: 
    """
    オブジェクトが画面内or画面外かを判定し、真理値タプルを返す関数
    引数1:画面surfaseのRect
    引数2:こうかとんまたは爆弾surfaceのRect
    返り値:objの縦、横が画面外に出ていたらFalseを返す
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    # 追加機能　２
    alufa = {
            (-1, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
            (-1, +1): pg.transform.rotozoom(kk_img, 45, 1.0),
            (0, +1): pg.transform.rotozoom(kk_img, 90, 1.0),
            (+1, +1): pg.transform.rotozoom(kk_img, 135, 1.0),
            (+1, 0): pg.transform.flip(kk_img, True,False),
            (+1, -1): pg.transform.rotozoom(kk_img, 225, 1.0),
            (0, -1): pg.transform.rotozoom(kk_img, 270, 1.0),
            (-1, -1): pg.transform.rotozoom(kk_img, 315, 1.0)
            }
    kk_rct = kk_img.get_rect()
    kk_rct.center = [900, 400]

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,( 255 ,0 ,0 ), ( 10 , 10 ), 10)  # 練習1
    bb_img.set_colorkey((0,0,0))  # 練習1
    x, y = random.randint(0,1600), random.randint(0, 900)
    screen.blit(bb_img, [x, y])
    vx, vy = +1, +1
    bb_rct = bb_img.get_rect()  # 練習４
    bb_rct.center = x, y  # 練習４

    tmr = 0

    accs = [a for a in range(1, 11)]
    fonto = pg.font.Font(None,80)
    txt = fonto.render("game over",
                       True,(255,255,255))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0


        tmr += 1
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
                print(mv)
                for ad,srf in alufa.items():
                    if ad == mv:
                        kk_img = srf
        if check_dound(screen.get_rect(),kk_rct) != (True,True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0],-mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        avx ,avy = vx*accs[min(tmr//1000,9)], vy*accs[min(tmr//1000,9)] # 追加機能１
        bb_rct.move_ip(avx, avy)
        yoko,tate = check_dound(screen.get_rect(),bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):  #追加機能３
            screen.blit(txt,[300,200])
        pg.display.update()
        if kk_rct.colliderect(bb_rct):
            time.sleep(5)  # 追加機能３
            return

        
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()