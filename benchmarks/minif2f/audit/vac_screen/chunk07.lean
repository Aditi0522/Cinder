import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_algebra_80
  (x : ℝ)
  (h₀ : x ≠ -1)
  (h₁ : (x - 9) / (x + 1) = 2) :
  x = -11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_100
  (n : ℕ)
  (h₀ : 0 < n)
  (h₁ : Nat.gcd n 40 = 10)
  (h₂ : Nat.lcm n 40 = 280) :
  n = 70 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_1124
  (n : ℕ)
  (h₀ : n ≤ 9)
  (h₁ : 18∣374 * 10 + n) :
  n = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_12 :
  Finset.card (Finset.filter (λ x => 20∣x) (Finset.Icc 15 85)) = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_127 :
  (∑ k ∈ (Finset.range 101), 2^k) % 7 = 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_135
  (n A B C : ℕ)
  (h₀ : n = 3^17 + 3^10)
  (h₁ : 11 ∣ (n + 1))
  (h₂ : [A,B,C].Pairwise (·≠·))
  (h₃ : {A,B,C} ⊂ Finset.Icc 0 9)
  (h₄ : Odd A ∧ Odd C)
  (h₅ : ¬ 3 ∣ B)
  (h₆ : Nat.digits 10 n = [B,A,B,C,C,A,C,B,A]) :
  100 * A + 10 * B + C = 129 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_150
  (n : ℕ)
  (h₀ : ¬ Nat.Prime (7 + 30 * n)) :
  6 ≤ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_175 :
  (2^2010) % 10 = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_185
  (n : ℕ)
  (h₀ : n % 5 = 3) :
  (2 * n) % 5 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_207 :
  8 * 9^2 + 5 * 9 + 2 = 695 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_212 :
  (16^17 * 17^18 * 18^19) % 10 = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_222
  (b : ℕ)
  (h₀ : Nat.lcm 120 b = 3720)
  (h₁ : Nat.gcd 120 b = 8) :
  b = 248 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_227
  (x y n : ℕ+)
  (h₀ : ↑x / (4:ℝ) + y / 6 = (x + y) / n) :
  n = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_229 :
  (5^30) % 7 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_233
  (b :  ZMod (11^2))
  (h₀ : b = 24⁻¹) :
  b = 116 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_234
  (a b : ℕ)
  (h₀ : 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9)
  (h₁ : (10 * a + b)^3 = 912673) :
  a + b = 16 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_235 :
  (29 * 79 + 31 * 81) % 10 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_237 :
  (∑ k ∈ (Finset.range 101), k) % 6 = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_239 :
  (∑ k ∈ Finset.Icc 1 12, k) % 4 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_247
  (n : ℕ)
  (h₀ : (3 * n) % 11 = 2) :
  n % 11 = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_254 :
  (239 + 174 + 83) % 10 = 6 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_277
  (m n : ℕ)
  (h₀ : Nat.gcd m n = 6)
  (h₁ : Nat.lcm m n = 126) :
  60 ≤ m + n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_293
  (n : ℕ)
  (h₀ : n ≤ 9)
  (h₁ : 11∣20 * 100 + 10 * n + 7) :
  n = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_296
  (n : ℕ)
  (h₀ : 2 ≤ n)
  (h₁ : ∃ x, x^3 = n)
  (h₂ : ∃ t, t^4 = n) :
  4096 ≤ n := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_299 :
  (1 * 3 * 5 * 7 * 9 * 11 * 13) % 10 = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

