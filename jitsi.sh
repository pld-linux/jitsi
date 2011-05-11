#!/bin/sh
exec java \
	-Dfelix.config.properties=file:/usr/share/java/jitsi/lib/felix.client.run.properties \
	-Djava.util.logging.config.file=/usr/share/java/jitsi/lib/logging.properties \
	org.apache.felix.main.Main
