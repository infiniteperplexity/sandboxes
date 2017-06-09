import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
path = "C:/Users/M543015/Desktop/GitHub/sandboxes/pymc"
#https://link.springer.com/article/10.1007%2Fs10508-016-0923-z
#7 out of 34 identified as other than straight 
#10 had same-sex attraction
#6 were attracted to both sexes
#use fake data for now?

xc = 0
xt = 7
ssize = 34
control = np.array([i<xc for i in range(ssize)]).astype(int)
treatment = np.array([i<xt for i in range(ssize)]).astype(int)

#priors
pc = pm.Uniform('pc',0.0,1.0)
pt = pm.Uniform('pt',0.0,1.0)
bc = pm.Binomial('bc',n=ssize,p=pc,value=xc,observed=True)
bt = pm.Binomial('bt',n=ssize,p=pt,value=xt,observed=True)
mc = pm.Model([pc,bc])
mt = pm.Model([pt,bt])

mcc = pm.MCMC(mc)
mcc.sample(iter=50000,burn=10000)
mct = pm.MCMC(mt)
mct.sample(iter=50000,burn=10000)
ratios = pt.trace()/pc.trace()
plt.hist(ratios, range=(0,5), bins=100)