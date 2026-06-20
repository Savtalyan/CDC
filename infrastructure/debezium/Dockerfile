FROM debezium/connect:2.7.3.Final

USER root

ENV CONFLUENT_VERSION=7.5.0

RUN curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/kafka-connect-avro-converter-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-converter/${CONFLUENT_VERSION}/kafka-connect-avro-converter-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/kafka-connect-avro-data-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-data/${CONFLUENT_VERSION}/kafka-connect-avro-data-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/kafka-avro-serializer-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/kafka-avro-serializer/${CONFLUENT_VERSION}/kafka-avro-serializer-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/kafka-schema-serializer-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/kafka-schema-serializer/${CONFLUENT_VERSION}/kafka-schema-serializer-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/kafka-schema-registry-client-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/${CONFLUENT_VERSION}/kafka-schema-registry-client-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/common-config-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/common-config/${CONFLUENT_VERSION}/common-config-${CONFLUENT_VERSION}.jar \
 && curl --fail -sS -L -o /kafka/connect/debezium-connector-postgres/common-utils-${CONFLUENT_VERSION}.jar \
      https://packages.confluent.io/maven/io/confluent/common-utils/${CONFLUENT_VERSION}/common-utils-${CONFLUENT_VERSION}.jar

USER 1001