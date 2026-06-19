<h1 align="center">
  <br>
  <img src="https://tdragon6.github.io/AgBox-Docs/logo.svg" width="60px" alt="AgBox">
</h1>

<h4 align="center">
    AgBox 是一个 OPC 数字员工托管平台，在这里，您可以轻松实现轻量需求的一人公司，只需抛出一个需求：“帮我开发一个前后端分离的企业管理系统”，之后您就可以离开了，后端工程师会自己完成后端开发，前端工程师会自己完成前端开发，最后测试工程师会进行完整的功能测试，他们会互相协作直到任务完成，您只需最后“收菜”即可，若有其他额外需求或不满意本次结果，您可以继续甩需求给 AgBox
</h4>

<p align="center">
	<img src="https://img.shields.io/github/license/tdragon6/AgBox">
	<img src="https://img.shields.io/github/stars/tdragon6/AgBox">
  <img src="https://img.shields.io/github/v/tag/tdragon6/AgBox">
	<img src="https://img.shields.io/github/v/release/tdragon6/AgBox">
	<img src="https://img.shields.io/github/issues/tdragon6/AgBox">
</p>
      
<p align="center">
  <a href="#功能特点">功能特点</a> •
  <a href="#任务类型">任务类型</a> •
  <a href="#协作说明">协作说明</a> •
  <a href="#快速部署">快速部署</a> •
  <a href="#使用文档">使用文档</a> •
  <a href="#部分功能预览">部分功能预览</a> •
  <a href="#版本信息">版本信息</a> •
  <a href="#免责声明">免责声明</a> •
  <a href="#LICENSE">LICENSE</a>
</p>

<p align="center">
  <a href="https://github.com/tdragon6/AgBox/blob/main/README.md">简体中文</a> •
  <a href="https://github.com/tdragon6/AgBox/blob/main/README_EN.md">English</a> 
</p>

---
本项目架构设计和代码开发均是人工完成，未参与任何 AI 与 Vibe Coding，可放心食用和维护

数字员工本质是一个包含 `agents.md` 规则、`skills` 和 其他信息的 `Agent Profile`，对应 `hermes-agent` 的 `profile` 或 `claude code` 目录级 Agent

`AgBox` 框架理论可接入任何 `Agent Loop` 引擎，目前以 `hermes-agent` 作为基座实现，

## 功能特点
- 内置一键部署、docker 部署和手动部署多种方式，最快一行命令即可体验
- 全套可视化管理，包括数字员工、规则、技能、任务、工作空间和模型配置等
- 支持会话任务、项目任务和定时任务，项目任务可加入多个独立的数字员工，通过内置同步和异步协调器自主调度，实现 OPC 多员工协同工作
- 各个数字员工与协调器的会话、上下文、配置和记忆等均独立，只专注自身专业领域的积累（包括记忆或会话等），模拟真实员工场景
- 完全开放的生态系统，可自由从本地或市场导入/安装数字员工或技能，数字员工生态支持官方市场、社区市场和任何符合格式的 `Github` 仓库，多种方式均可进行分发和安装
- 您的数字员工会在任务执行中不断成长，积攒记忆，同时更有升级惊喜
- 支持收件箱功能，第一时间接收任务完成或员工升级的通知
- 完善的API校验和安全防护机制，公网安心托管，随时随地均可访问

## 任务类型
- `会话任务`：传统单数字员工任务，场景类似直接使用 `claude code`、`hermes-agent`、`opencode` 等引擎启动单一会话提问
- `项目任务`：多数字员工协作任务，场景类似一个项目中，多次调用不同规则、技能和配置的上述 `Agent Loop` 引擎来依次或并行启动会话任务，并处理它们返回结果的协作问题，即 OPC 模式
- `定时任务`：挂载在 `会话任务` 或 `项目任务` 下，设置定时执行的任务，通过 `AgBox` 定时器实现，支持 `linux` 原生 `cron` 表达式

## 协作说明
- `同步协调器` 模拟人类真实调度各个数字员工协作的场景，用一个简单自实现的 `loop` 来模拟人类多次指挥AI直到任务完成的全过程，详情参考 `https://tdragon6.github.io/AgBox-Docs/quick/coordinator.md#同步协调器`
![](https://tdragon6.github.io/AgBox-Docs/images/quick/coordinator/sync_coordinator_workflow.png)
- `异步协调器` 接收用户需求，规划任务，处理任务依赖关系，并委派给对应的数字员工执行（通过 `agbox-assign-task` 技能实现），同时处理 git `worktrees` 分支合并相关问题，详情参考 `https://tdragon6.github.io/AgBox-Docs/quick/coordinator.md#异步协调器`
![](https://tdragon6.github.io/AgBox-Docs/images/quick/coordinator/async_coordinator_workflow.png)
- `AgBox` OPC 多数字员工协同的实现方式相比 `hermes-agent` 原生看板和其他 OPC 区别在于：
    - 一个项目为一个原子单位，所有参与项目的数字员工/协调器都标记同一个 `session_id`，但不同数字员工/协调器均在隔离的会话中运行
    - 一次需求是一个任务，同一项目同一数字员工/协调器中多任务间上下文共享，不同项目同一数字员工/协调器的会话和上下文互相独立
    - 每个数字员工/协调器的记忆、技能和规则等是跨会话跨项目共享的
    - 为了保证会话和上下文一致性，同一时间同一数字员工/协调器同一会话只能有一个任务在执行中，排队中的任务会进入队列等待
- `AgBox` OPC 实现机制的优势为：
    - 实现多 `Agent Loop` 的协作，解决同一 `Agent Loop` 上下文过大的问题，同时相对子Agent模式，除了上下文，会话、配置和记忆也都是完全独立的，模拟真实的员工
    - 组织形式以项目为单位，不通过心跳任务认领，而是通过协调器主动委派和队列机制实现，对于运行中的整体视角相对更清晰，便于项目查看和管理
    - 项目中的各个数字员工/协调器的执行任务可关联溯源，层级从项目 -> 任务 -> 消息
    - 在保证关联溯源的基础上，隔离不同数字员工/协调器的专业积累和上下文会话
    - 可扩展其他任何 `Agent Loop` 引擎

## 快速部署
```bash
curl -fsSL https://raw.githubusercontent.com/tdragon6/AgBox/refs/heads/main/install.sh | bash
```
- 设置用户名和密码：
```bash
agbox username      # 设置用户名
agbox password      # 设置密码
```
- 启动服务，访问 `8000` 端口
```bash
agbox start         # 启动服务
agbox start -d      # 后台启动
```
- 详细部署可参考 <a href="https://tdragon6.github.io/AgBox-Docs/quick/start.md" target="_blank">快速开始</a>，支持一键部署、docker 部署和手动部署多种方式

## 使用文档
<a href="https://tdragon6.github.io/AgBox-Docs/" target="_blank">AgBox 使用文档</a>

## 部分功能预览
### 数字员工
![](https://tdragon6.github.io/AgBox-Docs/images/usage/robots/manage/robots_manage.png)

### 任务管理
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project.png)

### 任务结果
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project_task_sync_view_result_1.png)
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project_task_sync_view_result_2.png)

### 技能管理
![](https://tdragon6.github.io/AgBox-Docs/images/usage/skills/skills.png)
![](https://tdragon6.github.io/AgBox-Docs/images/usage/skills/skills_view_file_operator.png)

### 模型配置
![](https://tdragon6.github.io/AgBox-Docs/images/usage/model/model_config_step_4.png)

### 工作空间
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/workspace/tasks_workspace_gif.gif)

## 版本信息
当前版本：
- `AgBox`：`v0.1.0`
- `hermes-agent`：`v0.16.0`

## 免责声明
本项目（AgBox）是一个开源的 OPC 数字员工托管平台，仅供学习、研究与合法场景下的自动化办公使用。在使用本项目前，您应确保其用途符合当地法律法规及您所在组织的合规要求，并已取得必要的授权。

本项目依赖第三方大语言模型 API、Skills / MCP 工具及开源库，AI 生成内容的准确性、合法性与适用性均由使用者自行判断与承担。由此产生的任何非法行为、数据泄露或损失，您需自行承担相应后果，作者将不承担任何法律及连带责任。

本项目支持从社区市场安装第三方的 Skills、数字员工与模型配置，其安全性、稳定性、合规性均由发布者与使用者各自承担。安装前请仔细审查源代码与作者信息。

因本项目目前为作者一人开发，难免会存在功能、性能和安全方面的问题或漏洞，由此产生的任何问题作者将不承担任何责任。

在使用本项目前，请您务必审慎阅读、充分理解各条款内容、免责声明、使用文档和LICENSE。除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要使用本项目。您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。

## LICENSE
`AgBox` 使用 [MIT License](https://github.com/tdragon6/AgBox/blob/main/LICENSE)

查看 `AgBox` 引用的第三方开源软件许可证 [third_party_licenses](https://github.com/tdragon6/AgBox/tree/main/third_party_licenses)
