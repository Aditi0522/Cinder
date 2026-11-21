import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem algebra_bleqa_apbon2msqrtableqambsqon8b
  (a b : ℝ)
  (h₀ : 0 < a ∧ 0 < b)
  (h₁ : b ≤ a) :
  (a + b) / 2 - Real.sqrt (a * b) ≤ (a - b)^2 / (8 * b) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_cubrtrp1oncubrtreq3_rcubp1onrcubeq5778
  (r : ℝ)
  (h₀ : r^(1 / 3: ℝ) + 1 / r^(1 / 3: ℝ) = 3) :
  r^3 + 1 / r^3 = 5778 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_ineq_nto1onlt2m1on
  (n : ℕ) :
  (n : ℝ) ^ (1 / n : ℝ) ≤ 2 - 1 / n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_others_exirrpowirrrat :
  ∃ a b, Irrational a ∧ Irrational b ∧ ¬ Irrational (a^b) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_at2malt1
  (a : ℝ) :
  a * (2 - a) ≤ 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_unitcircatbpabsamblt1
  (a b: ℝ)
  (h₀ : a^2 + b^2 = 1) :
  a * b + |a - b| ≤ 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sqineq_unitcircatbpamblt1
  (a b: ℝ)
  (h₀ : a^2 + b^2 = 1) :
  a * b + (a - b) ≤ 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem algebra_sum1onsqrt2to1onsqrt10000lt198 :
  ∑ k ∈ (Finset.Icc (2 : ℕ) 10000), (1 / Real.sqrt k) < 198 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p1
  (i m o : ℕ)
  (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i)
  (h₁ : i*m*o = 2001) :
  i+m+o ≤ 671 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p12
  (a m c : ℕ)
  (h₀ : a + m + c = 12) :
  a*m*c + a*m + m*c + a*c ≤ 112 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p20
  (x y z : ℝ)
  (h₀ : 0 < x ∧ 0 < y ∧ 0 < z)
  (h₁ : x + 1/y = 4)
  (h₂ : y + 1/z = 1)
  (h₃ : z + 1/x = 7/3) :
  x*y*z = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p6
  (p q : ℕ)
  (h₀ : Nat.Prime p ∧ Nat.Prime q)
  (h₁ : 4 ≤ p ∧ p ≤ 18)
  (h₂ : 4 ≤ q ∧ q ≤ 18) :
  p * q - (p + q) ≠ 194 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2001_p21
  (a b c d : ℕ)
  (h₀ : a * b * c * d = Nat.factorial 8)
  (h₁ : a * b + a + b = 524)
  (h₂ : b * c + b + c = 146)
  (h₃ : c * d + c + d = 104) :
  ↑a - ↑d = (10 : ℤ) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2001_p5 :
  Finset.prod (Finset.filter (λ x => ¬ Even x) (Finset.range 10000)) (id : ℕ → ℕ) = (10000!) / ((2^5000) * (5000!)) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2002_p13
  (a b : ℝ)
  (h₀ : 0 < a ∧ 0 < b)
  (h₁ : a ≠ b)
  (h₂ : abs (a - 1/a) = 1)
  (h₃ : abs (b - 1/b) = 1) :
  a + b = Real.sqrt 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2002_p6
  (n : ℕ)
  (h₀ : 0 < n) :
  ∃ m, (m > n ∧ ∃ p, m * p ≤ m + p) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2003_p23
  (S : Finset ℕ)
  (h₀ : ∀ (k : ℕ), k ∈ S ↔ 0 < k ∧ ((k * k) : ℕ) ∣ (∏ i ∈ (Finset.Icc 1 9), i !)) :
  S.card = 672 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2003_p5
  (A M C : ℕ)
  (h₀ : A ≤ 9 ∧ M ≤ 9 ∧ C ≤ 9)
  (h₁ : Nat.ofDigits 10 [0,1,C,M,A] + Nat.ofDigits 10 [2,1,C,M,A] = 123422) :
  A + M + C = 14 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2008_p25
  (a b : ℕ → ℝ)
  (h₀ : ∀ n, a (n + 1) = Real.sqrt 3 * a n - b n)
  (h₁ : ∀ n, b (n + 1) = Real.sqrt 3 * b n + a n)
  (h₂ : a 100 = 2)
  (h₃ : b 100 = 4) :
  a 1 + b 1 = 1 / (2^98) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p6
  (m n p q : ℝ)
  (h₀ : p = 2 ^ m)
  (h₁ : q = 3 ^ n) :
  p^(2 * n) * (q^m) = 12^(m * n) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p7
  (x : ℝ)
  (n : ℕ)
  (a : ℕ → ℝ)
  (h₁ : ∀ m, a (m + 1) - a m = a (m + 2) - a (m + 1))
  (h₂ : a 1 = 2 * x - 3)
  (h₃ : a 2 = 5 * x - 11)
  (h₄ : a 3 = 3 * x + 1)
  (h₅ : a n = 2009) :
  n = 502 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2013_p4 :
  (2^2014 + 2^2012) / (2^2014 - 2^2012) = (5:ℝ) / 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2019_p12 (x y : ℝ) (h : x > 0 ∧ y > 0) (h₀ : x ≠ 1 ∧ y ≠ 1)
    (h₁ : Real.log x / Real.log 2 = Real.log 16 / Real.log y) (h₂ : x * y = 64) :
    (Real.log (x / y) / Real.log 2) ^ 2 = 20 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2020_p10
  (n : ℕ)
  (h₀ : 1 < n)
  (h₁ : Real.logb 2 (Real.logb 16 n) = Real.logb 4 (Real.logb 4 n)) :
  (Nat.digits 10 n).sum = 13 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2020_p15
  (a b : ℂ)
  (h₀ : a^3 - 8 = 0)
  (h₁ : b^3 - 8 * b^2 - 8 * b + 64 = 0) :
  ‖a - b‖ ≤ 2 * Real.sqrt 21 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

