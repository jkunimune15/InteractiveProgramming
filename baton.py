class Baton(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.positions = [(0,0),(0,0),(0,0)]	# the 3 previous positions of this baton
		self.