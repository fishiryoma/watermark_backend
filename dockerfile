# 使用輕量 Python 映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製依賴檔案
COPY requirements.txt .

# 安裝依賴，包括字型支援
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 複製應用程式碼
COPY ./app .

# 暴露端口
EXPOSE 5000

# 運行 Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]