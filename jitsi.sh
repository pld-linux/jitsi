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

cd "$APPDIR"

for jar in lib/*.jar; do
	CLASSPATH=$CLASSPATH:$jar
done
for jar in sc-launcher.jar util.jar; do
	CLASSPATH=$CLASSPATH:sc-bundles/$jar
done

# extra options
OPTIONS="\
	-Djna.library.path=$LIBDIR \
	-Djava.library.path=$LIBDIR \
	-Dfelix.config.properties=file:lib/felix.client.run.properties \
	-Djava.util.logging.config.file=lib/logging.properties \
"

# set add LIBPATH to LD_LIBRARY_PATH for any sc natives (e.g. jmf .so's)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIBDIR

run "$@"
