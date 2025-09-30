import os
import sys
import pygame as pg
import time
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, 5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(5, 0)}


def check_bound(rct: pg.Rect) -> tuple[bool, bool] :
    """
    引数: こうかとんRect or 爆弾Rect
    戻り値: 横・縦の真理値タプル(True: 画面内/ False: 画面外)
    """
    tate, yoko = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 左右にはみ出たら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 上下にはみ出たら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    引数: gameover画面を表示するSurface
    戻り値: なし 
    動作: gameover画面を表示する関数
    """
    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, (0, 0, 0), (100,100,50,50))  # 黒色の矩形を生成
    gg_img.set_alpha(180)  # 矩形の透明度を指定
    gg_img_rct=gg_img.get_rect()
    gg_img_rct.center=WIDTH/2,HEIGHT/2 #screenの中央に配置
    
    gg_font = pg.font.Font(None, 80)  # fontサイズ80のインスタンスを生成
    gg_txt = gg_font.render("Game Over", True, (255, 255, 255))  # 白色の文字を付与
    gg_img.blit(gg_txt, [400, 300])
    
    kk_cry_img=pg.image.load("./fig/8.png")
    gg_img.blit(kk_cry_img, (350, 300))
    gg_img.blit(kk_cry_img, (725, 300))
    
    screen.blit(gg_img, gg_img_rct)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数: なし
    戻り値: 2つの要素を持つタプル(サイズの異なる爆弾の画像のリスト, 1から10までの整数が格納されたリスト)
    動作: サイズの異なる爆弾の画像を生成しリストに格納、加速度を格納したリストを生成、以上2つを渡す。
    """
    bb_accs = [i for i in range(1, 11)]
    bb_imgs=[0 for i in range(10)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs[r-1] = bb_img
    return (bb_imgs, bb_accs)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()
    #bb_img = pg.Surface((20, 20))  # 爆弾描写用の画像
    #pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾を描写
    #bb_img.set_colorkey((0, 0, 0))  # 背景を透過
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾のX座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾のy座標
    vx = 5  # 爆弾の横方向移動速度
    vy = 5  # 爆弾の縦方向移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            pg.display.update()
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]==1:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  # 横移動を反転
        if not tate:
            vy *= -1  # 縦移動を反転
        bb_img = bb_imgs[min(tmr//500, 9)]  # 500フレームごとにリスト内にある画像を切り替える
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        avx = vx*bb_accs[min(tmr//500, 9)]  # 500フレームごとに基本速度に加速係数を掛ける
        avy = vy*bb_accs[min(tmr//500, 9)]  
        
        tmr += 1
        bb_rct.move_ip(avx, avy)  # 爆弾移動
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
