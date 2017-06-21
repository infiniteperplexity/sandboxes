import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
#https://link.springer.com/article/10.1007%2Fs10508-016-0923-z
#7 out of 34 identified as other than straight 
#10 had same-sex attraction
#6 were attracted to both sexes
#use fake data for now?

xu = 0
xe = 7
ssize = 34

#priors
pu = pm.Uniform('pu',0.0,0.2)
pe = pm.Uniform('pe',0.0,0.2)

#@pm.stochastic(dtype=float)
#def pt(value=)

bu = pm.Binomial('bu',n=ssize,p=pu,value=xu,observed=True)
be = pm.Binomial('be',n=ssize,p=pe,value=xe,observed=True)
mu = pm.Model([pu,bu])
me = pm.Model([pe,be])

mcu = pm.MCMC(mu)
mcu.sample(iter=50000,burn=10000)
mce = pm.MCMC(me)
mce.sample(iter=50000,burn=10000)
ratios = pe.trace()/pu.trace()
plt.hist(ratios, range=(0,10), bins=100)


#set up data for logistic model
control = [i<xu for i in range(ssize)]
treatment = [i<xe for i in range(ssize)]
obs = np.array(control+treatment).astype(int)
ex = np.array([i>=ssize for i in range(2*ssize)]).astype(int)

#set up logistic model
baserate = 0.035
intercept = np.log(1/baserate-1)
nb = 0.001
na = 1/(intercept*intercept)
beta = pm.Normal("beta",0,nb, value=0)
alpha = pm.Normal("alpha", intercept, na, value=0)

@pm.deterministic
def p(ex=ex, alpha=alpha, beta=beta):
    return 1.0/(1.0+np.exp(alpha-beta*ex))

bern = pm.Bernoulli("bern", p, value=obs, observed=True)
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
plt.hist(odds, range=(0,50), bins=50)
plt.hist(ratios, range=(0,10), bins=25)

sum([1 for i in risks if i>1])/len(risks)
#99.49%
sum([1 for i in risks if i>2])/len(risks)
#91.66%
sum([1 for i in risks if i>5])/len(risks)
#44.67%
sum([1 for i in risks if i>10])/len(risks)
