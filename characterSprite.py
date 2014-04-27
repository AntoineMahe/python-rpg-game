
import pygame, math, time,sys
from PIL import Image
import fireballSprite
import globalconst
from pgu import gui


class characterSprite(pygame.sprite.Sprite):

	def __init__(self, image, position,displaylist_group,name="noname"):
		pygame.sprite.Sprite.__init__(self)
		#sprite carac
		self.image = pygame.image.load(image)
		self.PILimage=Image.open(image)
		self.position = position
		
		self.rect = self.image.get_rect()
		
		self.mask = pygame.mask.from_surface(self.image)
		
		self.action=[0,0,0,0,0]#[right,left,up,down,defaultaction]
		self.objectofthescene_group=displaylist_group
		#character carac
		self.name=name
		self.xp=0
		self.lvl=0
		
		self.items=[]
		self.carry=[]
		
		#item est une class abstrait
		#potion herite d'item. puis potion de vie / mana etc herite de potion ... 
		
		self.strength=1
		self.spirit=1
		self.agility=1
		
		
		self.energymax=5*(self.strength+self.spirit+self.agility)
		self.energy=self.energymax
		self.healthmax=10*self.strength
		self.health=self.healthmax
		
		
		
		self.restTime=time.time()
		
		self.killer=[]
		
		self.ghost=False
		
	def update(self):
		
		if self.health<0:
			self.health=0
		if self.energy<0:
			self.energy=0
		if self.health==0:
			app = gui.Desktop()
			app.connect(gui.QUIT,app.quit,None)
			e = gui.Button("Game Over")
			e.connect(gui.CLICK,app.quit,None)
			c = gui.Table()
			c.tr()
			
			c.td(gui.Label(self.name))
			c.td(gui.Label(str(self.lvl)))
			
			c.tr()
			c.td(e,colspan=2)
			app.run(c)
			self.kill()
			
		if self.xp>=100:
			self.levelup()
			if globalconst.DEBUG:
				print self.lvl
		if self.health<self.healthmax:
			t=time.time()
			if globalconst.DEBUG:
				print t-self.restTime
			if (t-self.restTime)>(30-(30/10) * math.log(self.agility,2)):#this calcul should be an attribut or such thing ...
				self.health+=self.spirit+self.strength
				if self.health>self.healthmax:
					self.health=self.healthmax
				self.restTime=t
		
		if self.health==self.healthmax and self.energy<self.energymax:
			t=time.time()
			if globalconst.DEBUG:
				print t-self.restTime
			if (t-self.restTime)>(5-(5/10) * math.log(self.agility,2)):
				self.energy+=self.spirit
				if self.energy>self.energymax:
					self.energy=self.energymax
				self.restTime=t
		
		x, y = self.position
		x += self.action[0]+self.action[1]
		y += self.action[2]+self.action[3]
		self.position = (x, y)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		
		image=self.PILimage.copy()
		
		manavoid=(float)(self.energymax-self.energy)/self.energymax
		healthvoid=(float)(self.healthmax-self.health)/self.healthmax
		
		
		
		beginPixelHealth=healthvoid*image.size[0]
		beginPixelMana=manavoid*image.size[0]
		
		beginPixelHealth=(int) (beginPixelHealth)
		beginPixelMana=(int)(beginPixelMana)
		
		
		boxhealth=(0,0,image.size[0]-beginPixelHealth,2)
		boxmana=(0,2,image.size[0]-beginPixelMana,4)
		
		healthbar=Image.new('RGB',(image.size[0]-beginPixelHealth,2),(0,255,0))
		manabar=Image.new('RGB',(image.size[0]-beginPixelMana,2),(0,0,255))
		
		image.paste(healthbar,boxhealth)
		image.paste(manabar,boxmana)
		#format==PNG
		image=image.convert('RGBA')
		imgstr=image.tostring()
	
		self.image=pygame.image.fromstring(imgstr,image.size,'RGBA')
		
		self.event()

	def collide(self,obj):
		x, y = self.position
		x -= self.action[0]+self.action[1]
		y -= self.action[2]+self.action[3]
		self.position = (x, y)
		d2=(obj.rect.center[0]-self.rect.center[0])*(obj.rect.center[0]-self.rect.center[0])+(obj.rect.center[1]-self.rect.center[1])*(obj.rect.center[1]-self.rect.center[1])
		dc=(obj.rect.width/2)*(obj.rect.width/2)+(obj.rect.height/2)*(obj.rect.height/2)
		if globalconst.DEBUG:
			print "d0 : ",obj.rect.center[0]-self.rect.center[0]
			print "d1 : ",obj.rect.center[1]-self.rect.center[1]
			print "width : ",obj.rect.width
			print "d2,dc : ",d2,dc
		if d2<dc:
			self.position = (obj.rect.center[0]-obj.rect.width, y)
			self.health-=1
		
		
	def event(self):
		if self.action[4]==1:
			if self.energy>0:
				self.energy-=1
				self.action[4]=0
				x, y = self.position
				v=[0,0]
				if self.action[0]!=0:
					v=[1,0]
					x+=self.rect.width/2
				elif self.action[1]!=0:
					v=[-1,0]
					x-=self.rect.width/2
				elif self.action[2]!=0:
					v=[0,-1]
					v[1]=-1
					y-=self.rect.height/2
				elif self.action[3]!=0:
					v=[0,1]
					y+=self.rect.height/2
				else:
					v=[1,0]
					x+=self.rect.width/2
				fireposition=(x,y)
				fireball=fireballSprite.fireballSprite('img/fireball.png',fireposition,self.name,v)
				fireball.power=self.spirit
				self.objectofthescene_group.add(fireball)
				
	def levelup(self):
		self.lvl+=1
		self.xp-=100
		app = gui.Desktop()
		app.connect(gui.QUIT,app.quit,None)
		c = gui.Table()
		c.tr()
		c.td(gui.Label("Character levelup"),colspan=4)
		c.tr()
		c.td(gui.Label("Name :"+self.name))
		c.tr()
		c.td(gui.Label("Level :"+str(self.lvl)))
		c.tr()
		c.td(gui.Label("Strength "+str(self.strength)))
		c.td(gui.Label("Spirit "+str(self.spirit)))
		c.td(gui.Label("Agility "+str(self.agility)))
		c.tr()
		g = gui.Group(value=1)
		c.td(gui.Radio(g,value=1))
		c.td(gui.Radio(g,value=2))
		c.td(gui.Radio(g,value=3))
		
		def doneit():
			if globalconst.DEBUG:
				print g.value
			if g.value==1:
				self.strength +=1
				self.healthmax=5*self.strength
			if g.value==2:
				self.spirit +=1
				self.energymax=5*(self.strength+self.spirit+self.agility)
			if g.value==3:
				self.agility+=1
		btn = gui.Button("Done")
		btn.connect(gui.CLICK,doneit)
		btn.connect(gui.CLICK,app.quit)
		c.tr()
		c.td(btn,colspan=4)
		app.run(c)
	def xpup(self,klvl):
		upxp=math.exp(((klvl-self.lvl)-3)/3)*100
		if upxp<1:
			upxp=1;
		if upxp>500:
			upxp=500+math.log(upxp-500)
		self.xp+=upxp
		print "xp :", self.xp
	
	
