> **Since English is not the author's native language, the English documentation has been AI-assisted translated and may contain errors. If you find the English documentation difficult to understand, please refer to the Chinese version and use translation tools or AI to help with translation and understanding.**

<h1 align="center">
  <br>
  <img src="https://tdragon6.github.io/AgBox-Docs/logo.svg" width="60px" alt="AgBox">
</h1>

<h4 align="center">
    AgBox is an OPC digital employee hosting platform. Here, you can easily realize a one-person company for lightweight needs — simply throw out a requirement: "Help me develop a full-stack enterprise management system," and then you can walk away. The backend engineer will complete the backend development on their own, the frontend engineer will complete the frontend development on their own, and finally the QA engineer will perform comprehensive functional testing. They will collaborate with each other until the task is complete. All you need to do is "harvest" the results. If you have additional requirements or are unsatisfied with the outcome, you can continue to throw new requirements at AgBox.
</h4>

<p align="center">
	<img src="https://img.shields.io/github/license/tdragon6/AgBox">
	<img src="https://img.shields.io/github/stars/tdragon6/AgBox">
  <img src="https://img.shields.io/github/v/tag/tdragon6/AgBox">
	<img src="https://img.shields.io/github/v/release/tdragon6/AgBox">
	<img src="https://img.shields.io/github/issues/tdragon6/AgBox">
</p>

<p align="center">
  <a href="#quick-deployment">Quick Deployment</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#environment">environment</a> •
  <a href="#features">Features</a> •
  <a href="#task-types">Task Types</a> •
  <a href="#collaboration">Collaboration</a> •
  <a href="#feature-preview">Feature Preview</a> •
  <a href="#disclaimer">Disclaimer</a> •
  <a href="#license">LICENSE</a>
</p>

<p align="center">
  <a href="https://github.com/tdragon6/AgBox/blob/main/README.md">简体中文</a> •
  <a href="https://github.com/tdragon6/AgBox/blob/main/README_EN.md">English</a>
</p>

---
The architecture design, front-end and back-end code development of this project are entirely hand-crafted, without any AI or Vibe coding involvement — feel free to use and maintain with confidence.

A digital employee is essentially an `Agent Profile` containing `agents.md` rules, `skills`, and other information, corresponding to the `profile` in `hermes-agent` or the directory-level Agent in `claude code`.

The `AgBox` framework is theoretically compatible with any `Agent Loop` engine, and currently uses `hermes-agent` as its base implementation.

## Quick Deployment
```bash
curl -fsSL https://raw.githubusercontent.com/tdragon6/AgBox/refs/heads/main/install.sh | bash
```
- Set username and password:
```bash
agbox username      # Set username
agbox password      # Set password
```
- Start the service and access port `8000`
```bash
agbox start         # Start the service
agbox start -d      # Start in background
```
- For detailed deployment instructions, refer to <a href="https://tdragon6.github.io/AgBox-Docs/en/quick/start.md" target="_blank">Quick Start</a>, which supports one-click deployment, Docker deployment, and manual deployment

## Documentation
<a href="https://tdragon6.github.io/AgBox-Docs/en/" target="_blank">AgBox Documentation</a>

## Environment
- Current Version:
    - `AgBox`: `v0.1.0`
    - `hermes-agent`: `v0.16.0`
- Frontend Stack (`frontend`): `TypeScript` + `Less` + `Vue3` + `Arco Vue Pro`
- Backend Stack (`backend`): `Python3` + `FastApi` + `SQLAlchemy` + `SQLite3`
- For easier deployment, the built frontend code is served by the `FastApi` service. To develop or deploy the frontend separately:
    - In the `frontend` directory, run `npm run dev`. The API base URL needs to be configured in `env.development` and `env.production`.
    - In the `backend` directory, run `python main.py`.

## Features
- Built-in one-click deployment, Docker deployment, and manual deployment options — experience it with a single command
- Full visual management, including digital employees, rules, skills, tasks, workspaces, and model configurations
- Supports conversation tasks, project tasks, and scheduled tasks. Project tasks can include multiple independent digital employees, orchestrated by built-in sync and async coordinators for autonomous scheduling, enabling OPC multi-employee collaboration
- Each digital employee and coordinator has independent sessions, context, configuration, and memory — each focuses solely on accumulating expertise in its own domain (including memory and sessions), simulating real employee scenarios
- Fully open ecosystem — freely import/install digital employees or skills from local sources or the marketplace. The digital employee ecosystem supports the official marketplace, community marketplace, and any `Github` repository that conforms to the format, with multiple distribution and installation methods
- Your digital employees grow over time through task execution, accumulating memories, with upgrade surprises along the way
- Inbox support — receive notifications about task completions or employee upgrades in real time
- Robust API validation and security mechanisms — safely host on public networks and access from anywhere

## Task Types
- `Conversation Task`: A traditional single digital employee task, similar to directly using an `Agent Loop` engine like `claude code`, `hermes-agent`, or `opencode` to start a single conversation session
- `Project Task`: A multi-digital-employee collaborative task, similar to a project where multiple sessions of the above `Agent Loop` engines with different rules, skills, and configurations are invoked sequentially or in parallel, and their returned results are coordinated — i.e., the OPC pattern; All `Project Task` are initiated through coordinators for planned execution.
- `Scheduled Task`: Mounted under a `Conversation Task` or `Project Task`, executed on a schedule via the `AgBox` built-in scheduler, supporting native `linux` `cron` expressions

## Collaboration
- `Synchronous Coordinator` simulates the real-world scenario of a human orchestrating multiple digital employees. It uses a simple custom `loop` to simulate the process of a human repeatedly directing AI until the task is complete. For details, refer to `https://tdragon6.github.io/AgBox-Docs/en/quick/coordinator.md#Synchronous-Coordinator`
![](https://tdragon6.github.io/AgBox-Docs/images/quick/coordinator/sync_coordinator_workflow_en.png)
- `Asynchronous Coordinator` receives user requirements, plans tasks, handles task dependencies, and delegates them to the corresponding digital employees for execution (via the `agbox-assign-task` skill), while also handling git `worktrees` branch merging issues. For details, refer to `https://tdragon6.github.io/en/AgBox-Docs/quick/coordinator.md#Asynchronous-Coordinator`
![](https://tdragon6.github.io/AgBox-Docs/images/quick/coordinator/async_coordinator_workflow_en.png)
- The key differences between `AgBox`'s OPC multi-digital-employee collaboration and `hermes-agent`'s native kanban and other OPC implementations:
    - A project is an atomic unit — all digital employees/coordinators participating in the project share the same `session_id`, but each runs in an isolated session
    - A single requirement is a task. Within the same project and the same digital employee/coordinator, context is shared across multiple tasks; across different projects, sessions and context are independent
    - Each digital employee/coordinator's memory, skills, and rules are shared across sessions and projects
    - To ensure session and context consistency, only one task can be executing at a time for the same digital employee/coordinator in the same session; queued tasks wait in a queue
- Advantages of `AgBox`'s OPC implementation:
    - Enables collaboration across multiple `Agent Loop` instances, solving the problem of excessive context within a single `Agent Loop`. Compared to the sub-Agent pattern, not only context but also sessions, configuration, and memory are fully independent — simulating real employees
    - Organized around projects rather than heartbeat-based task claiming, using coordinator-driven delegation and queue mechanisms for a clearer overall operational view, making project monitoring and management easier
    - Tasks and messages of each digital employee/coordinator in the project support associative traceability, with the hierarchy ranging from Project → Task → Message.
    - While maintaining traceability, the professional accumulation and context/sessions of different digital employees/coordinators are isolated
    - Extensible to any other `Agent Loop` engine

## Feature Preview
### Digital Employees
![](https://tdragon6.github.io/AgBox-Docs/images/usage/robots/manage/robots_manage.png)

### Task Management
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project.png)

### Task Results
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project_task_sync_view_result_1.png)
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/project/tasks_project_task_sync_view_result_2.png)

### Skill Management
![](https://tdragon6.github.io/AgBox-Docs/images/usage/skills/skills.png)
![](https://tdragon6.github.io/AgBox-Docs/images/usage/skills/skills_view_file_operator.png)

### Model Configuration
![](https://tdragon6.github.io/AgBox-Docs/images/usage/model/model_config_step_4.png)

### Workspace
![](https://tdragon6.github.io/AgBox-Docs/images/usage/tasks/workspace/tasks_workspace_gif.gif)

## Version Info
- Current version:
    - `AgBox`: v0.1.0
    - `hermes-agent`: v0.16.0

## Disclaimer
This project (AgBox) is an open-source OPC digital employee hosting platform, intended solely for learning, research, and lawful automated office use. Before using this project, you should ensure that your use complies with local laws and regulations as well as your organization's compliance requirements, and that you have obtained the necessary authorizations.

This project relies on third-party large language model APIs, Skills / MCP tools, and open-source libraries. The accuracy, legality, and applicability of AI-generated content are solely the responsibility of the user. You shall bear the consequences of any illegal activities, data breaches, or losses arising therefrom, and the author shall not bear any legal or joint liability.

This project supports installing third-party Skills, digital employees, and model configurations from the community marketplace. Their security, stability, and compliance are the responsibility of both the publishers and the users. Please carefully review the source code and author information before installation.

As this project is currently developed by a single author, there may inevitably be issues or vulnerabilities in functionality, performance, and security. The author shall not bear any responsibility for any problems arising therefrom.

Before using this project, please carefully read, fully understand, and accept all terms of the disclaimer, documentation, and LICENSE. Unless you have fully read, completely understood, and accepted all terms of this agreement, please do not use this project. Your use of this project, or any other explicit or implicit indication of acceptance of this agreement, constitutes your acknowledgment that you have read and agree to be bound by this agreement.

## LICENSE
`AgBox` is licensed under the [MIT License](https://github.com/tdragon6/AgBox/blob/main/LICENSE)

View third-party open-source software licenses referenced by `AgBox` at [third_party_licenses](https://github.com/tdragon6/AgBox/tree/main/third_party_licenses)
