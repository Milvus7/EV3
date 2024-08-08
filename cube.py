
class Colors: 
    WHITE = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    ORANGE = 4
    GREEN = 5
    
#  w
#g r b o
#  y
#r er front
#  0
#5 1 2 4
#  3
#          +--------+
#          |0  1  2 |
#          |3  4  5 |
#          |6  7  8 |
# +--------+--------+--------+--------+
# |45 46 47|9  10 11|18 19 20|36 37 38|
# |48 49 50|12 13 14|21 22 23|39 40 41|
# |51 52 53|15 16 17|24 25 26|42 43 44|
# +--------+--------+--------+--------+
#          |27 28 29|
#          |30 31 32|
#          |33 34 35|
#          +--------+

#returns a list rotated by 90 deg clockwise n times 
def rotate_list(inn_list, rotations):
    out_list = inn_list
    for _ in range(rotations):
        out_list = [list(row) for row in zip(*reversed(out_list))]
    return out_list

class Cube():
    def __init__(self):
        self.cube = [0]*(9*6)
        for i in range(6):
            for j in range(9):
                self.cube[i*9+j] = i
    
    #face = 3*3 matrix (assumed, pls be correct)
    #face_above = int 0-5
    #sets the corresponding face of the cube (looks at centre of face (1, 1) to see witch face to edit)
    def insert_face(self, face, above_color: int):
        my_color = face[1][1]
        #rotate face to face correct direction
        face = self.rotate_towards_face(face, above_color)
        #un-nest it
        face = sum(face, [])
        
        #insert it into the cube
        self.cube[my_color*9:(my_color+1)*9]
        
       
        
    def rotate_towards_face(self, face, above_color: int):    
        my_color = face[1][1]
        #cant rotate towards itself
        if above_color == my_color:
            raise "Cant rotate face towards itself: " + above_color
        #cant rotate to opposite face
        if (my_color+3)%6 == my_color:
            raise "Cant rotate to opposite face: " + my_color + " and opposite: " + (my_color+3)%6
            
        if my_color == Colors.YELLOW: 
            #1=>0
            #2=>1
            #4=>2
            #5=>3   
            above_color -= 1
            if above_color > 2:
                above_color -= 1
                
            return rotate_list(face, above_color)
        
        if my_color == Colors.WHITE:
            #1=>2
            #2=>1
            #4=>0
            #5=>3   
            if above_color > 3:
                above_color -= 1
            my_face = (4-my_face+3)%4
            
            return rotate_list(face, above_color)
            
        #0 needs no change
        if my_color == Colors.WHITE:
            return face
        
        #yellow always needs a 180 rotation
        if above_color == Colors.YELLOW:
            return rotate_list(face, 2)
        
        #you must at this point rotate at least once
        rotate_list(face, 1)
        
        #blue and orange has a pattern that i exploit here
        if (my_color == Colors.BLUE or my_color == Colors.ORANGE) and above_color < my_color:
            return rotate_list(face, 2)
        
        if (my_color == Colors.RED and above_color == Colors.GREEN):
            return rotate_list(face, 2)
        
        if (my_color == Colors.GREEN and above_color == Colors.ORANGE):
            return rotate_list(face, 2)
        
        #needed only one rotation
        return face
        
            
    def __str__(self):
        out ="      +-----+\n"
        out+="      |" + str(self.cube[0 ]) + " " + str(self.cube[1 ]) + " " + str(self.cube[2 ])+"|\n"
        out+="      |" + str(self.cube[3 ]) + " " + str(self.cube[4 ]) + " " + str(self.cube[5 ])+"|\n"
        out+="      |" + str(self.cube[6 ]) + " " + str(self.cube[7 ]) + " " + str(self.cube[8 ])+"|\n"
        out+="+-----+-----+-----+-----+\n"
        
        out+="|" + str(self.cube[45]) + " " + str(self.cube[46]) + " " + str(self.cube[47])+"|" + str(self.cube[9 ]) + " " + str(self.cube[10]) + " " + str(self.cube[11])+"|"
        out+=str(self.cube[18]) + " " + str(self.cube[19]) + " " + str(self.cube[20])+"|" + str(self.cube[36]) + " " + str(self.cube[37]) + " " + str(self.cube[38])+"|\n"

        out+="|" + str(self.cube[48]) + " " + str(self.cube[49]) + " " + str(self.cube[50])+"|" + str(self.cube[12]) + " " + str(self.cube[13]) + " " + str(self.cube[14])+"|"
        out+=str(self.cube[21]) + " " + str(self.cube[22]) + " " + str(self.cube[23])+"|" + str(self.cube[39]) + " " + str(self.cube[40]) + " " + str(self.cube[41])+"|\n"

        out+="|" + str(self.cube[51]) + " " + str(self.cube[52]) + " " + str(self.cube[53])+"|" + str(self.cube[15]) + " " + str(self.cube[16]) + " " + str(self.cube[17])+"|"
        out+=str(self.cube[24]) + " " + str(self.cube[25]) + " " + str(self.cube[26])+"|" + str(self.cube[42]) + " " + str(self.cube[43]) + " " + str(self.cube[44])+"|\n"

        out+="+-----+-----+-----+-----+\n"
        out+="      |" + str(self.cube[27]) + " " + str(self.cube[28]) + " " + str(self.cube[29])+"|\n"
        out+="      |" + str(self.cube[30]) + " " + str(self.cube[31]) + " " + str(self.cube[32])+"|\n"
        out+="      |" + str(self.cube[33]) + " " + str(self.cube[34]) + " " + str(self.cube[35])+"|\n"
        out+="      +-----+"
        return out
    
    #example: "l r2 f'"
    def do_sequence(self, sequence):
        sequence = sequence.split(" ")
        for i in range(len(sequence)):
            face = -1
            dir = 1
            
            #replacement match case
            match_str = sequence[i][0].lower()
            if match_str == "f":
                face = 1
            elif match_str == "r":
                face = 2
            elif match_str == "l":
                face = 5
            elif match_str == "u":
                face = 0
            elif match_str == "d":
                face = 3
            elif match_str == "b":
                face = 4
            else:
                raise "ERROR in sequence: " + sequence[i]
            
            if (len(sequence[i]) == 2):
                #replacement match case
                if sequence[i][1:] == "'":
                    dir = -1
                elif sequence[i][1:] == "2":
                    dir = 2
                else:
                    raise "ERROR in sequence: " + sequence[i]
            
            self.rotate_face(face, dir)

    def rotate_face(self, face, dir=1):
    #1 is clockwise
    #-1 is counterclockwise 
    #2 is twice
        self.rotate_pieces(face*9, face*9+2, face*9+8, face*9+6, dir)
        self.rotate_pieces(face*9+1, face*9+5, face*9+7, face*9+3, dir)
        
        #replacement match case
        if face == 0:
            for i in range(3):
                self.rotate_pieces(9+i, 45+i, 36+i, 18+i, dir)
        elif face == 1:
            for i in range(3):
                self.rotate_pieces(6+i, 18+3*i, 29-i, 53-3*i, dir)
        elif face == 2: 
            for i in range(3):
                self.rotate_pieces(8-3*i, 36+3*i, 35-3*i, 17-3*i, dir)
        elif face == 3: 
            for i in range(3):
                self.rotate_pieces(51+i, 15+i, 24+i, 42+i, dir)
        elif face == 4:
            for i in range(3):
                self.rotate_pieces(2-i, 45+3*i, 33+i, 26-3*i, dir)
        elif face == 5:
            for i in range(3):
                self.rotate_pieces(3*i, 9+3*i, 27+3*i, 44-3*i, dir)
        else:
            raise "Unknown face "+face
            
    
    def is_valid(self): #checks if cube is a valid cube in a simple manner to see if scan was correct
        for i in range(6):
            #centers are correct
            if (self.cube[i*9+4] != i):
                return False
            
            if (self.cube.count(i) != 9):
                return False
                     
        return True
    


    def rotate_pieces(self, a, b, c, d, dir): #rotates the four 
    #1 is clockwise
    #-1 is counterclockwise
    #2 is twice
        temp = self.cube[a]
        if dir == -1:
            self.cube[a] = self.cube[b]
            self.cube[b] = self.cube[c]
            self.cube[c] = self.cube[d]
            self.cube[d] = temp
        elif dir == 1:
            self.cube[a] = self.cube[d]
            self.cube[d] = self.cube[c]
            self.cube[c] = self.cube[b]
            self.cube[b] = temp
        elif dir == 2:
            self.cube[a] = self.cube[c]
            self.cube[c] = temp
            temp = self.cube[b]
            self.cube[b] = self.cube[d]
            self.cube[d] = temp
        else:
            raise "Unknown direction: "+dir
    
    #TODO
    def simple_solve(self):
        temp_cube = Cube()
        temp_cube.cube = self.cube.copy()
        out_moves = []
        white_edges = []
        for i in range(len(self.cube)):
            if (i%9%2 != 1): continue
            if self.cube[i] == 0:
                white_edges.append(i)
        
        if (len(white_edges) != 4): raise "incorrect number of edges: " + len(white_edges)        
        
        #correct top edge, most important so done first
        for edge in white_edges:
            if (edge >= 9):
                temp_cube.rotate_face(out_moves[-1], 2)
                continue
            
            #replacement match case
            if edge%9 == 1:
                out_moves.append(1)
            elif edge%9 == 3:
                out_moves.append(5)
            elif edge%9 == 5:
                out_moves.append(2)
            elif edge%9 == 7:
                out_moves.append(4)
            else:
                raise "HELP SOMETHING WENT HORRIBLY WRONG"
                    
                
            
        #print(temp_cube)
        return out_moves

#cube = Cube()
#cube.cube = [0, 2, 0, 0, 0, 4, 0, 5, 0, 2, 0, 5, 4, 1, 1, 5, 3, 2, 1, 3, 4, 3, 2, 1, 4, 0, 1, 3, 2, 3, 5, 3, 4, 3, 5, 3, 5, 0, 2, 2, 4, 5, 2, 3, 5, 4, 1, 1, 1, 5, 2, 1, 4, 4]
#print(cube)
#cube.simple_solve
#print(cube.simple_solve())