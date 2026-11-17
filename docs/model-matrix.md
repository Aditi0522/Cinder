# Phase 2 Model Matrix

Candidate prover models for Cinder, with licenses, architectures, Lean/Mathlib versions, and prompting/decoding configuration.

_Compiled 2026-11-17 from the Hugging Face model cards, the Kimina blog post, and the Goedel and Pythagoras papers/cards. Fields marked **NOT STATED** were not found on the primary source and must be confirmed before they are treated as pinned. Fields marked **(secondary)** came from a source other than the official card. Revised the same day to add the Qwen3 size ladder, the Kimina variants and an expanded risk list (section 7)._

## 1. Summary

| # | Model | Role | Params | Base model | License | Lean version (per authors) |
|---|-------|------|--------|-----------|---------|----------------------------|
| 1a | `AI-MO/Kimina-Prover-Distill-8B` | Specialist | 8B | Qwen3-8B | Apache-2.0 (secondary) | Lean 4.15.0 / Mathlib v4.15 (blog + Kimina server default) |
| 1b | `AI-MO/Kimina-Prover-Distill-1.7B` | Small dev model | 1.7B | Qwen3-1.7B | Apache-2.0 (secondary) | Lean 4.15.0 / Mathlib v4.15 |
| 1c | `AI-MO/Kimina-Prover-RL-1.7B` | Optional: RL variant of 1b | 1.7B | Fine-tuned from Kimina-Prover-Distill-1.7B | Apache-2.0 (secondary) | Lean 4.15.0 / Mathlib v4.15 (assumed same as 1b; confirm) |
| 1d | `AI-MO/Kimina-Prover-Distill-0.6B` and `-RL-0.6B` | Optional: extends the size ladder | 0.6B | Qwen3-0.6B (assumed from naming; confirm) | **NOT STATED** | Presumably 4.15.0; confirm |
| 2 | `deepseek-ai/DeepSeek-Prover-V2-7B` | Specialist | 7B | DeepSeek-Prover-V1.5-Base | DeepSeek License Agreement v1.0 (use-based restrictions) | Lean 4.9.0 (V1.5 environment) |
| 3 | `Pythagoras-LM/Pythagoras-Prover-4B` | Specialist | 4B | Qwen3-4B-Base (LoRA SFT, then RL) | Apache-2.0 | Lean 4.9.0-rc1 |
| 4 | `Qwen/Qwen3-4B` | General baseline | 4.0B | Qwen3-4B-Base | Apache-2.0 | None (not Lean-specific) |
| 4a | `Qwen/Qwen3-1.7B` | General baseline (about 1B slot) | 1.7B | Qwen3-1.7B-Base | Apache-2.0 (Qwen3 family; confirm on card) | None (not Lean-specific) |
| 4b | `Qwen/Qwen3-8B` | General baseline (about 8B slot) | 8B | Qwen3-8B-Base | Apache-2.0 (Qwen3 family; confirm on card) | None (not Lean-specific) |
| 4c | A Gemma model (optional, size to be chosen) | General baseline from a different family | **NOT STATED** | **NOT STATED** | Gemma terms, not Apache-2.0 (confirm before use) | None (not Lean-specific) |
| 5 | `Goedel-LM/Goedel-Prover-V2-8B` | Optional specialist | 8B | Qwen3-8B | Apache-2.0 | Lean 4.9.0 (follows DeepSeek-Prover-V1.5) |

### Lean environments to prepare

| Environment | Lean | Models |
|-------------|------|--------|
| A | 4.9.0 (4.9.0-rc1 for Pythagoras's own evals) + matching Mathlib | DeepSeek-Prover-V2-7B, Goedel-Prover-V2-8B, Pythagoras-Prover-4B |
| B | 4.15.0 + Mathlib v4.15 | Kimina-Prover-Distill-8B / 1.7B (and the RL-1.7B and 0.6B variants if used) |
| General baselines | Run under the same environment as the specialist of the same size it is compared against, or under both | Qwen3-1.7B / 4B / 8B, Gemma (if added) |

**Open decision, settle before the miniF2F loader:** either maintain two environments with two statement variants (A and B above), or pick one Lean version for all models and accept the cost to the specialists trained on the other. Record the choice and the owner in the decision log.

Caveat: Lean 4.9 and 4.15 Mathlib differ (for example the `∑ i in s` vs `∑ i ∈ s` notation, and renamed lemmas). The pinned miniF2F statements have to compile in each environment. Expect to need either two statement variants or a single Lean version for all models, with the cost to specialists that were trained on the other version. Decide this before the loader work.

## 2. Architecture and training details

| Model | Architecture | Context | Training notes |
|-------|--------------|---------|----------------|
| Kimina-Prover-Distill-8B / 1.7B | Qwen3 dense decoder | 32K listed (mirror site) | Distilled from Kimina-Prover-72B (RL on Qwen2.5-72B). The 72B family also does error-fixing and TTRL search, which the distilled variants do not advertise. |
| DeepSeek-Prover-V2-7B | Llama-architecture decoder, BF16 | 32K (extended from V1.5) | Cold start from DeepSeek-V3 subgoal decomposition, then RL with binary correct/incorrect reward. Trained to emit a proof plan then Lean code. |
| Pythagoras-Prover-4B | Qwen3 dense decoder, BF16 | 8K training context, evaluated with a 30K token generation limit | LoRA SFT with difficulty curriculum, RL with Lean-compile reward, then continued SFT on the ALF corpus. No self-correction or test-time RL. |
| Qwen3-4B | Qwen3 dense decoder | 32K native | General model with thinking and non-thinking modes. Not trained as a Lean prover. |
| Goedel-Prover-V2-8B | Qwen3 dense decoder, BF16 | 32K standard, 40K in self-correction mode | Scaffolded data synthesis, expert iteration and RL, verifier-guided self-correction, model averaging. |
| Qwen3-1.7B / Qwen3-8B | Qwen3 dense decoder | 32K native | Same family and modes as Qwen3-4B. Not trained as Lean provers. |
| Kimina-Prover-RL-1.7B / Distill-0.6B / RL-0.6B | Qwen3 dense decoder | 40,960 listed for RL-1.7B (mirror site); others not checked | RL variants are fine-tuned from the matching Distill model. 0.6B details not verified. |

Kimina naming: the current distilled releases are 0.6B, 1.7B and 8B (Hugging Face collection `AI-MO/kimina-prover`). The phase plan's "Kimina-Prover distilled 7B" does not match a current release and should be changed to 8B (and 1.7B for the small slot).

## 3. Prompting configuration

All three of DeepSeek-Prover-V2, Goedel-V2 and Pythagoras use the same chat prompt (user turn only, no system prompt shown on the cards):

````
Complete the following Lean 4 code:

```lean4
{formal_statement}```

Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.
````

Formal statement header used on all three cards:

```lean4
import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem ... := by
  sorry
```

Note `maxHeartbeats 0` removes the elaboration timeout. Cinder's verifier should decide whether to keep that header or enforce its own limit, and record the choice, because it changes what counts as a pass.

**Kimina (secondary, reconstructed from a community Space that wraps the 8B model; confirm against the official card):**

- System: `You are an expert in mathematics and Lean 4.`
- User: `Think about and solve the following problem step by step in Lean 4.` / `# Problem: Provide a formal proof for the following statement.` / `# Formal statement:` followed by the statement in a `lean4` fenced block.
- The Space's default Lean header was not retrieved in full, so the exact header is **NOT CONFIRMED**.

**Qwen3-4B:** no official Lean prompt. Use the same prompt as the specialists above for a like-for-like comparison, and record that choice. Record also whether the checkpoint is base or instruct and whether thinking is enabled.

## 4. Decoding configuration

| Model | Settings found | Source |
|-------|----------------|--------|
| Kimina-Prover-Distill-8B | temperature 0.6, top_p 0.95, max tokens 2500 default in the Space (the Space's UI range is 150 to 4096, which is likely too short for real runs) | secondary, Space code |
| Kimina-Prover-Distill-1.7B | **NOT STATED** | none found |
| DeepSeek-Prover-V2-7B | Quick-start uses `max_new_tokens=8192`, `torch.manual_seed(30)`, BF16. Temperature and top_p **NOT STATED** on the card. | model card |
| Pythagoras-Prover-4B | Quick-start uses `max_new_tokens=8192`, BF16. Benchmarks used a 30,000 token generation limit with a verbatim-statement pass criterion. Temperature and top_p **NOT STATED** on the card. | model card |
| Qwen3-4B | Thinking mode: temperature 0.6, top_p 0.95, top_k 20, min_p 0. Non-thinking: temperature 0.7, top_p 0.8, top_k 20, min_p 0. Do not use greedy decoding (repetition and degradation). | Qwen3 model card |
| Goedel-Prover-V2-8B | Quick-start uses `max_new_tokens=32768` (standard mode); self-correction mode does 2 revision rounds, 40K total tokens. Temperature and top_p **NOT STATED** on the card. | model card |

Action for the generation script: for every model whose temperature and top_p are not stated, read the authors' repo scripts (Goedel: `scripts/pipeline.sh`; Pythagoras: GitHub repo; DeepSeek: V2 GitHub) or the `generation_config.json` shipped with the weights, then record the value we actually used in the generation metadata.

## 5. Published miniF2F-test results (for orientation only)

| Model | Pass@32 | Notes |
|-------|---------|-------|
| Kimina-Prover-Distill-1.7B | 72.95% (card) / 73.4% (blog) | The two sources disagree slightly |
| Kimina-Prover-RL-1.7B | 76.63% (mirror site, secondary) | RL on top of Distill-1.7B, reported as +3.68 points |
| Kimina-Prover-Distill-8B | 77.86% (card) / 78.3% (blog) | Same |
| DeepSeek-Prover-V2-7B | 75.6% | Kimina blog and Pythagoras table agree |
| Pythagoras-Prover-4B | 86.07% | Lean 4.9.0-rc1, 30K tokens. Authors' own evaluation. |
| Goedel-Prover-V2-8B | 83.0% (Goedel card) / 84.6% (Pythagoras table) | Different protocols |
| Qwen3-4B | no published Lean figure found | |

These numbers come from each team's own protocol (Lean version, token limit, header, pass criterion) and are not comparable with each other. Our phase 3 results must come from a single Cinder protocol.

## 6. Licensing and fit for weight-space modification research

Our use: load the weights, generate proofs, and later modify the weights (targeted edits, fine-tuning) to study failure patterns. This is not legal advice.

| Model | Verdict | Notes |
|-------|---------|-------|
| Qwen3-1.7B / 4B / 8B | OK | Apache-2.0 (checked on the 4B card; 1.7B and 8B assumed to match, confirm) permits use, modification and redistribution with license and notice retained. |
| Pythagoras-Prover-4B | OK | Apache-2.0 per card. |
| Goedel-Prover-V2-8B | OK | Apache-2.0 per card. Inherits Qwen3's Apache-2.0 terms. |
| Kimina-Prover-Distill-8B / 1.7B | OK, with a check | Apache-2.0 per third-party mirrors. Confirm the license field on the official Hugging Face card before we share anything. The 72B model is built on Qwen2.5-72B and is not in scope here. |
| DeepSeek-Prover-V2-7B | OK for research, read the terms | Governed by the DeepSeek License Agreement v1.0 (a source-available license, not Apache or MIT). It lists finetuning, running, training and evaluating the model as permitted uses. It also imposes use-based restrictions (Attachment A) that must be passed on to anyone we redistribute the model or derivatives to, and it covers derivatives, defined to include modified weights. I could read the summary but not the full text of Attachment A, so read it before publishing any modified DeepSeek weights. Releasing only sparse delta files (the Phase 5 plan) may still count as a derivative under the license's wording ("modifications to the Model, works based on the Model"), so treat deltas like full weights until the full text is read. |

Practical consequences:

- Keeping modified weights private or internal, and publishing only results, is the low-risk path for all five.
- If we release edited checkpoints, the Apache models need license and notice files carried over. The DeepSeek derivative must carry the use-based restrictions.
- Generated proofs: DeepSeek's license says DeepSeek claims no rights in output, but we are accountable for it. The others are Apache-2.0 and do not restrict output.
- If a Gemma model is added, it falls under Google's Gemma terms rather than Apache-2.0. Read them before including it, and before releasing any edit of it.

## 7. Risks for the benchmark

- **Contamination.** All of these models were trained or RL-tuned with miniF2F-adjacent data in mind, and Pythagoras and Goedel used synthetic data derived from public problem sets. A high miniF2F score may partly reflect memorisation. The miniF2F audit and any held-out problems should account for this.
- **Statement fidelity.** Pythagoras reports a "verbatim-statement" pass criterion. Cinder's verifier should also check that the proof is for the exact pinned statement, and that no `sorry`, `axiom`, or altered theorem is accepted.
- **8B models fit only across both GPUs.** T4 and P100 GPUs have no BF16 support and 16 GB of memory, so an 8B model (about 16 GB of weights in 16-bit) needs fp16 with tensor parallelism across the two T4s, or quantisation. Phase 5 also needs an in-memory edit copy plus forward passes, so limit editing targets to 4B or smaller. Use the 8B models for the survey and as references. Check the accelerator Kaggle actually gives you at run time.
- **Untested software stack.** Not yet confirmed: that vLLM runs well on T4s (Turing, fp16 only), and that these BF16-trained models stay numerically stable in fp16. Test both in the Kaggle generation script task, with the 1.7B and 4B models for the first end-to-end test, before committing to the survey grid.
- **Goedel reproduction cost.** The Phase 2 check that our Goedel-Prover-V2-8B pass@32 lands within about 10 points of its published figure is expensive on Kaggle with long outputs (the card uses up to 32K new tokens). Measure tokens per second on the first model, extrapolate, and if it does not fit, use fewer samples, a problem subset, or the smaller models for the harness check. Note the published figures differ by protocol (83.0% on the Goedel card, 84.6% in the Pythagoras table), so the tolerance has to account for that.
- **Survey grid gaps.** The phase plan wants general models at about 1B, 4B and 8B. This matrix now lists Qwen3-1.7B, 4B and 8B, and an optional Gemma, but the Gemma size and checkpoint are not chosen. Kimina's 0.6B and RL variants extend the size ladder if budget allows.
- **Lean environments.** See the open decision in section 1: two Lake projects and statement variants, or one Lean version for all.

## 8. Sources

- DeepSeek-Prover-V2-7B model card: https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-7B
- Goedel-Prover-V2-8B model card: https://huggingface.co/Goedel-LM/Goedel-Prover-V2-8B
- Pythagoras-Prover-4B model card: https://huggingface.co/Pythagoras-LM/Pythagoras-Prover-4B
- Kimina-Prover blog: https://huggingface.co/blog/project-numina/kimina-prover
- Kimina Prover collection: https://huggingface.co/collections/AI-MO/kimina-prover
- Kimina-Prover-Distill-8B (mirror listing): https://featherless.ai/models/AI-MO/Kimina-Prover-Distill-8B
- Kimina Lean server (Lean 4.15.0 default): https://github.com/Sequential-Intelligence-Lab/kimina-lean-server
- Community Space with Kimina-8B prompt and sampling: https://huggingface.co/spaces/Tonic/Math
- Qwen3-4B model card: https://huggingface.co/Qwen/Qwen3-4B
- DeepSeek License Agreement v1.0 (summary): https://scancode-licensedb.aboutcode.org/deepseek-la-1.0.html
