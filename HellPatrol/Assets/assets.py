import pygame

class Assets:
    images = {}
    animations = {}

    @staticmethod
    def loadImages():

        Assets.images["player"] = pygame.image.load("Assets/Images/Player/hellPlayerMG.png").convert_alpha()
        Assets.images["playershortbullet"] = pygame.image.load("Assets/Images/Bullets/PlayerBullets/smallbullet.png").convert_alpha()
        Assets.images["playerlongbluebullet"] = pygame.image.load("Assets/Images/Bullets/PlayerBullets/longbluebullet.png").convert_alpha()
        Assets.images["playerwidebullet"] = pygame.image.load("Assets/Images/Bullets/PlayerBullets/widebullet.png").convert_alpha()
        Assets.images["playersquaredbullet"] = pygame.image.load("Assets/Images/Bullets/PlayerBullets/squaredbullet.png").convert_alpha()
        Assets.images["playerfirebullet"] = pygame.image.load("Assets/Images/Bullets/PlayerBullets/firebullet.png").convert_alpha()
        Assets.images["hellTile11"]=pygame.image.load("Assets/Images/Tiles/hellTile1-1.png").convert_alpha()
        Assets.images["hellTile12"]=pygame.image.load("Assets/Images/Tiles/hellTile1-2.png").convert_alpha()
        Assets.images["hellTile13"]=pygame.image.load("Assets/Images/Tiles/hellTile1-3.png").convert_alpha()
        Assets.images["hellTile21"]=pygame.image.load("Assets/Images/Tiles/hellTile2-1.png").convert_alpha()
        Assets.images["hellTile22"]=pygame.image.load("Assets/Images/Tiles/hellTile2.png").convert_alpha()
        Assets.images["hellTile31"]=pygame.image.load("Assets/Images/Tiles/hellTile3-1.png").convert_alpha()
        Assets.images["hellTile32"]=pygame.image.load("Assets/Images/Tiles/hellTile3.png").convert_alpha()
        Assets.images["hellGrateS1"]=pygame.image.load("Assets/Images/Tiles/hellGrateS1.png").convert_alpha()
        Assets.images["hellVent1"]=pygame.image.load("Assets/Images/Tiles/hellVent1.png").convert_alpha()
        Assets.images["hellVent2"]=pygame.image.load("Assets/Images/Tiles/hellVent2.png").convert_alpha()

        Assets.images["walkB"] = pygame.image.load("Assets/Images/Player/WalkAnimation/Body/playerWalkB-0.png").convert_alpha()
        Assets.images["walkH"] = pygame.image.load("Assets/Images/Player/WalkAnimation/Head/playerWalkH-0.png").convert_alpha()
        Assets.images["gun"] = pygame.image.load("Assets/Images/Player/Guns/MachineGun/machinegun-0.png").convert_alpha()
        Assets.images["crosshair1"] = pygame.image.load("Assets/Images/Reticles/Reticle2/crosshairSquare.png").convert_alpha()


    @staticmethod
    def loadAnimations():

        Assets.animations["playerIdleB"] = [
            pygame.image.load(f"Assets/Images/Player/WalkAnimation/Body/playerWalkB-{i}.png").convert_alpha() for i in range(1)
        ]

        Assets.animations["playerIdleH"] = [
            pygame.image.load(f"Assets/Images/Player/WalkAnimation/Head/playerWalkH-{i}.png").convert_alpha() for i in range(1)
        ]

        Assets.animations["playerWalkB"] = [
            pygame.image.load(f"Assets/Images/Player/WalkAnimation/Body/playerWalkB-{i}.png").convert_alpha() for i in range(3)
        ]

        Assets.animations["playerWalkH"] = [
            pygame.image.load(f"Assets/Images/Player/WalkAnimation/Head/playerWalkH-{i}.png").convert_alpha() for i in range(3)
        ]

        Assets.animations["playerMGInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/MachineGun/machinegun-{i}.png").convert_alpha() for i in range(3)
        ]

        Assets.animations["playerMGNotInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/MachineGun/machinegun-2.png").convert_alpha()
        ]

        Assets.animations["playerSPInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/Sniper/sniper-{i}.png").convert_alpha() for i in range(3)
        ]

        Assets.animations["playerSPNotInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/Sniper/sniper-2.png").convert_alpha()
        ]

        Assets.animations["playerSGInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/Shotgun/shotgun-{i}.png").convert_alpha() for i in range(3)
        ]

        Assets.animations["playerSGNotInCombat"] = [
            pygame.image.load(f"Assets/Images/Player/Guns/Shotgun/shotgun-2.png").convert_alpha()
        ]