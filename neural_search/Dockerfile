FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime as base
# Create a working directory
RUN mkdir /app

# Add requirements file
WORKDIR /app/
ADD requirements.txt /app/

# Install requirements
RUN pip3 install -r requirements.txt

ENV CHROMADB_PATH "/chroma"
ENV EMBEDDING_MODEL_EN "/embedding_en"
ENV EMBEDDING_MODEL_KO "/embedding_ko"

# Move required resources                     
COPY ./api /app/api/

# Run FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
