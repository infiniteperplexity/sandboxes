import pymc as pm
import numpy as np
import matplotlib.pyplot as plt

#path = "C:/Users/M543015/Desktop/GitHub/sandboxes/pymc/"
path = "C:/Users/Glenn Wright/Documents/GitHub/sandboxes/pymc/"
import csv

with open(path+"Survey_CSV.csv") as f:
	reader = csv.reader(f)
	indata = [row for row in reader]
	headers = indata[0]
	data = indata[1:]

for n, item in enumerate(headers):
	print(n, item)

dancer = [row[62] for row in data]
mask = [row[65] for row in data]
gender = [row[4] for row in data]


def freq(lst):
	freqs = {}
	values = list(set(lst))
	for value in values:
		freqs[value] = 0

	for item in lst:
		freqs[item]+=1

	for value in freqs:
		freqs[value] = (freqs[value],round(freqs[value]/len(lst),3))

	return freqs


freq(dancer)
freq(mask)
freq(gender)

weakdancer = (
	'I was able to see the dancer as spinning in either direction, or even switch between them at will',
	'I was eventually able to see the dancer as spinning in either direction, or even switch between them at will'
)

weakmask = (
	'I can see it as either of these two, or it seems to switch back and forth',
	'A Einstein mask facing away from the viewer, as if it were ready to fit onto your own face'
)

transf = 'F (transgender m -> f)'
transm = 'M (transgender f -> m)'
trans = (transf,transm)

schizo = [row[68] for row in data]
autism = [row[69] for row in data]

freq(schizo)
freq(autism)

condition = (
	'I think I might have this condition, although I have never been formally diagnosed',
	'I have a formal diagnosis of this condition'
)

def model(q1, vals1, q2, vals2):
	col1 = [row[q1] for row in data]
	col2 = [row[q2] for row in data]
	n1_0 = len([value for value in col1 if value not in vals1])
	n1_1 = len([value for value in col1 if value in vals1])
	n2_0 = len([row for row in data if row[q1] not in vals1 and row[q2] in vals2])
	n2_1 = len([row for row in data if row[q1] in vals1 and row[q2] in vals2])
	p0 = pm.Uniform('p0',0.0,1.0)
	p1 = pm.Uniform('p1',0.0,1.0)
	b0 = pm.Binomial('0',n=n1_0, p=p0,value=n2_0,observed=True)
	b1 = pm.Binomial('b1',n=n1_1, p=p1,value=n2_1,observed=True)
	m0 = pm.Model([p0,b0])
	m1 = pm.Model([p1,b1])
	mc0 = pm.MCMC(m0)
	mc0.sample(iter=50000,burn=10000)
	mc1 = pm.MCMC(m1)
	mc1.sample(iter=50000,burn=10000)
	ratios = mc0.trace('p0')[:, None]/mc1.trace('p1')[:, None]
	print(sum(ratios)/len(ratios))
	plt.hist(ratios)
	table = [(i, sum(ratio>i for ratio in ratios)/len(ratios)) for i in range(1,2,0.1)]
	print table
