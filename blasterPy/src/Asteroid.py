import pygame
import random

def CollisionDetect(toCheck,objectList):
	if len(objectList) == 0:
		return [False,None]
	for num,obj in enumerate(objectList):
		x_range_obj = [-obj.width/1.2+obj.x,obj.width/1.2+obj.x]
		y_range_obj = [-obj.height/1.2+obj.y,obj.height/1.2+obj.y]
		if x_range_obj[0]<=toCheck.x<=x_range_obj[1] and y_range_obj[0]<=toCheck.y<=y_range_obj[1]:
			return [True,num]
	return [False,None]

class Asteroid:
	def __init__(self,img_name,x,y,y_speed):
		img = pygame.image.load(img_name)
		self.img_path = img_name
		self.x = x
		self.y = y 
		self.img = img
		self.width = img.get_width()
		self.height = img.get_height()
		self.x_chg = 0
		self.y_chg = y_speed
	def load(self):
		return self.img,tuple([self.x-self.width/2,self.y-self.height/2])

	def changeXY(self,WINDOW_WIDTH = None,WINDOW_HEIGHT = None,WINDOW_DIMENSIONS = None):
		if WINDOW_DIMENSIONS is not None:
			WINDOW_WIDTH,WINDOW_HEIGHT = WINDOW_DIMENSIONS
		if self.width/2<self.x+self.x_chg and self.x+self.x_chg+self.width<WINDOW_WIDTH+self.width*1.5:
			self.x+=self.x_chg
		if -self.height<self.y+self.y_chg and self.y+self.y_chg+self.height<WINDOW_HEIGHT+self.height*1.5:
			self.y+=self.y_chg
		else:
			return False
		return True
