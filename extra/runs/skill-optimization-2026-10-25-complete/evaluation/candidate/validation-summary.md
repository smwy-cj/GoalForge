# Candidate forward-validation deliveries

First attempts are frozen. DOC003 has a separately stored source-driven revision; it is not substituted for the frozen comparison sample.

|Document|First goals / relations / groups|Current goals / relations / groups|Engineering|
|---|---:|---:|---|
|DOC003|49 / 24 / 3|51 / 26 / 3|passed; reviewable|
|DOC010|23 / 13 / 2|23 / 13 / 2|passed; reviewable|
|DOC013|25 / 10 / 2|25 / 10 / 2|passed; reviewable|
|DOC020|38 / 15 / 2|38 / 15 / 2|passed; reviewable|
|DOC023|15 / 11 / 1|15 / 11 / 1|passed; reviewable|
|DOC031|15 / 11 / 1|15 / 11 / 1|passed; reviewable|
|DOC028|25 / 17 / 2|25 / 17 / 2|passed; reviewable|
|DOC036|26 / 16 / 2|26 / 16 / 2|passed; reviewable|

Every coverage check reports structure=passed and workflow=recorded; semantic_completeness=not_assessed. Every model inspection is passed/reviewable. All groups remain proposed/partial and established refinement count is zero. Independent semantic review and formal proof were not run; human approval is pending.

Actual failures: a source-display encoding failure repaired by UTF-8 display, output truncation repaired by bounded source reads, and one DOC036 model-question target-reference failure repaired locally with its failed input retained. DOC003 has an explicitly separate semantic omission repair. Full commands and hashes are in execution.json, pipeline-execution.json and delivery-index.json.
