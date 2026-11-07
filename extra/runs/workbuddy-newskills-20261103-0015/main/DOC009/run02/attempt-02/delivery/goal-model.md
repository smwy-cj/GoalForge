# 目标模型

版本：v1。人工待审。

- Use an AI assistant as a replacement for traditional web search to get results, except when the results must be perfectly factually correct.
  适用条件：例外：需要结果完全事实正确时不交给助手（改用传统搜索）
- Compose professional emails (and, to a lesser extent, personal emails) with an AI assistant from just a few prompts.
  适用条件：主要用于专业邮件，个人邮件次要；方式是少量提示
- Write long-form documents for work or assignments with AI assistance.
  适用条件：适用于工作文档与作业；与校对（G004）为分开的独立任务
- Proofread self-written documents with AI assistance for spelling, grammar and tone checks.
  适用条件：对象是本人已写好的文档；检查项为拼写、语法、语气
- Generate digital art with AI and embed it in blog posts or social media posts, despite the stakeholder not being a skilled artist.
  适用条件：用途是嵌入博客与社交媒体帖子；自述本人绘画能力差，AI 使其作品看起来不像外行（T013）；加速创作过程是已实现的现状，未作为独立要求
- Create multimedia content with AI assistance for blog posts and social media posts.
  适用条件：用途包括博客与社交媒体帖子的构思；也用于工作场景
- Use AI assistant tools for assignments whose rules permit their use.
  适用条件：仅限允许使用 AI 助手的作业；使用频率约每周 3-4 次（写文档与作业合计，现状）；主要用途为头脑风暴与更好表达已有想法
- Use AI assistance to brainstorm different ideas.
  适用条件：用于写文档与作业；被列为主要任务之一
- Use AI assistance to articulate the stakeholder's own existing ideas better.
  适用条件：用于写文档与作业；对象是本人已有的想法
- Give prompts to the AI assistant over voice, if the capability existed.
  适用条件：条件是助手具备直接接收语音提示的能力；原文为'might consider'，采纳未确认；目前主要通过内嵌文本框输入文本并附带附件
- Use AI assistance for coding or programming tasks at work.
  适用条件：工作场景限定为编码/编程；与邮件、文档、多媒体并列的重要活动
- Have the AI assistant process and output standardized formats such as JSON or XML in addition to natural language for coding tasks.
  适用条件：限定在编程/编码任务的输入输出；例举格式为 JSON、XML；原文语气为建议（it would make sense）
- Receive succinct responses from the AI assistant rather than verbose conversational ones.
  适用条件：前提：使用助手是为了提高生产力且时间是关键要素；强度为偏好（appreciate / more towards），非硬性要求
- Improve the stakeholder's productivity by using AI assistant tools.
  适用条件：原文以'given the premise'方式陈述为使用助手的前提目的；未给出可验证指标或阈值
- Have the AI assistant hold memory or history of previous interactions to provide context about the stakeholder's requirements.
  适用条件：目的：为助手提供上下文与自身需求；与'不必重复自己'（G016）为手段与结果，分别保留
- Not have to repeat the stakeholder's context in every query or conversation with the AI assistant.
  适用条件：适用于每次查询与每次对话；强度为 super important
- Cross-check answers to mathematical problems with multiple AI assistants.
  适用条件：仅限数学/解题场景；原因是助手在数学上容易出错；语言任务不需比较（现状，未写入本目标）
- Have AI assistant output be factually accurate rather than hallucinated.
  适用条件：由负面体验、顾虑与条件推断的期望，原文未直接提出改进请求；T045 中受访者自述对如何达成没有解决方案；T003 中'需要完全事实正确时改用传统搜索'为其条件
- Fully automate certain pipelines with AI assistance without needing a human in the loop.
  适用条件：当前因生成内容可能事实不准确、需人工在环而未能实现；原文以反事实方式表达愿望（若能做到自动化就能更好提升生产力）；未说明是哪些流水线，也未给出实现方式
- Have hallucinations detected and corrected, which the stakeholder sees as requiring a technological breakthrough and for which no solution is offered.
  适用条件：受访者明确自述想不出解决方案；被视为更广泛的技术挑战，尚未解决；未确认是否作为对助手的具体要求
- Have an AI assistant interface that is not cluttered or distracting.
  适用条件：来自对 perplexity（屏幕上元素过多而分散注意力）与 Gemini（网页设计令人不适）的负面体验；不满本身为明确表达，目标表述（界面应不杂乱）含泛化推断，故 origin 为 explicit 而支持判断为 inferred；受访者自述不确定偏好是出于习惯还是界面本身更好；未要求统一的具体界面规范
- Have the AI assistant support text-to-video generation.
  适用条件：现有能力支持文生图，文生视频是有用的补充；受访者称该方向已有研究但尚未产品化
- Have AI assistants act as agents that perform described tasks, rather than only returning text to copy and paste.
  适用条件：方向是从问答式文本补全转向可自主执行任务的 agent；示例（自动打开邮件客户端撰写并发送邮件）用于演示该能力，不另立为固定业务目标；未说明适用范围与验收标准

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Generate digital art with AI and embed it in blog posts or social media posts, despite the stakeholder not being a skilled artist. —[范围具体化]→ Create multimedia content with AI assistance for blog posts and social media posts.
  依据：T009 把多媒体创作列为前三用例并以博客/社交媒体帖子为例，T013 在追问多媒体时把同一用途具体化为生成数字艺术并嵌入博客/社交媒体帖子；G006 是 G005 在同一用途下的具体情境，方向为具体情境指向一般目标。未声称数字艺术覆盖 G005 的全部适用范围。
  条件／假设：假设 T013 的数字艺术生成是 T009 多媒体创作用例的实际形态
- 有依据的联系：Have the AI assistant process and output standardized formats such as JSON or XML in addition to natural language for coding tasks. —[有助于]→ Use AI assistance for coding or programming tasks at work.
  依据：T027 同一段中，先说明用助手做编程工作时常需要输入输出为特定格式，再提出应能格式化为编码任务使用的标准格式；格式能力有助于完成编程任务，但原文未声称其足以实现编程帮助，故为 contribution 而非精化。
  条件／假设：限定在编码/编程任务的输入输出
- 有依据的联系：Receive succinct responses from the AI assistant rather than verbose conversational ones. —[实现方式]→ Improve the stakeholder's productivity by using AI assistant tools.
  依据：T031 以'前提是我用助手提高生产力、且时间是关键要素'直接给出偏好简洁回答的理由，简洁回应是服务于提高生产力这一目的的实现方式；未声称简洁回答在所有情况下足以提高生产力。
  条件／假设：假设节省阅读冗长回答的时间即为提高生产力的途径之一
- 有依据的联系：Have the AI assistant hold memory or history of previous interactions to provide context about the stakeholder's requirements. —[实现方式]→ Not have to repeat the stakeholder's context in every query or conversation with the AI assistant.
  依据：T033 先说不必在每次查询或对话中重复自己非常重要，紧接着以'因此若它能保存以往交互的记忆或历史会非常有帮助'给出实现方式；方式与结果在同一问答中明确对应，未声称记忆在所有情况下足以避免重复。
- 有依据的联系：Fully automate certain pipelines with AI assistance without needing a human in the loop. —[有助于]→ Improve the stakeholder's productivity by using AI assistant tools.
  依据：T043 明确说若能做到自动化就能更好地把任务生产力化（productivize my tasks much better），自动化对提高生产力有帮助；原文未说明实现自动化的条件与范围，故为 contribution 而非精化。
  条件／假设：假设'更好地提升生产力'中的 productivize 与 G014 的生产力目的同义
- 有依据的联系：Have AI assistant output be factually accurate rather than hallucinated. —[有助于]→ Fully automate certain pipelines with AI assistance without needing a human in the loop.
  依据：T043 说明未能自动化某些流水线的原因是生成内容可能事实不准确、因此需要人工在环；输出事实准确有助于实现自动化。未声称准确性单独足以实现自动化（T045 仍认为需要技术突破）。
  条件／假设：假设消除事实不准确即可移除人工在环这一阻碍
- 待确认联系：Have hallucinations detected and corrected, which the stakeholder sees as requiring a technological breakthrough and for which no solution is offered. —[有助于]→ Have AI assistant output be factually accurate rather than hallucinated.
  依据：T041 说明易产生幻觉影响生成陈述的事实准确性，T045 在追问改进时说需要技术突破才能检测并纠正幻觉；据此提出检测纠正幻觉有助于事实准确。因端点 G020 支持为 insufficient（受访者自述无方案），按联系发现规则不能标 supported，保留 proposed 待确认。
  条件／假设：假设检测并纠正幻觉能够减少不准确输出

## 需要确认

- 原文尚不足以支持这项目标，或存在相反证据。
- 原文尚不足以支持这项目标，或存在相反证据。
- 来源与支持标签不同；两者不必相等，请在判断理由中解释差异，未自动覆盖原值。
- 语音输入提示是您希望具备的能力，还是仅在具备时会考虑使用？
- 检测并纠正幻觉是您期望助手具备的能力，还是仅视为行业技术挑战？
- 事实准确是普遍要求还是仅在关键任务/需要完全正确时适用？是否有可接受的错误率？
- 希望自动化的'某些流水线'具体指哪些任务？是否要求取消人工复核？
- 界面简洁的诉求适用于所有助手还是仅针对竞品的具体界面？
- 作业场景与撰写文档、头脑风暴之间是并列用途还是层级关系？
- 作业场景与撰写文档、头脑风暴之间是并列用途还是层级关系？
- 作业场景与撰写文档、头脑风暴之间是并列用途还是层级关系？
- 作业场景与撰写文档、头脑风暴之间是并列用途还是层级关系？
- 已检查但无依据（并列用例）：G002（邮件）、G003（撰写文档）、G004（校对）、G005/G006（多媒体）、G011（编程）之间的四类联系均已逐对检查。原文在 T009、T015、T027 中并列列举这些用例，未说明任一项服务于另一项、或构成另一项的具体情境/实现方式，属同主题并列，按联系发现规则不构成联系，故不建边。
- 已检查但无依据（用途与目的）：G008（头脑风暴）、G009（更好表达想法）与 G003（撰写文档）、G007（作业）之间已检查 contribution。T017 的语义是'助手帮助我头脑风暴与表达想法'，并非'头脑风暴有助于完成作业或文档'，未给出目的—手段依据，故不建边。
- 已检查但无依据（precedes）：全篇已检查是否存在两个目标结果之间的先后依赖。T055 的'描述任务→执行任务'属同一目标（G023）内部的步骤，不构成两个目标之间的 precedes；其余目标间原文未给出先后依赖，故 precedes 关系为 0 条。
- 已检查但无依据（G017 与 G018）：交叉核对是受访者为应对数学易错而采取的核对做法，原文未说明该做法会使助手输出更准确，贡献方向不成立；也不构成具体化或实现方式，故不建边。
- 已检查但无依据（G022 与 G005/G006）：文本转视频与多媒体创作同属多媒体主题，T055 只说视频是现有文生图能力的有用补充，未说明它服务于博客/社交帖子创作目标；同主题不构成联系，故不建边。
- 已检查但无依据（G021、G010、G001、G012 与其他目标）：G021 界面诉求在 T053 中仅作为令人 frustration 的竞品特性列出，未连接到生产力或其他结果；G010 语音输入为条件性考虑，无共同场景；G001 与 G018 之间是 T003 的例外条件关系，已写入 G001 context 而非联系；G012 的格式需求与 G023 的 agent 方向无共同依据。均不建边。
- 已检查但不足以成立（精化组）：对 G014（提高生产力）判断，G013 与 G019 只覆盖回应风格与自动化两条途径，原文另列举邮件、文档、多媒体、编程等用途，不能声称共同充分，GR1 保持 proposed+partial；对 G007（作业）判断，G008+G009 仅为原文所说的主要用例，作业还涉及撰写与校对，GR2 保持 proposed+partial。其余目标 G001-G006、G008-G013、G015-G023 均无原文依据可声称存在共同充分的子目标组（原访谈未以整组方式描述任何父目标的实现条件），故成立精化组数为 0，不为凑层级硬造根或组。
- 语音输入提示是您实际希望助手具备的能力，还是仅在具备时会考虑使用？T023 使用 might consider，采纳强度未确认。
- 检测并纠正幻觉是您期望助手具备的能力，还是仅视为行业待解决的技术挑战？T045 明确自述想不出解决方案。
- 事实准确是普遍硬性要求，还是仅在关键任务或需要完全正确时适用？原文未给阈值或适用范围。
- 希望自动化的'某些流水线'具体指哪些任务？原文未列举，也未说明是否需要取消人工复核。
- 界面简洁的诉求适用于所有助手，还是仅针对 perplexity 与 Gemini 的具体界面？受访者自述不确定是出于习惯还是界面本身更好。
- 标准化格式支持是否需要覆盖您在反问中提到的 HTML 或 LaTeX，还是仅限编码任务中的 JSON/XML 一类格式？
- 提高生产力是否有可验证的指标或阈值？原文仅以前提方式陈述该目的。
- GR1 未成立：缺少能证明 G013 与 G019 共同充分实现 G014 的依据，且异常场景（关键任务仍需人工复核，T041/T043）为反例；是否还有原文未覆盖的生产力途径需补充？
- GR2 未成立：T017 只说明头脑风暴与表达想法是作业中的主要用例，未声称二者共同充分；作业还需撰写与校对（T015/T021），缺口未解决。
- R7 保持 proposed：端点 G020 的支持为 insufficient（T045 自述无方案），端点支持不足时不能标 supported；若确认检测纠正幻觉是明确要求，可重评该联系与相关组。
- 这组层级仍需确认，尚未作为成立的精化展示。
- 这组层级仍需确认，尚未作为成立的精化展示。
- 这项联系尚待确认，不表示充分精化。
- 仅依据分配的 DOC009 转写（59 轮），未读取仓库其他目录、未联网、未参考任何历史目标或参考答案
- 转写为口语，存在重复、自我修正与疑似转写错误（如 T003 的 Camus、T043 的 automated automation、T031 的 give given），均按原文原样引用，未做校正或润色
- T025、T029、T049 等回合受访者仅作反问确认，未形成新目标
- 本轮为生成方自检，独立语义审查与形式证明未执行（not_run），人工接受状态为 pending
- 未做逐句分类；source_checks 只登记实际回查的重要片段，空处不代表已穷尽意图

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
