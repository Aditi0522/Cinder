import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_numbertheory_35 (S : Finset ℕ) (h₀ : ∀ n : ℕ, n ∈ S ↔ n ∣ Nat.sqrt 196) :
    (∑ k ∈ S, k) = 24 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_37 : Nat.lcm 9999 100001 = 90900909 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_370 (n : ℕ) (h₀ : n % 7 = 3) : (2 * n + 1) % 7 = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_403 : (∑ k ∈ Nat.properDivisors 198, k) = 270 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_405 (a b c : ℕ) (t : ℕ → ℕ) (h₀ : t 0 = 0) (h₁ : t 1 = 1)
  (h₂ : ∀ n > 1, t n = t (n - 2) + t (n - 1)) (h₃ : a ≡ 5 [MOD 16]) (h₄ : b ≡ 10 [MOD 16])
  (h₅ : c ≡ 15 [MOD 16]) : (t a + t b + t c) % 7 = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_412 (x y : ℤ) (h₀ : x % 19 = 4) (h₁ : y % 19 = 7) :
  (x + 1) ^ 2 * (y + 5) ^ 3 % 19 = 13 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_42 (S : Set ℕ) (u v : ℕ) (h₀ : ∀ a : ℕ, a ∈ S ↔ 0 < a ∧ 27 * a % 40 = 17)
    (h₁ : IsLeast S u) (h₂ : IsLeast (S \ {u}) v) : u + v = 62 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_43 : IsGreatest { n : ℕ | 15 ^ n ∣ 942! } 233 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_45 : Nat.gcd 6432 132 + 11 = 23 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_458 (n : ℕ) (h₀ : n % 8 = 7) : n % 4 = 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_461 (n : ℕ)
  (h₀ : n = Finset.card (Finset.filter (fun x => Nat.gcd x 8 = 1) (Finset.Icc 1 7))) :
  3 ^ n % 8 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_466 : (∑ k ∈ Finset.range 11, k) % 9 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_48 (b : ℕ) (h₀ : 0 < b) (h₁ : 3 * b ^ 2 + 2 * b + 1 = 57) : b = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_530 (n k : ℕ) (h₀ : 0 < n ∧ 0 < k) (h₀ : (n : ℝ) / k < 6)
  (h₁ : (5 : ℝ) < n / k) : 22 ≤ Nat.lcm n k / Nat.gcd n k := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_629 : IsLeast { t : ℕ | 0 < t ∧ Nat.lcm 12 t ^ 3 = (12 * t) ^ 2 } 18 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_64 : IsLeast { x : ℕ | 30 * x ≡ 42 [MOD 47] } 39 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_640 : (91145 + 91146 + 91147 + 91148) % 4 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_668 (l r : ZMod 7) (h₀ : l = (2 + 3)⁻¹) (h₁ : r = 2⁻¹ + 3⁻¹) :
  l - r = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_690 :
    IsLeast { a : ℕ | 0 < a ∧ a ≡ 2 [MOD 3] ∧ a ≡ 4 [MOD 5] ∧ a ≡ 6 [MOD 7] ∧ a ≡ 8 [MOD 9] } 314 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_709 (n : ℕ) (h₀ : 0 < n) (h₁ : Finset.card (Nat.divisors (2 * n)) = 28)
  (h₂ : Finset.card (Nat.divisors (3 * n)) = 30) : Finset.card (Nat.divisors (6 * n)) = 35 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_739 : 9! % 10 = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_780 (m x : ℤ) (h₀ : 0 ≤ x) (h₁ : 10 ≤ m ∧ m ≤ 99) (h₂ : 6 * x % m = 1)
  (h₃ : (x - 6 ^ 2) % m = 0) : m = 43 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_81 : 71 % 3 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_84 : Int.floor ((9 : ℝ) / 160 * 100) = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_92 (n : ℕ) (h₀ : 5 * n % 17 = 8) : n % 17 = 5 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

