import olpcgames

# Class name must match 'class' property in activity/activity.info:
class XoMazeActivity(olpcgames.PyGameActivity):
	"""A Pygame game as a Sugar activity."""
	game_name = 'runXoMaze'        # game_name must match name of your Pygame module
	game_title = 'XoMaze'
	game_size = (1200,825)