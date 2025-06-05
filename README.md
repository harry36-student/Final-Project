
# LM Studio ChatGPT WebApp

## 如何使用

1. 開啟 LM Studio，載入模型並啟用 API Server（OpenAI API 格式，預設 port 是 1234）。
2. 安裝 Python 套件：
   ```bash
   pip install fastapi uvicorn requests
   ```
3. 執行後端：
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. 用瀏覽器開啟 `index.html` 開始聊天！
