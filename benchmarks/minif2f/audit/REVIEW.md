# Manual review queue

Both reviewers judge each statement against the informal problem, independently. Set `decision` in `exclusions.jsonl` to `exclude` or `keep` and fill `reviewers`.

## amc12_2001_p5 (test) — findings

```lean
theorem amc12_2001_p5 :
  Finset.prod (Finset.filter (λ x => ¬ Even x) (Finset.range 10000)) (id : ℕ → ℕ) = (10000!) / ((2^5000) * (5000!))
```

- [maybe/None] Integer Division Truncation: 10000! / 2 ^ 5000 * 5000! may truncate (truncates toward zero)
- [maybe/None] 0-Indexed Range: Finset.range 10000 is 0-indexed: [0, 1, ..., 10000-1]

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## amc12a_2020_p13 (valid) — findings

```lean
theorem amc12a_2020_p13 (a b c : ℕ) (n : NNReal) (h₀ : n ≠ 1) (h₁ : 1 < a ∧ 1 < b ∧ 1 < c)
  (h₂ : (n * (n * n ^ (1 / c)) ^ (1 / b)) ^ (1 / a) = (n ^ 25) ^ (1 / 36)) : b = 3
```

- [maybe/None] Integer Division Truncation: 1 / c may truncate (truncates toward zero)
- [maybe/None] Integer Division Truncation: 1 / b may truncate (truncates toward zero)
- [maybe/None] Integer Division Truncation: 1 / a may truncate (truncates toward zero)
- [proven/definitional] Integer Division Truncation: 1 / 36 definitely truncates to wrong value (1 / 36 = 0 in integer division, but 0.027778 mathematically)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## amc12a_2021_p3 (test) — findings

```lean
theorem amc12a_2021_p3
  (x y : ℕ)
  (h₀ : x + y = 17402)
  (h₁ : 10∣x)
  (h₂ : x / 10 = y) :
  ↑x - ↑y = (14238:ℤ)
```

- [maybe/None] Integer Division Truncation: x / 10 may truncate (truncates toward zero)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_170 (test) — findings

```lean
theorem mathd_algebra_170
  (S : Finset ℤ)
  (h₀ : ∀ (n : ℤ), n ∈ S ↔ abs (n - 2) ≤ 5 + 6 / 10) :
  S.card = 11
```

- [proven/definitional] Integer Division Truncation: 6 / 10 definitely truncates to wrong value (6 / 10 = 0 in integer division, but 0.600000 mathematically)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_208 (test) — findings

```lean
theorem mathd_algebra_208 :
  Real.sqrt 1000000 - 1000000^(1/3) = 900
```

- [proven/definitional] Integer Division Truncation: 1 / 3 definitely truncates to wrong value (1 / 3 = 0 in integer division, but 0.333333 mathematically)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_275 (test) — findings

```lean
theorem mathd_algebra_275
  (x : ℝ)
  (h : ((11:ℝ)^(1 / 4))^(3 * x - 3) = 1 / 5) :
  ((11:ℝ)^(1 / 4))^(6 * x + 2) = 121 / 25
```

- [proven/definitional] Integer Division Truncation: 1 / 4 definitely truncates to wrong value (1 / 4 = 0 in integer division, but 0.250000 mathematically)
- **Tier 1 candidate**

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_282 (valid) — findings

```lean
theorem mathd_algebra_282 (f : ℝ → ℝ) (h₀ : ∀ x : ℝ, ¬ (Irrational x) → f x = abs (Int.floor x))
  (h₁ : ∀ x, Irrational x → f x = (Int.ceil x) ^ 2) :
  f (8 ^ (1 / 3)) + f (-Real.pi) + f (Real.sqrt 50) + f (9 / 2) = 79
```

- [proven/definitional] Integer Division Truncation: 1 / 3 definitely truncates to wrong value (1 / 3 = 0 in integer division, but 0.333333 mathematically)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_314 (test) — findings

```lean
theorem mathd_algebra_314
  (n : ℕ)
  (h₀ : n = 11) :
  (1 / 4)^(n + 1) * 2^(2 * n) = 1 / 4
```

- [proven/definitional] Integer Division Truncation: 1 / 4 definitely truncates to wrong value (1 / 4 = 0 in integer division, but 0.250000 mathematically)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_algebra_392 (test) — findings

```lean
theorem mathd_algebra_392
  (n : ℕ)
  (h₀ : Even n)
  (h₁ : ((n:ℤ) - 2)^2 + (n:ℤ)^2 + ((n:ℤ) + 2)^2 = 12296) :
  ((n - 2) * n * (n + 2)) / 8 = 32736
```

- [maybe/None] Truncated Nat Subtraction: n - 2 has no guard ensuring 2 ≤ n
- [maybe/None] Integer Division Truncation: (n - 2) * n * (n + 2) / 8 may truncate (truncates toward zero)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_numbertheory_328 (test) — unaudited_linter_error

```lean
theorem mathd_numbertheory_328 :
  (5^999999) % 7 = 6
```


Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_numbertheory_530 (valid) — findings

```lean
theorem mathd_numbertheory_530 (n k : ℕ) (h₀ : 0 < n ∧ 0 < k) (h₀ : (n : ℝ) / k < 6)
  (h₁ : (5 : ℝ) < n / k) : 22 ≤ Nat.lcm n k / Nat.gcd n k
```

- [maybe/None] Integer Division Truncation: n.lcm k / n.gcd k may truncate (truncates toward zero)

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## mathd_numbertheory_543 (valid) — unaudited_timeout

```lean
theorem mathd_numbertheory_543 : (∑ k ∈ Nat.divisors (30 ^ 4), 1) - 2 = 123
```


Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## numbertheory_2pownm1prime_nprime (test) — unaudited_timeout

```lean
theorem numbertheory_2pownm1prime_nprime
  (n : ℕ)
  (h₀ : 0 < n)
  (h₁ : Nat.Prime (2^n - 1)) :
  Nat.Prime n
```


Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## numbertheory_3pow2pownm1mod2pownp3eq2pownp2 (test) — unaudited_linter_abort

```lean
theorem numbertheory_3pow2pownm1mod2pownp3eq2pownp2
  (n : ℕ)
  (h₀ : 0 < n) :
  (3^(2^n) - 1) % (2^(n + 3)) = 2^(n + 2)
```


Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____

## numbertheory_prmdvsneqnsqmodpeq0 (valid) — findings

```lean
theorem numbertheory_prmdvsneqnsqmodpeq0 (n : ℤ) (p : ℕ) (h₀ : Nat.Prime p) :
  ↑p ∣ n ↔ n ^ 2 % p = 0
```

- [maybe/None] Modulo Edge Case: n ^ 2 % ↑p has no guard ensuring ↑p ≠ 0

Decision: ____  Reviewer A: ____  Reviewer B: ____  Notes: ____
