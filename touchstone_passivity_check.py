"""Audit sampled one/two-port Touchstone S matrices at a shared real reference."""
from __future__ import annotations
import argparse,json,math,re,sys
from pathlib import Path

MAX_BYTES=1024*1024
def number(s):
    if len(s)>64 or not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]{1,3})?',s):raise ValueError('bounded decimal number required')
    n=float(s)
    if not math.isfinite(n):raise ValueError('nonfinite number')
    return n

def analyze(text,ports,tolerance=1e-9):
    if ports not in (1,2) or not math.isfinite(tolerance) or not 0<=tolerance<=1e-3:raise ValueError('ports1/2 and finite tolerance0..0.001 required')
    if len(text.encode('ascii'))>MAX_BYTES:raise ValueError('Touchstone exceeds1MiB')
    options=None;tokens=[];comments=0
    for line in text.splitlines():
        content,sep,comment=line.partition('!')
        if sep:
            comments+=1
            if any(w in comment.lower() for w in ('port impedance','gamma','modal')):raise ValueError('frequency-dependent/complex impedance annotations unsupported')
        content=content.strip()
        if not content:continue
        if content.startswith('#'):
            v=content[1:].upper().split()
            if options is not None or tokens or len(v)!=5 or v[0] not in ('HZ','KHZ','MHZ','GHZ') or v[1]!='S' or v[2] not in ('RI','MA','DB') or v[3]!='R':raise ValueError('one explicit # unit S RI/MA/DB R real option line required')
            reference=number(v[4])
            if not 0<reference<=1e6:raise ValueError('shared positive real reference<=1e6 required')
            options=v
        else:
            if options is None or '[' in content or ']' in content:raise ValueError('explicit options before data; Touchstone1 subset only')
            tokens.extend(content.split())
            if len(tokens)>4096*(1+2*ports*ports):raise ValueError('sample budget4096 exceeded')
    width=1+2*ports*ports
    if options is None or not tokens or len(tokens)%width:raise ValueError('complete nonempty frequency/matrix rows required; no noise records')
    unit,_,form,_,_=options;scale={'HZ':1,'KHZ':1000,'MHZ':1000000,'GHZ':1000000000}[unit];rows=[];prior=-1
    for pos in range(0,len(tokens),width):
        f=number(tokens[pos])*scale
        if not prior<f<=1e15 or f<0:raise ValueError('strictly increasing nonnegative bounded frequencies required')
        prior=f;values=[]
        for i in range(pos+1,pos+width,2):
            a,b=number(tokens[i]),number(tokens[i+1])
            if form=='RI':
                if max(abs(a),abs(b))>1000:raise ValueError('RI component magnitude budget1000')
                z=complex(a,b)
            else:
                if abs(b)>360000:raise ValueError('angle magnitude budget360000 degrees')
                if form=='DB':
                    if not -600<=a<=60:raise ValueError('dB magnitude budget -600..60')
                    a=10**(a/20)
                elif not 0<=a<=1000:raise ValueError('MA magnitude budget0..1000')
                angle=math.radians(b);z=complex(a*math.cos(angle),a*math.sin(angle))
            values.append(z)
        if ports==1:power=abs(values[0])**2;reciprocity=None
        else:
            s11,s21,s12,s22=values
            a=abs(s11)**2+abs(s21)**2;d=abs(s12)**2+abs(s22)**2;b=s11.conjugate()*s12+s21.conjugate()*s22
            power=(a+d+math.sqrt((a-d)**2+4*abs(b)**2))/2;reciprocity=abs(s12-s21)
        amplitude=math.sqrt(power);rows.append({'frequency_hz':f,'max_singular_value':amplitude,'largest_power_gain':power,'sample_passes':amplitude<=1+tolerance,'reciprocity_difference':reciprocity})
    failures=[i for i,r in enumerate(rows) if not r['sample_passes']];worst=max(range(len(rows)),key=lambda i:rows[i]['max_singular_value'])
    return {'ports':ports,'shared_real_reference_ohms':reference,'format':form,'tolerance_on_singular_value':tolerance,'samples':rows,'failing_sample_indices':failures,'worst_sample_index':worst,'ignored_comments':comments,
        'scope':'Sampled S^H S eigenvalue test at a shared positive real reference; no interpolation, impedance renormalization, causality, measurement uncertainty or physical-device certification. Reciprocity difference is informational, not a passivity condition.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--ports',type=int,choices=(1,2),required=True);p.add_argument('--tolerance',type=float,default=1e-9);a=p.parse_args()
    try:
        with Path(a.input).open('rb') as f:raw=f.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError('Touchstone exceeds1MiB')
        r=analyze(raw.decode('ascii'),a.ports,a.tolerance);print(json.dumps(r,indent=2,sort_keys=True));return int(bool(r['failing_sample_indices']))
    except (ValueError,OSError,UnicodeError,OverflowError) as e:print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
