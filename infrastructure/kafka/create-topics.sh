#!/bin/bash
set -euo pipefail

BOOTSTRAP=kafka_broker:9092

create() {
  /opt/kafka/bin/kafka-topics.sh --bootstrap-server "$BOOTSTRAP" \
    --create --if-not-exists --topic "$1" --partitions "$2" --replication-factor 1 "${@:3}"
}

create cdc.public.users 4
create cdc.public.posts 4
/opt/kafka/bin/kafka-topics.sh --bootstrap-server "$BOOTSTRAP" --list