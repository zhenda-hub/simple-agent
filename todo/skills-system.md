# Add Skills System with SKILL.md Standard

## Context

Agent 目前只有固定的工具和 system prompt。用户希望能动态加载 "skills"（Prompt + 工具组合），并支持从 GitHub 仓库或 URL 下载 skills。采用主流的 Agent Skills (SKILL.md) 开放标准格式，而非自定义格式。

## Skill 文件格式（SKILL.md 标准）

每个 skill 是一个目录，核心文件为 `SKILL.md`：

```
skills/
  translator/
    SKILL.md              # 必需：YAML frontmatter + Markdown 指令
    scripts/              # 可选：可执行脚本（Python/Bash）
    references/           # 可选：参考文档
    assets/               # 可选：模板和资源
```

**SKILL.md 格式**：
```markdown
---
name: Translator
description: >
  This skill should be used when the user asks to "translate",
  "翻译", "convert language", "中英互译".
version: 1.0.0
---

# Translator Skill

你是一个专业翻译，擅长中英互译...

## 使用指南
- 保持原文风格和语气
- 专业术语保持原文或附注原文
```

- frontmatter：`name`（必需）、`description`（必需，含触发短语）、`version`（可选）
- body：Markdown 格式的指令，注入到 agent system prompt
- 三级加载：metadata（始终加载）→ SKILL.md body（触发时加载）→ resources（按需加载）

## 文件变更

### 1. 新增 `skills.py` — Skills 管理器

核心功能：

- `SKILLS_DIR = Path("skills/")` — 本地 skills 存放目录
- `list_skills() -> list[dict]` — 扫描 `skills/*/SKILL.md`，解析 frontmatter 返回 `[{name, description, version, loaded}]`
- `load_skill(name) -> str` — 读取 `skills/<name>/SKILL.md`，返回 body 内容用于注入 system prompt。如果 `scripts/` 目录存在，扫描 `.py` 文件并动态 import 注册工具
- `unload_skill(name)` — 反注册该 skill 注入的工具
- `download_skill(source: str)` — 从 GitHub 或 URL 下载 skill
  - GitHub: `https://github.com/user/repo[/tree/branch/path]` → 使用 GitHub API 下载对应目录
  - 直接 URL: 下载 zip/tar 或单个 SKILL.md
  - 使用 `httpx` 下载，解压到 `skills/<name>/`
- `create_skill(name: str, description: str, instructions: str, scripts_dir: str = None)` — 交互式创建 skill，生成 `skills/<name>/SKILL.md`，可选创建 `scripts/` 目录

**SKILL.md 解析**：用正则提取 `---` 之间的 YAML frontmatter，剩余部分作为 prompt body。用 `yaml` 库解析 frontmatter（新增依赖）。

**脚本动态注册**：skill 的 `scripts/*.py` 中的函数，如果带 `@tool` 装饰器，import 时自动注册到 `_TOOL_REGISTRY`。需要在 `tools/__init__.py` 添加 `unregister_tools(module_name)` 支持。

**创建 Skill 流程**：
1. 用户输入 `/skills create`
2. 交互式输入：skill name、description（触发短语）、instructions（prompt body）
3. 可选：指定 scripts 目录路径（自动复制）或手动创建
4. 生成 `skills/<name>/SKILL.md` 文件
5. 创建后自动加载

### 2. 修改 `tools/__init__.py`

- 添加 `unregister_tools_by_prefix(prefix: str)` — 反注册以 prefix 开头的工具（用于 skill unload）
- Skill 的 `scripts/*.py` 中使用现有的 `@tool` 装饰器，import 时自动注册

### 3. 修改 `agent.py`

- `Agent.__init__` 新增 `self.loaded_skills: dict[str, str]` 跟踪已加载的 skills
- `_build_system_prompt()` 在基础 prompt 后追加所有已加载 skill 的 SKILL.md body
- `load_skill(name)` / `unload_skill(name)` 方法：加载/卸载 skill 并重建 system prompt

### 4. 修改 `main.py`

新增 CLI 命令处理：

| 命令 | 描述 |
|------|------|
| `/skills` | 列出所有已下载 skills（标记已加载/未加载） |
| `/skills load <name>` | 加载 skill（注册脚本工具 + 注入 prompt） |
| `/skills unload <name>` | 卸载 skill |
| `/skills create` | 交互式创建新 skill |
| `/download <url>` | 从 GitHub 或 URL 下载 skill |

### 5. 依赖变更（`pyproject.toml`）

- 添加 `httpx` — 用于下载 skills
- 添加 `pyyaml` — 用于解析 SKILL.md 的 YAML frontmatter

## 关键文件路径

- `agent.py` — ReAct 循环 + system prompt 构建
- `main.py` — CLI 入口，添加命令处理
- `tools/__init__.py` — 工具注册表，添加反注册
- `config.py` — 配置（无需修改）
- `skills.py` — 新增，skills 管理器
- `.gitignore` — 添加 `skills/` 忽略（下载的 skills 不提交）

## 验证

1. 手动创建测试 skill `skills/translator/SKILL.md`
2. `/skills` 查看列表
3. `/skills load translator` 加载
4. 对话测试（如 "把这段话翻译成英语"），验证 prompt 注入生效
5. 创建带 `scripts/` 的 skill，验证工具注册
6. `/skills unload translator` 验证卸载
7. `/skills create` 交互式创建新 skill
8. `/download <github-url>` 测试从 GitHub 下载 skill
