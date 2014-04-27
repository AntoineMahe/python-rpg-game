#!/usr/bin/python
import pygame, math, sys, time
import pygame.locals
import characterSprite
import stillSprite 
import fireballSprite
import globalconst
import random
from pgu import gui

if len(sys.argv)>1:
	if sys.argv[1]=='-d':
	    globalconst.DEBUG=True



def creationpopup(character):
   
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)
    c = gui.Table()
    c.tr()
    c.td(gui.Label("Character creation"),colspan=4)
    c.tr()
    c.td(gui.Label("Name :"))
    w = gui.Input(value='noname',size=8)
    c.td(w,colspan=3)
    c.tr()
    def doneit():
	character.name=w.value
    btn = gui.Button("Done")
    btn.connect(gui.CLICK,doneit)
    btn.connect(gui.CLICK,app.quit)
    c.tr()
    c.td(btn,colspan=4)
    app.run(c)



def main():

    screen = pygame.display.set_mode((1024,768))
    random.seed()
    clock = pygame.time.Clock()   
    
    BLACK = (0,0,0)
    
    rect=screen.get_rect()
    
    defaultposition=(0,0)
    
    objectofthescene_group = pygame.sprite.Group()
    
    name="no name"

    #name=raw_input("What's your name ?\n")
    
    character = characterSprite.characterSprite('img/mage.png', list(rect.center),objectofthescene_group,name)
    objectofthescene_group.add(character)
    character_group = pygame.sprite.Group(character)

    creationpopup(character)
    
    TreeTime=time.time()
    deltaTree=30
    Treeposition=list(rect.center)
    Treeposition[0]+=400
    
    Tree = stillSprite.stillSprite('img/tree.png', Treeposition,objectofthescene_group,1)
    objectofthescene_group.add(Tree)
    still_group = pygame.sprite.Group(Tree)
    
    Treeposition=list(rect.center)
    Treeposition[0]+=200
    Treeposition[1]+=200
    
    Trreee = stillSprite.stillSprite('img/tree.png', Treeposition,objectofthescene_group,10)
    objectofthescene_group.add(Trreee)
    still_group.add(Trreee)
    

    gost_group = pygame.sprite.Group()#should be use instead of the gost attribut
	
	
    #game life
    while 1:
	# USER INPUT
	deltat=clock.tick(30)
	for event in pygame.event.get():
	    if not hasattr(event, 'key'): continue
	    down = event.type == pygame.locals.KEYDOWN     # key down or up?
	    if event.key == pygame.locals.K_RIGHT: character.action[0] = down * 5
	    elif event.key == pygame.locals.K_LEFT: character.action[1] = down * -5
	    elif event.key == pygame.locals.K_UP: character.action[2] = down * -5
	    elif event.key == pygame.locals.K_DOWN: character.action[3] = down * 5
	    elif event.key == pygame.locals.K_SPACE: character.action[4]=down*1
	    elif event.key == pygame.locals.K_ESCAPE: sys.exit(0)     # quit the game
	screen.fill(BLACK)
	
	# SIMULATION
	
	if globalconst.DEBUG :
	    print len(objectofthescene_group)
	if time.time()-TreeTime>deltaTree:
	    lvl=random.randint(1,35)
	    print "lvl : ",lvl
	    if lvl>10:
		Treeposition=[random.randint(100,900),random.randint(100,600)]
		randTree = stillSprite.stillSprite('img/tree.png', Treeposition,objectofthescene_group,1)
		objectofthescene_group.add(randTree)
		still_group.add(randTree)
	    TreeTime=time.time()
	    Treeposition=[random.randint(100,900),random.randint(100,600)]
	    randTree = stillSprite.stillSprite('img/tree.png', Treeposition,objectofthescene_group,lvl)
	    objectofthescene_group.add(randTree)
	    still_group.add(randTree)
	    deltatTree=random.randint(10,90)

	
	objectofthescene_group.update()
	
	for obj in objectofthescene_group :
	    obj_list = pygame.sprite.spritecollide(obj,objectofthescene_group,False,collided=pygame.sprite.collide_mask)
	    obj_list.remove(obj)
	    if obj_list:
		for col_obj in obj_list:
		    obj.collide(col_obj)
	
	objectofthescene_group.draw(screen)
	# RENDERING
	pygame.display.flip()

main()
