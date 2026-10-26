import glob,os,re,sys
names=[os.path.basename(os.path.dirname(p)) for p in glob.glob('skills/*/*/card.md')]
for p in sys.argv[1:]:
    t=open(p).read(); s=re.sub(r'\(http[^)]*\)','',t); low=s.lower()
    own=os.path.basename(os.path.dirname(p))
    print(p, len(re.findall(r'[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)*',s)))
    for w in ['funnel','prototype','backlog','customer profile','cohort','a/b']:
        if w in low: print('  WORD',w)
    for n in names:
        full=n.replace('_',' ')
        if full.replace(' ','-')==own: continue
        core=full.replace(' model','').replace(' analysis','').replace(' method','').replace(' matrix','').replace(' canvas','').replace(' metrics','').replace(' scoring','')
        for v in {full,core}:
            if len(v)>3 and v in low: print('  TOOL',n,'via',repr(v))
