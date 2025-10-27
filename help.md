## Core Principles for Effective Tools

1. Tool Selection & Design

Quality over quantity - Build fewer, more thoughtful tools targeting high-impact workflows

Consolidate functionality - Combine multi-step operations into single tools (e.g., schedule_event instead of separate list_users + create_event)

Match agent capabilities - Design for LLM agents' limited context window; avoid tools that return excessive data

2. Tool Organization

Use namespacing - Group related tools with prefixes/suffixes (e.g., asana_search, jira_search) to help agents select appropriate tools

Clear, distinct purposes - Each tool should have a well-defined function that matches how humans would subdivide tasks

3. Response Optimization

Return high-signal information - Prioritize contextual relevance over technical details; use meaningful identifiers instead of cryptic UUIDs

Control response verbosity - Implement response formats (concise/detailed) to manage token usage

Optimize token efficiency - Use pagination, filtering, and truncation with helpful error messages

4. Tool Descriptions

Write clear, explicit descriptions - Explain tools as you would to a new team member, including specialized terminology and expected behaviors

Avoid ambiguity - Use precise parameter names (e.g., user_id instead of user)

Refine through evaluation - Small improvements in tool descriptions can dramatically boost agent performance


## 编写高效工具的原则

1. 选择合适的工具

工具数量 ≠ 效果更好：避免简单封装现有软件或 API，应针对智能体（agent）的特性设计工具。

考虑智能体的限制：智能体上下文有限，不适合处理大量数据（如返回全部联系人）。应设计针对性工具（如 search_contacts 而非 list_contacts）。

工具应整合功能：将多步骤操作合并为一个工具（如 schedule_event 替代 list_users + create_event）。

2. 工具命名与分类

命名空间（Namespacing）：使用前缀或后缀对工具分组（如 asana_search, jira_search），避免智能体混淆。

明确工具用途：每个工具应有清晰、独特的用途，减少智能体的决策负担。

3. 返回有意义的上下文

提供高价值信息：工具响应应包含对智能体有用的信息（如 name、file_type），而非低价值技术标识（如 uuid）。

支持多种响应格式：通过参数（如 ResponseFormat 枚举）控制返回简洁或详细内容，提升灵活性。

优化响应结构：根据任务选择最适合的响应格式（JSON、XML、Markdown 等）。

4. 优化令牌效率

控制响应长度：通过分页、筛选、截断等方式限制工具响应的令牌数量（如默认限制 25,000 令牌）。

提供明确错误提示：错误信息应具体、可操作，引导智能体调整输入或使用更高效的策略。

5. 优化工具描述

清晰描述工具功能：像向新员工解释一样，明确说明工具的用途、参数和输出。

避免歧义：参数命名应明确（如用 user_id 替代 user）。

