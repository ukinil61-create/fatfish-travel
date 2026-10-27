"""Generative-but-handwritten score: sections at 96 BPM (2.5 s per 4/4 bar), rendered with FluidSynth."""
import mido, random, sys, json
BPM=96; TPB=480; BAR=4*TPB
random.seed(5)
CH={'box':(0,10),'piano':(1,0),'pizz':(2,45),'str':(3,48),'harp':(4,46),'flute':(5,73),'bass':(6,32),'glock':(7,9),'horn':(8,60),'celesta':(10,8),'timp':(11,47),'str2':(12,49)}
CHORD={'F':(41,[53,57,60]),'C/E':(40,[55,60,64]),'Dm':(38,[50,53,57]),'Bb':(34,[50,53,58]),'F/A':(45,[53,57,60]),'Gm7':(43,[50,53,58]),
 'C7sus':(36,[53,55,58]),'C7':(36,[52,55,58]),'C':(36,[52,55,60]),'Am':(33,[52,57,60]),'F7':(41,[51,57,60]),'Db':(37,[53,56,61]),
 'Eb':(39,[55,58,63]),'Fsus':(41,[53,58,60]),'Fmaj7':(41,[52,57,60,64]),'Gm':(43,[50,55,58])}
N=lambda s:{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[s[0]]+(1 if '#' in s else -1 if 'b' in s[1:] else 0)+12*(int(s[-1])+1)
def mel(spec):  # "A4:1 C5:1 F5:1.5 E5:.5" ; R = rest
    out=[];t=0
    for tok in spec.split():
        n,d=tok.split(':');d=float(d)
        if n!='R':out.append((N(n),t,d))
        t+=d
    return out
A_MEL=[mel('A4:1 C5:1 F5:1.5 E5:.5'),mel('D5:1 C5:1 G4:2'),mel('A4:1 D5:1 F5:1 E5:.5 D5:.5'),mel('C5:3 R:1'),
       mel('A4:1 C5:1 F5:1 G5:1'),mel('A5:1.5 G5:.5 F5:1 D5:1'),mel('F5:1 E5:1 D5:1 C5:1'),mel('E5:3 R:1')]
A_END=mel('F5:4')
A_PROG=['F','C/E','Dm','Bb','F/A','Gm7','C7sus','C7']
B_MEL=[mel('F5:1.5 D5:.5 F5:1 Bb5:1'),mel('A5:2 G5:1 E5:1'),mel('E5:1.5 C5:.5 E5:1 A5:1'),mel('G5:1 F5:1 D5:2'),
       mel('D5:1 G5:1 Bb5:1 A5:1'),mel('G5:1.5 F5:.5 E5:1 C5:1'),mel('A5:1 G5:1 F5:1 C6:1'),mel('A5:3 R:1'),
       mel('F5:1.5 D5:.5 F5:1 Bb5:1'),mel('C6:2 Bb5:1 A5:1'),mel('G5:1.5 E5:.5 G5:1 C6:1'),mel('A5:1 G5:1 F5:2'),
       mel('D5:1 G5:1 Bb5:1 D6:1'),mel('C6:1.5 Bb5:.5 A5:1 G5:1'),mel('F5:1 A5:1 C6:1 F6:1'),mel('E6:2 F6:2')]
B_PROG=['Bb','C','Am','Dm','Gm','C','F','F7','Bb','C','Am','Dm','Gm','C7','F','F']
CL_MEL=[mel('F5:2 Ab5:1 Db6:1'),mel('Eb6:2 Db6:1 Bb5:1'),mel('C6:4'),mel('A5:2 C6:1 F6:1')]
CL_PROG=['Db','Eb','Fsus','F']

class Song:
    def __init__(s):s.ev=[]  # (tick, kind, ch, a, b)
    def note(s,inst,p,t,d,v):
        ch=CH[inst][0];v=max(1,min(127,int(v+random.randint(-5,5))));t=max(0,int(t+random.randint(-6,6)))
        s.ev.append((t,1,ch,p,v));s.ev.append((t+max(10,int(d)),0,ch,p,0))
    def dr(s,p,t,v):
        s.ev.append((max(0,int(t+random.randint(-5,5))),1,9,p,max(1,min(127,int(v+random.randint(-6,6))))));s.ev.append((int(t)+60,0,9,p,0))
    def cc(s,inst,t,num,val):s.ev.append((int(t),2,CH[inst][0],num,int(val)))
    def write(s,path):
        m=mido.MidiFile(ticks_per_beat=TPB);tr=mido.MidiTrack();m.tracks.append(tr)
        tr.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM),time=0))
        for k,(ch,prog) in CH.items():
            tr.append(mido.Message('program_change',channel=ch,program=prog,time=0))
            tr.append(mido.Message('control_change',channel=ch,control=91,value=70 if k not in('bass','timp') else 40,time=0))
            tr.append(mido.Message('control_change',channel=ch,control=93,value=20,time=0))
            tr.append(mido.Message('control_change',channel=ch,control=7,value={'box':100,'piano':88,'pizz':80,'str':78,'harp':86,'flute':70,'bass':92,'glock':62,'horn':84,'celesta':72,'timp':90,'str2':70}[k],time=0))
            tr.append(mido.Message('control_change',channel=ch,control=10,value={'box':70,'piano':58,'pizz':40,'str':64,'harp':86,'flute':50,'bass':64,'glock':80,'horn':54,'celesta':76,'timp':64,'str2':70}[k],time=0))
        ev=sorted(s.ev,key=lambda e:(e[0],e[1]));last=0
        for t,k,ch,a,b in ev:
            dt=t-last;last=t
            if k==1:tr.append(mido.Message('note_on',channel=ch,note=a,velocity=b,time=dt))
            elif k==0:tr.append(mido.Message('note_off',channel=ch,note=a,velocity=0,time=dt))
            else:tr.append(mido.Message('control_change',channel=ch,control=a,value=b,time=dt))
        tr.append(mido.MetaMessage('end_of_track',time=TPB*8))
        m.save(path)

def melody(S,t0,notes,inst,vel,oct=0,legato=.95):
    for p,b,d in notes:S.note(inst,p+12*oct,t0+b*TPB,d*TPB*legato,vel)
def piano_arp(S,t0,ch,vel,style='arp'):
    bass,tones=CHORD[ch]
    S.note('piano',bass+12 if bass<40 else bass,t0,BAR*.98,vel+6)
    seq=[tones[0],tones[1],tones[2],tones[1]+12,tones[2]+12,tones[1]+12,tones[2],tones[1]] if style=='arp' else []
    for i,p in enumerate(seq):
        if i==0:continue
        S.note('piano',p,t0+i*TPB/2,TPB*1.6,vel-6+(4 if i==4 else 0))
    if style=='off':
        for b in (1,3):
            for p in tones:S.note('piano',p+12,t0+b*TPB+TPB/2*0,TPB*.45,vel-4)
        for b in (1.5,3.5):
            for p in tones:S.note('piano',p+12,t0+b*TPB,TPB*.3,vel-12)
def pad(S,t0,ch,vel,bars=1,inst='str'):
    bass,tones=CHORD[ch]
    for p in tones:S.note(inst,p,t0,BAR*bars*.99,vel)
    S.note(inst,bass+12,t0,BAR*bars*.99,vel-8)
def pizz(S,t0,ch,vel,busy=False):
    bass,tones=CHORD[ch]
    S.note('pizz',bass+12,t0,TPB*.5,vel+6);S.note('pizz',tones[0]+12 if bass<40 else bass+19,t0+2*TPB,TPB*.5,vel)
    if busy:
        S.note('pizz',tones[1]+12,t0+1.5*TPB,TPB*.4,vel-10);S.note('pizz',tones[2]+12,t0+3.5*TPB,TPB*.4,vel-10)
def bassline(S,t0,ch,vel):
    bass,_=CHORD[ch];b=bass if bass>=36 else bass+12
    S.note('bass',b,t0,TPB*1.8,vel);S.note('bass',b+7 if b+7<52 else b-5,t0+2*TPB,TPB*1.4,vel-8);S.note('bass',b+12 if b<43 else b,t0+3.5*TPB,TPB*.4,vel-16)
def groove(S,t0,vel,kick=True):
    for i in range(8):S.dr(82,t0+i*TPB/2,vel-(8 if i%2 else 0))
    if kick:S.dr(35,t0,vel+14);S.dr(35,t0+2*TPB,vel+4)
def harp_gliss(S,t0,ch,vel,up=True,length=TPB*2,low=53,high=89):
    _,tones=CHORD[ch];pcs={p%12 for p in tones}
    ps=[p for p in range(low,high) if p%12 in pcs]
    if not up:ps=ps[::-1]
    for i,p in enumerate(ps):S.note('harp',p,t0+i*length/len(ps),TPB*2,vel-6+i*0.3)
def glock(S,t0,p,vel):S.note('glock',p,t0,TPB,vel)

def build(sections,path):
    S=Song();t=0;marks=[]
    for name,nb,opt in sections:
        marks.append({'name':name,'bar':int(t/BAR),'bars':nb,'t':t/BAR*2.5})
        for i in range(nb):
            b0=t+i*BAR
            if name=='intro':  # music box alone + soft harp rolls
                k=opt.get('start',0)+i;ch=A_PROG[k%8]
                melody(S,b0,A_MEL[k%8],'box',78)
                if i%2==0:harp_gliss(S,b0,ch,44,length=TPB,low=41,high=72)
                pad(S,b0,ch,30,1,'str2')
            elif name=='home':
                k=opt.get('start',0)+i;ch=A_PROG[k%8]
                melody(S,b0,A_MEL[k%8],'box',84);piano_arp(S,b0,ch,52)
                if i>=4:pad(S,b0,ch,36)
                if i%4==0:glock(S,b0,84,40)
            elif name=='game':
                k=opt.get('start',0)+i;ch=A_PROG[k%8]
                melody(S,b0,A_MEL[k%8],'box',86);melody(S,b0,A_MEL[k%8],'celesta',50,oct=1)
                piano_arp(S,b0,ch,48,'off');pizz(S,b0,ch,64,busy=True);bassline(S,b0,ch,62);groove(S,b0,38,kick=i>0)
            elif name=='leave':
                k=opt.get('start',6)+i;ch=A_PROG[k%8]
                melody(S,b0,A_MEL[k%8],'box',88);piano_arp(S,b0,ch,54);pad(S,b0,ch,40+i*12)
                if i==nb-1:
                    harp_gliss(S,b0+2*TPB,ch,70,length=TPB*2,low=53,high=96)
                    for j in range(8):S.note('str',60+j,b0+2*TPB+j*TPB/4,TPB/4,50+j*4)
                    S.dr(49,b0+3.75*TPB,34)
            elif name=='travel':
                k=opt.get('start',0)+i;ch=B_PROG[k%16];m=B_MEL[k%16]
                melody(S,b0,m,'box',90);melody(S,b0,m,'celesta',56,oct=0)
                if k>=8:melody(S,b0,m,'flute',58,oct=-1)
                piano_arp(S,b0,ch,50);pad(S,b0,ch,44);pizz(S,b0,ch,56);bassline(S,b0,ch,66);groove(S,b0,36)
                if i%2==0:glock(S,b0,CHORD[ch][1][-1]+24,46);S.dr(81,b0,40)
                if opt.get('per_bar_sparkle'):glock(S,b0,CHORD[ch][1][-1]+24,40)
            elif name=='climax':
                k=opt.get('start',0)+i;ch=CL_PROG[k%4];m=CL_MEL[k%4]
                melody(S,b0,m,'horn',84,oct=-1);melody(S,b0,m,'box',92);melody(S,b0,m,'str2',62)
                pad(S,b0,ch,54+i*5);bassline(S,b0,ch,70)
                for j in range(16):S.note('timp',CHORD[ch][0]-12 if CHORD[ch][0]>=40 else CHORD[ch][0],b0+j*TPB/4,TPB/4,32+j*(1.6 if i==0 else .8))
                harp_gliss(S,b0,ch,62,length=TPB*1.5,low=48,high=96)
                piano_arp(S,b0,ch,56)
                if i==0:S.dr(49,b0,70)
                S.dr(35,b0,80);S.dr(35,b0+2*TPB,66)
            elif name=='outro':
                k=opt.get('start',0)+i;last=i==nb-1
                ch='F' if last else A_PROG[k%8];m=A_END if last else A_MEL[k%8]
                melody(S,b0,m,'box',82);melody(S,b0,m,'celesta',44,oct=1)
                piano_arp(S,b0,ch,48-i*2);pad(S,b0,ch,40)
                if i<nb-2:pizz(S,b0,ch,48)
                if last:harp_gliss(S,b0+TPB,'Fmaj7',56,length=TPB*2.5,low=53,high=101)
            elif name=='ring':
                pad(S,b0,'Fmaj7',36,1);S.note('piano',41,b0,BAR,40);glock(S,b0,89,36);glock(S,b0+TPB*1.5,96,30)
        t+=nb*BAR
    S.write(path);return marks,t/BAR*2.5

if __name__=='__main__':
    H=[('intro',4,{}),('home',8,{}),('game',8,{}),('leave',2,{'start':6}),('travel',16,{}),('climax',4,{}),('outro',8,{}),('ring',2,{})]
    V=[('intro',2,{}),('home',6,{'start':2}),('game',4,{}),('leave',2,{'start':6}),('travel',8,{'start':8,'per_bar_sparkle':True}),('climax',2,{'start':0}),('outro',4,{'start':4}),('ring',1,{})]
    mh,dh=build(H,'h.mid');mv,dv=build(V,'v.mid')
    build([('home',8,{}),('travel',16,{}),('home',8,{}),('travel',16,{}),('home',2,{})],'loop.mid')
    json.dump({'h':{'marks':mh,'dur':dh},'v':{'marks':mv,'dur':dv}},open('marks.json','w'),indent=1)
    print('h',dh,'v',dv)
