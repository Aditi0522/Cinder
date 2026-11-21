import Mathlib
set_option maxHeartbeats 200000
open BigOperators Real Nat Topology Rat

theorem mathd_numbertheory_149 :
  (∑ k ∈ Finset.filter (fun x => x % 8 = 5 ∧ x % 6 = 3) (Finset.range 50), k) = 66 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_155 :
  Finset.card (Finset.filter (fun x => x % 19 = 7) (Finset.Icc 100 999)) = 48 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_156 (n : ℕ) (h₀ : 0 < n) : Nat.gcd (n + 7) (2 * n + 1) ≤ 13 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_169 : Nat.gcd 20! 200000 = 40000 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_188 : Nat.gcd 180 168 = 12 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_198 : 5 ^ 2005 % 100 = 25 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_200 : 139 % 11 = 7 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_202 : (19 ^ 19 + 99 ^ 99) % 10 = 8 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_211 :
  Finset.card (Finset.filter (fun n => 6 ∣ 4 * ↑n - (2 : ℤ)) (Finset.range 60)) = 20 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_22 (b : ℕ) (h₀ : b < 10)
  (h₁ : Nat.sqrt (10 * b + 6) * Nat.sqrt (10 * b + 6) = 10 * b + 6) : b = 3 ∨ b = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_221 (S : Finset ℕ)
  (h₀ : ∀ x : ℕ, x ∈ S ↔ 0 < x ∧ x < 1000 ∧ x.divisors.card = 3) : S.card = 11 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_232 (x y z : ZMod 31) (h₀ : x = 3⁻¹) (h₁ : y = 5⁻¹)
  (h₂ : z = (x + y)⁻¹) : z = 29 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_236 : 1999 ^ 2000 % 5 = 1 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_24 : (∑ k ∈ Finset.Icc 1 9, 11 ^ k) % 100 = 59 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_252 : 7! % 23 = 3 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_257 (x : ℕ) (h₀ : 1 ≤ x ∧ x ≤ 100)
    (h₁ : 77 ∣ (∑ k ∈ Finset.range 101, k) - x) : x = 45 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_269 : (2005 ^ 2 + 2005 ^ 0 + 2005 ^ 0 + 2005 ^ 5) % 100 = 52 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_284 (a b : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9)
  (h₁ : 10 * a + b = 2 * (a + b)) : 10 * a + b = 18 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_30 :
  (33818 ^ 2 + 33819 ^ 2 + 33820 ^ 2 + 33821 ^ 2 + 33822 ^ 2) % 17 = 0 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_301 (j : ℕ) (h₀ : 0 < j) : 3 * (7 * ↑j + 3) % 7 = 2 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_303 (S : Finset ℕ)
  (h₀ : ∀ n : ℕ, n ∈ S ↔ 2 ≤ n ∧ 171 ≡ 80 [MOD n] ∧ 468 ≡ 13 [MOD n]) : (∑ k ∈ S, k) = 111 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_32 (S : Finset ℕ) (h₀ : ∀ n : ℕ, n ∈ S ↔ n ∣ 36) : (∑ k ∈ S, k) = 91 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_326 (n : ℤ) (h₀ : (n - 1) * n * (n + 1) = 720 ) : n + 1 = 10 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_33 (n : ℕ) (h₀ : n < 398) (h₁ : n * 7 % 398 = 1) : n = 57 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

theorem mathd_numbertheory_335 (n : ℕ) (h₀ : n % 7 = 5) : 5 * n % 7 = 4 := by
  exfalso
  first | omega | linarith | nlinarith | (norm_num at *; done) | (simp_all <;> linarith)

