import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_algebra_109 (a b : ℝ) (h₀ : 3 * a + 2 * b = 12) (h₁ : a = 4) : b = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_11 (a b : ℝ) (h₀ : a ≠ b) (h₁ : a ≠ 2 * b)
    (h₂ : (4 * a + 3 * b) / (a - 2 * b) = 5) : (a + 11 * b) / (a - b) = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_110 (q e : ℂ) (h₀ : q = 2 - 2 * Complex.I) (h₁ : e = 5 + 5 * Complex.I) :
    q * e = 20 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_116 (k x : ℝ) (h₀ : x = (13 - Real.sqrt 131) / 4)
    (h₁ : 2 * x ^ 2 - 13 * x + k = 0) : k = 19 / 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_119 (d e : ℝ) (h₀ : 2 * d = 17 * e - 8) (h₁ : 2 * e = d - 9) : e = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_123 (a b : ℕ) (h₀ : 0 < a ∧ 0 < b) (h₁ : a + b = 20) (h₂ : a = 3 * b) :
  a - b = 10 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_126 (x y : ℝ) (h₀ : 2 * 3 = x - 9) (h₁ : 2 * -5 = y + 1) : x = 15 ∧ y = -11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_13 (a b : ℝ)
  (h₀ : ∀ x, x - 3 ≠ 0 ∧ x - 5 ≠ 0 → 4 * x / (x ^ 2 - 8 * x + 15) = a / (x - 3) + b / (x - 5)) :
  a = -6 ∧ b = 10 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_131 (a b : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = 2 * x ^ 2 - 7 * x + 2)
  (h₁ : f a = 0) (h₂ : f b = 0) (h₃ : a ≠ b) : 1 / (a - 1) + 1 / (b - 1) = -1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_132 (x : ℝ) (f g : ℝ → ℝ) (h₀ : ∀ x, f x = x + 2) (h₁ : ∀ x, g x = x ^ 2)
  (h₂ : f (g x) = g (f x)) : x = -1 / 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_140 (a b c : ℝ) (h₀ : 0 < a ∧ 0 < b ∧ 0 < c)
  (h₁ : ∀ x, 24 * x ^ 2 - 19 * x - 35 = (a * x - 5) * (2 * (b * x) + c)) : a * b - 3 * c = -9 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_144 (a b c d : ℕ) (h₀ : 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d) (h₀ : (c : ℤ) - b = d)
    (h₁ : (b : ℤ) - a = d) (h₂ : a + b + c = 60) (h₃ : a + b > c) : d < 10 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_149 (f : ℝ → ℝ) (h₀ : ∀ x < -5, f x = x ^ 2 + 5)
  (h₁ : ∀ x ≥ -5, f x = 3 * x - 8) (h₂ : Fintype (f ⁻¹' {10})) :
  (∑ k ∈ (f ⁻¹' {10}).toFinset, k) = 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_15 (s : ℕ → ℕ → ℕ)
    (h₀ : ∀ a b, 0 < a ∧ 0 < b → s a b = a ^ (b : ℕ) + b ^ (a : ℕ)) : s 2 6 = 100 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_151 : Int.ceil (Real.sqrt 27) - Int.floor (Real.sqrt 26) = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_159 (b : ℝ) (f : ℝ → ℝ)
  (h₀ : ∀ x, f x = 3 * x ^ 4 - 7 * x ^ 3 + 2 * x ^ 2 - b * x + 1) (h₁ : f 1 = 1) : b = -2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_181 (n : ℝ) (h₀ : n ≠ 3) (h₁ : (n + 5) / (n - 3) = 2) : n = 11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_182 (y : ℂ) : 7 * (3 * y + 2) = 21 * y + 14 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_185 (s : Finset ℤ) (f : ℤ → ℤ) (h₀ : ∀ x, f x = abs (x + 4))
  (h₁ : ∀ x, x ∈ s ↔ f x < 9) : s.card = 17 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_190 : ((3 : ℝ) / 8 + 7 / 8) / (4 / 5) = 25 / 16 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_192 (q e d : ℂ) (h₀ : q = 11 - 5 * Complex.I) (h₁ : e = 11 + 5 * Complex.I)
    (h₂ : d = 2 * Complex.I) : q * e * d = 292 * Complex.I := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_206 (a b : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = x ^ 2 + a * x + b) (h₁ : 2 * a ≠ b)
  (h₂ : f (2 * a) = 0) (h₃ : f b = 0) : a + b = -1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_214 (a : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = a * (x - 2) ^ 2 + 3) (h₁ : f 4 = 4) :
  f 6 = 7 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_22 : Real.logb (5 ^ 2) (5 ^ 4) = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_224 (S : Finset ℕ)
  (h₀ : ∀ n : ℕ, n ∈ S ↔ Real.sqrt n < 7 / 2 ∧ 2 < Real.sqrt n) : S.card = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

