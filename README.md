# Blockchain_Lab_01

## Thành viên tham gia

* 21127077  -   Huỳnh Đăng Khoa

* 21127311  -   Trần Quốc Tuấn

* 21127409  -   Nguyễn Minh Quốc

* 21127570  -   Trần Minh Đạt

* 21127658  -   Trần Hà Minh Nhật

## BUILD PROTO

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Raft.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. RaftManager.proto
```

* windows

```
cmd ./BuildProto.bat
```

## Run Node Manager

Chỉ chạy node manager

```
python RaftManager.py
```