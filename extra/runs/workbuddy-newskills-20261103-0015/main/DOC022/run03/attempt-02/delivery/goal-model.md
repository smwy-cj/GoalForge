# 目标模型

版本：v1。人工待审。

- Be able to open plain vim in the terminal and modify code on any server that has no graphical user interface
  适用条件：服务器/机器无 UI，仅能通过命令行终端访问
- Customize the local development environment by installing plugins and configuring the vim interface to fit personal experience
  适用条件：限于本地开发环境，非服务器上的纯 vim
- Make every system's vim behave like the local customized vim by keeping and reusing the config file
  适用条件：配置文件可移植，可放到服务器上
- Prefer a lightweight editor that opens quickly and avoids the RAM/CPU cost of graphical editors
  适用条件：这是选择 vim 的理由/看重属性，属偏好而非硬性强制
- Keep hands on the keyboard without using the mouse in order to improve coding efficiency
- Use whichever development tool gives better efficiency, since efficiency is what developers ultimately want
- Have an editor that must support plugins or extensions so tools can fit every requirement of a developer
  适用条件：面向开发者；编辑器本用于编辑文本文件，但开发者还需很多东西
- Have a large community around the editor so users can see how people solve issues and see real people improving the product
  适用条件：关键是社区规模/使用人数，而非社区所在平台（Stack Overflow、Reddit、Youtube 均可）
- Be able to start work at any device by getting familiar with every tool
- Not stick to a single tool for a developer; evaluate each situation and choose the best plan
- Keep using vim out of habit even though looking cool no longer matters
  适用条件：明确放弃'酷'这一动机：I don't care about how cool I am anymore（T063）；T075 仍说享受终端编码、觉得酷，与 T063 存在强度张力，见未决问题
- Avoid recommending vim for front-end development because vim cannot display the colors front-end work needs
  适用条件：仅针对前端开发情境；强度为建议（won't recommend），非绝对禁止；原文留有'也许可以解决但要花很多力气'的例外（T061）
- Have an editor that integrates the whole development pipeline (coding, build, test, deploy, code review, monitoring, cloud access) in one app through extensions
  适用条件：需求随时间变化、由产品创造（T081）；描述的是 VS Code 目前覆盖的能力
- Be able to resume the tmux/vim working session immediately after the computer shuts down
  适用条件：tmux 保存进程；适用于电脑意外关机
- Make the editor's customization/configuration easy to understand and maintain without a separate config-file language
  适用条件：仅以抱怨/障碍线索出现（T055/T069/T093）

## 需要确认

- 原文尚不足以支持这项目标，或存在相反证据。
- T063 明确说已不在意'酷'，T075 又说仍觉得终端编码酷；'继续使用 vim'的动机强度应如何界定？
- 配置复杂度只以抱怨/障碍线索出现，应保留为 insufficient 目标，还是仅作为限制/问题？
- 编辑器集成整条流水线、编辑器应有大社区这两项，是受访者明确要求还是对 VS Code 现状/价值的描述？
- 编辑器集成整条流水线、编辑器应有大社区这两项，是受访者明确要求还是对 VS Code 现状/价值的描述？
- 访谈对象谈的是个人工具选择与评价，哪些应视为对'待建编辑器'的需求而非现状描述？
- 原文多为并列的偏好/要求/评价，缺少明确连接两个已核验目标的独立联系原句，也缺少可声称'子目标共同满足足以实现父目标'的整组依据；故 relations 与 AND 精化组均留空，不为连边或凑层级造节点。如需建立层级请补充相应依据。
- 配置复杂度仅以抱怨/障碍线索出现（T055/T069/T093），按目标边界不自动升级为明确要求，保留 insufficient；请确认是否删除或补充正面依据。
- '社区重要'为评价性陈述，社区规模被推断为对编辑器的要求；请确认该推断是否成立。
- T063 '不再在意酷' 与 T075 '仍觉得酷' 的强度张力未解决；请确认维持使用 vim 的动机强度。
- 原文为英文语音转写，存在大量同音误写（vim 记作 being/beam/bin/vein/vime 等，VS Code 记作 Vs cord/Vs culture/vehicle 等），引文逐字符保留原识别结果，未按语义更正。
- 访谈对象为单一受访者（开发者/计算机科学学生），陈述多为个人工具偏好、现状与评价，未明确区分'对现有工具的描述'与'对新系统的要求'。
- 仅依据提供的 DOC022.json 的 118 轮转写；未读取任何参考目标、历史答案、评分材料或仓库其他目录，未联网。
- 未进行独立语义审查、形式证明或人工接受；支持判断由本次生成会话依据原文编制。
- 语音识别不清处无音频可核，相关语义以保留原句与不确定项处理，不冒充人工核验。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
