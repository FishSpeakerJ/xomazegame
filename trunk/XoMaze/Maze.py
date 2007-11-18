import random

import pygame

def generateRandomBoolean():
	return random.randint( 0, 1 ) == 0

def blendColors( a, b ):
	ar, ag, ab = a
	br, bg, bb = b
	return (ar+br)/2,(ag+bg)/2,(ab+bb)/2

def factorColor( a, factor=2 ):
	ar, ag, ab = a
	return ar/factor, ag/factor, ab/factor

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
		self.beenVisited = False
		self.isContainingHead = False
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
				return
		raise "did not knock down wall"
	def getRandomDirection( self ):
		return self.directions[ random.randint( 0, 3 ) ]
	def __repr__( self ):
		return "(x=" + `self.column` + ",y=" + `self.row` + ")"

class Maze:
	def __init__(self, game, xCellCount=8, yCellCount=6):
		self._game = game
		self._xPixelOffset = 0
		self._yPixelOffset = 0
		self._headsRollingAnimationPortion = -1
		self.initialize(xCellCount, yCellCount)

		# HACK:
		self._x0 = 0
		self._y0 = 0
		self._w = 0
		self._h = 0
		self._cellSize = 0
	def initialize(self, xCellCount, yCellCount):
		self._rowCount = yCellCount
		self._columnCount = xCellCount
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
		#self.constructRandom()

	def _getNeighborCell(self, r, c):
		if r<0 or r>=self._rowCount or c<0 or c>=self._columnCount:
			return None
		else:
			return self._getCellRC( r, c )
	def _getCellRC(self, r,c):
		return self.getCellXY( c, r )
	
	def getXCellCount(self):
		return self._columnCount
	def getYCellCount(self):
		return self._rowCount
	def getCellXY(self, x, y):
		return self._cells[ y ][ x ]
	def getRandomCell(self):
		r = random.randint( 0, self._rowCount-1 )
		c = random.randint( 0, self._columnCount-1 )
		return self._getCellRC( r, c )

	def getRandomUnusedCell(self):
		r = random.randint( 2, self._rowCount-3 )
		c = random.randint( 0, self._columnCount-1 )
		return self._getCellRC( r, c )

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

	def _clearWallsBetween( self, a, b ):
		a.knockDownWallToward( b )
		b.knockDownWallToward( a )
	def _clearStartWallsForPlayer( self, player ):
		self._clearWallsBetween( player.beginCell, player.beginCell.east.neighbor )
		self._clearWallsBetween( player.beginCell, player.beginCell.west.neighbor )
		self._clearWallsBetween( player.beginCell, player.beginCell.north.neighbor )

	def _clearEndWalls( self ):
		for cell in self._game.playerManager.endCells:
			self._clearWallsBetween( cell, cell.east.neighbor )
			self._clearWallsBetween( cell, cell.west.neighbor )
			self._clearWallsBetween( cell, cell.south.neighbor )
	
	def constructRandom(self, portionOfWallsToBeRemoved=0.025):		
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				for direction in cell.directions:
					direction.isWalled = True
				c += 1
			r += 1
		
		cellStack = []
			
		currentCell = self.getRandomCell()
		visitedCellCount = 1
		totalCellCount = self._rowCount * self._columnCount
		
		n = totalCellCount / 10
		i = 0
		while visitedCellCount < totalCellCount:
			nextCell = self._selectRandomNeighborCellWithAllWallsInTact( currentCell )
			if nextCell:
				self._clearWallsBetween( currentCell, nextCell )
				cellStack.append( currentCell )
				currentCell = nextCell
				visitedCellCount += 1
				i += 1
				i %= n
				if i == 0:
					pass
					#self.paint( self._game.boardSurface )
					#pygame.display.update()
			else:
				currentCell = cellStack.pop();
		
		if self._game.playerManager:
			for player in self._game.playerManager.playerIdsToPlayers.values():
				self._clearStartWallsForPlayer( player )
			self._clearEndWalls()

		wallCount = 0
		r = 0
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				for direction in self._cells[ r ][ c ].directions:
					if direction.isWalled:
						wallCount += 1
				c += 1
			r += 1
		
		wallsToRemoveCount = wallCount * portionOfWallsToBeRemoved
		while wallsToRemoveCount > 0:
			cell = self.getRandomCell()
			direction = cell.getRandomDirection()
			if direction.neighbor:
				if direction.isWalled:
					self._clearWallsBetween( cell, direction.neighbor )
					wallsToRemoveCount -= 1

	def mapX( self, fx ):
		return int( self._x0 + fx*self._cellSize + 0.5 ) + self._xPixelOffset
	def mapY( self, fy ):
		return int( ( self._y0 + self._h ) - (fy*self._cellSize) + 0.5 )  + self._yPixelOffset
	
	def mapPoint( self, fp ):
		return self.mapX( fp[0] ), self.mapY( fp[1] )
	
	def mapWidth( self, fw ):
		return int( fw*self._cellSize + 0.5 )
	def mapHeight( self, fh ):
		return int( fh*self._cellSize + 0.5 )
	
	def drawLine( self, surface, color, ax, ay, bx, by, width=1 ):
		pygame.draw.line( surface, color, (self.mapX(ax), self.mapY(ay)), (self.mapX(bx), self.mapY(by)), int( width ) )

	def drawCircle( self, surface, color, cx, cy, radius ):
		rect = (self.mapX(cx-radius), self.mapY(cy+radius), self.mapWidth(radius+radius)+1, self.mapHeight(radius+radius)+1)
		pygame.draw.ellipse( surface, color, rect )
	
	def drawPolygon( self, surface, color, points ):
		pixelPoints = [ None ]*len(points)
		i = 0
		n = len( pixelPoints )
		while i<n:
			pixelPoints[ i ] = self.mapPoint( points[ i ] )
			i += 1
		pygame.draw.polygon( surface, color, pixelPoints )
	
	def mapCell( self, cell, offset ):
		return ( self.mapX( cell.column+offset ), self.mapY( cell.row+offset ) )
	def drawPathStart( self, offset, cell ):
		self._points = []
		self._points.append( self.mapCell( cell, offset ) )
		
	def drawPathNextCell( self, offset, cell ):
		self._points.append( self.mapCell( cell, offset ) )

	def drawPathEnd( self, surface, stroke, fill, isSignaling ):
		if isSignaling and stroke:
			width = 0.15
			lineWidth = self.mapWidth( width )
			pygame.draw.lines( surface, stroke, False, self._points, lineWidth )
		width = 0.1
		lineWidth = max( self.mapWidth( width ), 1 )
		pygame.draw.lines( surface, fill, False, self._points, lineWidth )

	def drawPath( self, surface, stroke, fill, offset, isSignaling, path ):
		currentCell = path[ 0 ]
		self.drawPathStart( offset, path[ 0 ] )
		for nextCell in path[ 0: ]:
			self.drawPathNextCell( offset, nextCell )
		self.drawPathEnd( surface, stroke, fill, isSignaling )

	def __drawX( self, surface, stroke, fill, x, y, isSignaling ):
		lineWidth = self.mapWidth(0.2)
		radius = 0.25
		if isSignaling:
			self.drawLine( surface, stroke, x-radius, y-radius, x, y, lineWidth )
			self.drawLine( surface, stroke, x, y, x+radius, y-radius, lineWidth )
			self.drawLine( surface, stroke, x-radius, y, x+radius, y, lineWidth )
		else:
			self.drawLine( surface, stroke, x-radius, y-radius, x+radius, y+radius, lineWidth )
			self.drawLine( surface, stroke, x-radius, y+radius, x+radius, y-radius, lineWidth )

		lineWidth *= 0.75
		radius *= 0.85
		if isSignaling:
			self.drawLine( surface, fill, x-radius, y-radius, x, y, lineWidth )
			self.drawLine( surface, fill, x, y, x+radius, y-radius, lineWidth )
			self.drawLine( surface, fill, x-radius, y, x+radius, y, lineWidth )
		else:
			self.drawLine( surface, fill, x-radius, y-radius, x+radius, y+radius, lineWidth )
			self.drawLine( surface, fill, x-radius, y+radius, x+radius, y-radius, lineWidth )


	def _drawX( self, surface, color, x, y, isSignaling, radius, capRadius ):
		if isSignaling:
			cosTheta = 0.499
			sinTheta = 0.866
		else:
			cosTheta = 0.707
			sinTheta = 0.707

		capRadiusSinTheta = capRadius*0.707
		
		p0 = x+radius*cosTheta, y+radius*sinTheta
		p1 = x-radius*cosTheta, y+radius*sinTheta
		p2 = x-radius*cosTheta, y-radius*sinTheta
		p3 = x+radius*cosTheta, y-radius*sinTheta

		p0a = p0[0]+capRadiusSinTheta, p0[1]-capRadiusSinTheta
		p0b = p0[0]-capRadiusSinTheta, p0[1]+capRadiusSinTheta
		p1a = p1[0]+capRadiusSinTheta, p1[1]+capRadiusSinTheta
		p1b = p1[0]-capRadiusSinTheta, p1[1]-capRadiusSinTheta
		p2a = p2[0]-capRadiusSinTheta, p2[1]+capRadiusSinTheta
		p2b = p2[0]+capRadiusSinTheta, p2[1]-capRadiusSinTheta
		p3a = p3[0]-capRadiusSinTheta, p3[1]-capRadiusSinTheta
		p3b = p3[0]+capRadiusSinTheta, p3[1]+capRadiusSinTheta

		ce = (x+capRadius, y)
		cn = (x, y+capRadius)
		cw = (x-capRadius, y)
		cs = (x, y-capRadius)

		self.drawCircle( surface, color, p0[0], p0[1], capRadius ) 
		self.drawCircle( surface, color, p1[0], p1[1], capRadius ) 
		self.drawCircle( surface, color, p2[0], p2[1], capRadius ) 
		self.drawCircle( surface, color, p3[0], p3[1], capRadius )

		self.drawPolygon( surface, color, [ce,p0a,p0b,cn,p1a,p1b,cw,p2a,p2b,cs,p3a,p3b,ce] )

	def drawX( self, surface, stroke, fill, x, y, isSignaling ):
		if stroke:
			self._drawX( surface, stroke, x, y, isSignaling, 0.4, 0.08 )
		if fill:
			self._drawX( surface, fill, x, y, isSignaling, 0.35, 0.04 )

	def drawO( self, surface, stroke, fill, x, y, factor=1.0 ):
		#x += offset
		#y += offset
		radius = 0.125*factor
		if stroke:
			self.drawCircle(surface, stroke, x, y, radius)
		radius *= 0.75
		if fill:
			self.drawCircle(surface, fill, x, y, radius)
		
	def drawHeadRolling(self, surface, player, portion):
		x, y0 = player.getPosition()
		y0 += 0.3
		y1 = y0 + 4.0
		y = y0 + (y1-y0)*portion
		self.drawO( surface, player.getStrokeColor(), player.getFillColor(), x, y )
	
	def handleHeadsRollingAnimation(self, portion):
		if portion == 0.0:
			self._game.playerManager.unattachHeads()
		self._headsRollingAnimationPortion = portion
		if portion == 1.0:
			self._headsRollingAnimationPortion = -1
		
	def drawPlayer( self, surface, player ):
		isSignaling = player.isSignaling()
		x, y = player.getPosition()
		self.drawX( surface, player.getStrokeColor(), player.getFillColor(), x, y, isSignaling )
		if player.headAttached:
			factor = 1.0
			y += 0.3
		else:
			factor = 2.0
			x = player.headCell.column + 0.5
			y = player.headCell.row + 0.5
		self.drawO( surface, player.getStrokeColor(), player.getFillColor(), x, y, factor )
	
	def drawDockingBays( self, surface ):
		for cell in self._game.playerManager.endCells:
			x = cell.column + 0.5
			y = cell.row + 0.5
			shadow = (48,48,48)
			highlight = (192,192,192)
			#sunken = (128,128,128)
			sunken = (48,48,64)
			self._xPixelOffset = -1
			self._yPixelOffset = -1
			self.drawX( surface, shadow, None, x, y, False )
			self.drawO( surface, shadow, None, x, y + 0.3 )
			self._xPixelOffset = 1
			self._yPixelOffset = 1
			self.drawX( surface, highlight, None, x, y, False )
			self.drawO( surface, highlight, None, x, y + 0.3 )
			self._xPixelOffset = 0
			self._yPixelOffset = 0
			self.drawX( surface, sunken, None, x, y, False )
			self.drawO( surface, sunken, None, x, y + 0.3 )
	
	def drawPlayerPath( self, surface, player ):
		#strokeColor = blendColors( player.getStrokeColor(), (32,32,32))
		#fillColor = blendColors( player.getFillColor(), (32,32,32))
		strokeColor = player.getStrokeColor()
		fillColor = player.getFillColor()
				
		path = player.getPath()
		if len( path ):
			self.drawPath( surface, None, factorColor( player.getFillColor(), 4 ), player.offset, player.isSignaling(), path )
			
			prunedPath = path[:]
			
			i = 1
			while i<len(prunedPath):
				j = i+1
				jFound = -1
				while j<len(prunedPath):
					if prunedPath[i] is prunedPath[j]:
						jFound = j
					j += 1
				if jFound != -1:
					prunedPath = prunedPath[:i]+prunedPath[jFound:]
				else:
					i += 1

			if len( prunedPath ):
				self.drawPath( surface, strokeColor, fillColor, player.offset, player.isSignaling(), prunedPath )
				lastCell = path[-1]
				if lastCell == prunedPath[-1]:
					self._points = []
					self._points.append( self.mapCell( lastCell, player.offset ) )
					x, y = player.getPosition()
					self._points.append( ( self.mapX( x ), self.mapY( y ) ) )
					self.drawPathEnd( surface, strokeColor, fillColor, player.isSignaling() )
					
					
	def paint(self, surface):
		PAD = 4
		self._w = surface.get_width() - PAD
		self._h = surface.get_height() - PAD
		cellWidth = self._w/self._columnCount
		cellHeight = self._h/self._rowCount
		self._cellSize = min( cellWidth, cellHeight )

		w = self._cellSize*self._columnCount
		h = self._cellSize*self._rowCount
		self._x0 = (self._w-w)/2
		self._y0 = (self._h-h)/2
		self._w = w
		self._h = h
		
		black = (0,0,0)
		white = (255,255,255)
		yellow = (255,255,0)
		red = (255,0,0)
		green = (0,255,0)
		gray = (128,128,128)


		#pygame.draw.rect( surface, black, (self._x0, self._y0, self._w, self._h) )
		pygame.draw.rect( surface, black, (0, 0, surface.get_width(), surface.get_height()) )

		#self._drawX( surface, red, yellow, 5, 5, True )
		self.drawDockingBays(surface)
		pad0 = 0.0
		pad1 = 1.0-pad0
		r = 0
		wallWidth = self.mapWidth(0.1)
		while r<self._rowCount:
			c = 0
			while c<self._columnCount:
				cell = self._cells[ r ][ c ]
				if cell.south.isWalled:
					if cell.row == 0:
						self.drawLine( surface, white, c+pad0, r+pad0, c+pad1, r+pad0, wallWidth )
				if cell.west.isWalled:
					if cell.column == 0:
						self.drawLine( surface, white, c+pad0, r+pad0, c+pad0, r+pad1, wallWidth )
				if cell.north.isWalled:
					self.drawLine( surface, white, c+pad0, r+pad1, c+pad1, r+pad1, wallWidth )
				if cell.east.isWalled:
					self.drawLine( surface, white, c+pad1, r+pad0, c+pad1, r+pad1, wallWidth )
				c += 1
			r += 1
		
		if self._game.playerManager:
			for player in self._game.playerManager.playerIdsToPlayers.values():
				self.drawPlayerPath( surface, player )
			for player in self._game.playerManager.playerIdsToPlayers.values():
				self.drawPlayer( surface, player )
			for player in self._game.playerManager.playerIdsToPlayers.values():
				if self._headsRollingAnimationPortion < 0:
					return
				delta = max( 0.0, self._headsRollingAnimationPortion - player.id*0.2 )
				if delta > 0.0:
					self._game.playerManager.playUhOh( player.id )
				self.drawHeadRolling(surface, player, delta )

#		self._x0 = None
#		self._y0 = None
#		self._w = None
#		self._h = None
#		self._cellSize = None
