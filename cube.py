


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


class Cube():
    def __init__(self):
        self.cube = [0]*(9*6)
        for i in range(6):
            for j in range(9):
                self.cube[i*9+j] = i
    
    def __str__(self):
        return f"""      +-----+
      |{self.cube[0]} {self.cube[1]} {self.cube[2]}|
      |{self.cube[3]} {self.cube[4]} {self.cube[5]}|
      |{self.cube[6]} {self.cube[7]} {self.cube[8]}|
+-----+-----+-----+-----+
|{self.cube[45]} {self.cube[46]} {self.cube[47]}|{self.cube[9]} {self.cube[10]} {self.cube[11]}|{self.cube[18]} {self.cube[19]} {self.cube[20]}|{self.cube[36]} {self.cube[37]} {self.cube[38]}|
|{self.cube[48]} {self.cube[49]} {self.cube[50]}|{self.cube[12]} {self.cube[13]} {self.cube[14]}|{self.cube[21]} {self.cube[22]} {self.cube[23]}|{self.cube[39]} {self.cube[40]} {self.cube[41]}|
|{self.cube[51]} {self.cube[52]} {self.cube[53]}|{self.cube[15]} {self.cube[16]} {self.cube[17]}|{self.cube[24]} {self.cube[25]} {self.cube[26]}|{self.cube[42]} {self.cube[43]} {self.cube[44]}|
+-----+-----+-----+-----+
      |{self.cube[27]} {self.cube[28]} {self.cube[29]}|
      |{self.cube[30]} {self.cube[31]} {self.cube[32]}|
      |{self.cube[33]} {self.cube[34]} {self.cube[35]}|
      +-----+"""
    
    #example: "l r2 f'"
    def do_sequence(self, sequence):
        sequence = sequence.split(" ")
        for i in range(len(sequence)):
            face = -1
            dir = 1
            match sequence[i][0].lower():
                case "f":
                    face = 1
                case "r":
                    face = 2
                case "l":
                    face = 5
                case "u":
                    face = 0
                case "d":
                    face = 3
                case "b":
                    face = 4
                case _:
                    raise "ERROR in sequence: " + sequence[i]
            
            if (len(sequence[i]) == 2):
                match sequence[i][1:]:
                    case "'":
                        dir = -1
                    case "2":
                        dir = 2
                    case _:
                        raise "ERROR in sequence: " + sequence[i]
            
            self.rotate_face(face, dir)

    def rotate_face(self, face, dir=1):
    #1 is clockwise
    #-1 is counterclockwise 
    #2 is twice
        self.rotate_pieces(face*9, face*9+2, face*9+8, face*9+6, dir)
        self.rotate_pieces(face*9+1, face*9+5, face*9+7, face*9+3, dir)
        match face:
            case 0:
                for i in range(3):
                    self.rotate_pieces(9+i, 45+i, 36+i, 18+i, dir)
            case 1:
                for i in range(3):
                    self.rotate_pieces(6+i, 18+3*i, 29-i, 53-3*i, dir)
            case 2: 
                for i in range(3):
                    self.rotate_pieces(8-3*i, 36+3*i, 35-3*i, 17-3*i, dir)
            case 3: 
                for i in range(3):
                    self.rotate_pieces(51+i, 15+i, 24+i, 42+i, dir)
            case 4:
                for i in range(3):
                    self.rotate_pieces(2-i, 45+3*i, 33+i, 26-3*i, dir)
            case 5:
                for i in range(3):
                    self.rotate_pieces(3*i, 9+3*i, 27+3*i, 44-3*i, dir)
            case _:
                raise f"Unknown face {face}"
            
    
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
            raise f"Unknown direction: {dir}"
        
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
            match edge%9:
                case 1:
                    out_moves.append(1)
                case 3:
                    out_moves.append(5)
                case 5:
                    out_moves.append(2)
                case 7:
                    out_moves.append(4)
                case _:
                    raise "HELP SOMETHING WENT HORRIBLY WRONG"
                    
                
            
        print(temp_cube)
        return out_moves

cube = Cube()
cube.cube = [0, 2, 0, 0, 0, 4, 0, 5, 0, 2, 0, 5, 4, 1, 1, 5, 3, 2, 1, 3, 4, 3, 2, 1, 4, 0, 1, 3, 2, 3, 5, 3, 4, 3, 5, 3, 5, 0, 2, 2, 4, 5, 2, 3, 5, 4, 1, 1, 1, 5, 2, 1, 4, 4]
print(cube)
cube.simple_solve
print(cube.simple_solve())