import sys
import heapq

def bus(test):
	l = [s for s in test.strip().split(';')]

	path = l[0].strip('()').split(',')

	routes = {}
	for i in range(1, len(l)):
		a, b = l[i].split('=')
		routes[a.strip()] = b.strip('[]').split(',')

	g = {}

	for r in routes:
		p = routes[r]
		for i in range(len(p)):
			if p[i] not in g:
				if i == 0:
					g[p[i]] = [(r, p[1])]
				elif i == len(p)-1:
					g[p[i]] = [(r, p[i-1])]
				else:
					g[p[i]] = [(r, p[i-1]), (r, p[i+1])]
			else: 
				if i == 0:
					g[p[i]].append((r, p[1]))
				elif i == len(p)-1:
					g[p[i]].append((r, p[i-1]))
				else:
					g[p[i]].append((r, p[i-1]))
					g[p[i]].append((r, p[i+1]))

	pqueue = []

	heapq.heappush(pqueue, (0, [('', path[0])]))

	opened = []
	inq = [(path[0],'')]
	cost = {}

	nodes = 0

	while pqueue:
		#print pqueue
		p = heapq.heappop(pqueue)[1]
		#print p
		current = p[-1]
		#print current

		opened.append(current[1])
		nodes += 1
		#print current

		if current[1] == path[1]:
			print 'Nodes:', nodes
			return pc(p)

		edges = g[current[1]]

		for r, s in edges:
			if s not in opened:
				#print edge, current
				new_path = list(p)
				new_path.append((r,s))
				path_cost = pc(new_path)
				#print current, edge, path_cost
				if path[1] in routes[r]:
					h = 0
				else: h = 7

				if (s,r) not in inq:
					heapq.heappush(pqueue, (path_cost + h, new_path))
					cost[(s,r)] = path_cost + h
					inq.append((s,r))

				elif cost[(s,r)] > path_cost + h:
					#pqueue.remove((cost[(s,r)], s, r))
					heapq.heappush(pqueue, (path_cost + h, new_path))

	print 'Nodes:', nodes
	
	return 'None'

def pc(path):
	c = (len(path)-1) * 7
	for x in range(len(path)):
		if path[x][0] != path[x-1][0] and x > 1:
			c += 12
	return c

test_cases = open(sys.argv[1], 'r')
for test in test_cases:
    # ignore test if it is an empty line
    # 'test' represents the test case, do something with it
    # ...
    # ...
    if test != '\n':
		print bus(test)

test_cases.close()
	
