
import pygame, math, time
from PIL import Image
import globalconst

class stillSprite(pygame.sprite.Sprite):

	def __init__(self, image, position,displaylist_group, lvl):
		pygame.sprite.Sprite.__init__(self)
		self.objectofthescene_group=displaylist_group
		self.image = pygame.image.load(image)
		self.PILimage=Image.open(image)
		self.PILdyingimg=Image.open('img/fire.png')
		self.mask = pygame.mask.from_surface(self.image)
		self.position = position
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.lvl=lvl
		self.strength=1*lvl
		self.spirit=0
		self.agility=0
		self.energymax=5*(self.strength+self.spirit+self.agility)
		self.energy=self.energymax
		self.healthmax=10*self.strength
		self.health=self.healthmax
		self.killer=[]
		self.ghost=False
	def update(self):
		if self.health!=self.healthmax:
			if self.health<0:
				self.health=0
			if self.health<self.healthmax:
				t=time.time()
				if globalconst.DEBUG:
					print t-self.restTime
				if (t-self.restTime)>60:
					self.health+=self.spirit+self.strength
					if self.health>self.healthmax:
						self.health=self.healthmax
					self.restTime=t
			
			alpha=(float)(self.healthmax-self.health)/self.healthmax
			image=Image.blend(self.PILimage, self.PILdyingimg,alpha )
			
			#drawing the health bar ... could be something like a function or an ineherit attribut of abstract class for all objet with life ...
			beginPixelHealth=alpha*image.size[0]
			beginPixelHealth=(int) (beginPixelHealth)
			boxhealth=(0,0,image.size[0]-beginPixelHealth,2)
			healthbar=Image.new('RGB',(image.size[0]-beginPixelHealth,2),(0,255,0))
			image.paste(healthbar,boxhealth)
			image=image.convert('RGBA')
			
			imgstr=image.tostring()
			self.image=pygame.image.fromstring(imgstr,image.size,'RGBA')
			if self.health<=0:
				for killer in self.killer:
					for obj in self.objectofthescene_group:
						if hasattr(obj,"name"):
							if obj.name==killer:
								obj.xpup(self.lvl)
				self.kill()
	def collide(self,obj):
	    if globalconst.DEBUG:
	        print "Tree collide with", obj
