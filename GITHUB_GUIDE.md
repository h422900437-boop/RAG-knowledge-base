# 📤 GitHub 发布指南

按照这个步骤将项目发布到 GitHub，分享给其他人。

## 🔑 1. 创建 GitHub Repository

### 在 GitHub 上创建新仓库
1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `RAG-knowledge-base`
   - **Description**: "AI HR Assistant - Retrieval-Augmented Generation System"
   - **Visibility**: Public（可公开访问）
   - **Initialize**: 不勾选（我们已有代码）

3. 点击 "Create repository"

## 📝 2. 本地初始化 Git（如果还没初始化）

```bash
cd /Users/huangguowei/Desktop/RAG-knowledge-base

# 检查是否已初始化
git status

# 如果没初始化，执行：
git init
git add .
git commit -m "Initial commit: RAG knowledge base with multimodal support"
```

## 🔗 3. 添加远程仓库

```bash
# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/RAG-knowledge-base.git

# 验证
git remote -v
```

## 📤 4. 推送到 GitHub

```bash
# 重命名 branch（如需要）
git branch -M main

# 推送
git push -u origin main
```

## ✅ 5. 验证上传

访问 `https://github.com/YOUR_USERNAME/RAG-knowledge-base`，应该能看到你的代码。

## 📋 6. 项目文件清单

确保这些文件都推送上去了：

```
✅ README.md                          # 项目说明
✅ requirement.txt                    # 依赖列表
✅ .gitignore                         # Git 忽略文件
✅ backend/
   ├── main.py                       # FastAPI 应用
   ├── rag_core.py                   # RAG 核心
   ├── file_extractors.py            # 多模态提取器
   └── test_*.py                     # 测试脚本
✅ frontend/
   └── app.py                        # Streamlit UI
✅ data/
   └── company_policies.txt          # 示例数据
✅ SETUP_GUIDE.md                    # 安装指南
✅ MULTIMODAL_IMPLEMENTATION.md       # 功能说明
✅ STREAMING_DEBUG.md                # 流式优化说明
✅ DEEPSEEK_STREAMING_FIX.md         # DeepSeek 说明
```

## 🚫 7. 重要：不要上传的文件

这些文件会被 `.gitignore` 自动忽略（无需手动删除）：

```
❌ .venv/                            # 虚拟环境
❌ chroma_db/                        # 向量数据库
❌ data/                             # 临时上传文件
❌ __pycache__/                      # Python 缓存
❌ *.log                             # 日志文件
```

验证：
```bash
git status  # 应该不显示上面这些文件
```

## 👥 8. 分享给别人

### 方式 1：直接分享 GitHub 链接
```
https://github.com/YOUR_USERNAME/RAG-knowledge-base
```

### 方式 2：让别人 Clone
他们可以这样使用：
```bash
git clone https://github.com/YOUR_USERNAME/RAG-knowledge-base.git
cd RAG-knowledge-base
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
# 按 README.md 说明启动
```

## 📝 9. 后续更新代码

每次修改后：

```bash
# 查看改动
git status

# 添加所有改动
git add .

# 提交
git commit -m "描述你的改动"

# 推送到 GitHub
git push
```

## 🏷️ 10. 添加 Tags（版本标记）

发布新版本时：

```bash
# 创建 tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送 tag
git push origin v1.0.0

# 或推送所有 tags
git push origin --tags
```

## 📊 11. GitHub 最佳实践

### 好的 Commit 信息
```
✅ "Add multimodal document support (PDF, Word, Excel)"
✅ "Fix streaming response latency issue"
✅ "Improve error handling for file extraction"
```

### 不好的 Commit 信息
```
❌ "update"
❌ "fix bug"
❌ "changes"
```

## 🔐 12. 保护敏感信息

**绝对不要上传：**
- API keys 或 tokens
- 数据库密码
- 个人信息

**做法：**
- 将敏感信息放在环境变量中
- 在 README 中说明需要设置 `DEEPSEEK_TOKEN`
- 使用 `.env` 文件管理本地开发配置（已在 .gitignore 中）

## 📚 13. 添加 Topics

在 GitHub 页面右侧添加 Topics（标签）：
- `rag`
- `llm`
- `deepseek`
- `streamlit`
- `fastapi`
- `knowledge-base`

这样别人更容易找到你的项目。

## 💡 14. 优化项目页面

### 添加 Badge（徽章）

在 README.md 开头添加：
```markdown
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
```

### 添加贡献指南

创建 `CONTRIBUTING.md`：
```markdown
# 贡献指南

欢迎提交 Issues 和 Pull Requests！

## 如何贡献
1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. Commit 改动 (`git commit -m 'Add some AmazingFeature'`)
4. Push 到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request
```

## 📞 15. 常见问题

### Q: 如何更新代码？
```bash
git add .
git commit -m "你的改动说明"
git push
```

### Q: 如何回滚？
```bash
git log  # 查看历史
git revert <commit-hash>
git push
```

### Q: 别人如何为我的项目做贡献？
1. 他们 Fork 你的仓库
2. 在自己的 Fork 上做改动
3. 提交 Pull Request
4. 你审核后 Merge

### Q: 如何处理 Pull Request？
1. 在 GitHub 页面查看 PR
2. Review 代码
3. Comment 或 Approve
4. Merge 或 Close

## 🎉 完成！

现在你的项目已经在 GitHub 上了，任何人都可以：
- ⭐ Star 你的项目（表示喜欢）
- 🔀 Fork 项目（复制到自己的账户）
- 🐛 提交 Issues（报告 bug）
- 🚀 提交 Pull Requests（贡献代码）

---

**需要帮助？**
- GitHub 帮助文档：https://docs.github.com
- Git 教程：https://git-scm.com/book/en/v2
