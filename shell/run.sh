#!/bin/bash

POD_NAME=$1
EXCLUDE_POD_NAME=$2

POD_ID=$(kubectl get po | awk '{print $1}' | grep -v NAME | grep -v Terminating | grep ${POD_NAME})

if [[ $EXCLUDE_POD_NAME ]]; then
    POD_ID=$(kubectl get po | awk '{print $1}' | grep -v NAME | grep -v Terminating | grep ${POD_NAME} | grep -v ${EXCLUDE_POD_NAME})
fi

kubectl exec -it ${POD_ID} -- python3 -u main.py