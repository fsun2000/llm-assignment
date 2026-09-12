# RouteLab: An LLM Experimentation Lab

## Target audience

This self-study assignment is for Python learners who can read and write small scripts and who have made, or are ready to make, their first LLM API call. Modules 1–4 are Beginner level. Modules 5–8 are Intermediate extensions of the same project.

Estimated time: 6–10 hours. Use one codebase and one dataset throughout.

## The learning loop

Your goal is not merely to obtain the highest score. Your goal is to practice a repeatable engineering loop:

```text
build → evaluate → analyze → improve → evaluate again
```

By the end, you should be able to:

1. build a simple LLM text classifier;
2. evaluate predictions against labeled data;
3. inspect errors and label confusions;
4. state a testable improvement hypothesis;
5. change one part of the system at a time; and
6. decide from measurements whether the change helped.

## Prerequisites

- Python 3.10 or newer
- Basic Python: functions, lists/dictionaries, files, and command-line scripts
- Access to an Azure OpenAI resource with a deployed text-generation model
- An Azure OpenAI API key (the beginner path in this lab)
- Familiarity with JSON is helpful

No model training, fine-tuning, agents, orchestration framework, database, or production deployment is required.

## Scenario and dataset

You are routing incoming requests for **CloudDesk**, a fictional SaaS product. Given one support message, your program must return exactly one routing label.

The synthetic dataset uses eight labels. Several are deliberately easy to confuse.

| Label | Route here when… | Do not confuse with… |
| --- | --- | --- |
| `account_access` | the user cannot sign in, reset a password, or complete authentication | a product function failing after sign-in (`technical_bug`) |
| `cancel_subscription` | the user wants to end a paid subscription or prevent renewal | changing tier or billing cycle (`plan_change`) |
| `duplicate_charge` | the same purchase appears to have been charged more than once | asking where an already-promised refund is (`refund_status`) |
| `refund_status` | the user asks about the progress, timing, or absence of a refund | requesting cancellation without an existing refund (`cancel_subscription`) |
| `plan_change` | the user wants to upgrade, downgrade, or change billing cycle/seats | ending the subscription (`cancel_subscription`) |
| `invoice_request` | the user needs an invoice, receipt, tax detail, or billing document | disputing a charge (`duplicate_charge`) |
| `technical_bug` | an existing product capability is broken or behaves incorrectly | requesting a capability that does not exist (`feature_request`) |
| `feature_request` | the user proposes or asks for a new product capability | reporting that an existing capability is broken (`technical_bug`) |

Files:

- `data/train.jsonl`: 64 labeled examples. Use for understanding labels and selecting demonstrations.
- `data/dev.jsonl`: 32 labeled examples. Reuse for Modules 1–7 so comparisons are fair.
- `data/final.jsonl`: 32 labeled examples. Do not inspect or evaluate this split until Module 8.
- `data/labels.json`: machine-readable label definitions.

Every JSONL row has this shape:

```json
{"id":"dev-001","input":"I was billed twice for one renewal.","label":"duplicate_charge"}
```

The data is synthetic, balanced by label within each split, and safe to redistribute. Because this is a self-study lab, the final labels are present locally; honor the holdout rule rather than tuning against them.

## Setup

1. Create and activate a virtual environment.
2. Install the supplied dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in your Azure resource endpoint, API key, and **model deployment name**. Never commit `.env`.
4. Use the OpenAI Python SDK's **Responses API** through Azure OpenAI. In requests, `model` must be your Azure deployment name, not an assumed public model ID.
5. Read JSONL one line at a time with Python's `json` module.
6. Implement your work under `src/` or use another simple structure.

The starter files contain interfaces and TODOs, not a solution. Your central interface should remain simple:

```python
def predict(text: str) -> str:
    """Return one valid routing label."""
```

Use `src/azure_client.py` for the small amount of connection setup supplied with the assignment. Your prediction code should make independent calls through:

```python
response = client.responses.create(
    model=deployment_name,
    input=your_prompt,
)
```

Read plain-text output from `response.output_text`. In Module 6, use `client.responses.parse(..., text_format=YourPydanticModel)` and read `response.output_parsed`, if the deployed Azure model supports structured outputs. The assignment deliberately leaves the prompt, schema, parsing policy, and evaluation implementation to you.

The Azure endpoint value should look like `https://YOUR-RESOURCE-NAME.openai.azure.com`; the supplied helper appends `/openai/v1/`. If your organization requires Microsoft Entra ID instead of an API key, ask your instructor to adapt only the authentication helper—the experiments do not otherwise change.

For reproducible comparisons, keep the evaluation rows and model settings fixed unless the experiment explicitly changes them. Use low or zero sampling temperature if your API supports it. Save raw outputs as well as parsed labels when practical.

## Ground rules for experiments

- Change one main variable per experiment.
- Evaluate on the same development examples in Modules 1–7.
- Record every result, including negative results.
- Do not silently convert an invalid response into a correct label.
- Do not use `final.jsonl` for prompt writing, example selection, or debugging.
- Cap your run before calling the API. A 32-row development pass means 32 model calls for a single-call classifier.
- Cache predictions so rerunning metric code does not spend more money.

---

## Module 1 — Build a baseline

**Difficulty:** Beginner

### Objective

Create the smallest working, single-call LLM classifier.

### Task

Load `data/dev.jsonl`. For each message, call an LLM and ask it to choose one of the eight valid labels. Return only a label, validate it, and save one prediction per row. Calculate accuracy. Start with no demonstrations and no label definitions beyond the label names.

### Required measurements

- Azure deployment name, underlying model/version if known, and relevant generation settings
- exact prompt text
- number of evaluated examples
- correct predictions and accuracy
- invalid-output count and rate
- number of API calls

### Deliverables

- a working `predict(text)` path
- saved baseline predictions including `id`, `predicted_label`, and optionally `raw_output`
- experiment-log row `exp_01_baseline`

### Progressive hints

1. Clearly list every allowed label in the prompt.
2. Ask for only the predicted label, with no explanation.
3. Strip surrounding whitespace, then test membership in the allowed-label set. Treat anything else as invalid.

### Reflection

- Which parts were harder: calling the API, parsing output, or evaluation?
- What does an invalid output reveal about the interface between your code and the model?

---

## Module 2 — Analyze errors

**Difficulty:** Beginner

### Objective

Turn baseline failures into testable ideas.

### Task

Join baseline predictions to their ground-truth rows by `id`. Inspect every error. Summarize common actual→predicted label pairs and select at least five representative mistakes. Assign each selected error a short reason such as ambiguous wording, unclear label boundary, or output-format failure. State at least two hypotheses that could improve the system.

### Required measurements

- total classification errors
- invalid outputs, reported separately
- accuracy by true label
- three most common confusion pairs, or all tied pairs if counts are small

### Deliverables

- a compact error table with `id`, shortened input, true label, prediction, and suspected reason
- two specific, testable hypotheses

### Progressive hints

1. Group mistakes by `(true_label, predicted_label)` before reading them one by one.
2. Compare the wording of labels the model frequently swaps.
3. Turn an observation into a prediction: “If I add X, performance on Y should improve because Z.”

### Reflection

- Is the largest error category caused by the model, the prompt, parsing, or label ambiguity?
- Which hypothesis is cheapest and clearest to test first?

---

## Module 3 — Improve the prompt

**Difficulty:** Beginner

### Objective

Test one prompt-level hypothesis against the baseline.

### Task

Choose one Module 2 hypothesis. Modify only the prompt—for example, add concise label definitions or a decision rule for a confusing pair. Run the same model on the same 32 development examples. Do not add labeled demonstrations yet.

### Required measurements

- baseline and new accuracy
- percentage-point difference
- invalid-output counts for both runs
- errors fixed, errors introduced, and net errors changed

### Deliverables

Record:

```text
Baseline accuracy:
New accuracy:
Difference in percentage points:
Hypothesis:
Result:
Conclusion:
```

Add `exp_02_prompt_change` to the experiment log. A negative result is valid if measured and explained.

### Progressive hints

1. Use Module 2 evidence to choose what information the prompt lacks.
2. Definitions are more useful when they describe boundaries, not just synonyms.
3. Compare row IDs to see which old errors disappeared and which new errors appeared.

### Reflection

- Did the evidence support your hypothesis?
- Did the change help the intended labels, or improve for an unrelated reason?

---

## Module 4 — Experiment with demonstrations

**Difficulty:** Beginner → Intermediate

### Objective

Learn when labeled examples help enough to justify a larger prompt.

### Task

Compare zero-shot, one-shot, and few-shot prompts using examples selected only from `train.jsonl`. Keep the development rows, model, label definitions, and generation settings fixed. Document how you selected examples. Never use a development row as a demonstration.

Intermediate extension: compare two few-shot selection policies, such as random vs. label-balanced, or label-balanced vs. manually chosen boundary cases. Fix and record a random seed when sampling.

### Required measurements

- accuracy and invalid-output rate per strategy
- number of demonstrations
- approximate input tokens per evaluated message, using one stated counting method
- errors fixed and introduced relative to zero-shot

### Deliverables

- at least three experiment-log rows: 0, 1, and 3+ demonstrations
- the demonstration IDs and selection rule for every run
- a short recommendation with evidence

### Progressive hints

1. A single example teaches one label well but may bias predictions toward it.
2. Label-balanced examples expose the output space evenly.
3. Boundary examples can show the distinction between “broken existing feature” and “desired new feature.”

### Reflection

- Which demonstrations helped, and which examples became worse?
- Was the accuracy change worth the extra context?

---

## Module 5 — Improve evaluation

**Difficulty:** Intermediate

### Objective

See patterns that overall accuracy can hide.

### Task

Build a reusable evaluation function. Compare your baseline and best current system with per-label precision, recall, and F1, plus a confusion table or matrix. You may implement the calculations or use a lightweight library. Decide and document how invalid outputs enter the metrics; they must count as incorrect.

### Required measurements

- overall accuracy
- per-label precision, recall, F1, and support
- macro-F1
- confusion counts

### Deliverables

- reusable evaluation code
- a readable metric table for two systems
- strongest label, weakest label, and one systematic failure pattern

### Progressive hints

1. Overall accuracy gives each row equal weight; macro-F1 gives each label equal weight.
2. Use a fixed label order so matrices are comparable.
3. Low recall means true cases are being missed; low precision means other cases are being routed into the label.

### Reflection

- Why might two systems with the same accuracy be meaningfully different?
- What would you change if the weakest label were operationally expensive?

---

## Module 6 — Make outputs reliable

**Difficulty:** Intermediate

### Objective

Make the model–code boundary dependable.

### Task

Replace or strengthen free-text parsing using one supported mechanism: Azure OpenAI structured output through `responses.parse`, JSON output plus validation, or strict validation with one bounded retry. Preserve the classifier's semantic prompt as much as possible so this experiment primarily tests output reliability. Log retry attempts; never retry indefinitely.

### Required measurements

- invalid-output count and rate before and after
- accuracy before and after
- retry count and additional calls
- a small sample of raw malformed outputs, if any

### Deliverables

- validated prediction records
- experiment-log row describing the reliability method
- brief failure policy: what the program stores when all attempts are invalid

### Progressive hints

1. Separate the raw response from the parsed prediction.
2. A JSON response is not trustworthy until your code parses and validates it.
3. With OpenAI Python 2.x, a Pydantic model passed as `text_format` to `responses.parse` can express the valid-label set as an enum or `Literal` type. Confirm that your Azure deployment supports structured outputs.

### Reflection

- Did the reliability mechanism change only formatting, or also classification accuracy?
- Is a retry worth the extra latency and cost in this small system?

---

## Module 7 — Balance context and cost

**Difficulty:** Intermediate

### Objective

Find where additional context stops earning its cost.

### Task

Evaluate at least three configurations, such as 0, 3, and 8 demonstrations. Keep everything else fixed. Estimate tokens using an SDK tokenizer, API usage metadata, or a clearly stated characters-to-tokens approximation. If your provider publishes prices, calculate estimated cost; otherwise report tokens and calls without inventing a price.

Optional extension: choose demonstrations dynamically for each input using semantic similarity. An embeddings API is allowed but not required. Retrieve only from `train.jsonl`, exclude exact duplicates, and include embedding calls in cost and latency accounting.

### Required measurements

- accuracy and macro-F1
- invalid-output rate
- average input and output tokens per example
- total LLM calls and any embedding calls
- estimated cost when authoritative pricing is available
- latency, optional but recommended

### Deliverables

- a comparison table for at least three prompt sizes
- your preferred quality–cost tradeoff and the rule used to choose it
- experiment-log rows with token and call counts

### Progressive hints

1. Measure prompt size instead of assuming “few-shot” is cheap.
2. Calculate marginal gain: added quality divided by added tokens or cost.
3. For dynamic selection, represent each training input and query in the same embedding space, then retrieve nearest examples.

### Reflection

- At what point did more context stop helping enough?
- Would your choice change if traffic increased by 1,000×?

---

## Module 8 — Final held-out experiment

**Difficulty:** Intermediate

### Objective

Choose a final system from evidence and test whether the improvement generalizes.

### Task

Freeze your baseline and final configurations before opening `data/final.jsonl`. Write down the expected outcome. Then run each configuration exactly once on all 32 final rows. Do not modify the system after seeing final labels. Save final-system predictions in the required submission format.

### Required measurements

- baseline vs. final accuracy and macro-F1
- per-label results for the final system
- invalid-output count and rate
- approximate tokens, calls, and cost if available
- change from development to final performance

### Deliverables

- final predictions, one JSON object per line:

```json
{"id":"final-001","predicted_label":"duplicate_charge"}
```

- a baseline-vs-final comparison
- the final report described below

### Progressive hints

1. “Final” means chosen before you see holdout outcomes.
2. Reuse the exact code path that produced your recorded development result.
3. A smaller final gain does not invalidate the work; discuss sampling variation and possible overfitting to development errors.

### Reflection

- Did the improvement generalize to unseen examples?
- What is the most important remaining weakness, and what experiment would you run next?

## Experiment log

Use `experiments/results.csv`, JSON, or Markdown. Keep one row per evaluated configuration. The supplied CSV header is:

| Field | Meaning |
| --- | --- |
| `experiment_id` | stable name such as `exp_01_baseline` |
| `timestamp_utc` | when the run occurred |
| `split` | normally `dev`, then `final` in Module 8 |
| `model` | exact Azure deployment name; note underlying model/version separately if known |
| `change` | the one main change |
| `examples` | demonstration count |
| `accuracy` / `macro_f1` | values from 0 to 1 |
| `invalid_outputs` | count, not rate |
| `input_tokens` / `output_tokens` | totals or blank if unavailable |
| `api_calls` | generation calls plus clearly separated embedding calls in notes |
| `estimated_cost` | amount and currency, or blank |
| `observation` | short evidence-based interpretation |

Preserve prompts in code or separate text files and give them version names so a result can be reproduced.

## Final report

Aim for 600–1,000 words and use these sections:

1. **Baseline:** model, prompt strategy, development performance, and initial failure pattern.
2. **Experiments:** important hypotheses, controlled changes, measurements, and negative results.
3. **Final system:** the chosen configuration and why the evidence favored it.
4. **Final results:** baseline vs. final accuracy, macro-F1, invalid rate, and token/cost tradeoff.
5. **Reflection:** what helped, what did not, one limitation, and the next experiment.

## Required deliverables

1. Python code for a working LLM classifier and evaluation pipeline.
2. `predictions/final_predictions.jsonl` containing exactly one `id` and valid `predicted_label` per final row.
3. The completed experiment log.
4. The short final report.
5. A prompt record sufficient to reproduce the baseline and final configurations.

Do not submit API keys, virtual environments, or cached provider credentials.

## Grading rubric

| Category | Weight | What earns credit |
| --- | ---: | --- |
| Working Python + LLM pipeline | 20% | Loads data, calls an LLM, validates labels, and saves predictions |
| Evaluation implementation | 20% | Correct, reusable overall and per-label metrics; invalids handled transparently |
| Experimental process | 20% | Controlled comparisons, reproducible settings, and a complete log |
| Error analysis | 15% | Specific confusion evidence and plausible failure explanations |
| Improvements based on evidence | 15% | Changes follow hypotheses and are judged by measurements |
| Final conclusions | 10% | Clear tradeoff, limitation, and next experiment |

Final accuracy alone does not determine the grade. A well-designed negative experiment earns full experimental credit when it is measured and interpreted honestly.

## Brief instructor notes

- The dataset is intentionally balanced, so accuracy is readable; macro-F1 still reveals uneven label behavior.
- The central boundaries are cancellation vs. plan change, duplicate charge vs. refund status, and technical bug vs. feature request.
- Encourage a fixed API budget before students start. Development runs are 32 calls each for a single-call pipeline.
- The required API path is Azure OpenAI Responses through the OpenAI Python SDK. Model deployments and structured-output support vary by Azure resource, so Module 6 intentionally includes fallback approaches.
- Do not reveal a preferred prompt. Ask learners to justify selection with logged evidence.
- Audit that final predictions cover every final ID exactly once and contain only valid labels.
- If API access is unavailable, an instructor may provide cached raw model responses; the learner should still implement parsing, evaluation, analysis, and comparison.

## API references

- [Azure OpenAI Responses API (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?pivots=programming-language-python)
- [Azure OpenAI structured outputs (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
- [Responses create method (official OpenAI API reference)](https://developers.openai.com/api/reference/python/resources/responses/methods/create)
