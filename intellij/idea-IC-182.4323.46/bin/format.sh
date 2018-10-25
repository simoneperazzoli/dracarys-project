#!/bin/sh
# ------------------------------------------------------
# IntelliJ IDEA formatting script.
# ------------------------------------------------------

IDE_BIN_HOME="${0%/*}"
exec "$IDE_BIN_HOME/idea.sh" format "$@"
