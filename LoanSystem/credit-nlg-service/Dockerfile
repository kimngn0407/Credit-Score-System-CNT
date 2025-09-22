FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HUB_ENABLE_HF_TRANSFER=1 \
    TORCH_CUDA_ALLOC_CONF=max_split_size_mb:128

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip git gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python3.11 -m pip install --upgrade pip

WORKDIR /app

# Cài torch CUDA 12.1 trước
RUN python3.11 -m pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu121 \
  torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1

COPY requirements.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY llm_adapter ./llm_adapter

ENV BASE_MODEL=unsloth/gpt-oss-20b-unsloth-bnb-4bit
ENV ADAPTER_PATH=/app/llm_adapter
ENV GEN_MAX_NEW_TOKENS=400
ENV GEN_TEMPERATURE=0.2
ENV GEN_TOP_P=0.9
# Nếu muốn bật API key: docker run -e NLG_API_KEY=your-secret
# ENV NLG_API_KEY=

EXPOSE 8000
CMD ["python3.11", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
