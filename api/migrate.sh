#! /usr/bin/env bash

echo ""
echo "CREATING A NEW REVISION ... ..."
echo ""
alembic revision --autogenerate -m "${1}"
echo ""
echo "MIGRATING THE DB ... ..."
echo ""
alembic upgrade head
echo ""