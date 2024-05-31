.ONESHELL:

PYTHON_SERVER = ./server/venv/bin/python3
PIP_SERVER = ./server/venv/bin/pip

PYTHON_CLIENT = ./client/venv/bin/python3
PIP_CLIENT = ./client/venv/bin/pip


server_env:
	python3 -m venv server/venv
	chmod +x server/venv/bin/activate
	. ./server/venv/bin/activate
	$(PIP_SERVER) install -r server/requirements.txt


prepare_server: server_env
	$(PYTHON_SERVER) -m grpc_tools.protoc -I protos --python_out=server --grpc_python_out=server protos/requests.proto

run_server:
	. ./server/venv/bin/activate
	$(PYTHON_SERVER) server/main.py

drop_and_restore_data_base: server_env
	$(PYTHON_SERVER) server/db_prepare.py

clean_server:
	rm -rf server/__pycache__
	rm -rf server/venv
	rm -rf server/requests_pb2.py
	rm -rf server/requests_pb2_grpc.py


client_env:
	python3 -m venv client/venv
	chmod +x client/venv/bin/activate
	. ./client/venv/bin/activate

prepare_client: client_env
	$(PIP_CLIENT) install -r client/requirements.txt
	$(PYTHON_CLIENT) -m grpc_tools.protoc -I protos --python_out=client --grpc_python_out=client protos/requests.proto

venv_client:
	. ./client/venv/bin/activate


run_client: venv_client
	$(PYTHON_CLIENT) client/freak_shop.py


clean_client:
	rm -rf client/__pycache__
	rm -rf client/venv
	rm -rf client/requests_pb2.py
	rm -rf client/requests_pb2_grpc.py

test_client:
	PYTHONPATH=$(PWD)/client $(PYTHON_CLIENT) -m client.tests.test_view_model

end_to_end_requests:
	PYTHONPATH=$(PWD)/client $(PYTHON_CLIENT) -m client.tests.end_to_end_requests

test_server:
	PYTHONPATH=$(PWD)/server $(PYTHON_SERVER) -m server.tests.test_deck

test_server_requests:
	PYTHONPATH=$(PWD)/server $(PYTHON_SERVER) -m server.tests.test_requests
