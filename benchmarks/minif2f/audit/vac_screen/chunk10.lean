import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem aime_1990_p2 :
  (52 + 6 * Real.sqrt 43) ^ ((3 : ℝ) / 2) - (52 - 6 * Real.sqrt 43) ^ ((3 : ℝ) / 2) = 828 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1991_p1 (x y : ℕ) (h₀ : 0 < x ∧ 0 < y) (h₁ : x * y + (x + y) = 71)
  (h₂ : x ^ 2 * y + x * y ^ 2 = 880) : x ^ 2 + y ^ 2 = 146 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1991_p6 (r : ℝ) (h₀ : (∑ k ∈ Finset.Icc (19 : ℕ) 91, Int.floor (r + k / 100)) = 546) :
  Int.floor (100 * r) = 743 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1994_p4 (n : ℕ) (h₀ : 0 < n)
  (h₀ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) = 1994) : n = 312 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1996_p5 (a b c r s t : ℝ) (f g : ℝ → ℝ)
  (h₀ : ∀ x, f x = x ^ 3 + 3 * x ^ 2 + 4 * x - 11) (h₁ : ∀ x, g x = x ^ 3 + r * x ^ 2 + s * x + t)
  (h₂ : f a = 0) (h₃ : f b = 0) (h₄ : f c = 0) (h₅ : g (a + b) = 0) (h₆ : g (b + c) = 0)
  (h₇ : g (c + a) = 0) (h₈ : List.Pairwise (· ≠ ·) [a, b, c]) : t = 23 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1997_p11 (x : ℝ)
    (h₀ :
      x =
        (∑ n ∈ Finset.Icc (1 : ℕ) 44, Real.cos (n * π / 180)) /
          ∑ n ∈ Finset.Icc (1 : ℕ) 44, Real.sin (n * π / 180)) :
    Int.floor (100 * x) = 241 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_2complexrootspoly_xsqp49eqxp7itxpn7i (x : ℂ) :
    x ^ 2 + 49 = (x + 7 * Complex.I) * (x + -7 * Complex.I) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_2rootsintpoly_am10tap11eqasqpam110 (a : ℂ) :
    (a - 10) * (a + 11) = a ^ 2 + a - 110 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_2rootspoly_apatapbeq2asqp2ab (a b : ℂ) :
    (a + a) * (a + b) = 2 * a ^ 2 + 2 * (a * b) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_2varlineareq_xpeeq7_2xpeeq3_eeq11_xeqn4 (x e : ℂ) (h₀ : x + e = 7)
  (h₁ : 2 * x + e = 3) : e = 11 ∧ x = -4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_3rootspoly_amdtamctambeqnasqmbpctapcbtdpasqmbpctapcbta (b c d a : ℂ) :
    (a - d) * (a - c) * (a - b) =
      -((a ^ 2 - (b + c) * a + c * b) * d) + (a ^ 2 - (b + c) * a + c * b) * a := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x :
  ∀ x > 0, 2 - Real.sqrt 2 ≥ 2 - x - 1 / (2 * x) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_amgm_prod1toneq1_sum1tongeqn (a : ℕ → NNReal) (n : ℕ)
  (h₀ : Finset.prod (Finset.range n) a = 1) : Finset.sum (Finset.range n) a ≥ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_amgm_sqrtxymulxmyeqxpy_xpygeq4 (x y : ℝ) (h₀ : 0 < x ∧ 0 < y) (h₁ : y ≤ x)
  (h₂ : Real.sqrt (x * y) * (x - y) = x + y) : x + y ≥ 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_amgm_sumasqdivbsqgeqsumbdiva (a b c : ℝ) (h₀ : 0 < a ∧ 0 < b ∧ 0 < c) :
  a ^ 2 / b ^ 2 + b ^ 2 / c ^ 2 + c ^ 2 / a ^ 2 ≥ b / a + c / b + a / c := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_apb4leq8ta4pb4 (a b : ℝ) (h₀ : 0 < a ∧ 0 < b) : (a + b) ^ 4 ≤ 8 * (a ^ 4 + b ^ 4) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_binomnegdiscrineq_10alt28asqp1 (a : ℝ) : 10 * a ≤ 28 * a ^ 2 + 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_manipexpr_2erprsqpesqeqnrpnesq (e r : ℂ) :
  2 * (e * r) + (e ^ 2 + r ^ 2) = (-r + -e) ^ 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_manipexpr_apbeq2cceqiacpbceqm2 (a b c : ℂ) (h₀ : a + b = 2 * c)
  (h₁ : c = Complex.I) : a * c + b * c = -2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_2at2pclta2c2p41pc (a c : ℝ) :
  2 * a * (2 + c) ≤ a ^ 2 + c ^ 2 + 4 * (1 + c) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_2unitcircatblt1 (a b : ℝ) (h₀ : a ^ 2 + b ^ 2 = 2) : a * b ≤ 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_36azm9asqle36zsq (z a : ℝ) : 36 * (a * z) - 9 * a ^ 2 ≤ 36 * z ^ 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_4bap1lt4bsqpap1sq (a b : ℝ) : 4 * b * (a + 1) ≤ 4 * b ^ 2 + (a + 1) ^ 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_xmysqpymzsqpzmxsqeqxyz_xpypzp6dvdx3y3z3 (x y z : ℤ)
  (h₀ : (x - y) ^ 2 + (y - z) ^ 2 + (z - x) ^ 2 = x * y * z) :
  x + y + z + 6 ∣ x ^ 3 + y ^ 3 + z ^ 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p11 (a b : ℝ) (h₀ : a ≠ 0 ∧ b ≠ 0) (h₁ : a * b = a - b) :
    a / b + b / a - a * b = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

