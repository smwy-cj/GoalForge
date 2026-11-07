# 只读技术验收

本次验收与已冻结的基线生成分开；未读取匿名评审、另一生成分支或任何真实目标输出。不评价真实目标语义。仅新增本验收复现记录，未修改技能或测试。

## 已确认缺陷 P2：导出HTML的模板标记污染JSON

定位：`skills/goal-model-building/scripts/kaos_model.py` 原第607—609行，`package()`。

`__PAYLOAD__`先被替换成已编码的模型JSON，随后对整页执行`__CORE__`、`__UI__`字符串替换。合法模型文本字段（本复现在limitations中）只要包含任一同名字面串，就会在JSON字符串内部插入未作JSON编码的整段JavaScript。

实际结果：两个合成case均`inspect.structure=passed`、package完成、manifest生成；提取最终HTML的payload后，JSON解析抛出`Invalid control character`。浏览器启动入口也对该payload执行JSON.parse，因此审核/查看/导出交互无法初始化。JSON单独交付仍然可读。v1/v2共用package路径，问题并不只影响某一schema。

复现：在项目根目录运行`python -B runs/skill-optimization-2026-10-25-complete/technical-review/baseline-acceptance/reproduce_placeholder_collision.py`。脚本拒绝覆盖已有case与结果，复跑应使用新目录或保留现有结果后复制到新验收目录。

证据：`placeholder-collision-result.json`、`case-1/`、`case-2/`。所有输入与失败HTML交付均保留。建议对原模板占位符一次性替换，或先替换静态资源，最后插入payload，以避免再次扫描已插入的用户文本。

## 已核对范围与实际检查

- 读取发布工具、建模器、预览保存器、指定三个前端资产及相关v1/v2、反馈、修订、迁移、联系契约。
- 核对v1默认Python接口、显式CLI v1模式、v2独立联系与精化图、类型循环规则、支持与场景检查、输入字节绑定与引文定位、源文变化和证据变化传播、真实反馈未决保存、显式迁移和旧组快照、JSON/MD/SVG/HTML导出路径、本地保存校验、发布manifest/ZIP及安装后真实import路径。
- `python -B -m unittest discover -s tests -p 'test_kaos*.py'`：29项中28项成功；本地HTTP保存测试因本环境`WinError 10013`连接限制未完成。未将此项归因代码缺陷。
- `python -B -m unittest discover -s tests -p 'test_skill_release.py'`：2项成功，包含临时目录真实构建、安装及加载路径核对。
- `python -B -m unittest discover -s tests -p 'test_skill_migration.py'`：6项成功，包含仅三个同级技能的实际CLI兼容流程。
- `node --test tests/simple_review.test.js`：6项成功。
- 最小合成模板碰撞复现：2个case均重现上述缺陷。

除上述模板碰撞外，未确认其他具有实际影响的缺陷。未执行浏览器视觉与交互端到端检查、真实用户目录安装、应用自动发现或统计独立语义评审；本地HTTP端到端保存受环境限制。
