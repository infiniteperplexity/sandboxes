import pymc as pm
import numpy as np
import matplotlib.pyplot as plt

path = "C:/Users/M543015/Desktop/GitHub/sandboxes/pymc/"

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

ncis = len([value for value in gender if value not in trans])
ntrans = len([value for value in gender if value in trans])
nautism = len([value for value in autism if value in condition])
nschizo = len([value for value in schizo if value in condition])

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