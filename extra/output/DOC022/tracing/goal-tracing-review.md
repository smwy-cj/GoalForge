# 目标证据追溯审核文档

定位核验与语义判断分开；本文件不表示人工确认。

## DOC022-C001 在任意机器上都能改代码，尤其是没有图形界面的服务器。

支持判断：直接支持

T015 说明换机器时其他编辑器不一定可用，T021 说明服务器只有命令行，因此必须在终端里改代码。

> You have to work at different machines

来源：DOC022:S016；定位：exact；范围：full_text；全文位置：4131—4169；识别状态：native_text

> when I have to like change some things at at the server, I can just easily open the vim and and modify the code

来源：DOC022:S016；定位：exact；范围：full_text；全文位置：4640—4751；识别状态：native_text

> you can only run vim on the terminal, because you can only access to the command line interface

来源：DOC022:S022；定位：exact；范围：full_text；全文位置：6448—6543；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C002 把个人配置带到每一台机器，让各处环境一致。

支持判断：直接支持

T031 说明配置文件可复制到服务器，使远端环境与本地一致。

> make every system just like your local local customization

来源：DOC022:S032；定位：exact；范围：full_text；全文位置：10289—10347；识别状态：native_text

> if you put put it in the server and and the server will will be just like your local beam

来源：DOC022:S032；定位：exact；范围：full_text；全文位置：10389—10478；识别状态：native_text

> if I don't get used to the vim, I may find difficulty to easily modify codes on the server

来源：DOC022:S016；定位：exact；范围：full_text；全文位置：4774—4864；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C003 本地环境可深度定制：外观、快捷键、语法主题都按自己习惯来。

支持判断：直接支持

T015 说会装插件、改界面，T035 说快捷键与外观都可在配置文件里改。

> I will like customize them to to. I will install a bunch of like cool plugins

来源：DOC022:S016；定位：exact；范围：full_text；全文位置：5004—5081；识别状态：native_text

> I can customize like, which shortcut I want to activate it

来源：DOC022:S036；定位：exact；范围：full_text；全文位置：12381—12439；识别状态：native_text

> control. P is open the file in this project

来源：DOC022:S052；定位：exact；范围：full_text；全文位置：16112—16155；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C004 全部操作靠键盘完成，手不离键盘以提升效率。

支持判断：直接支持

T055 说全部操作都在键盘上、手不离键盘，T063 明确把这一点归为效率。

> everything you do is on the keyboard

来源：DOC022:S056；定位：exact；范围：full_text；全文位置：19103—19139；识别状态：native_text

> keep keeping your hands on the keyboard. Just do improve your efficiency

来源：DOC022:S064；定位：exact；范围：full_text；全文位置：23764—23836；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C005 在大型项目里按文件名快速定位文件，并能跨文件全局搜索。

支持判断：直接支持

T033 说装了模糊搜索插件，T041 说明它按文件名找文件、也能跨文件搜字符串。

> I can install like fuzzy search in in my, in my vein

来源：DOC022:S034；定位：exact；范围：full_text；全文位置：11031—11083；识别状态：native_text

> helps you to find the file by its name

来源：DOC022:S042；定位：exact；范围：full_text；全文位置：13195—13233；识别状态：native_text

> you can search the stream across every files in your project

来源：DOC022:S042；定位：exact；范围：full_text；全文位置：13971—14031；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C006 在同一个终端窗口内分屏：一边编辑、一边执行，立刻看到运行结果。

支持判断：直接支持

T051 描述 tmux 左右分屏，一边命令行一边 vim，改完立刻执行看结果。

> I will split the tmox split the window into half, and one is for command line one is for vim

来源：DOC022:S052；定位：exact；范围：full_text；全文位置：15228—15320；识别状态：native_text

> I will execute the code. There, I can. I can just see the result immediately

来源：DOC022:S052；定位：exact；范围：full_text；全文位置：16749—16825；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C007 从编码、提交、评审到部署与线上监控，尽量在同一工具内完成。

支持判断：直接支持

T081 说整条流水线正在被收进 VS Code，T087 逐项列出编码/推送/评审/部署/监控都可在其中完成。

> the whole pipeline is integrating Vs code like

来源：DOC022:S082；定位：exact；范围：full_text；全文位置：32810—32856；识别状态：native_text

> Everything can be finished on Vs code

来源：DOC022:S088；定位：exact；范围：full_text；全文位置：35476—35513；识别状态：native_text

> There's a extension on the Vs code

来源：DOC022:S092；定位：exact；范围：full_text；全文位置：37537—37571；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C008 编辑器必须支持插件/扩展，好把工具装配到满足自己的全部需求。

支持判断：直接支持

T103 明确说插件/扩展对编辑器是「must」，否则无法满足开发者的全部需求。

> there's a must for editor

来源：DOC022:S104；定位：exact；范围：full_text；全文位置：40306—40331；识别状态：native_text

> The the editor must supports plugins or extensions

来源：DOC022:S104；定位：exact；范围：full_text；全文位置：40832—40882；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C009 装扩展应像应用商店一样：可搜索、可看文档与评分，再一键安装。

支持判断：直接支持

T097 对比 VS Code 的应用商店式安装：搜索、看文档与评分、一键装。

> just go to the marketplace and search the extension you want

来源：DOC022:S098；定位：exact；范围：full_text；全文位置：39428—39488；识别状态：native_text

> You can see the ratings

来源：DOC022:S098；定位：exact；范围：full_text；全文位置：39602—39625；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C010 编辑器背后有活跃社区，遇到问题能查到别人的解法。

支持判断：直接支持

T109 说社区的价值在于能看到别人怎么解决问题，且规模比平台更重要。

> when it has a community, you can, you can see how people solve issues

来源：DOC022:S110；定位：exact；范围：full_text；全文位置：42070—42139；识别状态：native_text

> How big is the community

来源：DOC022:S110；定位：exact；范围：full_text；全文位置：42575—42599；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## DOC022-C011 写代码时获得语言相关的语法高亮与缩进支持，让代码更易读。

支持判断：直接支持

T009 说代码空间要适配语言、提供缩进与高亮，T011 说明高亮帮助读代码。

> you may have to like, like customize like in indent distance, or some like highlighting

来源：DOC022:S010；定位：exact；范围：full_text；全文位置：1434—1521；识别状态：native_text

> The syntax highlighting will help you like read the code better

来源：DOC022:S012；定位：exact；范围：full_text；全文位置：2940—3003；识别状态：native_text

问题：未另列问题

人工决定：

修改意见：

审核备注：

## 限制

- 定位工具不判断语义；语义结论来自另外保存的当前助手或人工判断，非独立审核。
- 处理目标清单中已有目标；不会自动新增或改写目标。
