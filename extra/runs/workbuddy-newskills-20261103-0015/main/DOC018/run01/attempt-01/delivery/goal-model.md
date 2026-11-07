# 目标模型

版本：v1。人工待审。

- Consolidate ebooks and course PDFs into a single application so that all reading material can be opened in one place.
  适用条件：At least for school reading, one application should handle both PDF and ebook formats；The primary reading device is an iPad；Reading is currently scattered across the Kindle app, Google Drive, Adobe Reader and the school portal
- Reduce the number of steps needed to import course articles and PDFs from the school portal onto the iPad, without first downloading them to a computer.
  适用条件：The current portal reading experience is described as cumbersome and disliked；The iPad is the main reading device；Current route: download to the computer, open Drive, then export the PDF
- Provide an export action that sends course reading material directly to one chosen destination, such as Google Drive or a Kindle account.
  适用条件：Ranked as the most important feature；The destination is not fixed: Google Drive, a Kindle account or a standalone application
- Save valuable course PDFs into a personal student library so that they remain accessible after the course or semester ends.
  适用条件：Materials currently become unavailable after the semester (for example the Spring 2024 courses)；Ranked second among the features
- Let students categorize and filter their reading material by the month or year in which they read it, so that they can find it again later.
  适用条件：Ranked third among the features；The stakeholder often remembers when a reading happened rather than its title or ISBN
- Show how far the reader is through the current chapter as a percentage, so that long chapters feel less daunting.
  适用条件：The Kindle app already shows the time remaining in the chapter；Ranked last among the four features
- Have the school provide its own online reading application in which professors' articles are available directly on the student's iPad.
  适用条件：Primarily for the school context；Would primarily be used on the iPad；Stakeholder is an online student with a full-time job
- Have the existing Kindle app also manage PDFs.
  适用条件：Stated as the easier option (it will be easier)；PDFs currently cannot be ported to Kindle as far as the stakeholder knows
- Include the school online-reading application at no separate cost to students.
  适用条件：Answer to whether the stakeholder would pay for the application；What the application should be included in (tuition, school service) is not stated

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Provide an export action that sends course reading material directly to one chosen destination, such as Google Drive or a Kindle account. —[实现方式]→ Reduce the number of steps needed to import course articles and PDFs from the school portal onto the iPad, without first downloading them to a computer.
  依据：导出功能是减少“下载到电脑→打开 Drive→导出 PDF”步骤的具体实现方式：同句把“export it to drive like very easily”与“not to download it to my computer”连在一起，说明导出服务于少步骤导入 iPad 的目的。
  条件／假设：For course articles delivered through the school portal
- 有依据的联系：Have the existing Kindle app also manage PDFs. —[实现方式]→ Consolidate ebooks and course PDFs into a single application so that all reading material can be opened in one place.
  依据：让现有 Kindle 应用管理 PDF 是“把 PDF 与电子书集中到一个应用”的一种选定实现方式；受访者说这样“会更方便”，未声称它足以覆盖全部阅读情境。
- 有依据的联系：Have the school provide its own online reading application in which professors' articles are available directly on the student's iPad. —[范围具体化]→ Consolidate ebooks and course PDFs into a single application so that all reading material can be opened in one place.
  依据：学校自建的在线阅读应用是“把阅读集中到一个应用”在校园情境下的具体化；教授发的文章直接在 iPad 上可读，但原文未说该应用覆盖校外的 Kindle 电子书与新闻阅读，故不声称覆盖一般目标的全部范围。
  条件／假设：School reading context only

## 需要确认

- 统一阅读应用应是全新独立应用、现有 Kindle 应用的扩展，还是学校门户内的功能？学校自建应用（G007）与个人统一应用（G001）是同一产品还是两个方案？
- 统一阅读应用应是全新独立应用、现有 Kindle 应用的扩展，还是学校门户内的功能？学校自建应用（G007）与个人统一应用（G001）是同一产品还是两个方案？
- 按时间分类指“阅读时间”还是“加入资料库的时间”？
- 导出的目标地究竟是 Google Drive、Kindle 账户，还是统一应用本身？
- 进度百分比应只按章显示，还是同时保留整本书的百分比？
- “They should be included”指纳入学费/学校既有服务，还是指包含在应用功能中？
- “不先下载到电脑”是必须条件，还是只是更快的路径？
- 按时间分类指阅读时间还是加入资料库的时间？T055 原话偏向阅读时间，T064 复述为加入时间，受访者只作总体确认。
- 统一阅读应用是全新独立应用、现有 Kindle 应用的扩展，还是学校门户内功能？T043、T047、T057、T064 分别指向不同落点。
- 导出的目标地应为 Google Drive、Kindle 账户还是统一应用本身？受访者说 I don't know，当前只保留“一个选定目的地”。
- 是否需要同时保留整本书的百分比？T049 先用整本 20% 举例，后明确要求按章显示。
- “They should be included”应纳入何处（学费/学校既有服务/应用功能）？这影响责任方与验收。
- “不先下载到电脑”是硬性条件还是仅更快的路径？原文把它与少步骤并列，未说明保留中转是否可接受。
- 本模型未建立 AND 精化组：原文的四项功能是并列候选而非共同充分的一组，且导出与学校应用更像替代路径；如需层级，需补充共同充分性证据。
- 原文为英文访谈自动转写，存在识别错误（如 Kendall 指 Kindle、Co. 之类残句），个别词句需按上下文理解。
- 全部内容来自单一受访者的一次访谈，未提供其他利益相关者或既有产品文档。
- 受访者对多个功能使用 I don't know / I think 等不确定措辞，产品边界与目的地未定。
- 多数目标无量化验收指标（如步骤数、章节百分比阈值），原文未给出，未编造。
- T064 的复述由采访者措辞，受访者只作总体确认，个别措辞（when they're added）与受访者原话有差异。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
