import pygame
import random as r
import mysql.connector as sql

pygame.init()
dispscore = sql.connect(
        host = "localhost",
        database = "pongscore",
        user = "raunak",
        password = "109169420" 
)
cursor = dispscore.cursor()

maxvel = float(input("Enter max velocity: "))
mscore = int(input("First to _ wins: "))

#initial ball velocity vector randomiser
def velrandom(m):
    velrx = r.uniform(m/2, m)  # Random float between 0 and m
    velry = (m**2 - velrx**2)**0.5
    rvelt = (velrx, velry)
    return rvelt

#scoreboard
def scorein(player1, player2, winner):
    scoresdb = sql.connect(
        host = "localhost",
        database = "pongscore",
        user = "raunak",
        password = "109169420" 
    )

    cursor = scoresdb.cursor()
    sql_insert_query = """INSERT INTO scores (player1, player2, winner) 
                          VALUES (%s, %s, %s)"""
    cursor.execute(sql_insert_query, (player1, player2, winner))
    scoresdb.commit()
    print("Scores inserted")

    cursor.close()
    scoresdb.close()

#constants
width, height  = 1000, 600
white = (200, 200, 200)
black = (0, 0, 0)
p1 = p2 = 0
font = pygame.font.SysFont("callibri", 64)
font2 = pygame.font.SysFont("callibri", 32)
wn = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")
run = True

#ball constants
radius = 14
ballx, bally = float(width/2 - radius/2), float(height/2 - radius/2)
bvelx = bvely = maxvel / (2**(1/2))

#paddle constants
pw, ph = 10, 120
lpy = rpy = height/2 - ph/2
lpx, rpx = 20 - pw/2, width - (30 - pw/2)
lpvel, rpvel = 0, 0

#game loop
while run:
        wn.fill(black)
        for i in pygame.event.get():
                if i.type == pygame.QUIT:
                        run = False
                        print("Pong closed")
                elif i.type == pygame.KEYDOWN:
                        if i.key ==  pygame.K_UP:
                                rpvel = -1
                        if i.key == pygame.K_DOWN:
                                rpvel = 1
                        if i.key == pygame.K_w:
                                lpvel = -1
                        if i.key == pygame.K_s:
                                lpvel = 1
                elif i.type == pygame.KEYUP:
                        lpvel, rpvel = 0, 0

        #always true
        if ballx <= 0:
                p2 += 1
                wzr = velrandom(maxvel)
                quadrant = r.choice([1,2])
                if quadrant == 1:
                        bvelx, bvely = wzr[0], wzr[1]
                elif quadrant == 2:
                        bvelx, bvely = wzr[0], -wzr[1]

                ballx, bally = width/2 - radius/2, height/2 - radius/2

        if ballx + radius >= 1000:
                p1 += 1
                wzr = velrandom(maxvel)
                quadrant = r.choice([1,2])

                if quadrant == 1:
                        bvelx, bvely = - wzr[0], wzr[1]
                elif quadrant == 2:
                        bvelx, bvely = - wzr[0], -wzr[1]

                ballx, bally = width/2 - radius/2, height/2 - radius/2

        if bally <= 0:
                bvely = -bvely
        if bally + radius >= 600:
                bvely = -bvely
        else:
                None

        integralballx = ballx//1
        integralbally = bally//1

        #paddle constraints
        if lpy <= 0:
                lpy = 0
        if lpy >= height - ph:
                lpy = height - ph
        if rpy <= 0:
                rpy = 0
        if rpy >= height - ph:
                rpy = height - ph

        #kinematic constants
        ballx += bvelx
        bally += bvely

        rpy += rpvel
        lpy += lpvel

        #collisions
        if lpx <= ballx <= lpx + pw:
                if lpy <= bally <= lpy + ph or lpy <= bally + radius <= lpy + ph:
                        ballx = lpx + pw
                        bvelx *= 1.06
                        bvely *= 1.06
                        bvelx = (-bvelx)

        if rpx <= ballx <= rpx + pw:
                if rpy <= bally <= rpy + ph or rpy <= bally + radius <= rpy + ph:
                        ballx = rpx
                        bvelx *= 1.06
                        bvely *= 1.06
                        bvelx = (-bvelx)

        #scoreboard
        score = font.render(str(p1) + "    " + str(p2) , True, white)
        wn.blit(score, (450, 25))

        #entities
        pygame.draw.rect(wn, (100,50,50), pygame.Rect(width/2, 0, 5, 600))
        pygame.draw.rect(wn, white, pygame.Rect(integralballx, integralbally, radius, radius))
        pygame.draw.rect(wn, white, pygame.Rect(rpx, rpy, pw, ph))
        pygame.draw.rect(wn, white, pygame.Rect(lpx, lpy, pw, ph))

        pygame.display.update()

        if p1 == mscore:
                wn.fill(black)
                scorein(p1, p2, "Left")

                for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                                run = False
                                print("Pong closed")
                enscrn = font2.render(("Game over, Left Wins " + str(p1) + ":" + str(p2) + " Press space to restart or TAB to view scoreboard"), True, white)
                wn.blit(enscrn, (100, 300))
                pygame.display.update()
                run2 = True
                while run2:
                        for i in pygame.event.get():
                                if i.type == pygame.KEYDOWN:
                                        if i.key == pygame.K_TAB:
                                                cursor.execute("select * from scores")
                                                for x in cursor:
                                                        print(x)
                                        if i.key ==  pygame.K_SPACE:
                                                p1 = p2 = 0
                                                run2 = False
                                if i.type == pygame.QUIT:
                                        run = False
                                        run2 = False

        if p2 == mscore:
                wn.fill(black)
                scorein(p1, p2, "Right")

                for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                                run = False
                                print("Pong closed")
                enscrn = font2.render(("Game over, Right Wins " + str(p1) + ":" + str(p2) + " Press space to restart or TAB to view scoreboard"), True, white)
                wn.blit(enscrn, (100, 300))
                pygame.display.update()
                run2 = True
                while run2:
                        for i in pygame.event.get():
                                if i.type == pygame.KEYDOWN:
                                        if i.key == pygame.K_TAB:
                                                cursor.execute("select * from scores")
                                                for x in cursor:
                                                        print(x)
                                        if i.key ==  pygame.K_SPACE:
                                                p1 = p2 = 0
                                                run2 = False
                                if i.type == pygame.QUIT:
                                        run = False
                                        run2 = False