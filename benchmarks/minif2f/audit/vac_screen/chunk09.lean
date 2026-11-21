import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_numbertheory_582
  (n : ℕ)
  (h₀ : 0 < n)
  (h₁ : 3∣n) :
  ((n + 4) + (n + 6) + (n + 8)) % 9 = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_618
  (n : ℕ)
  (hn : n > 0)
  (p : ℕ → ℕ)
  (h₀ : ∀ x, p x = x^2 - x + 41)
  (h₁ : 1 < Nat.gcd (p n) (p (n+1))) :
  41 ≤ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_66 :
  194 % 11 = 7 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_711
  (m n : ℕ)
  (h₀ : 0 < m ∧ 0 < n)
  (h₁ : Nat.gcd m n = 8)
  (h₂ : Nat.lcm m n = 112) :
  72 ≤ m + n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_728 :
  (29^13 - 5^13) % 7 = 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_764
  (p : ℕ)
  (h₀ : Nat.Prime p)
  (h₁ : 7 ≤ p) :
  ∑ k ∈ Finset.Icc 1 (p-2), ((k: ZMod p)⁻¹ * ((k: ZMod p) + 1)⁻¹) = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_765
  (x : ℤ)
  (h₀ : x < 0)
  (h₁ : (24 * x) % 1199 = 15) :
  x ≤ -449 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_769 :
  (129^34 + 96^38) % 11 = 9 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_85 :
  1 * 3^3 + 2 * 3^2 + 2*3 + 2 = 53 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_99
  (n : ℕ)
  (h₀ : (2 * n) % 47 = 15) :
  n % 47 = 31 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_4x3m7y3neq2003
  (x y : ℤ) :
  4 * x^3 - 7 * y^3 ≠ 2003 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_aoddbdiv4asqpbsqmod8eq1
  (a : ℤ)
  (b : ℤ)
  (h₀ : Odd a)
  (h₁ : 4 ∣ b)
  (h₂ : b >= 0) :
  (a^2 + b^2) % 8 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_exk2powkeqapb2mulbpa2_aeq1
  (a b : ℕ)
  (h₀ : 0 < a ∧ 0 < b)
  (h₁ : ∃ k > 0, 2^k = (a + b^2) * (b + a^2)) :
  a = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_fxeq4powxp6powxp9powx_f2powmdvdf2pown
  (m n : ℕ)
  (f : ℕ → ℕ)
  (h₀ : ∀ x, f x = 4^x + 6^x + 9^x)
  (h₁ : 0 < m ∧ 0 < n)
  (h₂ : m ≤ n) :
  f (2^m)∣f (2^n) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_notEquiv2i2jasqbsqdiv8 :
  ¬ (∀ a b : ℤ, (∃ i j, a = 2*i ∧ b=2*j) ↔ (∃ k, a^2 + b^2 = 8*k)) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem numbertheory_x5neqy2p4
  (x y : ℤ) :
  x^5 ≠ y^2 + 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aimeII_2001_p3 (x : ℕ → ℤ) (h₀ : x 1 = 211) (h₂ : x 2 = 375) (h₃ : x 3 = 420)
  (h₄ : x 4 = 523) (h₆ : ∀ n ≥ 5, x n = x (n - 1) - x (n - 2) + x (n - 3) - x (n - 4)) :
  x 531 + x 753 + x 975 = 898 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aimeII_2020_p6 (t : ℕ → ℚ) (h₀ : t 1 = 20) (h₁ : t 2 = 21)
  (h₂ : ∀ n ≥ 3, t n = (5 * t (n - 1) + 1) / (25 * t (n - 2))) :
  ↑(t 2020).den + (t 2020).num = 626 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aimeI_2000_p7 (x y z : ℝ) (m : ℚ) (h₀ : 0 < x ∧ 0 < y ∧ 0 < z) (h₁ : x * y * z = 1)
  (h₂ : x + 1 / z = 5) (h₃ : y + 1 / x = 29) (h₄ : z + 1 / y = m) (h₅ : 0 < m) :
  ↑m.den + m.num = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1983_p9 (x : ℝ) (h₀ : 0 < x ∧ x < Real.pi) :
  12 ≤ (9 * (x ^ 2 * Real.sin x ^ 2) + 4) / (x * Real.sin x) := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1984_p15 (x y z w : ℝ)
    (h₀ :
      x ^ 2 / (2 ^ 2 - 1) + y ^ 2 / (2 ^ 2 - 3 ^ 2) + z ^ 2 / (2 ^ 2 - 5 ^ 2) +
          w ^ 2 / (2 ^ 2 - 7 ^ 2) =
        1)
    (h₁ :
      x ^ 2 / (4 ^ 2 - 1) + y ^ 2 / (4 ^ 2 - 3 ^ 2) + z ^ 2 / (4 ^ 2 - 5 ^ 2) +
          w ^ 2 / (4 ^ 2 - 7 ^ 2) =
        1)
    (h₂ :
      x ^ 2 / (6 ^ 2 - 1) + y ^ 2 / (6 ^ 2 - 3 ^ 2) + z ^ 2 / (6 ^ 2 - 5 ^ 2) +
          w ^ 2 / (6 ^ 2 - 7 ^ 2) =
        1)
    (h₃ :
      x ^ 2 / (8 ^ 2 - 1) + y ^ 2 / (8 ^ 2 - 3 ^ 2) + z ^ 2 / (8 ^ 2 - 5 ^ 2) +
          w ^ 2 / (8 ^ 2 - 7 ^ 2) =
        1) :
    x ^ 2 + y ^ 2 + z ^ 2 + w ^ 2 = 36 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1984_p5 (a b : ℝ) (h₀ : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5)
  (h₁ : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7) : a * b = 512 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1987_p8 :
  IsGreatest { n : ℕ | 0 < n ∧ ∃! k : ℕ, (8 : ℝ) / 15 < n / (n + k) ∧ (n : ℝ) / (n + k) < 7 / 13 } 112 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1988_p3 (x : ℝ) (h₀ : 0 < x)
  (h₁ : Real.logb 2 (Real.logb 8 x) = Real.logb 8 (Real.logb 2 x)) : Real.logb 2 x ^ 2 = 27 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem aime_1988_p4 (n : ℕ) (a : ℕ → ℝ) (h₀ : ∀ n, abs (a n) < 1)
  (h₁ : (∑ k ∈ Finset.range n, abs (a k)) = 19 + abs (∑ k ∈ Finset.range n, a k)) : 20 ≤ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

