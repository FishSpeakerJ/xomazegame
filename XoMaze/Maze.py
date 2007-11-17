import random

import pygame

def generateRandomBoolean():
	return random.randint( 0, 1 ) == 0

class Direction:
	def __init__(self):
		self.isWalled = True
		self.neighbor = None

class Cell:
	def __init__(self, row, column):
		self.row = row
		self.column = column
		self.north = Direction()
		self.east = Direction()
		self.south = Direction()
		self.west = Direction()
		self.directions = ( self.north, self.east, self.south, self.west )
	def generateRandom(self):
		self.north.isWalled = generateRandomBoolean()
		self.east.isWalled = generateRandomBoolean()
		self.south.isWalled = generateRandomBoolean()
		self.west.isWalled = generateRandomBoolean()
	def areAllWallsInTact(self):
		return self.north.isWalled and self.east.isWalled and self.south.isWalled and self.west.isWalled
	def knockDownWallToward(self, other):
		for direction in self.directions:
			if direction.neighbor == other:
				direction.isWalled = False
	def __repr__( self ):
		return "(" + `self.row` + "," + `self.column` + ")"

class Path:
	def __init__(self, row, column):
		self.cells = []
	def addCell(self, cell):
		self.cells.append(cell)

class Maze:
	def __init__(self, rowCount=16, columnCount=16):
		self.initialize(rowCount, columnCount)
	def initialize(self, rowCount, columnCount):
		self._rowCount = rowCount
		self._columnCount = columnCount
		self._cells = [None]*self._rowCount
		r = 0
		while r<self._rowCount:
			self._cells[ r ] = [None]*self._columnCount
			c = 0
			while c<self._columnCount:
				self._cells[ r ][ c ] = Cell( r, c )
				c += 1
			r += 1
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				cell.north.neighbor = self._getNeighborCell( r+1, c )
				cell.east.neighbor = self._getNeighborCell( r, c+1 )
				cell.south.neighbor = self._getNeighborCell( r-1, c )
				cell.west.neighbor = self._getNeighborCell( r, c-1 )
				c += 1
			r += 1
		#self.generateRandom()
		self.constructRandom()
	def _getNeighborCell(self, r, c):
		try:
			return self.getCell( r, c )
		except:
			return None
	def getRowCount(self):
		return self._rowCount
	def getColumnCount(self):
		return self._columnCount
	def getCell(self, row, column):
		return self._cells[ row ][ column ]
	def generateRandom(self):
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				self._cells[ r ][ c ].generateRandom()
				c += 1
			r += 1
	def getRandomCell(self):
		r = random.randint( 0, self._rowCount-1 )
		c = random.randint( 0, self._columnCount-1 )
		return self.getCell( r, c )
	def _selectRandomNeighborCellWithAllWallsInTact(self, cell):
		allWallsInTactNeighbors = []
		for direction in cell.directions:
			if direction.neighbor and direction.neighbor.areAllWallsInTact():
				allWallsInTactNeighbors.append( direction.neighbor )
		n = len( allWallsInTactNeighbors )
		if n:
			return allWallsInTactNeighbors[ random.randint( 0, n-1 ) ]
		else:
			return None
	def constructRandom(self):
#		r = 2
#		c = 2
#		currentCell = self.getCell( r, c )
#		nextCell = self.getCell( r, c+1 )
#		print currentCell, nextCell
#		currentCell.knockDownWallToward( nextCell )
#		nextCell.knockDownWallToward( currentCell )
#		return
		
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				for direction in self._cells[ r ][ c ].directions:
					direction.isWalled = True
				c += 1
			r += 1
		cellStack = []
		
		currentCell = self.getRandomCell()
		visitedCellCount = 1
		totalCellCount = self._rowCount * self._columnCount
		while visitedCellCount < totalCellCount:
			nextCell = self._selectRandomNeighborCellWithAllWallsInTact( currentCell )
			if nextCell:
				currentCell.knockDownWallToward( nextCell )
				nextCell.knockDownWallToward( currentCell )
				cellStack.append( currentCell )
				currentCell = nextCell
				visitedCellCount += 1
			else:
				currentCell = cellStack.pop();

	def mapX( self, fx ):
		return self._x0 + fx*self._cellSize
	
	def mapY( self, fy ):
		return ( self._y0 + self._h ) - (fy*self._cellSize)
	
	def drawLine( self, surface, color, ax, ay, bx, by ):
		pygame.draw.line( surface, color, (self.mapX(ax), self.mapY(ay)), (self.mapX(bx), self.mapY(by)) )

	def paint(self, surface, x0, y0, w, h):
		self._x0 = x0
		self._y0 = y0
		self._w = w
		self._h = h
		self._cellWidth = self._w/self._columnCount
		self._cellHeight = self._h/self._rowCount
		self._cellSize = min( self._cellWidth, self._cellHeight )
		
		white = (255,255,255)
		yellow = (255,255,0)
		red = (255,0,0)
		green = (0,255,0)
		
		cellWidth = w/self._columnCount
		cellHeight = h/self._rowCount
		
		cellSize = min( cellWidth, cellHeight )
		
		PAD = 4
		
		pad0 = 0.025
		pad1 = 1.0-pad0
		y = y0 + h + 50
		r = 0
		while r<self._rowCount:
			c = 0
			x = x0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				if cell.north.isWalled:
#					self.drawLine( surface, yellow, r+pad0, c+pad1, r+pad1, c+pad1 )
					pygame.draw.line( surface, white, (x, y), (x+cellSize, y) )
				if cell.west.isWalled:
#					self.drawLine( surface, yellow, r+pad0, c+pad0, r+pad0, c+pad1 )
					pygame.draw.line( surface, white, (x, y), (x, y+cellSize) )
				if cell.south.isWalled:
#					self.drawLine( surface, white, r+pad0, c+pad0, r+pad1, c+pad0 )
					pygame.draw.line( surface, yellow, (x, y+cellSize), (x+cellSize, y+cellSize) )
				if cell.east.isWalled:
#					self.drawLine( surface, white, r+pad1, c+pad0, r+pad1, c+pad1 )
					pygame.draw.line( surface, yellow, (x+cellSize, y), (x+cellSize, y+cellSize) )
				x += cellSize + PAD
				c += 1
			y -= cellSize + PAD
			r += 1
		
		self._x0 = None
		self._y0 = None
		self._w = None
		self._h = None
		self._cellWidth = None
		self._cellHeight = None
		self._cellSize = None
