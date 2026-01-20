
class ControlAnimation:
    
    def __init__(self,animations):
        self.animations={}

        for animation in animations:
            self.animations[animation.name]=animation
        self.current=animations[0]

    def switchTo(self,name):
        if self.current.name != name:
            self.current = self.animations[name]
            self.current.reset()
    
    def playCurrent(self,dt):
        self.current.play(dt)
    
    def currentImage(self):
        return self.current.currentframe