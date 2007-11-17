import random

import pygame

def generateRandomBoolean():
	return random.randint( 0, 1 ) == 0

class Direction:
	def __init__(self):
		self.isWalled = True
		self.neighbor = None
	

class Cell:
	def __init__(self):
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
				print self, other

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
				self._cells[ r ][ c ] = Cell()
				c += 1
			r += 1
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				cell.north.neighbor = self._getNeighborCell( r-1, c )
				cell.east.neighbor = self._getNeighborCell( r, c+1 )
				cell.south.neighbor = self._getNeighborCell( r+1, c )
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
	def _knockDownWallBetween(self, currentCell, nextCell):
		currentCell.knockDownWallToward( nextCell )
		nextCell.knockDownWallToward( currentCell )
	def constructRandom(self):
		cellStack = []
		currentCell = self.getRandomCell()
		visitedCellCount = 1
		totalCellCount = self._rowCount * self._columnCount
		while visitedCellCount < totalCellCount:
			nextCell = self._selectRandomNeighborCellWithAllWallsInTact( currentCell )
			if nextCell:
				self._knockDownWallBetween( currentCell, nextCell )
				cellStack.append( currentCell )
				currentCell = nextCell
				visitedCellCount += 1
			else:
				currentCell = cellStack.pop();

	def paint(self, surface, x0, y0, w, h):
		red = (255,0,0)
		white = (255,255,255)
		
		cellWidth = w/self._columnCount
		cellHeight = w/self._rowCount
		
		y = y0
		r = 0
		while r<self._rowCount:
			c = 0
			x = x0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				if cell.north.isWalled:
					pygame.draw.line( surface, white, (x, y), (x+cellWidth, y) )
				if cell.west.isWalled:
					pygame.draw.line( surface, white, (x, y), (x, y+cellHeight) )
				x += cellWidth
				c += 1
			y += cellHeight
			r += 1
	
	def echo(self):	
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