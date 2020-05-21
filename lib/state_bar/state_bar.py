

from lib.state_bar.TypeChecker import MapBlock
from lib.state_bar.state.MapState import MapState
from lib.state_bar.state.SplitState import SplitState
from lib.state_bar.state.MergeState import MergeState

height =  150
width = 150

class StateBar:


    def __init__(self,**kwg):
        # vs
        self.vs = kwg["vs"]

        # mapping filter
        self.mp = kwg["mp"]
        self.mapblock = None

        # coordinate
        self.x1 = kwg["x1"]
        self.y1 = 10
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height


        # self.vs.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="blue")

        # generate the map block
        self._generate()

        # generate the map
        self.mapstate = MapState(self)

        # generate the split
        self.splitstate = SplitState(self)

        # generate the merge
        self.mergestate = MergeState(self)


    def _generate(self):
        self.mapblock = MapBlock(self.mp.formatData())
