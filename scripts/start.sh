#!/bin/bash

set -exuo pipefail

cd $(dirname "$0")/..

export OPENAI_API_KEY=${OPENAI_API_KEY:-"ExampleKey"}

uv run python ./main.py
