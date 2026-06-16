FROM debezium/connect:2.7.3.Final

USER root 

RUN curl -L -O https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-converter/7.5.0/kafka-connect-avro-converter-7.5.0.jar \
    && mv kafka-connect-avro-converter-7.5.0.jar /kafka/connect/debezium-connector-postgres/

USER 1001