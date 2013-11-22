#!/bin/sh

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK UFO:AI

exec uforadiant "\$@"
