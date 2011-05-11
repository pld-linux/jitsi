#!/bin/sh
set -e

# set JAVA_HOME from jpackage-utils if available
if [ ! -f /usr/share/java-utils/java-functions ]; then
	echo >&2 "jpackage-utils not found."
	exit 1
fi
. /usr/share/java-utils/java-functions

LIBDIR=/usr/lib/jitsi
APPDIR=/usr/share/jitsi
MAIN_CLASS=net.java.sip.communicator.launcher.SIPCommunicator

for jar in $APPDIR/lib/*.jar; do
	CLASSPATH=$CLASSPATH:$jar
done
for jar in sc-launcher.jar util.jar; do
	CLASSPATH=$CLASSPATH:$APPDIR/sc-bundles/$jar
done

# extra JVM options
OPTIONS="\
	-Djna.library.path=$LIBDIR \
	-Djava.library.path=$LIBDIR \
	-Dfelix.config.properties=file:$APPDIR/lib/felix.client.run.properties \
	-Djava.util.logging.config.file=$APPDIR/lib/logging.properties \
"

run "$@"
