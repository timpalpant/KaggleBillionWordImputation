#!/usr/bin/env bash

GPU_ID=0
DATA_DIR=../../data/
if [ ! -d $DATA_DIR ]; then
    echo "Data directory not found: $DATA_DIR"
    exit 1
fi

~/Documents/Workspace/caffe/build/tools/caffe train \
    -solver lstm_lm_solver.prototxt \
    -gpu $GPU_ID
