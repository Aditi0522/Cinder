# Phase 2 Model Matrix
Candidate models for Cinder, with licenses, architectures, Lean/Mathlib versions, and prompting/decoding configuration.
_Originally compiled 2026-11-17 from the Hugging Face model cards, the Kimina blog post, and the Pythagoras paper/card. Revised 2026-11-17 to the final four-model set: Qwen3-0.6B, Pythagoras-Prover-4B, Kimina-Prover-Preview-Distill-1.5B and Qwen3-4B-Thinking-2507. Fields marked **NOT STATED** were not found on a primary source and must be confirmed before they are treated as pinned. Fields marked **(secondary)** came from a source other than the official card. Fields marked **(confirm)** are from memory or assumed from the model family and have not been checked against the card in this revision._

## 1. Summary
| # | Model | Role | Params | Base model | License | Lean version (per authors) |
|---|-------|------|--------|-----------|---------|----------------------------|
| 1 | `AI-MO/Kimina-Prover-Preview-Distill-1.5B` | Small specialist | 1.5B | Qwen2.5-family 1.5B (confirm exact base on card) | Apache-2.0 (confirm on official card) | Lean 4.15.0 / Mathlib v4.15 (assumed from blog + Kimina server default; confirm) |
| 2 | `Pythagoras-LM/Pythagoras-Prover-4B` | Specialist | 4B | Qwen3-4B-Base (LoRA SFT, then RL) | Apache-2.0 | Lean 4.9.0-rc1 |
| 3 | `Qwen/Qwen3-0.6B` | General baseline (smallest slot) | 0.6B | Qwen3-0.6B-Base | Apache-2.0 (Qwen3 family; confirm on card) | None (not Lean-specific) |
| 4 | `Qwen/Qwen3-4B-Thinking-2507` | General baseline (4B slot) | 4.0B | Qwen3-4B lineage (2507 thinking-only update) | Apache-2.0 (Qwen3 family; confirm on card) | None (not Lean-specific) |

Size ladder: 0.6B (general), 1.5B (specialist), 4B (specialist), 4B (general). The only matched-size pair is Pythagoras-Prover-4B vs Qwen3-4B-Thinking-2507.

### Lean environments to prepare
| Environment | Lean | Models |
|-------------|------|--------|
| A | 4.9.0 (4.9.0-rc1 for Pythagoras's own evals) + matching Mathlib | Pythagoras-Prover-4B |
| B | 4.15.0 + Mathlib v4.15 (confirm for the Preview release) | Kimina-Prover-Preview-Distill-1.5B |
| General baselines | Run under the same environment as the specialist they are compared against, or under both | Qwen3-0.6B (compare against Kimina-1.5B, so B, or both), Qwen3-4B-Thinking-2507 (compare against Pythagoras-4B, so A, or both) |

**Open decision, settle before the miniF2F loader:** either maintain two environments with two statement variants (A and B above), or pick one Lean version for all models and accept the cost to the specialist trained on the other. Record the choice and the owner in the decision log.

Caveat: Lean 4.9 and 4.15 Mathlib differ (for example the `∑ i in s` vs `∑ i ∈ s` notation, and renamed lemmas). The pinned miniF2F statements have to compile in each environment. With only two specialists, the single-version option is cheaper than before, but it still penalises one of them.

## 2. Architecture and training details
| Model | Architecture | Context | Training notes |
|-------|--------------|---------|----------------|
| Kimina-Prover-Preview-Distill-1.5B | Qwen2.5-family dense decoder (confirm) | **NOT STATED** here; confirm on card | Distilled from the Kimina-Prover Preview 72B (RL on Qwen2.5-72B). The 72B also does error-fixing and TTRL search, which the distilled variants do not advertise. |
| Pythagoras-Prover-4B | Qwen3 dense decoder, BF16 | 8K training context, evaluated with a 30K token generation limit | LoRA SFT with difficulty curriculum, RL with Lean-compile reward, then continued SFT on the ALF corpus. No self-correction or test-time RL. |
| Qwen3-0.6B | Qwen3 dense decoder | 32K native (confirm) | General model with thinking and non-thinking modes. Not trained as a Lean prover. |
| Qwen3-4B-Thinking-2507 | Qwen3 dense decoder | 262,144 native (confirm) | Thinking-only variant of Qwen3-4B (no non-thinking mode, chat template inserts the think opening). Not trained as a Lean prover. |

Kimina naming: "Kimina-Prover-Preview-Distill" (1.5B and 7B) is the earlier, Qwen2.5-based release. It is a different release from the current "Kimina-Prover-Distill" series (0.6B, 1.7B, 8B, Qwen3-based) in the collection `AI-MO/kimina-prover`. Make sure the model ID in the generation script is the Preview one, and update any phase-plan text that says "Kimina-Prover distilled 7B" to the 1.5B Preview model.

## 3. Prompting configuration
**Pythagoras-Prover-4B** uses the chat prompt below (user turn only, no system prompt shown on the card):
````
Complete the following Lean 4 code:
```lean4
{formal_statement}```
Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.
````
Formal statement header used on the card:
```lean4
import Mathlib
import Aesop
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat
theorem ... := by
  sorry
```
Note `maxHeartbeats 0` removes the elaboration timeout. Cinder's verifier should decide whether to keep that header or enforce its own limit, and record the choice, because it changes what counts as a pass.

**Kimina-Prover-Preview-Distill-1.5B (secondary, reconstructed from the Kimina prompt format used by a community Space wrapping a Kimina model; confirm against the official card):**
- System: `You are an expert in mathematics and Lean 4.`
- User: `Think about and solve the following problem step by step in Lean 4.` / `# Problem: Provide a formal proof for the following statement.` / `# Formal statement:` followed by the statement in a `lean4` fenced block.
- The exact Lean header is **NOT CONFIRMED**.

**Qwen3-0.6B and Qwen3-4B-Thinking-2507:** no official Lean prompt. Use the same prompt as the specialist they are compared against (Pythagoras prompt for the 4B, Kimina prompt for the 0.6B, or run both prompts on both), and record the choice. Also record, per run:
- Qwen3-0.6B: base or instruct checkpoint, and whether thinking is enabled.
- Qwen3-4B-Thinking-2507: thinking is always on, so the output contains a reasoning block before the answer. The verifier must extract the final Lean block after the reasoning, and the token budget must cover both.

## 4. Decoding configuration
| Model | Settings found | Source |
|-------|----------------|--------|
| Kimina-Prover-Preview-Distill-1.5B | **NOT STATED** here. A community Space wrapping a Kimina model used temperature 0.6, top_p 0.95 (secondary; that was for a different Kimina checkpoint). | none found for this checkpoint |
| Pythagoras-Prover-4B | Quick-start uses `max_new_tokens=8192`, BF16. Benchmarks used a 30,000 token generation limit with a verbatim-statement pass criterion. Temperature and top_p **NOT STATED** on the card. | model card |
| Qwen3-0.6B | Thinking mode: temperature 0.6, top_p 0.95, top_k 20, min_p 0. Non-thinking: temperature 0.7, top_p 0.8, top_k 20, min_p 0. Do not use greedy decoding (repetition and degradation). | Qwen3 model card family (confirm on the 0.6B card) |
| Qwen3-4B-Thinking-2507 | Temperature 0.6, top_p 0.95, top_k 20, min_p 0. Card recommends 32,768 output tokens for most queries and up to 81,920 for very hard problems (confirm on card). | model card (confirm) |

Action for the generation script: for every model whose temperature and top_p are not stated, read the authors' repo scripts (Pythagoras: GitHub repo; Kimina: Kimina blog/repo) or the `generation_config.json` shipped with the weights, then record the value we actually used in the generation metadata.

## 5. Published miniF2F-test results (for orientation only)
| Model | Pass@32 | Notes |
|-------|---------|-------|
| Kimina-Prover-Preview-Distill-1.5B | **NOT VERIFIED** in this revision | Look up on the card or the Kimina blog before quoting any figure |
| Pythagoras-Prover-4B | 86.07% | Lean 4.9.0-rc1, 30K tokens. Authors' own evaluation. |
| Qwen3-0.6B | no published Lean figure found | |
| Qwen3-4B-Thinking-2507 | no published Lean figure found | |

These numbers come from each team's own protocol (Lean version, token limit, header, pass criterion) and are not comparable with each other. Our phase 3 results must come from a single Cinder protocol.

## 6. Licensing and fit for weight-space modification research
Our use: load the weights, generate proofs, and later modify the weights (targeted edits, fine-tuning) to study failure patterns. This is not legal advice.

| Model | Verdict | Notes |
|-------|---------|-------|
| Qwen3-0.6B | OK | Apache-2.0 (Qwen3 family; confirm on the 0.6B card) permits use, modification and redistribution with license and notice retained. |
| Qwen3-4B-Thinking-2507 | OK | Apache-2.0 (Qwen3 family; confirm on the card). Same terms as above. |
| Pythagoras-Prover-4B | OK | Apache-2.0 per card. |
| Kimina-Prover-Preview-Distill-1.5B | OK, with a check | Apache-2.0 expected; confirm the license field on the official Hugging Face card before we share anything. The 72B teacher is built on Qwen2.5-72B and is not in scope here. |

Practical consequences:
- Keeping modified weights private or internal, and publishing only results, is the low-risk path for all four.
- If we release edited checkpoints (including sparse delta files), carry over the license and notice files for each Apache-2.0 base.
- Generated proofs: all four are Apache-2.0 (pending the confirmations above), which does not restrict output.

## 7. Risks for the benchmark
- **Contamination.** Pythagoras used synthetic data derived from public problem sets, and Kimina was RL-tuned on competition-style data. A high miniF2F score may partly reflect memorisation. The miniF2F audit and any held-out problems should account for this.
- **Statement fidelity.** Pythagoras reports a "verbatim-statement" pass criterion. Cinder's verifier should also check that the proof is for the exact pinned statement, and that no `sorry`, `axiom`, or altered theorem is accepted.
- **Hardware fit.** All four models are 4B or smaller. In 16-bit, the 4B models need about 8 GB of weights, so each fits on a single 16 GB T4 or P100 with room for KV cache, and Phase 5 editing (an in-memory edit copy plus forward passes) is feasible at 4B. T4 and P100 have no BF16 support, so inference runs in fp16 or quantised. Check the accelerator Kaggle actually gives you at run time.
- **Untested software stack.** Not yet confirmed: that vLLM runs well on T4s (Turing, fp16 only), and that the BF16-trained models (Pythagoras and the Qwen3 models) stay numerically stable in fp16. Test both in the Kaggle generation script task, using Qwen3-0.6B and Kimina-1.5B for the first end-to-end test, before committing to the survey grid.
- **Thinking-model token cost.** Qwen3-4B-Thinking-2507 always emits a long reasoning block. Measure tokens per sample on a small pilot, set the token limit with that in mind (the card suggests 32K or more), and make sure truncated outputs are counted as failures and logged, not silently dropped.
- **Cross-family comparisons.** Kimina-1.5B is Qwen2.5-based, while Pythagoras and the general baselines are Qwen3-based. Qwen3-4B-Thinking-2507 is a later post-training update of the Qwen3-4B line, not the exact base Pythagoras started from, so the 4B comparison is close but not a clean base-vs-fine-tune pair. Note both caveats when interpreting results.
- **Survey grid gaps.** The phase plan wanted general models at about 1B, 4B and 8B. This matrix has general models at 0.6B and 4B only, with no 8B and no general model near 1.5B to pair with Kimina-1.5B. Decide whether that is acceptable or whether to add one (for example Qwen3-1.7B) later.
- **No reproduction target.** Goedel-Prover-V2-8B is no longer in the set, so the planned check that our Goedel pass@32 lands within about 10 points of its published figure needs a new target. Use Pythagoras-Prover-4B (86.07% published, 30K tokens) or Kimina-1.5B (once its published figure is looked up), and set the tolerance with the protocol differences in mind. Measure tokens per second on the first model and extrapolate cost before committing.
- **Lean environments.** See the open decision in section 1: two Lake projects and statement variants, or one Lean version for both specialists.

## 8. Sources
- Pythagoras-Prover-4B model card: https://huggingface.co/Pythagoras-LM/Pythagoras-Prover-4B
- Kimina-Prover blog: https://huggingface.co/blog/project-numina/kimina-prover
- Kimina Prover collection: https://huggingface.co/collections/AI-MO/kimina-prover
- Kimina Lean server (Lean 4.15.0 default): https://github.com/Sequential-Intelligence-Lab/kimina-lean-server
- Community Space with Kimina prompt and sampling: https://huggingface.co/spaces/Tonic/Math
- Qwen3 model cards (0.6B, 4B-Thinking-2507): https://huggingface.co/Qwen/Qwen3-0.6B and https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507
