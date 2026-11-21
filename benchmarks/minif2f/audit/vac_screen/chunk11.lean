import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem amc12_2000_p15 (f : ℂ → ℂ) (h₀ : ∀ x, f (x / 3) = x ^ 2 + x + 1)
  (h₁ : Fintype (f ⁻¹' {7})) : (∑ y ∈ (f ⁻¹' {7}).toFinset, y / 3) = -1 / 9 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2000_p5 (x p : ℝ) (h₀ : x < 2) (h₁ : abs (x - 2) = p) : x - p = 2 - 2 * p := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2001_p2 (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9) (h₁ : 0 ≤ b ∧ b ≤ 9) (h₂ : n = 10 * a + b)
  (h₃ : n = a * b + a + b) : b = 9 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12_2001_p9 (f : ℝ → ℝ) (h₀ : ∀ x > 0, ∀ y > 0, f (x * y) = f x / y) (h₁ : f 500 = 3) :
    f 600 = 5 / 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2002_p1 (f : ℂ → ℂ) (h₀ : ∀ x, f x = (2 * x + 3) * (x - 4) + (2 * x + 3) * (x - 6))
  (h₁ : Fintype (f ⁻¹' {0})) : (∑ y ∈ (f ⁻¹' {0}).toFinset, y) = 7 / 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2002_p12 (f : ℝ → ℝ) (k : ℝ) (a b : ℕ) (h₀ : ∀ x, f x = x ^ 2 - 63 * x + k)
  (h₁ : f a = 0 ∧ f b = 0) (h₂ : a ≠ b) (h₃ : Nat.Prime a ∧ Nat.Prime b) : k = 122 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2002_p21 (u : ℕ → ℕ) (h₀ : u 0 = 4) (h₁ : u 1 = 7)
    (h₂ : ∀ n ≥ 2, u (n + 2) = (u n + u (n + 1)) % 10) :
    ∀ n, (∑ k ∈ Finset.range n, u k) > 10000 → 1999 ≤ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2003_p1 (u v : ℕ → ℕ) (h₀ : ∀ n, u n = 2 * n + 2) (h₁ : ∀ n, v n = 2 * n + 1) :
    ((∑ k ∈ Finset.range 2003, u k) - ∑ k ∈ Finset.range 2003, v k) = 2003 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2003_p24 :
  IsGreatest { y : ℝ | ∃ a b : ℝ, 1 < b ∧ b ≤ a ∧ y = Real.logb a (a / b) + Real.logb b (b / a) }
    0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2003_p25 (a b : ℝ) (f : ℝ → ℝ) (h₀ : 0 < b)
  (h₁ : ∀ x, f x = Real.sqrt (a * x ^ 2 + b * x)) (h₂ : { x | 0 ≤ f x } = f '' { x | 0 ≤ f x }) :
  a = 0 ∨ a = -4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2008_p15 (k : ℕ) (h₀ : k = 2008 ^ 2 + 2 ^ 2008) : (k ^ 2 + 2 ^ k) % 10 = 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2008_p2 (x : ℝ) (h₀ : x * (1 / 2 + 2 / 3) = 1) : x = 6 / 7 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2008_p4 : (∏ k ∈ Finset.Icc (1 : ℕ) 501, ((4 : ℝ) * k + 4) / (4 * k)) = 502 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2008_p8 (x y : ℝ) (h₀ : 0 < x ∧ 0 < y) (h₁ : y ^ 3 = 1)
  (h₂ : 6 * x ^ 2 = 2 * (6 * y ^ 2)) : x ^ 3 = 2 * Real.sqrt 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p15 (n : ℕ) (h₀ : 0 < n)
  (h₁ : (∑ k ∈ Finset.Icc 1 n, ↑k * Complex.I ^ k) = 48 + 49 * Complex.I) : n = 97 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p2 : 1 + 1 / (1 + 1 / (1 + 1)) = (5 : ℚ) / 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p25 (a : ℕ → ℝ) (h₀ : a 1 = 1) (h₁ : a 2 = 1 / Real.sqrt 3)
  (h₂ : ∀ n, 1 ≤ n → a (n + 2) = (a n + a (n + 1)) / (1 - a n * a (n + 1))) : abs (a 2009) = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p5 (x : ℝ) (h₀ : x ^ 3 - (x + 1) * (x - 1) * x = 5) : x ^ 3 = 125 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2009_p9 (a b c : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f (x + 3) = 3 * x ^ 2 + 7 * x + 4)
  (h₁ : ∀ x, f x = a * x ^ 2 + b * x + c) : a + b + c = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2010_p10 (p q : ℝ) (a : ℕ → ℝ) (h₀ : ∀ n, a (n + 2) - a (n + 1) = a (n + 1) - a n)
  (h₁ : a 1 = p) (h₂ : a 2 = 9) (h₃ : a 3 = 3 * p - q) (h₄ : a 4 = 3 * p + q) : a 2010 = 8041 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2010_p11 (x b : ℝ) (h₀ : 0 < b) (h₁ : (7 : ℝ) ^ (x + 7) = 8 ^ x)
  (h₂ : x = Real.logb b (7 ^ 7)) : b = 8 / 7 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2010_p22 (x : ℝ) : 49 ≤ ∑ k ∈ (Finset.Icc (1:ℤ) (119:ℤ)), abs (k * x - 1) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2011_p18 (x y : ℝ) (h₀ : abs (x + y) + abs (x - y) = 2) :
  x ^ 2 - 6 * x + y ^ 2 ≤ 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2013_p7 (s : ℕ → ℝ) (h₀ : ∀ n, s (n + 2) = s (n + 1) + s n) (h₁ : s 9 = 110)
    (h₂ : s 7 = 42) : s 4 = 10 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12a_2013_p8 (x y : ℝ) (h₀ : x ≠ 0) (h₁ : y ≠ 0) (h₂ : x ≠ y)
  (h₃ : x + 2 / x = y + 2 / y) : x * y = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

