import tkinter as tk
import random

#tick = time in ms between each refresh
startTick=110	#initial speed
stepTick=2		#speed difference when you eat an apple
minTick=50		#max speed

gg=0			#grid on/off  (works only if snake grid is >0)
snkG=2			#space between each snake block 
gC="grey15"		#grid color
bC="grey17"		#background color
snkC="white"	#snake color
appleC="red3"	#apple color
lostC="grey30"	#lost color
winC="green2"	#win color



class Snake(tk.Canvas):
	def __init__(self, g, gc, bc):
		#g: grid (On/Off) (1/0)
		#gc: grid color
		#bc: background color
		self.hsc=0				#highscore
		self.width=500			#game width in px
		self.height=500			#game height in px
		self.ww=25				#dimension of the single block
		self.maxXB=self.width//self.ww		#number of horizontal blocks
		self.maxYB=self.height//self.ww		#number of vertical blocks
		self.bc=bc  
		super().__init__(width=self.width, height=self.height, background=self.bc, highlightthickness=0)
		self.bind_all("<Key>", self.keyPress)
		if g==1:
			self.grid(gc)
		self.blockGrid()
		self.reset()
		self.refresh()

	def reset(self):
		#reset the snake
		self.tick=startTick
		self.mTick=minTick
		self.sTick=stepTick
		self.pos=[[0,1], [1,1], [2,1], [3,1]]    #last one is the head
		self.nextApple()
		self.keyDir="d"
		self.dir="d"
		self.dead=0
		for x in range(self.maxXB):     
			for y in range(self.maxYB):
				self.fillBlock(x,y,self.bc)
		self.fillBlock(self.pos[3][0],self.pos[3][1], snkC)
		self.fillBlock(self.pos[2][0],self.pos[2][1], snkC)
		self.fillBlock(self.apple[0],  self.apple[1], appleC)

	def blockGrid(self):
		#creates an array of blocks
		self.block=[]
		for xB in range(self.maxXB):
			self.block.append([])
			for yB in range(self.maxYB):
				self.block[xB].append(super().create_rectangle(xB*self.ww+snkG,  yB*self.ww+snkG,  (xB+1)*self.ww-snkG,  (yB+1)*self.ww-snkG,  fill=self.bc, outline=self.bc))

	def grid(self,c):
		#create a grid
		#c: grid color
		for x in range(self.ww,self.width,self.ww):
			super().create_line(x, 0, x, self.height, fill=c)
		for y in range(self.ww,self.height,self.ww):
			super().create_line(0, y, self.width, y, fill=c)

	def fillBlock(self,xB,yB,c):
		#change color to a block
		#xB,yB: block coordinates
		#c: fill color
		super().itemconfig(self.block[xB][yB], fill=c, outline=c)

	def refresh(self):
		#refresh the snake
		l=len(self.pos)
		self.fillBlock(self.pos[0][0],  self.pos[0][1],  self.bc)
		self.fillBlock(self.pos[l-1][0],  self.pos[l-1][1],  snkC)

	def fw(self):
		#finds the next block 
		if self.keyDir=="d":
			if self.dir!="a":
				self.dir="d"		
				self.right()
			else:
				self.forward()
		elif self.keyDir=="s":
			if self.dir!="w":
				self.dir="s"
				self.down()
			else:
				self.forward()
		elif self.keyDir=="a":
			if self.dir!="d":
				self.dir="a"
				self.left()
			else:
				self.forward()
		elif self.keyDir=="w":
			if self.dir!="s":
				self.dir="w"
				self.up()
			else:
				self.forward()
		else:					#if you type anyother key
			self.forward()

	def forward(self):
		#keeps going on the last direction	
		if self.dir=="d":
			self.right()
		elif self.dir=="s":
			self.down()
		elif self.dir=="a":
			self.left()
		elif self.dir=="w":
			self.up()	
		else:
			print ("error 404")

	def right(self):
		l=len(self.pos)	
		xB=self.pos[l-1][0]+1  # x+=1
		yB=self.pos[l-1][1]
		self.check(xB,yB)

	def down(self):
		l=len(self.pos)	
		xB=self.pos[l-1][0]
		yB=self.pos[l-1][1]+1  # y+=1
		self.check(xB,yB)

	def left(self):
		l=len(self.pos)	
		xB=self.pos[l-1][0]-1  #x-=1
		yB=self.pos[l-1][1]
		self.check(xB,yB)
		
	def up(self):
		l=len(self.pos)	
		xB=self.pos[l-1][0]
		yB=self.pos[l-1][1]-1  #y-=1
		self.check(xB,yB)

	def check(self,xB,yB):
		#xB,yB next block
		if xB<0 or xB>self.maxXB-1 or yB <0 or yB>self.maxYB-1:		#if you touch the borders	
			self.dead=1												#you die
		elif [xB,yB] in self.pos[1:]:							#if you touch yourself
			self.dead=1												#you die
		elif xB==self.apple[0] and yB==self.apple[1]:			#if you eat an apple
			if self.tick>self.mTick:								#if max speed isn't reached
				self.tick-=self.sTick									#goes faster
			self.pos.append([xB,yB])								#Add a block forward
			self.nextApple()
		else:													#if you do nothing
			del self.pos[0]											#Delete your last block
			self.pos.append([xB,yB])								#Add a block forward

	def nextApple(self):
		#randomly spawn the next apple
		x=random.randint(0,self.maxXB-1)
		y=random.randint(0,self.maxYB-1)
		if [x,y] in self.pos:									#If theres the snake on the next apple
			if len(self.pos)==(self.maxXB)*(self.maxYB): 		#If there aren't empty spaces
				self.dead=2												#You Win !!!
			else:
				self.nextApple()
		else:
			self.apple=[x,y]
			self.fillBlock(self.apple[0],  self.apple[1],  appleC)

	def keyPress(self, e):
		self.keyDir = e.keysym




def loop():
	l=len(snk.pos)
	if snk.dead==1:				#If your dead
		for i in range(1,l):
			snk.fillBlock(snk.pos[i][0],  snk.pos[i][1], lostC)
		if snk.hsc<l-4:			#refresh the highscore
			snk.hsc=l-4
		print ("Score: "+str(l-4))
		print ("Speed: "+str(snk.tick)+"ms per tick")
		gameOver()
	elif snk.dead==2:				#If You Won
		for x in range(snk.maxXB):		#Fill the screen with purple
			for y in range(snk.maxYB):
				snk.fillBlock(x,y,winC)
		print ("You WIN!!!  GGWP")
		gameOver(1)
	else:							#If your alive
		snk.after(snk.tick, loop)		#wait before recalling loop
		#autowin()												#uncomment for autowin
		snk.fw()						
		snk.refresh()

def gameOver(win=0):	
	global score
	global replay
	global over	
	if win==1:
		over = tk.Label(w, text="YOU WIN !!!", font=("Helvetica", 20), fg=winC, )
	else:
		over = tk.Label(w, text="GAME OVER", font=("Helvetica", 16), fg="red3", )
	over.pack()
	if len(snk.pos)-4==0:
		txt="a=left, w=up, d=right, s=down (CAPS Sensitive)"
	else:
		txt="Score: "+str(len(snk.pos)-4)+"    Highscore: "+str(snk.hsc)
	score= tk.Label(w, text=txt, font=("Helvetica", 14))
	score.pack()
	replay=tk.Button(w, text="Play Again", font=("Helvetica", 14), fg="green4", bg="grey85", command=restart)
	replay.pack()

def restart():
	score.pack_forget()
	replay.pack_forget()
	over.pack_forget()
	snk.reset()
	loop()

#in a 20x20 blocks screen at wich block you have to turn (same thing as autowin)
#a=[[18, 2], [18, 4], [18, 6], [18, 8], [18, 10], [18, 12], [18, 14], [18, 16], [18, 18], [19, 0]]
#s=[[18, 1], [0, 2], [18, 3], [0, 4], [18, 5], [0, 6], [18, 7], [0, 8], [18, 9], [0, 10], [18, 11], [0, 12], [18, 13], [0, 14], [18, 15], [0, 16], [18, 17], [0, 18], [0, 0]]
#d=[[0, 3], [0, 5], [0, 7], [0, 9], [0, 11], [0, 13], [0, 15], [0, 17], [0, 19], [0, 1]]
#w=[[19, 19]]

def autowin():					#automatic snake (works only in even number of blocks grid(es: 20x20))
	p=snk.pos[len(snk.pos)-1]
	if p[0]==snk.maxXB-1:
		if p[1]==snk.maxYB-1:
			snk.keyDir="w"
		elif p[1]==0:
			snk.keyDir="a"
		pass
	elif p[0]==0:
		if p[1]%2==1:
			snk.keyDir="d"
		else:
			snk.keyDir="s"
		pass
	elif p[0]==snk.maxXB-2:
		if p[1]%2==0 and p[1]!=0:
			snk.keyDir="a"
		elif p[1]!=snk.maxYB-1 and p[1]!=0:
			snk.keyDir="s"


w=tk.Tk() 
w.title("Snake")
w.resizable(False, False)
snk = Snake(gg,gC,bC)     #grey1=blackest grey,   grey99=whitest grey
snk.pack()
loop()
w.mainloop()