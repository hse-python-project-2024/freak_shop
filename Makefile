.ONESHELL:

PYTHON_SERVER = ./server/venv/bin/python3
PIP_SERVER = ./server/venv/bin/pip

PYTHON_CLIENT = ./client/venv/bin/python3
PIP_CLIENT = ./client/venv/bin/pip


server_env:
	python3 -m venv server/venv
	chmod +x server/venv/bin/activate
	. ./server/venv/bin/activate

prepare_the_server: server_env
	$(PIP_SERVER) install -r server/requirements.txt
	$(PYTHON_SERVER) -m grpc_tools.protoc -I protos --python_out=server --grpc_python_out=server protos/db.proto

venv_server: prepare_the_server
	. ./server/venv/bin/activate

run_server: venv_server
	$(PYTHON_SERVER) server/db_server.py

clean_server:
	rm -rf server/__pycache__
	rm -rf server/venv
	rm -rf server/db_pb2.py
	rm -rf server/db_pb2_grpc.py


client_env:
	python3 -m venv client/venv
	chmod +x client/venv/bin/activate
	. ./client/venv/bin/activate

prepare_the_client: client_env
	$(PIP_CLIENT) install -r client/requirements.txt
	$(PYTHON_CLIENT) -m grpc_tools.protoc -I protos --python_out=client --grpc_python_out=client protos/db.proto

venv_client: prepare_the_client
	. ./client/venv/bin/activate


run_client: venv_client
	$(PYTHON_CLIENT) client/db_client.py


clean_client:
	rm -rf client/__pycache__
	rm -rf client/venv
	rm -rf client/db_pb2.py
	rm -rf client/db_pb2_grpc.py