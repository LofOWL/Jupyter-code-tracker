

class MapState:


    def __init__(self,parent):
        self.total,self.total_100,self.total_90 = parent.mapblock.type_total()


    def create(self):


        # coordinate
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
