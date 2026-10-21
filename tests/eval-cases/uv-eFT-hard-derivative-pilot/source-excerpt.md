# Source excerpt: UV–EFT hard mixed-self-energy derivative

## Provenance and scope

This excerpt is a versioned local transcription of the user's working note:

- File: \`higgs_portal_mixing_unified_reviewer_response_and_uv_eft_UPDATED_v2(8)(20261021)(153)_matchete_mapping_version_history.md\`
- Relevant sections: §39.6–§39.7 and §40.1–§40.4; model-convention cross-reference §128.2–§128.3.
- Primary model reference: [arXiv:2608.27258v1 HTML](https://arxiv.org/html/2608.27258v1), submitted 2026-08-27.

**Evidence boundary:** the arXiv paper provides the UV model and field/mass conventions. The hard-kernel and PV expressions below are taken from the working note being audited. This pilot independently checks their internal PV-integral consistency and algebraic projection; it does not claim to independently regenerate the full UV loop kernel.

## Formula under audit

Define
\[
r=\frac{m^2}{M^2},\qquad L=\ln\frac{M^2}{\mu^2},\qquad r\ll1.
\]

The working note gives
\[
\overline B_{MM}(0)=-L,\qquad
B'_{MM}(0)=\frac{1}{6M^2},
\]
and
\[
\overline B_{mM}(0)=1-L+\frac{r\ln r}{1-r},
\]
\[
B'_{mM}(0)=\frac{1}{M^2}\left[
\frac{1+r}{2(r-1)^2}-\frac{r\ln r}{(r-1)^3}
\right].
\]

The hard-kernel derivative is
\[
F'_{\mathrm{hard}}(0)=K\left[
-2\overline B_{MM}(0)+8M^2B'_{MM}(0)
+4\overline B_{mM}(0)
-8(m^2+M^2)B'_{mM}(0)
\right].
\]

The stated asymptotic expansion is
\[
\frac{F'_{\mathrm{hard}}(0)}{K}
=\frac43-2L-4r\ln r-16r+O(r^2\ln r),
\]
so in particular
\[
F'_{\mathrm{hard}}(0)=K\left(\frac43-2L\right)+O(Kr\ln r).
\]

Using the note's insertion convention,
\[
\Pi'_{\mathrm{hard}}(0)=-\frac{F'_{\mathrm{hard}}(0)}{16\pi^2}.
\]
At \(\mu=M\), \(L=0\), hence
\[
\Pi'_{\mathrm{hard}}(0)=-\frac{K}{12\pi^2}+O(Kr\ln r).
\]

## Conditional operator projection

For \(\Phi_i=S_\ell H_i\) and
\[
\mathcal O_{\Phi D}=(D_\mu\Phi_i)^\dagger D^\mu\Phi_i,
\]
the radial expansion \(H^0=(v_h+h)/\sqrt2\), \(S=(v_s+s)/\sqrt2\) gives a cross-kinetic term
\[
\mathcal O_{\Phi D}\supset\frac{v_hv_s}{2}\,\partial_\mu h\,\partial^\mu s.
\]

If the local 1PI convention is defined by
\[
\Pi'_{\mathrm{local}}(0)
=-\frac{C_{\Phi D}}{\Lambda^2}\frac{v_hv_s}{2},
\]
then matching only this one operator direction gives
\[
\frac{C_{\Phi D}}{\Lambda^2}
=\frac{K}{6\pi^2v_hv_s}+O\!\left(\frac{Kr\ln r}{v_hv_s}\right).
\]

This last line is explicitly a **single-operator projection**, not a unique coefficient in a complete nonredundant dimension-six basis.

