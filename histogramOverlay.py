import numpy as np
import matplotlib.pyplot as plt

def overlayHist(X, t=None, t_sample=None,window=1,ybins=None, ax=None,
                t_mark=None, overlay=.5,normMax=True):
    """
    t=time points of sample, matches data.shape[1]
    X= data, (samples,timepoints)
    t_sample= timepoints to draw histogram for
    window=window around t_sample to make distribution from
    ybins=bins to make distribution with
    overlay=overlap between histograms, (0,1)
    """
    if type(t)=='NoneType':
        t=np.arange(X.shape[1])
    if type(t_sample)=='NoneType':
        t_sample=np.linspace(min(t),max(t),10)
    if type(ybins)=='NoneType':
        ybins=np.linspace(np.min(X),np.max(X),100)   
    if type(ax)==type(None):
        print('hi')
        fig=plt.figure()
        ax=fig.gca()
    bx=ybins[1:]-ybins[:-1]
    
    pos=0
    yticks=[]
    for i in t_sample:   
        #make histograme
        loc=np.argmin(np.abs(t-i))
        h,p=np.histogram(X[:,max(loc-window,0):min(loc+window,X.shape[1])],bins=ybins) 
        h=h/bx
        h=h/np.sum(h)
        if normMax:
            h=h/h.max()
        p=np.log10(p)
        #define color
        m=X[:,max(loc-window,0):min(loc+window,X.shape[1])].mean()
        m=(m-ybins[0])/(ybins[-1]-ybins[0])*2
        c=plt.cm.magma(m)
        #plot it
        line=np.ones(h.size)*pos
        ax.fill_between(p[1:],line,h+line,facecolor=c, alpha=1,edgecolor='k',lw=1)
        #move position
        yticks.append(pos)
        pos-=overlay
    ax.set_yticks(yticks)
    ax.set_yticklabels(np.round(t_sample,2))
    if not type(t_mark)==type(None):
        s=(t_mark[0]-t_sample[0])/(t_sample[-1]-t_sample[0])*(yticks[-1]-yticks[0])
        e=(t_mark[1]-t_sample[0])/(t_sample[-1]-t_sample[0])*(yticks[-1]-yticks[0])
        ax.fill_between(p[1:],np.ones(h.size)*e,np.ones(h.size)*s,zorder=-10,color='grey',alpha=.6)
    return

