# 修复记录（attempt-02）

## 触发原因

1. attempt-01 首次运行在 `prepare_source` 阶段失败：我在该目录手工运行过 `prepare_source.py` 生成 `work/source-input.json`、`source.txt`、`source-windows.json`，harness 要求全新输出目录，拒绝覆盖。
2. 清理 `work/` 后重跑，`judgment_template` 失败：`goal G027/G028` 的 `inference.basis_candidate_ids` 写成原始候选 `C028/C029`，而核验输入中只存在最终目标集合，报 `Unknown inference reference`。
3. 在同一 attempt 内再次重跑时，残留的空 `judgments.json` 触发 `FileExistsError`，说明同一 attempt 不能反复原地重跑。

## 改动对象与理由

| 对象 | 改动 | 理由 |
|---|---|---|
| `work/` 源文件 | 移出/清空，改由 harness 重新生成 | 工具要求全新输出目录；不改源文与窗口参数（4/2） |
| `G027.inference.basis_candidate_ids` | `C028` → `G027` | 引用必须指向本任务最终目标集合；G027 由 C028 承接，语义不变 |
| `G028.inference.basis_candidate_ids` | `C029` → `G028` | 同上 |
| 运行目录 | attempt-01 → attempt-02 | 按 brief 第 7 节，失败后不在原目录改产物 |

未改动任何引文、目标表述、判断标签、关系或覆盖处置。

## 结果

attempt-02 一次通过：coverage `structure=passed / workflow=recorded`，inspection `structure=passed / readiness=reviewable`，无 downgraded、无 warnings。
