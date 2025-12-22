# 测试验证清单

## 🔄 重新加载扩展

在测试之前，请先重新加载扩展：

1. 打开 `chrome://extensions`
2. 找到 "LinkedIn Easy Apply Automator"
3. 点击刷新图标 🔄

## ✅ 测试清单

### 测试 1：UI 界面检查

- [ ] 打开扩展 popup
- [ ] 验证有三个按钮：
  - ✨ 智能自动申请
  - 🔍 仅打开搜索页
  - ⚡ 申请此职位
- [ ] 验证职位输入框有默认值 "Senior backend engineer"
- [ ] 验证有工作流程说明卡片
- [ ] 验证有"设置简历"链接

### 测试 2：仅打开搜索页（最安全的测试）

**目的**：验证 URL 构建和页面打开功能

**步骤**：
1. [ ] 在职位输入框中输入 "test job"
2. [ ] 点击 "🔍 仅打开搜索页" 按钮
3. [ ] 验证打开了 LinkedIn 搜索页面
4. [ ] 验证 URL 包含：
   - `keywords=test%20job`
   - `f_AL=true`
5. [ ] 验证页面显示 Easy Apply 职位
6. [ ] 打开浏览器控制台（F12）
7. [ ] 检查控制台日志：
   ```
   Popup: 'Manual Search' button clicked.
   Popup: Opening LinkedIn search (manual mode): https://...
   ```
8. [ ] 验证没有自动申请行为

**预期结果**：✅ 页面正常打开，显示 Easy Apply 筛选后的职位，没有自动化操作

---

### 测试 3：申请当前页面

**目的**：验证单个职位申请功能

**步骤**：
1. [ ] 手动打开一个 LinkedIn Easy Apply 职位页面
   - URL 应该包含 `/jobs/view/`
2. [ ] 打开扩展 popup
3. [ ] 点击 "⚡ 申请此职位" 按钮
4. [ ] 观察页面行为：
   - [ ] Easy Apply 按钮被点击
   - [ ] 申请模态框打开
   - [ ] 表单字段开始自动填充
5. [ ] 检查控制台日志（LinkedIn 页面）：
   ```
   Content: Received 'startApplication'.
   Content: Starting application process on this page.
   Content: Clicking the main Easy Apply button.
   Content: Processing application modal step.
   Content: Found X questions.
   ```
6. [ ] 检查 Background 日志：
   ```
   Background: Received 'processJobQuestions' message.
   Background: Sending request to ZHIPU AI API.
   Background: Received response from ZHIPU AI API: ...
   Background: Parsed AI answers: {...}
   ```

**预期结果**：
- ✅ 申请流程启动
- ✅ 表单自动填写
- ⚠️ 可能需要手动完成某些步骤（取决于职位要求）

---

### 测试 4：智能自动申请（小规模测试）

**⚠️ 警告**：此测试会实际提交申请！请谨慎使用。

**建议**：先用一个不太重要的职位搜索词进行小规模测试。

**步骤**：
1. [ ] 在职位输入框中输入一个特定的职位名称
   - 例如："test engineer xyz" (使用不太常见的词以减少匹配数量)
2. [ ] 点击 "✨ 智能自动申请" 按钮
3. [ ] 观察浏览器行为：
   - [ ] 打开 LinkedIn 搜索页面
   - [ ] 等待 3 秒
   - [ ] 控制台显示找到的职位卡片数量
4. [ ] 检查控制台日志（搜索页面）：
   ```
   Content: Starting auto-apply process for job title: test engineer xyz
   Content: Searching for job cards...
   Content: Found X job cards on the page.
   Content: [1] Found job: "..."
   Content: ✓ Job matches filter: "..." 或 ✗ Job doesn't match filter: "..."
   Content: Found Y matching job links (out of X total).
   ```
5. [ ] 如果找到匹配的职位：
   - [ ] 观察浏览器自动打开职位详情页
   - [ ] 观察自动申请流程
   - [ ] 验证标签页在申请完成后自动关闭
6. [ ] 检查所有日志输出

**预期结果**：
- ✅ 自动找到匹配的职位
- ✅ 依次申请每个职位
- ✅ 申请完成后关闭标签页
- ✅ 所有职位处理完毕后停止

---

## 🐛 常见问题排查

### 问题 1：点击按钮没有反应

**排查步骤**：
1. [ ] 打开 popup 的控制台（右键点击扩展图标 → 检查弹出窗口）
2. [ ] 查看是否有 JavaScript 错误
3. [ ] 验证按钮 ID 是否正确：
   - `start-smart-apply`
   - `manual-search`
   - `apply-current-page`

**可能原因**：
- popup.html 中的按钮 ID 与 popup.js 不匹配
- 有 JavaScript 语法错误

### 问题 2："内容脚本未加载"

**排查步骤**：
1. [ ] 刷新 LinkedIn 页面
2. [ ] 检查 manifest.json 的 content_scripts 配置
3. [ ] 在扩展管理页面中检查权限

**可能原因**：
- LinkedIn 页面未完全加载
- Content script 未正确注入

### 问题 3："未找到职位卡片"

**排查步骤**：
1. [ ] 手动在 LinkedIn 搜索页面打开控制台
2. [ ] 运行选择器测试：
   ```javascript
   console.log('Test 1:', document.querySelectorAll('div.job-card-container--clickable').length);
   console.log('Test 2:', document.querySelectorAll('li.jobs-search-results__list-item').length);
   console.log('Test 3:', document.querySelectorAll('[data-job-id]').length);
   ```
3. [ ] 查看哪个选择器返回的数量 > 0

**可能原因**：
- LinkedIn UI 已更改
- 页面加载时间不足
- 网络延迟

### 问题 4：AI 没有正确回答问题

**排查步骤**：
1. [ ] 检查 Background 控制台日志
2. [ ] 查看 API 响应
3. [ ] 验证简历信息是否已在选项页面中设置

**可能原因**：
- API Key 无效或过期
- 简历信息不完整
- AI 无法理解特定问题

---

## 📊 成功标准

所有测试通过后，你应该能够：

1. ✅ 手动打开 Easy Apply 筛选的搜索页面
2. ✅ 在单个职位页面上快速申请
3. ✅ 完全自动化地搜索和申请多个职位
4. ✅ 看到清晰的日志输出，便于调试
5. ✅ 获得友好的错误提示（中英文双语）

---

## 📝 测试记录

**测试日期**：___________

**测试环境**：
- Chrome 版本：___________
- LinkedIn UI 版本：___________（可以从页面源代码中查看）

**测试结果**：

| 测试项 | 通过 | 失败 | 备注 |
|--------|------|------|------|
| UI 界面检查 | ☐ | ☐ | |
| 仅打开搜索页 | ☐ | ☐ | |
| 申请当前页面 | ☐ | ☐ | |
| 智能自动申请 | ☐ | ☐ | |

**遇到的问题**：
___________________________________________
___________________________________________
___________________________________________

**解决方案**：
___________________________________________
___________________________________________
___________________________________________

---

**下一步行动**：

如果所有测试通过：
- [ ] 更新 README.md
- [ ] 准备发布新版本

如果有测试失败：
- [ ] 记录详细的错误信息
- [ ] 查看相关日志
- [ ] 参考 REFACTORED_GUIDE.md 中的调试方法
- [ ] 必要时回滚代码或进一步修复
