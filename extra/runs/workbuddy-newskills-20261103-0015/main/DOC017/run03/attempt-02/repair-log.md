# 修复记录 attempt-02（第 1 次修复）

## 触发原因

在 `attempt-01` 首次运行
`python .../logs/harness.py "."`
时报错，harness 未产出交付物：

1. `prepare_source failed (2)`：`Use a fresh output directory; existing source artifacts will not be overwritten`。
   原因是我在跑 harness 之前用 `goal-extraction/scripts/prepare_source.py` 手工生成过 `work/source.txt` 等文件，harness 又要在同一位置重新准备源文，发生目录冲突。
2. 清除 `work/` 后重跑，前进到 `judgment_template` 再次失败：
   `ValueError: Unknown inference reference`（`trace_candidates.py` → `validate_input`）。
   原因：`G011` 的 `inference.basis_candidate_ids` 写成了原始候选 ID `["C017","C018","C027"]`，而核验阶段的目标集合使用最终目标 ID（`G***`），引用无法解析。

## 改动的对象

- `G011`（接收相关岗位更新）：`inference.basis_candidate_ids` 由 `["C017","C018","C027"]` 改为 `["G002","G016"]`，
  并在 `reason` 中说明这三处抱怨与已提取的“按技能集匹配”（G002）、“标记不感兴趣后不再出现”（G016）指向同一相关性诉求。
  语义结论（inferred / 不设阈值）未变。
- 无其他目标、关系、组、覆盖记录被改动。

## 为什么新建 attempt-02

`attempt-01` 已被前一次中断的运行写入了 `extraction.json`、`judgments.json`、`raw-candidates.json`、
`work/` 等中间文件，且 prepare_source 拒绝覆盖；按任务说明第 7 节，失败后不改 `attempt-01` 的生成产物，
改为把 `spec.json` 复制到 `attempt-02` 后重跑。`attempt-01` 全部内容保留原样。

## 未做的改动

- 未因该结构错误删除任何有依据的候选或目标；
- 未调整引文、处置、支持标签或关系状态来“凑通过”。
