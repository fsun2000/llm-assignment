# Challenge dataset

This is a second, independent RouteLab track. It keeps the same JSONL schema as the standard dataset but has 10 labels and deliberately less lexical separation.

| Split | Rows | Purpose |
| --- | ---: | --- |
| `train.jsonl` | 60 | Label study and demonstrations only |
| `dev.jsonl` | 30 | Reusable development evaluation |
| `final.jsonl` | 30 | Held-out evaluation; do not inspect before Module 8 |

## Why it is harder

- Messages frequently mention a second plausible support issue; route the issue the customer is asking to resolve now.
- Several boundaries depend on state and time: a duplicate must be *captured*, while a refund-status case must have an already promised refund.
- `account_access` is an authentication problem; `workspace_access` happens after successful sign-in and concerns membership or permissions.
- Subscription intent is separated by whether the customer is leaving altogether (`cancel_subscription`) or retaining service with different terms (`plan_change`).
- Product requests distinguish a documented feature that is malfunctioning (`technical_bug`) from functionality that is absent or insufficient (`feature_request`).

The label definitions in `labels.json` are the authoritative routing policy. For a multi-issue message, the requested next action and the explicit precedence rules in those definitions decide the label. The rows are synthetic, balanced (six train and three rows in each evaluation split per label), and safe to redistribute.

Use a separate experiment log for this track. Do not compare its accuracy directly with the standard track: it has a different label set and intentionally more adversarial wording.
