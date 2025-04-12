#! /usr/bin/env bash

# Start the App Server
uvicorn mspt.main:mspt_app --reload --host=0.0.0.0
