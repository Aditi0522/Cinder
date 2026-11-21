import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem amc12b_2021_p3
  (x : ℝ)
  (h₀ : 2 + 1 / (1 + 1 / (2 + 2 / (3 + x))) = 144 / 53) :
  x = 3 / 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12b_2021_p4
  (m a : ℕ)
  (h₀ : 0 < m ∧ 0 < a)
  (h₁ : ↑m / ↑a = (3:ℝ) / 4) :
  (84 * ↑m + 70 * ↑a) / (↑m + ↑a) = (76:ℝ) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem amc12b_2021_p9 :
  (Real.log 80 / Real.log 2) / (Real.log 2 / Real.log 40) - (Real.log 160 / Real.log 2) / (Real.log 2 / Real.log 20) = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1959_p1
  (n : ℕ)
  (h₀ : 0 < n) :
  Nat.gcd (21*n + 4) (14*n + 3) = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1960_p2
  (x : ℝ)
  (h₀ : 0 ≤ 1 + 2 * x)
  (h₁ : (1 - Real.sqrt (1 + 2 * x))^2 ≠ 0)
  (h₂ : (4 * x^2) / (1 - Real.sqrt (1 + 2*x))^2 < 2*x + 9)
  (h₃ : x ≠ 0) :
  -(1 / 2) ≤ x ∧ x < 45 / 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1962_p2
  (x : ℝ)
  (h₀ : 0 ≤ 3 - x)
  (h₁ : 0 ≤ x + 1)
  (h₂ : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1)) :
  -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1963_p5 :
  Real.cos (π / 7) - Real.cos (2 * π / 7) + Real.cos (3 * π / 7) = 1 / 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1964_p2
  (a b c : ℝ)
  (h₀ : 0 < a ∧ 0 < b ∧ 0 < c)
  (h₁ : c < a + b)
  (h₂ : b < a + c)
  (h₃ : a < b + c) :
  a^2 * (b + c - a) + b^2 * (c + a - b) + c^2 * (a + b - c) ≤ 3 * a * b * c := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1965_p2
  (x y z : ℝ)
  (a : ℕ → ℝ)
  (h₀ : 0 < a 0 ∧ 0 < a 4 ∧ 0 < a 8)
  (h₁ : a 1 < 0 ∧ a 2 < 0)
  (h₂ : a 3 < 0 ∧ a 5 < 0)
  (h₃ : a 6 < 0 ∧ a 7 < 0)
  (h₄ : 0 < a 0 + a 1 + a 2)
  (h₅ : 0 < a 3 + a 4 + a 5)
  (h₆ : 0 < a 6 + a 7 + a 8)
  (h₇ : a 0 * x + a 1 * y + a 2 * z = 0)
  (h₈ : a 3 * x + a 4 * y + a 5 * z = 0)
  (h₉ : a 6 * x + a 7 * y + a 8 * z = 0) :
  x = 0 ∧ y = 0 ∧ z = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1968_p5_1
  (a : ℝ)
  (f : ℝ → ℝ)
  (h₀ : 0 < a)
  (h₁ : ∀ x, f (x + a) = 1 / 2 + Real.sqrt (f x - (f x)^2)) :
  ∃ b > 0, ∀ x, f (x + b) = f x := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1969_p2
  (m n : ℝ)
  (k : ℕ)
  (a : ℕ → ℝ)
  (y : ℝ → ℝ)
  (h₀ : 0 < k)
  (h₁ : ∀ x, y x = ∑ i ∈ Finset.range k, ((Real.cos (a i + x)) / (2^i)))
  (h₂ : y m = 0)
  (h₃ : y n = 0) :
  ∃ t : ℤ, m - n = t * π := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1974_p3
  (n : ℕ) :
  ¬ 5∣∑ k ∈ Finset.range (n + 1), (Nat.choose (2 * n + 1) (2 * k + 1)) * (2^(3 * k)) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1977_p6
  (f : ℕ → ℕ)
  (h₀ : ∀ n, 0 < f n)
  (h₁ : ∀ n, 0 < n → f (f n) < f (n + 1)) :
  ∀ n, 0 < n → f n = n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1981_p6
  (f : ℕ → ℕ → ℕ)
  (g : ℕ → ℕ)
  (h₀ : ∀ y, f 0 y = y + 1)
  (h₁ : ∀ x, f (x + 1) 0 = f x 1)
  (h₂ : ∀ x y, f (x + 1) (y + 1) = f x (f (x + 1) y))
  (h₃ : g 0 = 2)
  (h₄ : ∀ n, g (n + 1) = 2^(g n)) :
  f 4 1981 = g 1983 - 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1982_p1
  (f : ℕ → ℕ)
  (h₀ : ∀ m n, (0 < m ∧ 0 < n) → f (m + n) - f m - f n = (0 : ℤ) ∨ f (m + n) - f m - f n = (1 : ℤ))
  (h₁ : f 2 = 0)
  (h₂ : 0 < f 3)
  (h₃ : f 9999 = 3333) :
  f 1982 = 660 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1983_p6
  (a b c : ℝ)
  (h₀ : 0 < a ∧ 0 < b ∧ 0 < c)
  (h₁ : c < a + b)
  (h₂ : b < a + c)
  (h₃ : a < b + c) :
  0 ≤ a^2 * b * (a - b) + b^2 * c * (b - c) + c^2 * a * (c - a) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1984_p6
  (a b c d k m : ℕ)
  (h₀ : 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d)
  (h₁ : Odd a ∧ Odd b ∧ Odd c ∧ Odd d)
  (h₂ : a < b ∧ b < c ∧ c < d)
  (h₃ : a * d = b * c)
  (h₄ : a + d = 2^k)
  (h₅ : b + c = 2^m) :
  a = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1985_p6
  (f : ℕ → NNReal → ℝ)
  (h₀ : ∀ x, f 1 x = x)
  (h₁ : ∀ x n, f (n + 1) x = f n x * (f n x + 1 / n)) :
  ∃! a, ∀ n, 0 < n → 0 < f n a ∧ f n a < f (n + 1) a ∧ f (n + 1) a < 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1992_p1
  (p q r : ℤ)
  (h₀ : 1 < p ∧ p < q ∧ q < r)
  (h₁ : (p - 1) * (q - 1) * (r - 1)∣(p * q * r - 1)) :
  (p, q, r) = (2, 4, 8) ∨ (p, q, r) = (3, 5, 15) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_1997_p5
  (x y : ℕ)
  (h₀ : 0 < x ∧ 0 < y)
  (h₁ : x^(y^2) = y^x) :
  (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_2001_p6
  (a b c d : ℕ)
  (h₀ : 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d)
  (h₁ : d < c)
  (h₂ : c < b)
  (h₃ : b < a)
  (h₄ : a * c + b * d = (b + d + a - c) * (b + d + c - a)) :
  ¬ Nat.Prime (a * b + c * d) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imo_2019_p1
  (f : ℤ → ℤ) :
  ((∀ a b, f (2 * a) + (2 * f b) = f (f (a + b))) ↔ (∀ z, f z = 0 \/ ∃ c, ∀ z, f z = 2 * z + c)) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem imosl_2007_algebra_p6
  (a : ℕ → NNReal)
  (h₀ : ∑ x ∈ Finset.range 100, ((a (x + 1))^2) = 1) :
  ∑ x ∈ Finset.range 99, ((a (x + 1))^2 * a (x + 2)) + (a 100)^2 * a 1 < 12 / 25 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_11div10tonmn1ton
  (n : ℕ) :
  11 ∣ (10^n - (-1 : ℤ)^n) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem induction_12dvd4expnp1p20
  (n : ℕ) :
  12 ∣ 4^(n+1) + 20 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

