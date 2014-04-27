
import pygame, time
import globalconst


class fireballSprite(pygame.sprite.Sprite):
	
	def __init__(self, image, position, launcher,v):
		pygame.sprite.Sprite.__init__(self)
		self.launcher=launcher
		self.image = pygame.image.load(image)
		self.mask = pygame.mask.from_surface(self.image)
		self.position = position
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.power=0
		self.v=v
		self.ghost=True
		
	def update(self):
		x, y = self.position
		x += 10*self.v[0]
		y +=10*self.v[1]
		if x>1024 or x<0 : 
			self.kill()
		self.position = (x, y)
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def collide(self,obj):
		if hasattr(obj, "name"):
			if obj.name==self.launcher:
				if globalconst.DEBUG:
					print "hey c moi"
				return
		
		
		if hasattr(obj, "health"):
			obj.health-=self.power
			obj.restTime=time.time()+60#les degats de type incendiaire empeche la regeneration mouahahaha
			if self.launcher not in obj.killer:
				obj.killer.append(self.launcher)
		
		
		if not obj.ghost:
			self.kill()
