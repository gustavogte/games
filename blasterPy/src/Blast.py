import pygame

class Blast:
	def __init__(self,img_name,x,y):
		img = pygame.image.load(img_name)
		self.img_path = img_name
		self.x = x
		self.y = y
		self.img = img
		self.width = img.get_width()
		self.height = img.get_height()
		self.after_images = 15

	def load(self):
		if self.after_images:
			self.after_images-=1
			return self.img,tuple([self.x-self.width/2,self.y-self.height/2])
		else:
			return False