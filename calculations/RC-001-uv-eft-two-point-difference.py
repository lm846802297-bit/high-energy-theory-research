#!/usr/bin/env python3
"""Exact algebra checks for §137 UV-EFT h-s two-point difference.
No loop library is invoked; this validates formulas/transcription and expansions.
"""
import sympy as sp
x,y,s,mu,k=sp.symbols('x y s mu k', positive=True)
Lx=sp.log(x/mu**2); Ly=sp.log(y/mu**2)
# UV and EFT pole coefficients with common Delta_MSbar factored out.
uv_pole=(4*x-s)+(4*y-s)-2*(2*x+2*y-s)
eft_pole=4*x+(4*x-s)
diff_pole=uv_pole-eft_pole
checks=[]
def ck(name, expr, expected=0):
    res=sp.simplify(expr-expected)
    assert res == 0, f'{name}: residual={res}'
    checks.append(name); print('PASS:',name)
ck('UV four-path pole cancels',uv_pole,0)
ck('EFT bubble plus contact pole is 8x-s',eft_pole,8*x-s)
ck('bare difference pole is s-8x',diff_pole,s-8*x)
# Difference after exact cancellation of light bubble.
uv_without_light=(4*y-s) # coefficient of B_yy
mixed_coeff=-2*(2*x+2*y-s)
ck('mixed B0 coefficient is -2(2x+2y-s)',mixed_coeff,-4*x-4*y+2*s)
# Zero-momentum finite exact difference from F_UV - F_EFT.
Fuv0=4*k*(2*x*y/(x-y)*sp.log(x/y)-(x+y))
Feft0=k*(4*x*(1-Lx)-4*x*Lx)
D0=sp.simplify(Fuv0-Feft0)
D0_expected=k*(8*x*y/(x-y)*sp.log(x/y)-4*y-8*x+8*x*Lx)
ck('exact zero-momentum finite difference',D0,D0_expected)
# Large-y expansion: verify the proposed asymptotic coefficients by formal algebra
# using B0 expansions through O(x,s) and A0 finite part.
B_yy=-Ly+s/(6*y)
B_xy=1-Ly-(x/y)*sp.log(y/x)+s/(2*y)
A0x=x*(1-Lx)
D_asym=sp.expand((4*y-s)*B_yy-2*(2*x+2*y-s)*B_xy-4*A0x)
# Remove terms beyond linear in x,s by polynomial truncation in dummy eps.
eps=sp.symbols('eps')
D_eps=sp.expand(D_asym.subs({x:eps*x,s:eps*s}))
D_linear=sp.expand(sp.series(D_eps,eps,0,2).removeO().subs(eps,1))
expected=-4*y+8*x*(Ly-1)+s*(sp.Rational(2,3)-Ly)
ck('large-mass expansion gives -4y+8x(Ly-1)+s(2/3-Ly)',D_linear,expected)
# Common normalization: kappa=2*yh*ys.
yh,ys=sp.symbols('y_h y_s')
ck('12x-2s in yh*ys normalization equals 6x-s in kappa normalization',
   yh*ys*(12*x-2*s), 2*yh*ys*(6*x-s))
ck('contact tadpole adds 2*kappa*x to EFT pole', (8*x-s)-(6*x-s),2*x)
# Leading portal threshold matches CW result after kappa asymptotic substitution.
yH,lam,v,vs,M=sp.symbols('y_H lam v v_s M', positive=True)
kappa_lead=yH**2*lam**2*v*vs/(2*M**2)
ck('leading -4*kappa*M^2/(16 pi^2) matches CW portal mass threshold',
   -4*kappa_lead*M**2/(16*sp.pi**2),-yH**2*lam**2*v*vs/(8*sp.pi**2))
print(f'RESULT: {len(checks)} exact symbolic checks passed')
print('SCOPE: exact algebra and asymptotic coefficient checks only; no Mathematica/FeynCalc/Matchmakereft execution.')
