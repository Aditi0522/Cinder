import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem induction_1pxpownlt1pnx
  (x : ℝ)
  (n : ℕ)
  (h₀ : -1 < x)
  (h₁ : 0 < n) :
  (1 + ↑n*x) ≤ (1 + x)^(n:ℕ) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_nfactltnexpnm1ngt3
  (n : ℕ)
  (h₀ : 3 ≤ n) :
  (n)! < n^(n - 1) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_pord1p1on2powklt5on2
  (n : ℕ)
  (h₀ : 0 < n) :
  ∏ k ∈ Finset.Icc 1 n, (1 + (1:ℝ) / 2^k) < 5 / 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_pprime_pdvdapowpma
  (p a : ℕ)
  (h₀ : 0 < a)
  (h₁ : Nat.Prime p) :
  p ∣ (a^p - a) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_prod1p1onk3le3m1onn
  (n : ℕ)
  (h₀ : 0 < n) :
  ∏ k ∈ Finset.Icc 1 n, (1 + (1:ℝ) / k^3) ≤ (3:ℝ) - 1 / ↑n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_sumkexp3eqsumksq
  (n : ℕ) :
  ∑ k ∈ Finset.range n, k^3 = (∑ k ∈ Finset.range n, k)^2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_107
  (x y : ℝ)
  (h₀ : x^2 + 8 * x + y^2 - 6 * y = 0) :
  (x + 4)^2 + (y-3)^2 = 5^2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_113
  (x : ℝ) :
  x^2 - 14 * x + 3 ≥ 7^2 - 14 * 7 + 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_114
  (a : ℝ)
  (h₀ : a = 8) :
  (16 * (a^2) ^ (1 / 3 : ℝ)) ^ (1 / 3 : ℝ) = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_125
  (x y : ℕ)
  (h₀ : 0 < x ∧ 0 < y)
  (h₁ : 5 * x = y)
  (h₂ : (↑x - (3:ℤ)) + (y - (3:ℤ)) = 30) :
  x = 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_129
  (a : ℝ)
  (h₀ : a ≠ 0)
  (h₁ : 8⁻¹ / 4⁻¹ - a⁻¹ = 1) :
  a = -2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_137
  (x : ℕ)
  (h₀ : ↑x + (4:ℝ) / (100:ℝ) * ↑x = 598) :
  x = 575 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_139
  (s : ℝ → ℝ → ℝ)
  (h₀ : ∀ x, ∀ y, x≠0 -> y≠0 -> s x y = (1/y - 1/x) / (x-y)) :
  s 3 11 = 1/33 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_141
  (a b : ℝ)
  (h₁ : (a * b)=180)
  (h₂ : 2 * (a + b)=54) :
  (a^2 + b^2) = 369 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_142
  (m b : ℝ)
  (h₀ : m * 7 + b = -1)
  (h₁ : m * (-1) + b = 7) :
  m + b = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_143
  (f g : ℝ → ℝ)
  (h₀ : ∀ x, f x = x + 1)
  (h₁ : ∀ x, g x = x^2 + 3) :
  f (g 2) = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_148
  (c : ℝ)
  (f : ℝ → ℝ)
  (h₀ : ∀ x, f x = c * x^3 - 9 * x + 3)
  (h₁ : f 2 = 9) :
  c = 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_153
  (n : ℝ)
  (h₀ : n = 1 / 3) :
  Int.floor (10 * n) + Int.floor (100 * n) + Int.floor (1000 * n) + Int.floor (10000 * n) = 3702 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_156
  (x y : ℝ)
  (f g : ℝ → ℝ)
  (h₀ : ∀t, f t = t^4)
  (h₁ : ∀t, g t = 5 * t^2 - 6)
  (h₂ : f x = g x)
  (h₃ : f y = g y)
  (h₄ : x^2 < y^2) :
  y^2 - x^2 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_158
  (a : ℕ)
  (h₀ : Even a)
  (h₁ : ∑ k ∈ Finset.range 8, (2 * k + 1) - ∑ k ∈ Finset.range 5, (a + 2 * k) = (4:ℤ)) :
  a = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_160
  (n x : ℝ)
  (h₀ : n + x = 97)
  (h₁ : n + 5 * x = 265) :
  n + 2 * x = 139 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_17
  (a : ℝ)
  (h₀ : Real.sqrt (4 + Real.sqrt (16 + 16 * a)) + Real.sqrt (1 + Real.sqrt (1 + a)) = 6) :
  a = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_170
  (S : Finset ℤ)
  (h₀ : ∀ (n : ℤ), n ∈ S ↔ abs (n - 2) ≤ 5 + 6 / 10) :
  S.card = 11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_171
  (f : ℝ → ℝ)
  (h₀ : ∀x, f x = 5 * x + 4) :
  f 1 = 9 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_176
  (x : ℝ) :
  (x + 1)^2 * x = x^3 + 2 * x^2 + x := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

