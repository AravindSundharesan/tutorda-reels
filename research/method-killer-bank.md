# Method Killer playbook and shortcut bank (28 Nov 2026)

Every worked example below is checked in `research/verify_shortcuts.py` in the tutorda-reels repo (51 checks, all pass). Re-run it before using an example, and verify any new example or practice question the same way.

## Part 1. How to explain a shortcut (the TutorDA method)

Grounded in Mayer's multimedia-learning principles (signalling, segmenting, temporal contiguity, coherence, worked examples) and in our own reel data.

1. **Open on the pain, not the topic.** Name the method every student has suffered through ("9 cofactors", "by parts twice"). "Every JEE student does this" is the line, and the long way is on screen, crossed out, within 0.3 s.
2. **Show the contrast on one screen.** Long way (crossed out) above, one-line answer box with blanks below. The viewer sees the promise before any explanation.
3. **One idea per beat.** One sentence and one change on screen per beat, about 4 s at most. Never two new symbols at once.
4. **Say it when it appears.** Each number or term animates on the exact word that names it (word-timed). Never read text that isn't on screen yet, never show text that hasn't been said.
5. **Highlight only what changes.** Colour or circle the piece being used; dim what's finished. Nothing moves for decoration.
6. **Give the reason in one line.** Every shortcut gets a "why" a student can repeat to a friend ("it's the product rule run backwards"). A trick with a reason is remembered and not misused; a bare trick is forgotten or misapplied.
7. **State the condition.** Say when the shortcut works and when it doesn't (limits 0 to π/2 only; linear factors only). One short line or on-screen tag. This is what separates a teacher from a trick account.
8. **Make them predict.** Before the reveal, the viewer commits to an answer (3-2-1). The answer comes last.
9. **Check it in one second when you can.** Differentiate back, plug a value in. It builds trust.
10. **Speak like the classroom.** "pi by 2", "x squared", "e to the x". Plain words, no jargon the student hasn't met.
11. **Give a near-transfer question.** The first comment uses the same rule with one twist (odd power, x³), so viewers apply it, not just watch it.
12. **Cut everything else.** If a symbol, sound or sentence doesn't serve the one idea, it goes.

Reel shape that follows from this (and from the MK1–MK5 data): 22–28 s; "Stop …" hook ≤ 7 words + "Every JEE student …" line; cross lands on "Stop"; contrast frame; word-timed build; 3-2-1; answer last; Follow card straight after the answer; end on the opening frame so it loops.

## Part 2. Ranked queue for the next Method Killers

Ranked on: how many JEE students meet the chapter (JEE Main expected questions per paper), how much they hate the school method, how few already know the shortcut, and how well it fits a 25 s visual. Already used: cover-up (MK1), repeated factor (MK2), P − P′ + P″ for P·eˣ (MK3), King's rule (MK4), Wallis (MK5).

| # | Chapter (Qs/paper) | Hook | Shortcut | Why it works (say this) | Verified example | Trap to state |
|---|---|---|---|---|---|---|
| 1 | Integration (2) | "Stop integrating by parts here." | ∫eˣ(f + f′) dx = eˣf + C | Product rule backwards: (eˣf)′ = eˣf + eˣf′ | ∫eˣ(1/x − 1/x²) dx = eˣ/x + C; ∫eˣ(sin x + cos x) dx = eˣ sin x + C | The bracket must be exactly f + f′; rewrite it first (eˣ(x − 1)/x² = eˣ(1/x − 1/x²)) |
| 2 | Matrices (1) | "Stop finding 9 cofactors." | Columns of A⁻¹ are r₂×r₃, r₃×r₁, r₁×r₂, divided by det A | A row dotted with the cross of the other two gives det A; with a repeated row it gives 0 | Checked on 50 random 3×3 matrices | Cyclic order, and they go in as COLUMNS, not rows |
| 3 | Limits (0–1) | "Stop taking log and L'Hôpital." | 1^∞ form: lim f^g = e^(lim g(f − 1)) | ln(1 + u) ≈ u when u is small | lim (cos x)^(1/x²) = e^(−1/2); lim (1 + 3/x)^(2x) = e^6 | Only when f → 1 and g → ∞; check the form first |
| 4 | 3D geometry (2) | "Stop writing the line and intersecting." | Image of P in ax + by + cz + d = 0: P + 2t·n, t = −(ax₁ + by₁ + cz₁ + d)/(a² + b² + c²); foot uses t once | Walk along the normal; t is how far, double it to cross | Image of (1, 2, 3) in x + y + z = 0 is (−3, −2, −1) | Plane must be in "= 0" form; foot = t, image = 2t |
| 5 | Integration (2) | "Stop doing parts three times." | DI / tabular: derivative column to 0, integral column, signs + − + − | It is integration by parts repeated, written as a table | ∫x³ sin x dx = −x³cos x + 3x² sin x + 6x cos x − 6 sin x + C | Only when one factor's derivatives reach 0 (a polynomial) |
| 6 | P&C / Binomial (1–2) | "Stop listing the cases." | Non-negative solutions of x₁ + … + xₖ = n: C(n + k − 1, k − 1) | n stars and k − 1 bars in a row; choose where the bars go | x + y + z = 10 has C(12, 2) = 66; also the number of terms in (x + y + z)¹⁰ | Positive solutions use C(n − 1, k − 1) |
| 7 | Sequences & series (2) | "Stop adding 20 terms." | Telescoping: split into neighbours, middle cancels | f(k) − f(k + 1) summed leaves first − last | Σ 1/(k(k + 1)) = n/(n + 1); Σ 1/(k(k + 1)(k + 2)) = 1/4 − 1/(2(n + 1)(n + 2)) | The three-factor case carries a ½ |
| 8 | Trigonometry (1–2) | "Stop using product-to-sum three times." | cos A cos 2A cos 4A = sin 8A / (8 sin A) | Multiply by sin A; 2 sin cos = sin 2× three times | cos 20° cos 40° cos 80° = 1/8 | Angles must keep doubling |
| 9 | Trigonometry (1–2) | "Stop expanding tan of sums." | tan A tan(60° − A) tan(60° + A) = tan 3A | It's the tan 3A identity, factored | tan 20° tan 40° tan 80° = √3 | Angles must be A, 60° − A, 60° + A |
| 10 | Complex numbers (1) | "Stop expanding the 7th power." | 1 + ω + ω² = 0, ω³ = 1: swap any two for minus the third | Cube roots of 1 add to zero | (1 + ω − ω²)⁷ = (−2ω²)⁷ = −128ω² | Reduce powers of ω mod 3 |
| 11 | Integration (2) | "Stop substituting x = a + b − x twice." | ∫ₐᵇ f(x)/(f(x) + f(a + b − x)) dx = (b − a)/2 | Add I to its mirror; the integrand sums to 1 | ∫₂⁸ √x/(√x + √(10 − x)) dx = 3 | Needs exactly the f/(f + mirror) shape |
| 12 | Statistics (1–2) | "Stop recomputing the variance." | Var(ax + b) = a²·Var(x); Var(1..n) = (n² − 1)/12 | Shifting doesn't change spread; scaling squares it | Var(1..10) = 99/12; Var(3x + 7) = 9 × that | SD scales by |a|, not a² |
| 13 | Quadratic (0–1) | "Stop finding the roots." | α² + β² = (α + β)² − 2αβ; α³ + β³ = (α + β)³ − 3αβ(α + β) | Sum and product come straight from the coefficients | x² − 5x + 3: α² + β² = 19, α³ + β³ = 80 | Sum = −b/a, product = c/a, mind the signs |
| 14 | Sequences / inequalities (2) | "Stop differentiating for the minimum." | ax + b/x ≥ 2√(ab) for x > 0 | AM ≥ GM; equality when ax = b/x | min of 4x + 9/x is 12, at x = 3/2 | x > 0 only |
| 15 | Limits (0–1) | "Stop using L'Hôpital three times." | Series: sin x = x − x³/6, tan x = x + x³/3 | Keep terms up to the power in the denominator | (x − sin x)/x³ → 1/6; (tan x − sin x)/x³ → 1/2 | Keep enough terms (to x³ here) |

## Part 3. More verified shortcuts (fillers, Story slides, first comments)
- **Trig range:** a sin x + b cos x lies in [−√(a² + b²), √(a² + b²)]. 3 sin x + 4 cos x has max 5.
- **Binomial sums:** sum of coefficients = put x = 1 ((3x − 2)¹⁰ → 1). Even-place coefficients of (1 + x)ⁿ add to 2ⁿ⁻¹.
- **Negative binomial:** coefficient of xʳ in (1 − x)⁻ⁿ is C(n + r − 1, r): x⁵ in (1 − x)⁻³ is 21.
- **Remainders:** find a power that gives ±1. 7² ≡ −1 (mod 25), so 7¹⁰³ ≡ 18 (mod 25).
- **Probability:** P(at least one) = 1 − P(none). At least one six in 4 throws = 671/1296.
- **Derangements:** D₄ = 9, D₅ = 44 (none in its own place).
- **Determinants:** |adj(kA)| = (kⁿ|A|)ⁿ⁻¹. 3×3, |A| = 3, k = 2: 576.
- **2×2 matrices:** inverse = swap the diagonal, negate the others, divide by det. Cayley–Hamilton: A² − (tr A)A + (det A)I = 0.
- **Vectors:** [a b c] = det of the three vectors; 0 means coplanar.
- **Parallel planes:** distance = |d₁ − d₂| / √(a² + b² + c²) after matching the normals (2x − y + 2z = 5 and = −7: distance 4).
- **2D foot of perpendicular:** same t formula as 3D. Foot from (2, 3) to 3x + 4y − 2 = 0 is (2/25, 11/25).
- **Conic tangents:** y = mx + c touches x²/a² + y²/b² = 1 when c² = a²m² + b², and touches y² = 4ax when c = a/m. Tangent length from a point to a circle = √S₁₁.
- **Series:** Σk³ = (Σk)². AGP: 1 + 2/3 + 3/9 + … = 9/4.
- **Definite integrals:** odd parts vanish on [−a, a] (∫₋₁¹ (x⁵ + x²) dx = 2/3); periodic: ∫₀^(100π) |sin x| dx = 200; ∫₀^π x sin x/(1 + cos²x) dx = π²/4 by King's rule.
- **Differentiation:** x = tan θ turns tan⁻¹(2x/(1 − x²)) into 2θ, so the derivative is 2/(1 + x²); (xˣ)′ = xˣ(ln x + 1).
- **Complex:** |z₁ + z₂|² + |z₁ − z₂|² = 2(|z₁|² + |z₂|²).

Sources: chapter weightage from [CollegeDekho, JEE Main 2026 Session 1 expected questions](https://www.collegedekho.com/articles/jee-main-2026-session-1-mathematics-chapter-wise-expected-number-of-questions/); explanation principles from [Mayer, research-based principles for multimedia instruction](https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf) and the [worked-examples principle](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8753055D1FB47CF1E2BB897FD44FBEF8/9781139547369c16_p391-412_CBO.pdf/worked_examples_principle_in_multimedia_learning.pdf).
