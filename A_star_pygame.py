import pygame
from pygame.locals import *
from queue import PriorityQueue

pygame.init() 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("A* Algorithm Visualization")
# ROWS = int(input('Enter the number of rows : '))
ROWS = 25
# COLUMNS = int(input('Enter the column : '))
COLUMNS = ROWS

# Color 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 168, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AQUA = (128, 255, 255)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)

#Class 
class Node():
    def __init__(self,row,col,width,height,total_rows,total_cols):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.x = col * width
        self.y = row * height
        self.total_cols = total_cols
        self.total_rows = total_rows
        self.color = WHITE
        self.neighbors = []

    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.height))

    def get_neighbors(self,grid):
        # top node
        if self.row>0:
            node = grid[self.row-1][self.col]
            if not node.is_barrier_node():
                self.neighbors.append(node)
            """if self.col>0:
                node = grid[self.row-1][self.col-1]
                if not node.is_barrier_node():
                    self.neighbors.append(node)
            if self.col < self.total_cols - 1:
                node = grid[self.row-1][self.col+1]
                if not node.is_barrier_node():
                    self.neighbors.append(node)"""

        # down node
        if self.row < self.total_rows - 1:
            node = grid[self.row+1][self.col]
            if not node.is_barrier_node():
                self.neighbors.append(node)
            """if self.col>0:
                node = grid[self.row+1][self.col-1]
                if not node.is_barrier_node():
                    self.neighbors.append(node)
            if self.col < self.total_cols - 1:
                node = grid[self.row+1][self.col+1]
                if not node.is_barrier_node():
                    self.neighbors.append(node)"""

        # left node
        if self.col>0:
            node = grid[self.row][self.col-1]
            if not node.is_barrier_node():
                self.neighbors.append(node)

        # right node
        if self.col < self.total_cols - 1:
            node = grid[self.row][self.col+1]
            if not node.is_barrier_node():
                self.neighbors.append(node)

    def make_white(self):
        self.color = WHITE
    
    def make_open(self):
        self.color = RED

    def make_path(self):
        self.color = GREEN
    
    def make_blue(self):
        self.color = BLUE

    def make_start_node(self):
        self.color = ORANGE

    def make_yellow(self):
        self.color = YELLOW

    def make_barrier_node(self):
        self.color = BLACK

    def make_goal_node(self):
        self.color = AQUA

    def make_grey(self):
        self.color = GREY
    
    def make_purple(self):
        self.color = PURPLE

    def isWhite(self):
        return self.color == WHITE
    
    def isOpened(self):
        return self.color == RED
    
    def isPath(self):
        return self.color == GREEN
    
    def isBlue(self):
        return self.color == BLUE
    
    def is_start_node(self):
        return self.color == ORANGE
    
    def isYellow(self):
        return self.color == YELLOW
    
    def is_barrier_node(self):
        return self.color == BLACK
    
    def is_goal_node(self):
        return self.color == AQUA
    
    def isGrey(self):
        return self.color == GREY
    
    def isPurple(self):
        return self.color == PURPLE
    
    def makeStartNode(self):
        self.make_start_node()

    def makeEndNode(self):
        self.make_goal_node()

    def makeBarrier(self):
        self.make_barrier_node()

def draw_grid(window,rows,columns,screen_width,screen_height):
    gapy = screen_width // rows
    gapx = screen_height // columns
    for i in range(rows):
        pygame.draw.line(window,GREY,(0,i*gapy),(screen_width,i*gapy))
        for j in range(columns):
            pygame.draw.line(window,GREY,(j*gapx,0),(j*gapx,screen_height))

def draw(window,grid,rows,columns,screen_width,screen_height):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)
    draw_grid(window,rows,columns,screen_width,screen_height)
    pygame.display.update()

def make_grid(screenWidth, screenHeight,rows,columns):
    grid = []
    node_width = screenWidth // columns
    node_height = screenHeight // rows
    for i in range(rows):
        row = []
        for j in range(columns):
            node = Node(i,j,node_width,node_height,rows,columns)
            row.append(node)
        grid.append(row)
    return grid

def getNodeRW(pos,rows,cols,screen_width,screen_height):
    gapRow = screen_height // rows
    gapCol = screen_width // cols
    x,y = pos
    col,row = x//gapCol , y//gapRow
    return row , col

def h_value(node,end):
    goalx , goaly = end.col , end.row
    nodex , nodey = node.col , node.row
    return abs(goalx-nodex) + abs(goaly-nodey)

def draw_final_path(window, grid,rows,cols,screen_width,screen_height,final_path,node):
    print("Final path found")
    while node in final_path:
        node.make_path()
        node = final_path[node]
    draw(window, grid,rows,cols,screen_width,screen_height)

def A_start_algo(window,grid,rows,cols,start,end,screen_width,screen_height):
    pQueue = PriorityQueue()
    g_value = {}
    order = 0
    f_value = {}
    final_path = {}
    for row in grid:
        for node in row:
            g_value[node] = float("inf")
            f_value[node] = float("inf")
    g_value[start]=0
    f_value[start]=h_value(start,end)
    pQueue.put((f_value[start],h_value(start,end),order,start))
    simpal_queue = {start}

    while not pQueue.empty():
        node = pQueue.get()[3]

        if node==end:
            draw_final_path(window, grid,rows,cols,screen_width,screen_height,final_path,node)
            end.make_goal_node()
            start.make_start_node()
            return True
        
        for neighbor in node.neighbors:
            g_value_temp = g_value[node]+1

            if g_value_temp < g_value[neighbor]:
                h = h_value(neighbor,end)
                g = g_value_temp
                f = h+g
                g_value[neighbor]=g
                f_value[neighbor]=f
                final_path[neighbor]=node
                if neighbor not in simpal_queue:
                    simpal_queue.add(neighbor)
                    order+=1
                    neighbor.make_open()
                    pQueue.put((f,h,order,neighbor))
            draw(window, grid,rows,cols,screen_width,screen_height)
        
    return False

def BFS(window,grid,rows,cols,start,end,screen_width,screen_height):
    visited = []
    opened = []
    final_path = {}
    opened.append(start)
    visited.append(start)
    while opened:
        node=opened.pop(0)
        if node==end:
            draw_final_path(window, grid,rows,cols,screen_width,screen_height,final_path,node)
            return True
        for neighbor in node.neighbors:
            if neighbor not in visited:
                opened.append(neighbor)
                visited.append(neighbor)
                neighbor.make_open()
                final_path[neighbor]=node
        draw(window, grid,rows,cols,screen_width,screen_height)
    return False

visited = []
final_path = {}

def DFS(window,grid,rows,cols,start,end,screen_width,screen_height):
    global visited
    if start==end:
        print("get")
        return True
    if start not in visited:
        visited.append(start)
        for child in start.neighbors:
            child.make_open()
            DFS(window,grid,rows,cols,child,end,screen_width,screen_height)
        draw(window, grid,rows,cols,screen_width,screen_height)
    return False

def DLS(window,grid,rows,cols,node,end,screen_width,screen_height,level,maxLevel,path):
    global final_path
    path.append(node)
    if node==end:
        print("get")
        return True
    if level==maxLevel:
        return False
    for child in node.neighbors:
        child.make_open()
        if node not in final_path.values():
            final_path[child]=node
        # draw(window, grid,rows,cols,screen_width,screen_height)
        if DLS(window,grid,rows,cols,child,end,screen_width,screen_height,level+1,maxLevel,path):
            return path
        
def IDDLS(window,grid,rows,cols,start,end,screen_width,screen_height,maxDepthLevel,path):
    for l in range(maxDepthLevel+1):
        f_path=DLS(window,grid,rows,cols,start,end,screen_width,screen_height,0,l,path)
        if f_path:
            draw_final_path(window, grid,rows,cols,screen_width,screen_height,final_path,end)
            return True

def main(screen_width,screen_height,window,rows,columns):
    grid = make_grid(screen_width,screen_height,rows,columns)
    start = None
    end = None
    running = True # True if algorithm is not running
    started = False # True if algorithm is started

    while running:
        draw(window, grid,rows,columns,screen_width,screen_height)
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                running=False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = getNodeRW(pos,rows,columns,screen_width,screen_height)
                node = grid[row][col]
                if not start and node!=end:
                    start=node
                    node.makeStartNode()
                elif not end and node!=start:
                    end=node
                    node.makeEndNode()
                elif node!=start and node!=end:
                    node.makeBarrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = getNodeRW(pos,rows,columns,screen_width,screen_height)
                node = grid[row][col]
                if node==start:
                    start=None
                elif node==end:
                    end=None
                node.make_white()
            if event.type==KEYDOWN:
                started=True
                for row in grid:
                    for node in row:
                        node.get_neighbors(grid)
                if event.key==K_SPACE and start and end:
                    if A_start_algo(window,grid,rows,columns,start,end,screen_width,screen_height):
                        print("get goal node")
                if event.key==K_i and start and end:
                    path = []
                    if BFS(window,grid,rows,columns,start,end,screen_width,screen_height):
                        print("get goal node")

    pygame.quit()


main(SCREEN_WIDTH,SCREEN_HEIGHT,WINDOW,ROWS,COLUMNS)