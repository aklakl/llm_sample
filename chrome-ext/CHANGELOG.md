# 更新日志 (Changelog)

## [2.0.0] - 2025-11-26

### 🎉 重大重构

此版本对整个扩展进行了全面重构，以解决"Apply on this Page"报错问题，并显著改善了用户体验和稳定性。

### ✨ 新增功能

#### 1. **三种工作模式**
- **智能自动申请** - 一键完成从搜索到申请的全流程自动化
- **仅打开搜索页** - 手动浏览模式，查看Easy Apply职位但不自动申请
- **申请此职位** - 对当前打开的职位详情页进行快速申请

#### 2. **改进的URL筛选策略**
- 使用 LinkedIn 原生的 `f_AL=true` URL参数来筛选Easy Apply职位
- 移除了不可靠的UI交互（点击"All filters"按钮和勾选toggle）
- 更快、更稳定的筛选流程

#### 3. **增强的用户反馈**
- 实时状态消息显示（🚀 正在打开LinkedIn搜索...）
- 中英文双语错误提示
- 详细的工作流程说明卡片

#### 4. **更好的选择器策略**
- 添加了多重后备选择器来查找职位卡片
- 支持不同版本的LinkedIn UI
- 详细的日志输出，便于调试选择器问题

### 🔧 改进

#### `popup.js`
- **完全重写**按钮事件处理逻辑
- 移除了 `auto-apply-checkbox`（功能已整合到按钮中）
- 添加了 `showStatus()` 函数来显示状态消息
- 改进了错误处理和用户提示
- 所有按钮都有清晰的功能说明和视觉反馈

#### `popup.html`
- 更新了按钮ID和文本：
  - `start-automation` → `apply-current-page`（申请此职位）
  - `search-jobs` → 移除
  - 新增 `start-smart-apply`（智能自动申请）
  - 新增 `manual-search`（仅打开搜索页）
- 添加了工作流程说明卡片
- 改进了视觉层次和用户体验

#### `content.js`
- **简化** `autoApplyProcess()` 函数
  - 移除了点击"All filters"按钮的逻辑（120行 → 70行）
  - 移除了查找和点击Easy Apply toggle的逻辑
  - 移除了点击"Show results"按钮的逻辑
- 添加了**多重后备选择器**：
  ```javascript
  'div.job-card-container--clickable'
  'li.jobs-search-results__list-item'
  '[data-job-id]'
  ```
- 改进了日志输出，显示每个职位的匹配状态
- 增加了详细的错误消息（中英文双语）

#### `background.js`
- 添加了 `autoApplyEnabled` 状态标志
- 在 `startAutoApplyProcess` 消息中支持 `autoApply` 参数
- 更新了 `chrome.tabs.onUpdated` 监听器：
  - 只有在 `autoApplyEnabled=true` 时才触发自动申请
  - 在手动搜索模式下清理状态变量
- 在 `processNextJob()` 中重置 `autoApplyEnabled`
- 改进了中文注释

### 🐛 修复

1. **"Apply on this Page" 报错问题**
   - 原因：依赖不稳定的UI元素选择器
   - 修复：使用URL参数代替UI交互

2. **"All filters" 按钮未找到**
   - 原因：LinkedIn UI变更导致选择器失效
   - 修复：完全移除对该按钮的依赖

3. **Easy Apply toggle 未找到**
   - 原因：模态框加载时机不可预测
   - 修复：通过URL参数 `f_AL=true` 直接筛选

4. **职位卡片选择器失效**
   - 原因：LinkedIn UI有多个版本
   - 修复：添加了后备选择器链

### 📚 文档

#### 新增文档
- `REFACTORED_GUIDE.md` - 详细的重构指南
  - 使用方法（三种模式）
  - 技术细节（URL参数、选择器策略）
  - 常见问题和解决方案
  - 调试方法
  
- `TEST_CHECKLIST.md` - 测试验证清单
  - 4个测试场景
  - 问题排查步骤
  - 测试记录表格

#### 更新文档
- `CHANGELOG.md` - 此文件，记录所有变更

### ⚠️ 破坏性变更

1. **移除了 `auto-apply-checkbox`**
   - 自动申请功能现在通过点击"智能自动申请"按钮来触发
   - 如果你的代码依赖这个checkbox，需要更新

2. **按钮ID变更**
   - `start-automation` → `apply-current-page`
   - `search-jobs` → 移除（功能拆分为两个新按钮）

3. **URL格式变更**
   - 旧：`https://www.linkedin.com/jobs/search/?keywords={jobTitle}`
   - 新：`https://www.linkedin.com/jobs/search/?keywords={jobTitle}&f_AL=true`

### 🔒 安全性

⚠️ **仍然存在的安全问题**：
- ZHIPU AI API Key 硬编码在 `background.js` 中
- **建议**：将API Key移到扩展选项页面，让用户自己输入

### 📊 代码统计

| 文件 | 修改前 | 修改后 | 变化 |
|------|--------|--------|------|
| `popup.js` | 85 行 | 152 行 | +67 行 |
| `popup.html` | 224 行 | 224 行 | ~重构 |
| `content.js` | 304 行 | 234 行 | -70 行 |
| `background.js` | 172 行 | 187 行 | +15 行 |

**总体**：代码更清晰，复杂度降低，功能更强大

### 🎯 升级建议

如果你正在使用旧版本：

1. **备份你的简历数据**
   - 打开扩展选项页面
   - 复制你的简历内容
   - 保存到安全的地方

2. **更新扩展**
   - 在 `chrome://extensions` 中刷新扩展
   - 或重新加载扩展文件夹

3. **测试新功能**
   - 使用 `TEST_CHECKLIST.md` 进行系统测试
   - 从"仅打开搜索页"开始测试（最安全）

4. **阅读新文档**
   - `REFACTORED_GUIDE.md` - 了解新的工作流程
   - `QUICK_START.md` - 快速开始指南（如果有更新）

### 🚀 下一步计划

- [ ] 将API Key移到选项页面（安全性改进）
- [ ] 添加申请进度跟踪（显示已申请X/总共Y个职位）
- [ ] 添加申请历史记录
- [ ] 支持更多的AI服务提供商
- [ ] 优化表单填写算法（处理更复杂的问题类型）
- [ ] 添加单元测试和集成测试

---

## [1.0.0] - 之前版本

### 初始功能
- 基本的Easy Apply自动化
- AI辅助问题回答
- 简历管理

### 已知问题（已在2.0.0中修复）
- "Apply on this Page"经常报错
- 依赖不稳定的UI选择器
- 缺少手动模式选项
- 错误消息不够友好

---

**版本说明**：
- 主版本号（Major）：不兼容的API变更
- 次版本号（Minor）：向下兼容的功能性新增
- 修订号（Patch）：向下兼容的bug修复

**当前版本**：2.0.0（重大重构版本）
