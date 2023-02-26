import numpy as np
import os
import time
def raw_data():
	with open("aoc9.txt","r") as f:
		lines=f.readlines()
		for line in lines:
			x,y=line.strip().split(" ")
			yield x,int(y)
steps=(list(raw_data()))
#steps=[("R",5),("U",8),("L",8),("D",3),("R",17),("D",10),("L",25),("U",20)]
def find_bbox(steps):
	x,y=0,0
	bounds={'R': ('x', 1), 'L': ('x', -1), 'U': ('y', 1), 'D': ('y', -1)}
	high, low = {}, {"x":0,"y":0}
	for step,n in steps:
		axis,direction=bounds[step]
		if axis=="x":
			x+=direction*n
			high[axis]=max(high.get(axis,x),x)
			low[axis]=min(low.get(axis,x),x)
		else:
			y+=direction*n
			high[axis]=max(high.get(axis,y),y)
			low[axis]=min(low.get(axis,y),y)
	x_axis=high["x"]-low["x"]
	y_axis=high["y"]-low["y"]
	center=abs(high["y"]),abs(low["x"])
	return y_axis+1,x_axis+1,center
h,w,origin=find_bbox(steps)
sigma=0
def add_tup(x,y):
	return tuple(map(lambda i,j:i+j,x,y))
def sub_tup(x,y):
	return tuple(map(lambda i,j:i-j,x,y))
class Head:
	def __init__(self,origin):
		self.coord=origin
class Tail:
	checks=[(i,j) for i in range(-1,2) for j in range(-1,2)]
	def __init__(self,head,origin):
		self.head=head
		self.coord=origin
	def close_to_head(self):
		if sub_tup(self.head.coord,self.coord) in self.checks:
			return True
		return False
	def update(self):
		sameaxis=[(0,2),(2,0),(-2,0),(0,-2),(2,2),(-2,2),(-2,-2),(2,-2)]
		if self.close_to_head():
			return
		dist=sub_tup(self.head.coord,self.coord)
		if dist in sameaxis:
			self.coord=add_tup(self.coord,tuple(map(lambda i:i//2,dist)))
			return
		tis=tuple(map(lambda i:-1 if i<0 else 1,dist))
		self.coord=add_tup(self.coord,tis)
		return
for x,y in steps:
	sigma+=y
arr=np.full((h,w),".")
steps_n=0
cumsum=0
direction={"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}
tail_visit=set()
def display(arr):
	os.system("clear")
	print("\n".join(["".join([n for n in row])for row in arr]))
class Rope:
	def __init__(self,origin):
		self.head=Head(origin)
		self.tails=[]
		current=self.head
		for _ in range(9):
			tail=Tail(current,origin)
			self.tails.append(tail)
			current=tail
		self.endtail=tail
	def move(self,where):
		arr[self.head.coord]="."
		tail_visit.add(self.endtail.coord)
		self.head.coord=add_tup(self.head.coord,direction[where])
		for i,obj in enumerate(self.tails):
			arr[obj.coord]="."
			obj.update()
			arr[obj.coord]=str(i+1)
		tail_visit.add(self.endtail.coord)
		for c in tail_visit:
			arr[c]="#"
		arr[obj.coord]=str(i+1)
		arr[self.head.coord]="H"
R=Rope(origin)
arr[R.head.coord]="H"
def update(frame):
	global steps_n,cumsum
	if frame==cumsum+steps[steps_n][1]-1:
		R.move(steps[steps_n][0])
		cumsum+=steps[steps_n][1]
		steps_n+=1
	else:
		R.move(steps[steps_n][0])
time.sleep(1)
for frame in range(sigma):
	update(frame)
	if (h-R.head.coord[0]>24 or R.head.coord[0]>24):
		i=R.head.coord[0]-25
		j=R.head.coord[0]+25
	if (w-R.head.coord[1]>29 or R.head.coord[1]>29):
		n=R.head.coord[1]-29
		m=R.head.coord[1]+30
	if h-R.head.coord[0]<25:
		i=h-50
		j=h
	if w-R.head.coord[1]<30:
		n=w-60
		m=w
	if R.head.coord[0]<25:
		i=0
		j=51
	if R.head.coord[1]<30:
		n=0
		m=60
	display([arr[x][n:m] for x in range(i,j)])
	print(f"Number of blocks that  end tail,9, visited:{len(tail_visit)}")
	print(f"Step {steps_n}/2000")
	time.sleep(0.2)
print(h,w)