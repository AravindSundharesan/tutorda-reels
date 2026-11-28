"""Verify every shortcut in the Method Killer bank (28 Nov 2026). Each check returns True or prints a mismatch."""
import sympy as s, itertools, math, random
from fractions import Fraction
x, t, n = s.symbols('x t n', real=True)
ok = {}
def chk(k, cond): ok[k] = bool(cond)

# ---------- Integration ----------
chk("int_ex_f_fprime", s.simplify(s.diff(s.exp(x)/x, x) - s.exp(x)*(1/x - 1/x**2)) == 0)
chk("int_ex_sin_cos", s.simplify(s.diff(s.exp(x)*s.sin(x), x) - s.exp(x)*(s.sin(x)+s.cos(x))) == 0)
DI = -x**3*s.cos(x) + 3*x**2*s.sin(x) + 6*x*s.cos(x) - 6*s.sin(x)
chk("int_DI_x3sin", s.simplify(s.diff(DI, x) - x**3*s.sin(x)) == 0)
chk("int_P_ex", s.simplify(s.diff(s.exp(x)*(x**3-3*x**2+6*x-6), x) - x**3*s.exp(x)) == 0)
chk("int_odd_even", s.integrate(x**5 + x**2 + x*s.cos(x), (x, -1, 1)) == s.Rational(2, 3))
I = s.Integral(s.sqrt(x)/(s.sqrt(x)+s.sqrt(10-x)), (x, 2, 8)).evalf(30); chk("int_a_plus_b_minus_x", abs(I-3) < 1e-20)
chk("int_kings_sqrt", abs(s.Integral(s.sqrt(s.sin(x))/(s.sqrt(s.sin(x))+s.sqrt(s.cos(x))), (x, 0, s.pi/2)).evalf(25) - s.pi.evalf(25)/4) < 1e-15)
chk("int_periodic_abs_sin", s.integrate(s.Abs(s.sin(x)), (x, 0, s.pi))*100 == 200)
chk("int_wallis_sin6", s.integrate(s.sin(x)**6, (x, 0, s.pi/2)) == 5*s.pi/32)
chk("int_wallis_sin5", s.integrate(s.sin(x)**5, (x, 0, s.pi/2)) == s.Rational(8, 15))
chk("int_x_f_sin_kings", abs(s.Integral(x*s.sin(x)/(1+s.cos(x)**2), (x, 0, s.pi)).evalf(30) - (s.pi**2/4).evalf(30)) < 1e-20)
# ---------- Limits ----------
chk("lim_1inf_3x", s.limit((1+3/x)**(2*x), x, s.oo) == s.exp(6))
chk("lim_1inf_cos", s.limit(s.cos(x)**(1/x**2), x, 0) == s.exp(-s.Rational(1, 2)))
chk("lim_x_minus_sin", s.limit((x - s.sin(x))/x**3, x, 0) == s.Rational(1, 6))
chk("lim_ax_bx", s.simplify(s.limit((5**x - 3**x)/x, x, 0) - s.log(s.Rational(5, 3))) == 0)
chk("lim_tan_minus_sin", s.limit((s.tan(x) - s.sin(x))/x**3, x, 0) == s.Rational(1, 2))
# ---------- Sequences & series ----------
k = s.symbols('k', integer=True, positive=True); N = s.symbols('N', integer=True, positive=True)
chk("ser_telescope_2", s.simplify(s.summation(1/(k*(k+1)), (k, 1, N)) - N/(N+1)) == 0)
chk("ser_telescope_3", s.simplify(s.summation(1/(k*(k+1)*(k+2)), (k, 1, N)) - (s.Rational(1, 4) - 1/(2*(N+1)*(N+2)))) == 0)
chk("ser_cubes_square", s.simplify(s.summation(k**3, (k, 1, N)) - s.summation(k, (k, 1, N))**2) == 0)
chk("ser_agp", s.summation(k/s.Integer(3)**(k-1), (k, 1, s.oo)) == s.Rational(9, 4))
f = 4*x + 9/x; chk("amgm_min", s.minimum(f, x, s.Interval.open(0, s.oo)) == 12 and f.subs(x, s.Rational(3, 2)) == 12)
# ---------- Binomial / P&C ----------
chk("multinomial_terms", len([c for c in itertools.product(range(11), repeat=3) if sum(c) == 10]) == math.comb(12, 2) == 66)
chk("neg_binomial_coeff", s.series((1-x)**-3, x, 0, 6).removeO().coeff(x, 5) == math.comb(7, 5) == 21)
chk("sum_coeffs_put1", sum(s.Poly((3*x-2)**10, x).all_coeffs()) == 1)
chk("even_coeff_sum", sum(math.comb(10, r) for r in range(0, 11, 2)) == 2**9)
chk("mod_7_103_25", pow(7, 103, 25) == 18)
chk("stars_bars", len([c for c in itertools.product(range(11), repeat=3) if sum(c) == 10]) == math.comb(12, 2))
def der(m): return sum(1 for p in itertools.permutations(range(m)) if all(p[i] != i for i in range(m)))
chk("derangement_4", der(4) == 9 and der(5) == 44)
chk("prob_at_least_one_six", 1 - Fraction(5, 6)**4 == Fraction(671, 1296))
# ---------- Matrices & determinants ----------
random.seed(1)
good = True
for _ in range(50):
    A = s.Matrix(3, 3, [random.randint(-6, 6) for _ in range(9)])
    if A.det() == 0: continue
    r1, r2, r3 = [A.row(i) for i in range(3)]
    cols = [r2.cross(r3).T, r3.cross(r1).T, r1.cross(r2).T]
    inv = s.Matrix.hstack(*cols) / A.det()
    good &= (inv - A.inv()).is_zero_matrix
chk("inv3x3_cross_products", good)
A2 = s.Matrix([[3, 5], [1, 2]]); chk("inv2x2_swap_negate", A2.inv() == s.Matrix([[2, -5], [-1, 3]]) / 1)
chk("cayley_hamilton_2x2", (A2**2 - A2.trace()*A2 + A2.det()*s.eye(2)).is_zero_matrix)
B = s.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]])  # det 3
chk("adj_kA", B.det() == 3 and (2*B).adjugate().det() == 576 == (2**3*3)**2)
# ---------- Vectors & 3D ----------
P = s.Matrix([1, 2, 3]); nrm = s.Matrix([1, 1, 1]); tpar = -(nrm.dot(P) + 0)/nrm.dot(nrm)
img = P + 2*tpar*nrm; chk("image_in_plane", list(img) == [-3, -2, -1])
chk("dist_parallel_planes", s.Abs(5-(-7))/s.sqrt(2**2+(-1)**2+2**2) == 4)
a, b, c = s.Matrix([1, 2, 3]), s.Matrix([2, -1, 1]), s.Matrix([3, 1, 4])
chk("stp_det_coplanar", a.dot(b.cross(c)) == s.Matrix.hstack(a, b, c).det() == 0)
# ---------- Coordinate geometry ----------
P2 = s.Matrix([2, 3]); L = (3, 4, -2); tt = -(L[0]*2+L[1]*3+L[2])/s.Integer(L[0]**2+L[1]**2)
foot = P2 + tt*s.Matrix([3, 4]); chk("foot_perp_line", list(foot) == [s.Rational(2, 25), s.Rational(11, 25)])
m_ = s.symbols('m'); cc = s.symbols('c')
sol = s.solve(s.discriminant(s.expand(x**2/16 + (m_*x+cc)**2/9 - 1)*144, x), cc)
chk("ellipse_tangent", all(s.simplify(sq**2 - (16*m_**2+9)) == 0 for sq in sol))
chk("parabola_tangent_c_a_over_m", s.solve(s.discriminant(s.expand((m_*x+cc)**2 - 4*3*x), x), cc) == [3/m_])
chk("tangent_length_sqrtS11", s.sqrt(5**2+4**2-4*5+6*4-12) == s.sqrt(33))
# ---------- Complex ----------
w = s.exp(2*s.pi*s.I/3)
chk("omega_power", abs(complex(((1+w-w**2)**7 - (-128*w**2)).evalf())) < 1e-9)
z1, z2 = 3+4j, 1-2j
chk("parallelogram_law", abs(abs(z1+z2)**2 + abs(z1-z2)**2 - 2*(abs(z1)**2+abs(z2)**2)) < 1e-9)
# ---------- Trigonometry ----------
chk("asin_bcos_range", s.maximum(3*s.sin(x)+4*s.cos(x), x, s.Interval(0, 2*s.pi)) == 5)
d = s.pi/180
chk("cos_product", abs((s.cos(20*d)*s.cos(40*d)*s.cos(80*d)).evalf(30) - s.Rational(1, 8)) < 1e-25)
chk("tan_product_60", abs((s.tan(20*d)*s.tan(40*d)*s.tan(80*d)).evalf(30) - s.sqrt(3).evalf(30)) < 1e-25)
# ---------- Statistics ----------
data = list(range(1, 11)); mu = Fraction(sum(data), 10); var = sum((Fraction(v)-mu)**2 for v in data)/10
chk("var_first_n", var == Fraction(10**2-1, 12))
chk("var_affine", sum((Fraction(3*v+7)-(3*mu+7))**2 for v in data)/10 == 9*var)
# ---------- Quadratics ----------
r = s.solve(x**2 - 5*x + 3, x); chk("sum_squares_roots", s.simplify(sum(ri**2 for ri in r) - (25 - 6)) == 0)
chk("cube_sum_roots", s.simplify(sum(ri**3 for ri in r) - (125 - 3*3*5)) == 0)
# ---------- Differentiation ----------
chk("inv_tan_sub", s.simplify(s.diff(s.atan(2*x/(1-x**2)), x) - 2/(1+x**2)) == 0)
chk("log_diff_xx", s.simplify(s.diff(x**x, x) - x**x*(s.log(x)+1)) == 0)

bad = [k for k, v in ok.items() if not v]
print(f"{len(ok)} checks, {len(ok)-len(bad)} passed"); print("FAILED:", bad)
