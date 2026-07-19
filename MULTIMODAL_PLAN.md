# 多模态上传支持 - 完整规划

## 📌 目标
支持用户上传多种文件格式（PDF、Word、Excel、图片等），自动提取文本，存入向量数据库。

## 🎯 当前状态
```
支持：✅ .txt 纯文本
不支持：❌ PDF、Word、Excel、图片、PPT 等
```

## 🔄 多模态处理流程

```
用户上传文件
    ↓
识别文件类型
    ↓
调用对应的提取器
    ├─ .pdf → PDFPlumber/PyPDF
    ├─ .docx → python-docx
    ├─ .xlsx → openpyxl/pandas
    ├─ .pptx → python-pptx
    ├─ .jpg/.png → OCR (Tesseract/EasyOCR)
    └─ .txt → 直接读取
    ↓
提取纯文本内容
    ↓
分块处理 (RecursiveCharacterTextSplitter)
    ↓
生成向量嵌入
    ↓
存入 Chroma 数据库
    ↓
返回成功信息
```

## 📋 具体要改的代码

### 1. **后端依赖库** (requirement.txt)
需要添加：
```
pypdf                 # PDF 处理
python-docx          # Word (.docx) 处理
openpyxl             # Excel 处理
python-pptx          # PowerPoint 处理
easyocr              # 图片 OCR 识别（可选，重）
pillow               # 图片处理
```

### 2. **新建文件提取模块** (backend/file_extractors.py)
```python
class FileExtractor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """根据文件类型，自动调用对应提取器"""
        
# 各种提取器类：
class TextExtractor:      # .txt
    extract() -> str

class PDFExtractor:       # .pdf
    extract() -> str

class DocxExtractor:      # .docx
    extract() -> str

class ExcelExtractor:     # .xlsx
    extract() -> str

class PPTExtractor:       # .pptx
    extract() -> str

class ImageExtractor:     # .jpg/.png
    extract() -> str (使用 OCR)
```

### 3. **修改后端主文件** (backend/main.py)
```python
# 修改 upload_endpoint：
- 识别文件类型
- 调用 FileExtractor 提取文本
- 传给 engine_instance.upload_document()
- 返回提取结果信息
```

### 4. **修改 RAG 引擎** (backend/rag_core.py)
```python
# upload_document() 方法改进：
- 支持接收已提取的纯文本（不需要再读文件）
- 完善元数据（文件类型、提取方式等）
- 添加提取失败的错误处理
```

### 5. **改进前端** (frontend/app.py)
```python
# 修改文件上传器：
- st.file_uploader() 支持多种类型
- 显示正在处理的文件类型
- 显示提取进度/结果
- 友好的错误提示
```

### 6. **新增测试脚本** (backend/test_multimodal.py)
```python
# 测试各种文件格式的上传和提取
# 验证提取的文本质量
```

## 🎯 实现细节

### 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| 完整方案（所有格式） | 功能完善，用户体验好 | 依赖多，维护复杂 | ⭐⭐⭐⭐⭐ |
| 轻量方案（PDF+txt） | 简单快速，覆盖 80% 需求 | 不支持表格数据 | ⭐⭐⭐⭐ |
| 极简方案（仅 txt） | 最简单 | 功能不足 | ⭐⭐ |

**建议：完整方案** - 多花点时间但功能完整

## 📂 文件结构改动

```
backend/
├── main.py                    ✏️ 改：upload_endpoint()
├── rag_core.py               ✏️ 改：upload_document()
├── file_extractors.py         ✨ 新：多模态提取器
└── test_multimodal.py         ✨ 新：测试脚本

frontend/
└── app.py                     ✏️ 改：文件上传器配置

requirement.txt               ✏️ 改：添加依赖库

文档：
└── MULTIMODAL_IMPLEMENTATION.md ✨ 新：实现细节文档
```

## 🔧 关键实现问题

### 问题 1：大文件处理
**问题：** PDF/图片文件可能很大，一次加载会很慢
**解决：** 
- 限制文件大小（如 50MB）
- 对 PDF 分页处理
- 显示处理进度

### 问题 2：表格数据
**问题：** Excel/PDF 表格如何保留格式信息？
**方案：** 
- 简单方案：转成文本，每行作为一个 chunk
- 高级方案：用 Markdown 格式保留表格结构

### 问题 3：图片 OCR
**问题：** EasyOCR 很重（需要下载模型）
**方案：** 
- 可选功能（提前给用户选择）
- 或改用轻量级方案（如 PaddleOCR）
- 或 API 调用（如 Google Vision）

### 问题 4：元数据丢失
**问题：** 从 Word/PDF 提取后，丢失原始结构信息
**解决：** 
- 保存原文件名、大小、修改时间
- 记录页码（对 PDF）、页数（对 Word）
- 记录提取方式和时间戳

## ✨ 优雅设计建议

### 1. 插件式架构
```python
# 易于扩展新的提取器
extractors = {
    '.pdf': PDFExtractor(),
    '.docx': DocxExtractor(),
    '.xlsx': ExcelExtractor(),
    '.txt': TextExtractor(),
    '.png': ImageExtractor(),
    '.jpg': ImageExtractor(),
}

extractor = extractors.get(file_ext)
if extractor:
    text = extractor.extract(file_path)
```

### 2. 错误恢复
```python
try:
    text = extractor.extract(file_path)
except Exception as e:
    # 记录错误，但不中断
    fallback_text = extract_fallback(file_path)
    return {"status": "partial", "error": str(e)}
```

### 3. 进度反馈
```python
# 前端显示：
"正在处理 document.pdf..."
"已提取 5/100 页..."
"正在分块处理..."
```

## 📊 依赖库详细说明

| 库 | 版本 | 用途 | 大小 | 说明 |
|---|------|------|------|------|
| pypdf | >=3.0 | PDF 文本提取 | 小 | 纯 Python，无需外部依赖 |
| python-docx | >=0.8 | Word 文本提取 | 小 | 支持 .docx |
| openpyxl | >=3.0 | Excel 表格提取 | 小 | 支持 .xlsx |
| pandas | >=1.3 | Excel 高级操作 | 中 | 可选，用于更好的表格处理 |
| python-pptx | >=0.6 | PowerPoint 提取 | 小 | 支持 .pptx |
| pillow | >=9.0 | 图片基础处理 | 中 | 已被很多库依赖 |
| easyocr | >=1.6 | OCR 识别 | 大 | 可选，首次使用会下载模型（~700MB） |

**推荐先装：** pypdf, python-docx, openpyxl, python-pptx, pillow
**可选装：** easyocr（用户需要时再装）

## 🚀 实现步骤建议

```
第 1 步：创建 file_extractors.py
  └─ 实现 TextExtractor（已有）
  └─ 实现 PDFExtractor
  └─ 实现 DocxExtractor
  └─ 实现 ExcelExtractor
  └─ 实现 PPTExtractor
  └─ 实现通用 FileExtractor 类

第 2 步：更新 requirement.txt
  └─ 添加必需的库

第 3 步：改进 backend/main.py
  └─ 修改 upload_endpoint()
  └─ 使用 FileExtractor

第 4 步：改进 backend/rag_core.py
  └─ upload_document() 支持预提取文本

第 5 步：改进 frontend/app.py
  └─ 支持多种文件类型上传
  └─ 显示更详细的上传信息

第 6 步：测试
  └─ 创建 test_multimodal.py
  └─ 手动测试各种格式
```

## 🎨 前端 UI 改进

```python
# 当前：
uploaded_file = st.file_uploader("Choose a policy document (.txt)", type=["txt"])

# 改进后：
uploaded_file = st.file_uploader(
    "📄 Upload document",
    type=["txt", "pdf", "docx", "xlsx", "pptx", "jpg", "png"],
    help="Supported: TXT, PDF, Word, Excel, PowerPoint, Images"
)

if uploaded_file:
    file_info = f"""
    📋 File: {uploaded_file.name}
    📊 Size: {uploaded_file.size / 1024:.1f} KB
    📅 Type: {uploaded_file.type}
    """
    st.info(file_info)
```

## ✅ 完成清单

- [ ] 创建 file_extractors.py 模块
- [ ] 实现各文件格式提取器
- [ ] 更新 requirement.txt
- [ ] 修改 backend/main.py
- [ ] 修改 backend/rag_core.py
- [ ] 修改 frontend/app.py
- [ ] 创建测试脚本
- [ ] 编写使用文档

---

## 📝 总结

**思路：** 
1. 创建统一的文件提取接口
2. 为每种文件格式实现提取器
3. 后端自动识别文件类型调用对应提取器
4. 提取后的文本走现有 RAG 流程
5. 前端支持多种文件上传

**难度：** ⭐⭐⭐（中等）

**优先级：**
- 必做：PDF、Word、Excel
- 可做：PPT
- 可选：图片 OCR

现在你看一下这个方案是否满意？需要我按这个思路改代码吗？
