.ONESHELL:

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

server_env:
	python3 -m venv server/venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate

prepare_the_server: server_env
	$(PIP) install -r server/requirements.txt
	$(PYTHON) -m grpc_tools.protoc -I protos --python_out=server --grpc_python_out=server protos/db.proto

venv_server: prepare_the_server
	. ./venv/bin/activate

run_server: venv_server
	$(PYTHON) server/db_server.py

clean_server:
	rm -rf server/__pycache__
	rm -rf server/venv
	rm -rf server/db_pb2.py
	rm -rf server/db_pb2_grpc.py


client_env:
	python3 -m venv client/venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate

prepare_the_client: client_env
	$(PIP) install -r client/requirements.txt
	$(PYTHON) -m grpc_tools.protoc -I protos --python_out=client --grpc_python_out=client protos/db.proto

venv_client: prepare_the_client
	. ./venv/bin/activate


run_client: venv_client
	$(PYTHON) client/db_client.py


clean_client:
	rm -rf client/__pycache__
	rm -rf client/venv
	rm -rf client/db_pb2.py
	rm -rf client/db_pb2_grpc.py