import pymc as pm
import numpy as np
import matplotlib.pyplot as plt

path = "C:/Users/M543015/Desktop/GitHub/sandboxes/pymc/"
#path = "C:/Users/Glenn Wright/Documents/GitHub/sandboxes/pymc/"
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
sjid = [row [27] for row in data]
polaff = [row[29] for row in data]
ampart = [row[31] for row in data]


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
	ratios = mc1.trace('p1')[:, None]/mc0.trace('p0')[:, None]
	print(sum(ratios)/len(ratios))
	plt.gcf().clear()
	plt.hist(ratios)
	table = [(i, len([ratio for ratio in ratios if ratio>i])/len(ratios)) for i in np.arange(1.0,3.1,0.1)]
	print(table)

model(4,trans,62,weakdancer)
model(4,trans,65,weakmask)
model(68,condition,62,weakdancer)
model(68,condition,65,weakmask)
model(69,condition,62,weakdancer)
model(69,condition,65,weakmask)



usedata = [(row[65] in weakmask, int(row[30])) for row in data if row[30] != ' ']
libmask = [row[0] for row in usedata]
liberal = [11-row[1] for row in usedata]


#set up logistic model
beta = pm.Normal("beta",0,0.001, value=0)
alpha = pm.Normal("alpha",0,0.001, value=0)

@pm.deterministic
def p(pol=liberal, alpha=alpha, beta=beta):
    return 1.0/(1.0+np.exp(alpha-beta*pol))

bern = pm.Bernoulli("bern", p, value=libmask, observed=True)
model = pm.Model([bern, beta, alpha])
map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(120000,100000,2)
alphas = mcmc.trace('alpha')[:, None]
base = 1/(1+np.exp(alphas))
plt.hist(base, range=(0,0.1),bins=25)
betas = mcmc.trace('beta')[:, None]
odds = np.exp(betas)
print(sum(odds)/len(odds))
plt.gcf().clear()
plt.hist(odds)


"""
#older code, not generalized

dancer = [row[62] for row in data]
mask = [row[65] for row in data]
gender = [row[4] for row in data]

ncis = len([value for value in gender if value not in trans])
ntrans = len([value for value in gender if value in trans])

ncisweakmask = len([row for row in data if row[4] not in trans and row[65] in weakmask])
ntransweakmask = len([row for row in data if row[4] in trans and row[65] in weakmask])

pmaskcis = pm.Uniform('pmaskcis',0.0,1.0)
pmasktrans = pm.Uniform('pmasktrans',0.0,1.0)

binmaskcis = pm.Binomial('binmaskcis',n=ncis, p=pmaskcis,value=ncisweakmask,observed=True)
binmasktrans = pm.Binomial('binmasktrans',n=ntrans, p=pmasktrans,value=ntransweakmask,observed=True)

modelmaskcis = pm.Model([pmaskcis,binmaskcis])
modelmasktrans = pm.Model([pmasktrans,binmasktrans])

mcmaskcis = pm.MCMC(modelmaskcis)
mcmaskcis.sample(iter=50000,burn=10000)
mcmasktrans = pm.MCMC(modelmasktrans)
mcmasktrans.sample(iter=50000,burn=10000)
ratios = mcmasktrans.trace('pmasktrans')[:, None]/mcmaskcis.trace('pmaskcis')[:, None]
plt.hist(ratios)

sum(ratio>1 for ratio in ratios)/len(ratios)
sum(ratio>1.5 for ratio in ratios)/len(ratios)
sum(ratio>2 for ratio in ratios)/len(ratios)

sum(ratios)/len(ratios)


ncisweakdancer = len([row for row in data if row[4] not in trans and row[62] in weakdancer])
ntransweakdancer = len([row for row in data if row[4] in trans and row[62] in weakdancer])

pdancercis = pm.Uniform('pdancercis',0.0,1.0)
pdancertrans = pm.Uniform('pdancertrans',0.0,1.0)


bindancercis = pm.Binomial('bindancercis',n=ncis, p=pdancercis,value=ncisweakdancer,observed=True)
bindancertrans = pm.Binomial('bindancertrans',n=ntrans, p=pdancertrans,value=ntransweakdancer,observed=True)

modeldancercis = pm.Model([pdancercis,bindancercis])
modeldancertrans = pm.Model([pdancertrans,bindancertrans])

mcdancercis = pm.MCMC(modeldancercis)
mcdancercis.sample(iter=50000,burn=10000)
mcdancertrans = pm.MCMC(modeldancertrans)
mcdancertrans.sample(iter=50000,burn=10000)
ratios = mcdancertrans.trace('pdancertrans')[:, None]/mcdancercis.trace('pdancercis')[:, None]
plt.hist(ratios)

sum(ratio>1 for ratio in ratios)/len(ratios)
sum(ratio>1.1 for ratio in ratios)/len(ratios)
sum(ratio>1.2 for ratio in ratios)/len(ratios)
sum(ratio>1.3 for ratio in ratios)/len(ratios)

sum(ratios)/len(ratios) 

"""