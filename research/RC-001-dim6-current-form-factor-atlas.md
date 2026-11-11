# RC-001 — Dimension-six one-gauge-field form-factor atlas

**Status:** amplitude/topology registry established; no new finite current-form-factor coefficient is claimed. CI is explicitly skipped as an unavailable infrastructure check. The missing diagram-level calculation remains a physics evidence gap.

## 1. Scope and separation from the four-point gauge atlas

This note complements `research/RC-001-dim6-gauge-diagram-atlas.md` and `research/RC-001-dim6-uv-eft-subtraction-ledger.md`. It registers the amplitudes with one external gauge field,
\[
\bar L_\ell L_\ell V,\qquad \bar\ell_R\ell_R V,
\]
and the corresponding two-fermion/two-scalar form factors derived from the tree-level heavy-\(E_\ell\) exchange. It does not claim that the one-loop form factors have been integrated.

The already recorded bosonic field-strength/current-to-gauge coefficients in master §254 remain the existing bosonic module. They must be imported once for consistency checks, not recomputed or added to the new fermionic coefficients. A current-current graph connected by a single gauge propagator is reducible in that propagator and must not be called a direct local 1PI four-scalar or four-fermion coefficient.

## 2. External-current insertion classes

The external gauge field \(V_\mu\) is attached to every UV line on which its covariant kinetic term supplies a vertex. This is distinct from the internal virtual gauge boson in the one-loop correction: the latter is enumerated by the line-pair IDs in the four-point atlas.

| Form-factor ID | External amplitude | Lines that can emit the external field at the matter vertex | Restrictions |
|---|---|---|---|
| LD-B-FF | \(\bar L_\ell L_\ell H^\dagger H\,B_\mu\) | \(E_\ell,\bar L_\ell,L_\ell,H^\dagger,H\) | Use the hypercharges in the gauge atlas; include external-field and input renormalization |
| LD-W-FF | \(\bar L_\ell L_\ell H^\dagger H\,W_\mu^I\) | \(\bar L_\ell,L_\ell,H^\dagger,H\) | \(E_\ell\) is an \(SU(2)_L\) singlet; retain the weak generator/tensor until projection |
| LD-X-FF | \(\bar L_\ell L_\ell H^\dagger H\,A'_\mu\) | \(E_\ell,\bar L_\ell,L_\ell\) | \(H,H^\dagger\) have zero \(X\)-charge |
| RD-B-FF | \(\bar\ell_R\ell_R S_\ell^\ast S_\ell\,B_\mu\) | \(E_\ell,\bar\ell_R,\ell_R\) | \(S_\ell\) is hypercharge neutral |
| RD-X-FF | \(\bar\ell_R\ell_R S_\ell^\ast S_\ell\,A'_\mu\) | \(E_\ell,\bar\ell_R,\ell_R,S_\ell^\ast,S_\ell\) | Keep the signed \(\eta_\ell\) factors on fermion and scalar lines |
| LD/RD-BX-FF | Same external states with the mixed \(B-A'\) propagator/field basis | The applicable \(B\) and \(A'\) insertions above | Conditional on the declared kinetic-mixing matrix, its boundary condition and threshold prescription |

For each row, generate the complete one-loop set, not only a vertex correction on the light-fermion line:

1. External \(V_\mu\) insertion on each allowed light-fermion, heavy-fermion, and scalar propagator segment, including both segments adjacent to the two conjugate Yukawa vertices where distinct.
2. All internal virtual-gauge attachments from the four-point atlas, with the external-current insertion placed on every compatible line/vertex of the resulting one-loop topology.
3. External-leg self-energies and LSZ/amputation terms in the same convention as the four-point amplitude.
4. Scalar seagull contributions and the corresponding scalar/gauge-field counterterms where allowed by the covariant kinetic terms.
5. Gauge-field wavefunction renormalization, \(B-A'\) field/kinetic mixing, and parameter counterterms. For non-Abelian external \(W^I\), include the gauge-sector and ghost contributions required by the chosen gauge fixing and Ward/Slavnov-Taylor identities.
6. EFT insertions of \(Q_{LD}\) or \(Q_{RD}\), including the one-gauge contact term from the covariant derivative, virtual-gauge attachments to external lines, EFT counterterms, and the same external-field convention.

This list is a topology-generation prescription. It is not a claim that every bullet corresponds to one individual Feynman graph; exact multiplicities and signs must be fixed by explicit graph generation or a documented manual enumeration.

## 3. EFT covariant-derivative contact terms

For both operators the differentiated composite is an \(SU(2)_L\) singlet:
\[
\Psi_L=H^\dagger L_\ell,\qquad \Psi_R=S_\ell\ell_R,\qquad
Y(\Psi_L)=Y(\Psi_R)=-1,\quad x(\Psi_L)=x(\Psi_R)=\eta_\ell.
\]
Consequently the single-external-gauge contact from the derivative insertion has \(B_\mu\) and \(A'_\mu\) components but no direct \(W_\mu^I\) component. This absence does not remove \(W\)-loop corrections to \(Q_{LD}\): the external \(L,H\) lines still couple to \(W\).

For the mixed \(B-A'\) sector, retain the full gauge kinetic/propagator matrix until the external-field basis and the renormalized mixing boundary are specified. Do not replace a signed mixed charge factor by a Boolean “allowed” flag.

### 3.1 Tree-level \(W\) Ward identity and the partial loop check

For the \(SU(2)_L\) sector define
\[
\Psi_L=H^\dagger L_\ell,\qquad \bar\Psi_L=\bar L_\ell H.
\]
Both composites are weak singlets, so
\[
D_\mu^{SU(2)}\Psi_L=\partial_\mu\Psi_L,\qquad
D_\mu^{SU(2)}\bar\Psi_L=\partial_\mu\bar\Psi_L.
\]
With \(D_\mu H=\partial_\mu H-i g_2T^IW_\mu^I H\) and \(D_\mu L=\partial_\mu L-i g_2T^IW_\mu^I L\),
\[
(D_\mu H)^\dagger L+H^\dagger D_\mu L
=\partial_\mu(H^\dagger L)
+i g_2H^\dagger T^IW_\mu^IL-i g_2H^\dagger T^IW_\mu^IL
=\partial_\mu(H^\dagger L).
\]
The cancellation holds generator by generator for \(I=1,2,3\), not only after summing over weak indices. Thus the tree-level EFT insertion \(Q_{LD}=\bar\Psi_L i\slashed D\Psi_L\) has no direct \(W_\mu^I\) contact vertex. This explicit expansion is independently checked in calculations/RC-001-dim6-WW-wick-multiplicity.py (five local regression tests; captured output in validation/RC-001-dim6-WW-wick-multiplicity.txt). The longitudinal external-\(W\) Ward contraction of the emissions from the two composite pairs is proportional to
\[
(t_{\bar L}^I+t_H^I)T_0,\qquad
(t_{H^\dagger}^I+t_L^I)T_0,
\]
and both vanish by the singlet identities in research/RC-001-dim6-SU2-attachment-projection.md. The same explicit Wick audit shows that the two endpoint assignments for each unordered pair cancel the \(1/2!\) in the second-order interaction, giving unit multiplicity; this is a manual combinatoric check, not a generated graph/sign census. Thus the tree-level operator insertion satisfies the \(W\)-current Ward identity without a derivative-contact term.

A separate partial one-loop check is now available for the internal-\(W\) four-point cross-box sub-block. Contracting the four cross-box numerators with the longitudinal propagator projector gives the kernels
\[
\left(A_{01}^{(L)},A_{02}^{(L)},A_{05}^{(L)},A_{06}^{(L)}\right)
=\left(-\frac{2K}{d},-\!J+\frac{2K}{d},
-\frac{2K}{d},-\!J+\frac{2K}{d}\right),
\]
whose \(T_3\) projection vanishes. This establishes gauge-parameter independence of that fixed-routing cross-box subset. It does **not** evaluate the one-loop external-\(W\) form factor, nor the complete Slavnov–Taylor identity including external-leg, gauge-sector, and counterterm contributions. Accordingly, LD-W-FF remains **NOT EVALUATED**.

### 3.2 EFT one-\(W\) contact associated with the \(T_3\) derivative tensor

The tree-level singlet operator \(Q_{LD}\) has no direct \(W\) contact. The \(T_3\) tensor generated by the cross-box sub-block is a different weak contraction and must be covariantized in the triplet representation. Define
\[
X^I=\bar L\sigma^I H,\qquad
Y^I=H^\dagger\sigma^I L,\qquad
Q_{LD}^{(3)}=X^I i\gamma^\mu(D_\mu^{\rm adj}Y)^I.
\]
The Pauli identity
\[
\sum_I\sigma^I_{ij}\sigma^I_{kl}
=2\delta_{il}\delta_{kj}-\delta_{ij}\delta_{kl}
=(T_3)_{ij,kl}
\]
shows that this operator has precisely the \(T_3\) four-point tensor, with no extra normalization factor in the Pauli-matrix convention.

For \(D_\mu=\partial_\mu-i g_2 W_\mu^I\sigma^I/2\) on doublets, the triplet derivative is
\[
(D_\mu^{\rm adj}Y)^I
=\partial_\mu Y^I+g_2\epsilon^{IJK}W_\mu^JY^K.
\]
Consequently, if a local coefficient \(C_3\) multiplies \(Q_{LD}^{(3)}\), its EFT one-\(W\) contact is
\[
\boxed{
\mathcal L_{\rm contact}
=i g_2 C_3\epsilon^{IJK}
(\bar L\sigma^I H)\gamma^\mu W_\mu^J
(H^\dagger\sigma^K L).
}
\]
The Pauli completeness and adjoint-commutator identities are checked in calculations/RC-001-dim6-WW-triplet-current-contact.py (four local tests; captured output in validation/RC-001-dim6-WW-triplet-current-contact.txt). In the fixed all-incoming Fourier convention \(e^{-ipx}\) of the WW cross-box note, the raw amplitude coefficient \(C_3^{WW,\rm box}\) multiplies \(+\slashed P T_3\), while the matrix element of the displayed \(Q_{LD}^{(3)}\) carries \(p_3+p_4=-P\). Thus \(C_{Q_{LD}^{(3)}}^{WW,\rm box}=-C_3^{WW,\rm box}\); the contact sign must follow the operator coefficient, not the raw \(+\slashed P\) amplitude label.

This is the **EFT contact implied by the local triplet derivative operator**, not the UV one-loop five-point form factor. It does not close LD-W-FF or determine the final \(C_{H\ell}^{(3)}\) coefficient. The UV current amplitude, its common off-shell EFT subtraction, the other derivative tensors, and the EOM/IBP projection remain required.

## 4. Form-factor decomposition and matching record

Use common nonexceptional off-shell external momenta (or one common infrared regulator) and the same gauge-fixing, \(\overline{\mathrm{MS}}\), and external-field conventions on both sides. For each amplitude, record separately:

- the tree-level form factor;
- the one-loop UV vertex/form-factor contribution;
- UV and IR poles before subtraction;
- the EFT soft contribution, including the derivative-contact graphs;
- external-field and parameter counterterms;
- the finite local polynomial after UV–EFT subtraction;
- the projection onto the chosen nonredundant current/operator basis;
- the gauge-EOM image, if used, and all induced current-current/source companions.

For a fermion current, retain a complete off-shell transverse/longitudinal tensor basis until the Ward identity is checked; do not infer a local Wilson coefficient from a single on-shell form factor. For a scalar current, keep the independent \((p+p')^\mu\) and \(q^\mu\) structures until the same projection is performed. The tensor basis and normalization must be identical in UV and EFT. The already-derived diagonal-gauge (y,\lambda,M_E) parameter-counterterm pieces are tabulated in `research/RC-001-dim6-gauge-parameter-counterterms.md`; the (Q_{LD}) internal-(W) weak-index contractions are tabulated in `research/RC-001-dim6-SU2-attachment-projection.md`. Neither record supplies the missing current-form-factor loop integrals.

The Ward-Takahashi/Slavnov-Taylor check is applied to the summed amplitude including external-leg pieces and contact vertices. A stripped vertex graph alone is insufficient. After the UV–EFT difference, separate local 1PI coefficients from gauge-reducible current exchange and apply gauge-field EOM only once.

## 5. Evidence ledger

| ID | UV graph/form-factor data | EFT subtraction | Counterterms and consistency tests | Status |
|---|---|---|---|---|
| LD-B-FF | External \(B\) on \(E,L,H\) lines plus all compatible one-loop gauge families | \(Q_{LD}\) insertion, \(B\)-contact, external-line and mixed-propagator graphs if retained | \(B\) field/input renormalization, Ward identity, local/reducible separation | NOT EVALUATED |
| LD-W-FF | External \(W^I\) on doublet fermion/scalar lines plus required gauge-sector graphs | \(Q_{LD}\) insertion and external-line \(W\) graphs; no direct \(W\) derivative contact | Weak tensor, Slavnov-Taylor identity, gauge/ghost and external-field terms | NOT EVALUATED |
| LD-X-FF | External \(A'\) on \(E,L\) lines; include kinetic-mixing effects where applicable | \(Q_{LD}\) insertion and \(A'\)-contact graphs | Signed flavor charges, mixing boundary, current/EOM bookkeeping | NOT EVALUATED |
| RD-B-FF | External \(B\) on \(E,\ell_R\) lines | \(Q_{RD}\) insertion and \(B\)-contact graphs | Hypercharge/input counterterms, Ward identity | NOT EVALUATED |
| RD-X-FF | External \(A'\) on \(E,\ell_R,S\) lines | \(Q_{RD}\) insertion and \(A'\)-contact graphs | Signed flavor/scalar charges, mixing boundary, Ward identity | NOT EVALUATED |
| MIX-FF | External-field rotations and mixed \(B-A'\) propagator contributions | Same full kinetic matrix and renormalization boundary on EFT side | No implicit \(\chi(\mu_R)=0\); state it as an input if chosen | CONDITIONAL / NOT EVALUATED |
| BASIS-FF | Sum all UV form-factor tensors at the same coupling order | Subtract matching EFT tensors before reduction | Apply Ward identities, EOM/IBP and current-source mapping once; keep reducible exchange separate | OPEN |

## 6. Explicit non-claims and closure

No finite \(O(g^2/M_E^2)\) fermionic current-form-factor coefficient is claimed in this file. The existing master §254 bosonic coefficients remain separate. The current environment lacks FeynArts/FeynCalc and equivalent diagram-level tools; independent graph-level signs, multiplicities and loop numerators remain unverified. CI is skipped by explicit project decision and is not a closure gate, but this does not waive the missing physics evidence.

Close these rows only after the individual UV and EFT form factors have been calculated, their UV/IR poles and counterterms documented, Ward identities verified on the summed amplitudes, and local/reducible contributions projected into the common operator basis. PR #4 remains Draft/Open until those physics requirements are met.
