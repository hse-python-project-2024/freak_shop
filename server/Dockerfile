FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r server/requirements.txt
RUN python -m grpc_tools.protoc -I protos --python_out=server --grpc_python_out=server protos/requests.proto

EXPOSE 50051

CMD ["python", "server/main.py"]
