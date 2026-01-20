

class Animation:

    def __init__(self,name,speed,animation):
        self.name=name
        self.speed=speed
        self.animation=animation
        self.currentframe=animation[0]
        self.framesIndex=0
        self.wait=0

    def play(self,dt):

        if self.wait<=0:
            self.framesIndex=(self.framesIndex+1)%len(self.animation)
            self.currentframe=self.animation[self.framesIndex]
            self.wait=1/self.speed
        else:
            self.wait-=dt

    def reset(self):
        self.wait = 0
        self.framesIndex = 0
        self.currentframe = self.animation[0]
