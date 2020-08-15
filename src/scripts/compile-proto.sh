#!/bin/sh
bin/protoc -I=. --python_out=. ./chandra_bot_data_model.proto
