# 目标模型

版本：v1。人工待审。

- Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  适用条件：when the week is busy or the purchase is the usual regular stock
- Generate a grocery list automatically from the user's past orders.
  适用条件：uses the user's own order history
- Provide reusable grocery-list templates that the user can customize for different occasions such as a weekly list and a party-planning list.
  适用条件：weekly shopping；party planning
- Reduce the typing and clicking needed for each order by letting the user open one saved list and read through it instead of rebuilding the list.
  适用条件：recurring grocery orders
- Keep the recurring grocery list comprehensive so that forgotten items do not force an extra trip to the store.
  适用条件：shopping from memory
- Every two weeks, show the user the grocery list for sign-off and then place the order for pickup.
  适用条件：biweekly cadence；user signs off before the order is placed；pickup
- Suggest features that are likely useful to the user based on how the user is using the platform.
  适用条件：existing features such as lists and Buy again are buried
- Make store-specific availability clearly visible while searching so that items unavailable at the selected store are not added to the cart.
  适用条件：searching Amazon before Whole Foods is selected
- Recommend products in a feed when the user is scrolling through a category such as snacks.
  适用条件：exploratory category browsing, e.g. snacks；not for routine known-item orders
- Find out how purchase data shared between the in-store and online grocery channels is used.
  适用条件：account linked to Whole Foods purchases

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Provide reusable grocery-list templates that the user can customize for different occasions such as a weekly list and a party-planning list. —[实现方式]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：可复用模板是实现“例行采购少花时间”的具体方式：原文把自定义清单列为提升便利性的功能，并在结尾摘要中被受访者确认。
  条件／假设：routine repeat purchasing
- 有依据的联系：Reduce the typing and clicking needed for each order by letting the user open one saved list and read through it instead of rebuilding the list. —[有助于]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：减少打字与点击直接降低每单的操作时间，对效率目标有正向帮助；原文同句给出该结果，但未声称它是效率的唯一保证。
  条件／假设：recurring orders
- 有依据的联系：Provide reusable grocery-list templates that the user can customize for different occasions such as a weekly list and a party-planning list. —[有助于]→ Keep the recurring grocery list comprehensive so that forgotten items do not force an extra trip to the store.
  依据：原文把“复用一份清单”与“更全面、不容易漏项”放在同一改造结果里，模板复用对清单完整性有正向帮助。
  条件／假设：list is reused rather than rebuilt
- 有依据的联系：Keep the recurring grocery list comprehensive so that forgotten items do not force an extra trip to the store. —[有助于]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：漏项会导致额外跑一趟实体店，浪费原本想节省的时间，因此清单完整性帮助效率目标；该联系由同一段叙述的两个结果连接，属于推断性贡献而非明示因果。
  条件／假设：an item is forgotten
- 有依据的联系：Generate a grocery list automatically from the user's past orders. —[有助于]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：原文说规划“这一两周到底要买什么”才是最费劲的部分，自动生成清单正好减少这段规划投入，因而帮助效率目标。
  条件／假设：user has past orders
- 待确认联系：Every two weeks, show the user the grocery list for sign-off and then place the order for pickup. —[实现方式]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：双周确认后自动下单是省去重复下单动作的具体方式，方向上实现效率目的；但原句只描述流程，未说明其目的，故记为待确认。
  条件／假设：routine restocking every two weeks；双周节奏与用户约每两周采购一次的频率相符
- 有依据的联系：Make store-specific availability clearly visible while searching so that items unavailable at the selected store are not added to the cart. —[有助于]→ Complete routine online grocery orders efficiently, without spending time exploring or browsing items.
  依据：若可用性能在加购前看清，就不必回头重新搜索不可用商品，直接减少返工时间，帮助效率目标。
  条件／假设：item not available at the selected store

## 需要确认

- 模板复用（G003）与减少打字点击（G004）是否应合并为一个目标？
- 模板复用（G003）与减少打字点击（G004）是否应合并为一个目标？
- 效率目标与探索型推荐流是否构成冲突或应分情境并存？
- 效率目标与探索型推荐流是否构成冲突或应分情境并存？
- 店铺可用性可见性目标是否得到足够依据？
- 对数据使用方式的好奇是否应作为产品目标？
- GR1 只覆盖常规补货的选品与下单，遇到新商品或缺货时仍缺口明显；是否需要补充搜索/可用性子目标后才可能成立？
- G008 由“图标不显眼、容易漏选店铺”的抱怨推断而来，原文未直接提出改进要求；是否应改为待确认而非已支持目标？
- 受访者怀疑双周清单功能可能已存在但被埋没（T068），该目标应保留为功能目标，还是改为“让已有功能可被发现”？
- 推荐流只适用于类目探索情境，与例行采购的效率目标条件不同；是否需要明确两者适用边界，避免被读成冲突？
- 已逐对检查其余目标（G002、G004、G005、G007、G009、G010 之间及与 G001 的组合），只能找到贡献或方式类联系，找不到可声称 AND 共同充分的组；该结论是否需要更多访谈证据确认？
- 这组层级仍需确认，尚未作为成立的精化展示。
- 这项联系尚待确认，不表示充分精化。
- 仅依据单次访谈转写；Buy again、Your list、双周清单等现有功能的实际实现未核实。
- 转写含口语重复与识别噪声（如 'I'm about like'、'a an option'），个别句子按上下文理解。
- 未获得产品文档或第二来源，现有能力与期望改进的边界只能按受访者口述判断。

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
