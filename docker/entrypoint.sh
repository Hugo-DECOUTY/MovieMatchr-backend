#!/bin/sh

retVal=-1;

# Attempt to connect and make migration
echo "==== Migration ====="

attempt=0

for attempt in $(seq 5)
do
  echo "Attempt $attempt"

  poetry run alembic upgrade head;
  retVal=$?;

  if [ $retVal = 0 ]
  then
    break;
  fi
done

if [ $attempt -ge 5 ]
then
  echo "Error while making migrations after ${attempt} attempts" 2>&1
  exit 1
fi

# Launch server
echo "===== Backend ====="
poetry run start;