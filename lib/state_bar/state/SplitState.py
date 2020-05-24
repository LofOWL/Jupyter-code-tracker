


gap_v = 10
gap_h = 20

height = 100
width = 90

line_width =  15
line_height = 15

class SplitState:


    def __init__(self,parent):
        self.parent = parent
        self.data = self.parent.splitdata

        self.create()


    def create(self):

        # coordiante
        self.x1 = self.parent.x1
        self.y1 = self.parent.y1
        self.x2 = self.x1 + width
        if len(self.data) != 0:
            self.y2 = self.y1 + gap_v * (len(self.data))+ 10 * (len(self.data)) + line_height * sum([len(i[1]) for i in self.data]) + 10 * sum([len(i[1]) for i in self.data])
        else:
            self.y2 = self.y1 + 10
        self.parent.vs.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="white")

        #create line
        line = []
        start_y1 = self.y1
        for data in self.data:
            line = self.Line(self,start_y1,data)
            line.create()
            start_y1 = line.end_y + 10



    class Line:


        def __init__(self,parent,start_y1,data):
            self.parent = parent

            self.data = data

            self.x1 = self.parent.x1 + gap_h
            self.y1 = start_y1 + gap_v

        def create(self):

            # first
            first_x1 = self.x1
            first_y1 = self.y1
            first_x2 = first_x1 + line_width
            first_y2 = first_y1 + line_height
            self.parent.parent.vs.create_rectangle(first_x1,first_y1,first_x2,first_y2,fill="white")

            #index
            index_text_x = first_x1 + line_width // 2
            index_text_y = first_y1 + line_height // 2
            self.parent.parent.vs.create_text(index_text_x,index_text_y,font=("Purisa",10),anchor='c',text=self.data[0])

            #parent_index
            start_y1 = self.y1

            for parent_block in self.data[1]:
                parent_x1 = first_x2 + gap_h
                parent_y1 = start_y1
                parent_x2 = parent_x1 + line_width
                parent_y2 = parent_y1 + line_height
                self.parent.parent.vs.create_rectangle(parent_x1,parent_y1,parent_x2,parent_y2,fill="red")

                #index
                index_text_x = parent_x1 + line_width // 2
                index_text_y = parent_y1 + line_height // 2
                self.parent.parent.vs.create_text(index_text_x,index_text_y,font=("Purisa",10),anchor='c',text=parent_block)

                #create lines
                first_mid_y = (first_y1 + first_y2) // 2

                parent_mid_y = (parent_y1 + parent_y2) // 2
                self.parent.parent.vs.create_line(first_x2,first_mid_y,parent_x1,parent_mid_y,fill="black",width=1)
                start_y1 = parent_y2 + 10

            self.end_y = start_y1
