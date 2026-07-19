# 📸 添加演示截图指南

## 操作步骤

### 1. 创建 docs 文件夹
```bash
mkdir -p /Users/huangguowei/Desktop/RAG-knowledge-base/docs
```

### 2. 保存截图

**方式 A：从浏览器直接保存**
1. 打开应用 http://localhost:8501
2. 运行几个问题获得好的效果
3. 截图（Command + Shift + 4）
4. 保存为 `/Users/huangguowei/Desktop/RAG-knowledge-base/docs/demo.png`

**方式 B：用 Mac 截图工具**
1. 按 Command + Shift + 5
2. 截取应用窗口
3. 点击保存按钮
4. 选择 `docs` 文件夹，命名为 `demo.png`

### 3. 优化截图（可选）

为了让截图看起来更好：
1. 在问答中包含：
   - 一个用户问题（左边气泡）
   - AI 的流式响应（右边气泡）
   - "View Retrieved Sources" 展开的部分
   - 左侧上传文档的面板

2. 推荐的窗口大小：1400x900 像素

### 4. 验证

检查文件是否存在：
```bash
ls -lh /Users/huangguowei/Desktop/RAG-knowledge-base/docs/demo.png
```

应该显示类似：
```
-rw-r--r--  1 user  staff  256KB  Jul 19 14:30 demo.png
```

## 📋 README 已经更新

README.md 已经包含了这一行：
```markdown
![Corporate AI HR Assistant Demo](docs/demo.png)
```

所以只需要确保 `docs/demo.png` 文件存在即可。

## ✅ 完成清单

- [ ] 创建 `docs` 文件夹
- [ ] 保存演示截图为 `docs/demo.png`
- [ ] 验证文件存在
- [ ] 推送到 GitHub

## 🎯 完成后

当你推送到 GitHub 时：
```bash
git add docs/demo.png
git commit -m "Add demo screenshot"
git push
```

GitHub 上的 README 会自动显示这张截图！

## 💡 小贴士

- **图片大小**：建议 < 500KB，太大会影响加载速度
- **文件格式**：PNG 或 JPG 都可以
- **路径**：务必是相对路径 `docs/demo.png`（不是绝对路径）
