export MODEL_CKPT_PATH="./models" # models 폴더의 경로를 입력해주세요
export LLM_PATH=$MODEL_CKPT_PATH/llm
export EMB_KO_PATH=$MODEL_CKPT_PATH/embedding_ko
export EMB_EN_PATH=$MODEL_CKPT_PATH/embedding_en

# Don't change except STREAMLIT_PORT
export LLM_PORT=40101
export STREAMLIT_PORT=40102
export SEARCH_PORT=40103
export HWP_PORT=40104

# LLM Serving(Huggingface TGI)
docker run -d \
    --name llm_serving \
    --restart unless-stopped \
    --gpus all \
    -p $LLM_PORT:80 \
    -v $LLM_PATH:/model \
    ghcr.io/huggingface/text-generation-inference:1.1.1 \
    --model-id /model \
    --dtype bfloat16 \
    --max-input-length 3072 \
    --max-total-tokens 4096 \
    --hostname 0.0.0.0 \
    --port 80 \
    --rope-scaling dynamic

# Neural Search Engine
docker build -t neural_search:0.1.0 \
    -f ./neural_search/Dockerfile \
    ./neural_search
docker run -d \
    --name neural_search \
    --restart unless-stopped \
    --gpus all \
    -p $SEARCH_PORT:80 \
    -v $EMB_EN_PATH:/embedding_en \
    -v $EMB_KO_PATH:/embedding_ko \
    -v ./chroma:/chroma \
    neural_search:0.1.0

# HWP to text converter
docker run -d \
    --name hwp-converter \
    --restart unless-stopped \
    -p $HWP_PORT:80 \
    vkehfdl1/hwp-converter-api:1.0.0

# Streamlit user interface
docker build -t streamlit_app:0.1.0 \
    -f ./streamlit_app/Dockerfile \
    ./streamlit_app
docker run -d \
    --name streamlit_app \
    --restart unless-stopped \
    -e STREAMLIT_SERVER_PORT=$STREAMLIT_PORT \
    -v ./files:/files \
    -v ./webpages:/webpages \
    --net host \
    streamlit_app:0.1.0
