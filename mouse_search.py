import pygame
import math
from queue import PriorityQueue
import time 
import pygame_menu


WIDTH = 800
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Mouse Game")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		# check if you are in the grid             check if not barrier
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

came_from = {}
visited = set()

def dfs_I(draw,grid,start,end):
	# pilha 
	stack, visited = [], []
	stack.append(start)
	print("\nDFS : ")
	while len(stack)>0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		cube = stack.pop()

		if cube == end:
			print("Achei o queijo!!")
			end.make_end()
			break
		
		print(f"Estou em ({cube.get_pos()[0]},{cube.get_pos()[1]})")

		if cube not in visited:
			visited.append(cube)
			print(cube.get_pos())
		for neighbor in cube.neighbors:
			if neighbor not in visited:
				stack.append(neighbor)
				neighbor.make_open()

		if cube != start:
			cube.make_closed()

		draw()    

visited_bfs = [] # List for visited nodes.
queue = []     #Initialize a queue	

def bfs(draw,grid, start,end): #function for BFS
	visited_bfs.append(start)
	queue.append(start)

	while queue:          # Creating loop to visit each node
		m = queue.pop(0) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		if m == end:
			print("Rato achou o queijo\nSe divirta com seu queijo!!")
			end.make_end()
			return True

		print(f"Estou em ({m.get_pos()[0]},{m.get_pos()[1]})")
		for neighbour in m.neighbors:

			if neighbour not in visited_bfs:
				visited_bfs.append(neighbour)
				queue.append(neighbour)
				neighbour.make_open()


		if m != start:
			m.make_closed()
		draw()


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def set_difficulty(value, difficulty):
	# Do the job here !
	pass

def start_the_game():
	# Do the job here !
	pass

def main(win, width):

	ROWS = 25
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True


	while run:
		draw(win, grid, ROWS, width)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				# verifica se já começou ou não e se não é o final
				if not start and spot != end:
					start = spot
					start.make_start()

				# verifica se já colocou o final e se não é o começo
				elif not end and spot != start:
					end = spot
					end.make_end()

				# se não for começo e nem final é barreira
				elif spot != end and spot != start:
					spot.make_barrier()

			# clique com a direita do mouse significa não seleciona mais
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					dfs_I(lambda: draw(win, grid, ROWS, width),grid,start,end)
					#bfs(lambda: draw(win, grid, ROWS, width),grid,start,end)
					#print(start.neighbors)
					#print(end.neighbors)

					print(f"Inicio era ({start.row},{start.col}) Final era ({end.row},{end.col})")

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
		

	pygame.quit()

main(WIN, WIDTH)