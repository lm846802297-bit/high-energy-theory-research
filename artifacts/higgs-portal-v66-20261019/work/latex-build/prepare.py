from pathlib import Path
import re
src=Path(r'C:\Users\84680\Desktop\axial-vector审稿意见回复\审稿意见-gpt\审稿意见分析v5.7-物理校核与专题连续阅读版.md')
work=Path(r'C:\Users\84680\Desktop\axial-vector审稿意见回复\work\latex-build')
s=src.read_text(encoding='utf-8')
lines=s.splitlines()
for i,line in enumerate(lines):
    m=re.fullmatch(r'<a id="([^"]+)"></a>',line.strip())
    if m:
        for j in range(i+1,min(i+8,len(lines))):
            if re.match(r'^#{1,6} ',lines[j]):
                if not re.search(r'\s\{#[^}]+\}\s*$',lines[j]): lines[j]=lines[j].rstrip()+f' {{#{m.group(1)}}}'
                lines[i]=''
                break
s='\n'.join(lines)+'\n'
s=s.replace(r'\mathbf\Pi', r'\boldsymbol{\Pi}')
texmap={'μ':r'\ensuremath{\mu}','τ':r'\ensuremath{\tau}','λ':r'\ensuremath{\lambda}','θ':r'\ensuremath{\theta}','ε':r'\ensuremath{\epsilon}','π':r'\ensuremath{\pi}','δ':r'\ensuremath{\delta}','ν':r'\ensuremath{\nu}','σ':r'\ensuremath{\sigma}','β':r'\ensuremath{\beta}','γ':r'\ensuremath{\gamma}','α':r'\ensuremath{\alpha}','Π':r'\ensuremath{\Pi}','𝛱':r'\ensuremath{\Pi}','①':r'\textcircled{1}','②':r'\textcircled{2}','③':r'\textcircled{3}','④':r'\textcircled{4}','⑤':r'\textcircled{5}','⑥':r'\textcircled{6}','≈':r'\ensuremath{\approx}','∝':r'\ensuremath{\propto}','≤':r'\ensuremath{\leq}','≥':r'\ensuremath{\geq}','′':r'\ensuremath{^\prime}','⁺':r'\ensuremath{^+}','⁻':r'\ensuremath{^-}'}
ascii={k:v for k,v in zip('μτλθεπδνσβγαΠ𝛱', ['mu','tau','lambda','theta','epsilon','pi','delta','nu','sigma','beta','gamma','alpha','Pi','Pi'])}
ascii.update({'①':'(1)','②':'(2)','③':'(3)','④':'(4)','⑤':'(5)','⑥':'(6)','≈':' approx ','∝':' proportional_to ','≤':'<=','≥':'>=', '′':"'",'ℓ':'ell','⁺':'^+','⁻':'^-','₂':'_2','⁴':'^4','∼':'~','≳':'>~','≲':'<~'})
out=[]; fence=False
for line in s.splitlines():
    if re.match(r'^\s*```',line):
        fence=not fence; out.append(line); continue
    if fence:
        for k,v in ascii.items(): line=line.replace(k,v)
    else:
        parts=line.split('`')
        for i in range(len(parts)):
            mapping=ascii if i%2 else texmap
            for k,v in mapping.items(): parts[i]=parts[i].replace(k,v)
        line='`'.join(parts)
    out.append(line)
(work/'source-for-pandoc.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
print('prepared',len(out),'lines')
