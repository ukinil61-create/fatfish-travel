import numpy as np, wave, sys
SR=48000
def out(mode):
    dur=130 if mode=='h' else 72.5
    N=int(SR*dur);L=np.zeros(N);Rr=np.zeros(N)
    rng=np.random.default_rng(1)
    def put(sig,t,pan=0.0,g=1.0):
        i=int(t*SR);n=min(len(sig),N-i)
        if n<=0:return
        L[i:i+n]+=sig[:n]*g*(1-max(0,pan));Rr[i:i+n]+=sig[:n]*g*(1+min(0,pan))
    tt=lambda d:np.arange(int(d*SR))/SR
    def bell(f,d=1.2,a=.2):
        x=tt(d);return a*(np.sin(2*np.pi*f*x)+.3*np.sin(2*np.pi*2.76*f*x)*np.exp(-x*6))*np.exp(-x*3.5)*np.minimum(1,x/.004)
    def chime(t,base=1046.5,n=5,g=1):
        for k,m in enumerate([0,4,7,12,16][:n]):put(bell(base*2**(m/12),1.6,.12),t+k*.07,pan=(k-2)*.15,g=g)
    def shutter(t):
        x=tt(.09);c1=rng.standard_normal(len(x))*np.exp(-x*90)*.22
        x2=tt(.12);c2=rng.standard_normal(len(x2))*np.exp(-x2*60)*.15
        put(np.convolve(c1,np.ones(6)/6,'same'),t);put(np.convolve(c2,np.ones(10)/10,'same'),t+.07)
    def whoosh(t,d=1.0,g=.25):
        x=tt(d);n=rng.standard_normal(len(x));n=np.convolve(n,np.ones(40)/40,'same');env=np.sin(np.pi*x/d)**2
        put(n*env*g,t,pan=-.2);put(np.roll(n,300)*env*g,t,pan=.2)
    def paper(t,g=.18):
        x=tt(.22);n=rng.standard_normal(len(x));n=n-np.convolve(n,np.ones(8)/8,'same');put(n*np.exp(-x*22)*g,t,pan=rng.uniform(-.4,.4))
    def splash(t,g=.5):
        x=tt(2.6);n=rng.standard_normal(len(x));lo=np.convolve(n,np.ones(60)/60,'same');hi=n-np.convolve(n,np.ones(4)/4,'same')
        env=np.minimum(1,x/.05)*np.exp(-x*1.6);put((lo*1.2+hi*.25)*env*g,t)
        for k in range(30):put(bell(rng.uniform(1800,4200),.25,.04),t+.1+rng.uniform(0,1.6),pan=rng.uniform(-.7,.7))
    def whale(t,d=3.2,g=.22):
        x=tt(d);f=np.interp(x,[0,d*.3,d*.6,d],[180,330,260,210])*(1+.012*np.sin(2*np.pi*5.5*x))
        ph=2*np.cumsum(f)/SR*np.pi;s=np.sin(ph)+.35*np.sin(2*ph)+.15*np.sin(3*ph)
        env=np.sin(np.pi*np.clip(x/d,0,1))**1.5;s=s*env*g
        # cheap reverb tail
        rv=np.zeros(len(s)+SR*2)
        for k,(dl,a) in enumerate([(.031,.5),(.047,.42),(.071,.35),(.113,.28),(.173,.2),(.251,.14),(.37,.1)]):
            j=int(dl*SR);rv[j:j+len(s)]+=s*a
        put(np.concatenate([s,np.zeros(SR*2)])+rv,t,pan=.15)
    if mode=='h':
        chime(1.7,g=.8);whoosh(53.9,1.2,.22)
        for i in range(7):shutter(55+5*i+5-.3)
        splash(97.9);whale(98.3);whale(101.2,2.8,.16)
        whoosh(104.1,1.2,.22)
        for k in range(9):paper(105.05+k*.62)
        chime(119.7,g=.7)
        chime(30+6.6+.8,base=880,n=4,g=.5)  # friend modal in gameplay
        chime(30+3.8+2.2+4.4+4.8+.4,base=1174.7,n=4,g=.5)  # postcard segment
    else:
        chime(.7,g=.8);whoosh(34,1.0,.2)
        for i in range(7):shutter(35+2.5*i+2.5-.28)
        splash(56.2,.45);whale(56.5,2.6,.2)
        whoosh(59.2,1.0,.2)
        for k in range(9):paper(60.05+k*.3,.14)
        chime(66.8,g=.7)
    st=np.stack([L,Rr],1);st=np.clip(st,-1,1)
    with wave.open(f'sfx_{mode}.wav','wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes())
out(sys.argv[1])
