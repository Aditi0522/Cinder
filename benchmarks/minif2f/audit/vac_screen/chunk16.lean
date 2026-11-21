import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_algebra_482 (m n : ℕ) (k : ℝ) (f : ℝ → ℝ) (h₀ : Nat.Prime m) (h₁ : Nat.Prime n)
  (h₂ : ∀ x, f x = x ^ 2 - 12 * x + k) (h₃ : f m = 0) (h₄ : f n = 0) (h₅ : m ≠ n) : k = 35 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_493 (f : ℝ → ℝ) (h₀ : ∀ x, f x = x ^ 2 - 4 * Real.sqrt x + 1) :
    f (f 4) = 70 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_509 :
  Real.sqrt ((5 / Real.sqrt 80 + Real.sqrt 845 / 9 + Real.sqrt 45) / Real.sqrt 5) = 13 / 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_51 (a b : ℝ) (h₀ : 0 < a ∧ 0 < b) (h₁ : a + b = 35) (h₂ : a = 2 / 5 * b) :
    b - a = 15 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_510 (x y : ℝ) (h₀ : x + y = 13) (h₁ : x * y = 24) :
  Real.sqrt (x ^ 2 + y ^ 2) = 11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_536 : ↑3! * ((2 : ℝ) ^ 3 + Real.sqrt 9) / 2 = (33 : ℝ) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_547 (x y : ℝ) (h₀ : x = 5) (h₁ : y = 2) : Real.sqrt (x ^ 3 - 2 ^ y) = 11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_55 (q p : ℝ) (h₀ : q = 2 - 4 + 6 - 8 + 10 - 12 + 14)
  (h₁ : p = 3 - 6 + 9 - 12 + 15 - 18 + 21) : q / p = 2 / 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_568 (a : ℝ) :
    (a - 1) * (a + 1) * (a + 2) - (a - 2) * (a + 1) = a ^ 3 + a ^ 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_59 (b : ℝ) (h₀ : (4 : ℝ) ^ b + 2 ^ 3 = 12) : b = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_616 (f g : ℝ → ℝ) (h₀ : ∀ x, f x = x ^ 3 + 2 * x + 1)
    (h₁ : ∀ x, g x = x - 1) : f (g 1) = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_67 (f g : ℝ → ℝ) (h₀ : ∀ x, f x = 5 * x + 3) (h₁ : ∀ x, g x = x ^ 2 - 2) :
    g (f (-1)) = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_69 (rows seats : ℕ) (h₀ : rows * seats = 450)
  (h₁ : (rows + 5) * (seats - 3) = 450) : rows = 25 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_73 (p q r x : ℂ) (h₀ : (x - p) * (x - q) = (r - p) * (r - q)) (h₁ : x ≠ r) :
  x = p + q - r := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_77 (a b : ℝ) (f : ℝ → ℝ) (h₀ : a ≠ 0 ∧ b ≠ 0) (h₁ : a ≠ b)
  (h₂ : ∀ x, f x = x ^ 2 + a * x + b) (h₃ : f a = 0) (h₄ : f b = 0) : a = 1 ∧ b = -2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_89 (b : ℝ) (h₀ : b ≠ 0) :
  (7 * b ^ 3) ^ 2 * (4 * b ^ 2) ^ (-(3 : ℤ)) = 49 / 64 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_algebra_96 (x y z a : ℝ) (h₀ : 0 < x ∧ 0 < y ∧ 0 < z)
  (h₁ : Real.log x - Real.log y = a) (h₂ : Real.log y - Real.log z = 15)
  (h₃ : Real.log z - Real.log x = -7) : a = -8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_101 : 17 * 18 % 4 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_102 : 2 ^ 8 % 5 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_109 (v : ℕ → ℕ) (h₀ : ∀ n, v n = 2 * n - 1) :
  (∑ k ∈ Finset.Icc 1 100, v k) % 7 = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_110 (a b : ℕ) (h₀ : 0 < a ∧ 0 < b ∧ b ≤ a) (h₁ : (a + b) % 10 = 2)
  (h₂ : (2 * a + b) % 10 = 1) : (a - b) % 10 = 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_126 (x a : ℕ) (h₀ : 0 < x ∧ 0 < a) (h₁ : Nat.gcd a 40 = x + 3)
  (h₂ : Nat.lcm a 40 = x * (x + 3))
  (h₃ : ∀ b : ℕ, 0 < b → Nat.gcd b 40 = x + 3 ∧ Nat.lcm b 40 = x * (x + 3) → a ≤ b) : a = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_13 (u v : ℕ) (S : Set ℕ)
  (h₀ : ∀ n : ℕ, n ∈ S ↔ 0 < n ∧ 14 * n % 100 = 46) (h₁ : IsLeast S u)
  (h₂ : IsLeast (S \ {u}) v) : (u + v : ℚ) / 2 = 64 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_132 : 2004 % 12 = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_136 (n : ℕ) (h₀ : 123 * n + 17 = 39500) : n = 321 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

