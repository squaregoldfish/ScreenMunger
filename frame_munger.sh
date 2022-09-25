#!/bin/bash

pipenv --bare run python -W ignore frame_munger.py "$1"
