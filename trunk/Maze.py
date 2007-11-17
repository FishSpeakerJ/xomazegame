import random

def generateRandomBoolean():
	return random.randint( 0, 1 ) == 0

class Cell:
	def __init__(self):
		self.north = True
		self.east = True
		self.south = True
		self.west = True
	def generateRandom(self):
		self.north = generateRandomBoolean()
		self.east = generateRandomBoolean()
		self.south = generateRandomBoolean()
		self.west = generateRandomBoolean()

class Maze:
	def __init__(self):
		self.initialize(8, 8)
	def initialize(self, rowCount, columnCount):
		self._rowCount = rowCount
		self._columnCount = columnCount
		self._cells = [None]*self._rowCount
		r = 0
		while r<self._rowCount:
			self._cells[ r ] = [None]*self._columnCount
			c = 0
			while c<self._columnCount:
				self._cells[ r ][ c ] = Cell()
				c += 1
			r += 1
		self.generateRandom()
	def getRowCount(self):
		return self._rowCount
	def getColumnCount(self):
		return self._columnCount
	def isWall(self, row, column, direction):
		return self._isWall[ row ][ column ][ direction ]
	def generateRandom(self):
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				self._cells[ r ][ c ].generateRandom()
				c += 1
			r += 1
	def paint(self, g, x, y, w, h):
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				if self._cells[ r ][ c ].south:
					print '_',
				else:
					print ' ',
				if self._cells[ r ][ c ].east:
					print '|',
				else:
					print ' ',
				c += 1
			print
			r += 1
		
#m = Maze()
#m.paint( None, 10, 10, 100, 100 )