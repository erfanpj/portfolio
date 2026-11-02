"""Port the original Hero 14 vectors into one mobile illustration, then wire the public page."""
import html
import math
import re
from copy import deepcopy
from xml.etree import ElementTree as ET


def mobile_scene(page):
    # The approved drawing already contains the real neuronal paths and laptop.
    # Give them one new, shared coordinate system instead of scaling two screenshots.
    raw = re.findall(r'<svg\b.*?</svg>', page, re.S)
    back, front = ET.fromstring(raw[0]), ET.fromstring(raw[5])
    lens = next(c for c in back if c.tag == 'g' and 'translate' in c.get('transform',''))
    lens.set('transform', 'translate(58 167) scale(.49)')
    # Text stays at reading size in the adjacent HTML list. Numbers remain on the lens.
    for child in list(lens):
        if child.tag == 'g' and child.get('font-size') == '19':
            lens.remove(child)
    new = ET.Element('svg', {'viewBox':'0 0 360 465','class':'mobileSignal','aria-hidden':'true','focusable':'false'})
    for d in back.findall('defs'):
        new.append(deepcopy(d))
    grad = ET.SubElement(new.find('defs'),'linearGradient',{'id':'mobile-cone','gradientUnits':'userSpaceOnUse','x1':'112','y1':'39','x2':'205','y2':'314'})
    for offset,color,opacity in [('0','#f2a541','.47'),('1','#f2a541','.07')]:
        ET.SubElement(grad,'stop',{'offset':offset,'stop-color':color,'stop-opacity':opacity})
    # The cone originates on the photographed cutaway, and its two edges are tangent to the actual lens.
    x,y = 111.6,38.0; cx,cy,r = 205.,314.,142.1
    dx,dy = x-cx,y-cy; d2 = dx*dx+dy*dy
    tx,ty = cx+r*r*dx/d2, cy+r*r*dy/d2
    q = r*math.sqrt(d2-r*r)/d2
    edge1,edge2 = (tx-q*dy,ty+q*dx),(tx+q*dy,ty-q*dx)
    left,right=f'{edge1[0]:.2f},{edge1[1]:.2f}',f'{edge2[0]:.2f},{edge2[1]:.2f}'
    ET.SubElement(new,'path',{'d':f'M{x},{y} L{left} L{right} Z','fill':'url(#mobile-cone)'})
    ET.SubElement(new,'path',{'d':f'M{left} L{x},{y} L{right}','fill':'none','stroke':'#f2a541','stroke-opacity':'.5','stroke-width':'.8'})
    # Reuse the same avatar and the exact head-relative cutaway location as the desktop.
    figure=ET.SubElement(new,'g',{'transform':'translate(-60,-247) scale(.52)'})
    ET.SubElement(figure,'image',{'href':'assets/erfan-avatar.png','x':'170','y':'500','width':'260','height':'283'})
    for c in list(front)[:20]:
        figure.append(deepcopy(c))
    ET.SubElement(figure,'image',{'href':'assets/brain-cutaway-theme.png','x':'304','y':'522','width':'52','height':'52'})
    new.append(lens)
    # Distinct ids also keep hidden desktop defs out of rendering on mobile Safari.
    ids={e.get('id') for e in new.iter() if e.get('id')}
    for e in new.iter():
        for a,v in list(e.attrib.items()):
            if a=='id': e.set(a,'m-'+v)
            else:
                for key in ids: v=v.replace('url(#'+key+')','url(#m-'+key+')')
                e.set(a,v)
    return ET.tostring(new,encoding='unicode',short_empty_elements=False)


MOTIFS=[
    ('Dopamine','Return to the question','An encouraging result makes me want to try the comparison again.'),
    ('Serotonin','Finish a test','There is satisfaction in an experiment that someone else can repeat.'),
    ('Oxytocin','Share the finding','I trust a result more after someone else has had a chance to question it.'),
    ('Endorphins','Enjoy the result','Solving a stubborn problem together feels good.'),
]


def finish(page):
    scene=mobile_scene(page)
    page=re.sub(r'<div class="mobileSceneWrap">.*?(?=<ol class="mobileStepGrid")',
                '<div class="mobileSceneWrap">'+scene+'</div>\n  ', page,count=1,flags=re.S)
    page=page.replace('<link rel="stylesheet" href="styles.css">','''<meta name="theme-color" content="#16151a">
  <link rel="canonical" href="https://erfanpj.com/">
  <meta property="og:url" content="https://erfanpj.com/">
  <meta property="og:image" content="https://erfanpj.com/assets/social-preview.jpg">
  <meta property="og:image:alt" content="Erfan’s illustrated portrait, brain cutaway and six-stage signal diagram">
  <link rel="icon" href="assets/mark.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="refinements.css">''')
    page=page.replace('AI · machine learning · brain exploration','Computer vision · applied machine learning')
    page=page.replace('<a href="#approach">Approach</a>', '<a href="#skills">Skills</a><a href="#approach">Approach</a>')
    page=page.replace('Illustrated process motifs only — not biological or clinical claims.', 'Illustration: a metaphor for how I work.')
    page=page.replace('Process illustration only — not a biological or clinical claim:', 'Four feelings I associate with the process. The chemistry is an illustration.')
    page=page.replace('id="mobile-nav" hidden>', 'id="mobile-nav" hidden>')
    page=page.replace('<div class="sheet" role="dialog" aria-modal="true" aria-label="Site menu">','<nav class="sheet" aria-label="Site menu">')
    page=page.replace('Download CV (PDF)</a>\n    </div>\n  </div>','Download CV (PDF)</a>\n    </nav>\n  </div>')
    page=page.replace('class="case" href="#case-', 'class="case" aria-haspopup="dialog" href="#case-')
    # A real, unscaled masthead retains the original wordmark/nav at all widths.
    # Desktop and phone artwork live below it, independently of keyboard navigation.
    page=re.sub(r'<header class="top"[^>]*>.*?</header>', '', page,count=1,flags=re.S)
    page=re.sub(r'(<div class="mobileHero" id="mobile-hero">)\s*<header>.*?</header>',r'\1',page,count=1,flags=re.S)
    mast='''<header class="masthead"><div class="mast-inner"><a class="brand" href="#home">Erfan Pirjahandideh<span>.</span></a><nav class="wide-nav" aria-label="Primary"><a href="#skills">Skills</a><a href="#approach">Approach</a><a href="#work">Work</a><a href="#log">Progress log</a><a href="#cv">CV</a><a class="contact-link" href="#contact">Contact</a></nav><button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="mobile-nav">Menu</button></div></header>'''
    page=page.replace('<main id="home">',mast+'\n<main id="home">')
    page=page.replace('<div class="mobile-nav-panel" id="mobile-nav" hidden>','<dialog class="mobile-nav-panel" id="mobile-nav" aria-label="Site menu">')
    page=page.replace('Download CV (PDF)</a>\n    </nav>\n  </div>','Download CV (PDF)</a>\n    </nav>\n  </dialog>')
    page=page.replace('<div class="mobileSceneWrap">','<div class="scene-key"><span>Fig. 01 / Signal study</span><button type="button" class="hero-play" id="mobile-hero-play" aria-controls="mobile-hero">Pause scene</button></div><div class="mobileSceneWrap">')
    page=page.replace('href="#home" class="back">', 'href="#home" class="back">')
    def desktop(i):
        name,short,note=MOTIFS[i]
        return f'<span class="tip" id="desk-tip-{i}" role="tooltip"><strong>{name}</strong>{html.escape(note)}</span>'
    # Change the meaning as well as the accessible label: these are Erfan’s metaphors.
    i=iter(range(4))
    page=re.sub(r'<span class="tip"[^>]*>.*?</span>',lambda _:desktop(next(i)),page,count=4,flags=re.S)
    for j,(name,short,note) in enumerate(MOTIFS):
        page=re.sub(rf'(<button type="button" class="hor2 [^"]*hon{j}"[^>]*?)>',rf'\1 aria-expanded="false" aria-controls="desk-tip-{j}" aria-describedby="desk-tip-{j}">',page,count=1)
        page=re.sub(rf'(<div class="hlab off A lon{j}"[^>]*>\s*<strong>[^<]*</strong>\s*<span>).*?(</span>)',rf'\g<1>{html.escape(short)}\2',page,count=1,flags=re.S)
    buttons=''.join(f'<button type="button" data-chem="{j}" aria-controls="mobile-motif-note" aria-expanded="false"><b>{name}</b><span>{html.escape(short)}</span></button>' for j,(name,short,_) in enumerate(MOTIFS))
    page=re.sub(r'(<div class="mobileChem"[^>]*>).*?</div>',r'\1'+buttons+'</div><p class="motif-note" id="mobile-motif-note" aria-live="polite" hidden></p>',page,count=1,flags=re.S)
    # Add a familiar evidence trail for each project without repetitive link names.
    for j,name in enumerate(('Brain Signals Lab','OpsDesk','Reachboard')):
        page=page.replace(f'href="#case-{j}">Case study',f'href="#case-{j}" aria-label="Read the {name} case study">Case study')
    return page
