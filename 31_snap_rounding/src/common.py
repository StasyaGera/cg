from sortedcontainers import SortedList
from utils import bound
from random import uniform
from structs import Point, Segment, SweepLine as SL

source = [ [(0.9, 4.72), (9.9, 2.3)], [(5.1, 2.0), (3.1, 8.36)] ]
segments  = list(map(lambda s: Segment(
		Point(s[0][0], s[0][1]), 
		Point(s[1][0], s[1][1])
	), source))

def generate_segs(n):
	rand = lambda : uniform(0, bound)
	build_segs([ [(rand(), rand()), (rand(), rand())] for i in range(n) ])

def build_segs(source):
	global segments
	segments.extend(list(map(lambda s: Segment(
		Point(s[0][0], s[0][1]), 
		Point(s[1][0], s[1][1])
	), source)))

hot = []
current = SortedList()
line = SL(segments)
