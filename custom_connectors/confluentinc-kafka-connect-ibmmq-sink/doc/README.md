# Kafka Connect Suite of JMS Sink Connectors

This project provides a suite of connectors that sink records from Apache Kafka to 
various JMS brokers.

## Supported JMS Brokers

* Generic JMS (configured via JNDI)
* ActiveMQ
* IBM MQ
* Solace

## Future JMS Brokers

* TIBCO EMS

## Development

The core of this suite is implemented in the `kafka-connect-jms-common` module. 

Each connector has to extend a few abstractions to get going -

* `JmsConnection`
    * Implement `createConnectionFactory(JmsConnectorConfig config)`
    * Implement `isOpen()`
* `BaseJmsSinkConnector`
    * Supply a subclass of the `io.confluent.connect.jms.JmsConnectorConfig`
* `BaseJmsSinkTask`:
    * Supply a subclass of the `io.confluent.connect.jms.JmsConnectorConfig`
    * Configure an instance of your `JmsConnection` implementation
    * Configure an instance of a `MessageBuilder` _(optional)_
        * Default: `DefaultMessageBuilder`

See `kafka-connect-jms-sink`, `kafka-connect-activemq-sink`, or `kafka-connect-ibmmq-sink` for examples of this.
