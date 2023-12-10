# 2023 Corning AI challenge _ ITEM 1

## 🏴‍☠️ Large language models (LLMs)를 이용한 query engine

### Who are we
- HAI(Hanyang Tech Artificial Intelligence Studygroup)
- See https://github.com/HanyangTechAI

### 💡 Purpose of project:

With the vast amount of data available on the internet, it has become increasingly challenging for users to find relevant information quickly and efficiently. Traditional search engines rely on keywords and algorithms to rank search results, which can be limiting and often fail to provide accurate and relevant information. To address this issue, we’d like to develop a query engine that leverages the power of large language models to provide more accurate and efficient search results.

<br/>

### 🔑 Objectives:

The primary objective of this project is to develop a query engine that utilizes large language models to understand the intent behind a user's search query and provide more accurate and relevant search results (including references). The following are the specific objectives of this project.

   * LLMs should be run locally. (The maximum usage of VRAM should be less than 80 GB) 
   * Read/handle various file formats (ppt, excel, word, pdf, and text).
   * Need to extract the exact contents or units of a table contained in the document.
   * Developed model should be able to handle English (or both Korean and English) doucumnets.
   * Need to return a reference list of its contents after searching.

<br/>

### How to run
- Environments tested
    - Ubuntu 20.04(64bit)
    - NVIDIA RTX 3090 24GB
    - Docker, with nvidia runtime
        - https://docs.nvidia.com/ai-enterprise/deployment-guide-vmware/0.1.0/docker.html

- Step 0. Clone(or download) this repository
    - Then you will be able to see directories & files like:
```bash
.
├── neural_search
│   └── api
├── README.md
├── run.sh
├── shutdown.sh
└── streamlit_app
    └── src
        └── locales
            ├── en
            └── ko
```

- Step 1. Download model checkpoints
    - You should download model checkpoint binarys for LLM and embeddings.
    - Create a directory named `models`, and save checkpoints like:
```bash
./models
├── embedding_en
│   ├── 1_Pooling
│   │   └── config.json
│   ├── config.json
│   ├── config_sentence_transformers.json
│   ├── data_config.json
│   ├── modules.json
│   ├── pytorch_model.bin
│   ├── README.md
│   ├── sentence_bert_config.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   ├── train_script.py
│   └── vocab.txt
├── embedding_ko
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── README.md
│   ├── sentence_bert_config.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── vocab.txt
└── llm
    ├── config.json
    ├── generation_config.json
    ├── model-00001-of-00004.safetensors
    ├── model-00002-of-00004.safetensors
    ├── model-00003-of-00004.safetensors
    ├── model-00004-of-00004.safetensors
    ├── model.safetensors.index.json
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    └── tokenizer.json
```

- Step 2. Build & Run
    - Just start with shell script like `sh run.sh`.
        - If you are unable to run shell script, do: `chmod +x run.sh`
    - The system will automatically build & run each modules.
    - You can exec `shutdown.sh` to remove all containers.
        - Regardless of whether the entire system is shut down, the contents of the Vector database for search engines are not deleted.

