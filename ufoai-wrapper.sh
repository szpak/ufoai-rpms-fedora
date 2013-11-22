#!/bin/sh

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK UFO:AI

confdir="$HOME/.ufoai/2.3.1/base"
conffile="$confdir/config.cfg"

if glxinfo | grep "renderer string" | grep Intel &> /dev/null ; then
    if [ -f $conffile ]; then
        if grep r_programs $conffile | grep 1 &> /dev/null ; then
            zenity --warning --text "You have GLSL Shaders enabled in your ufoai configuration file while using Intel OpenGL driver. This is known to crash the game or the X Server. It is highly recommended to turn the option off (Options => Video => GLSL Shaders)."
        fi
    else
        mkdir -p $confdir
        echo 'set r_programs "0" a' > $conffile
        zenity --info --text "Intel OpenGL driver detected. Disabling GLSL Shaders due to known problems (game or X Server crash)."
    fi
fi

exec ufo \
	+set fs_i18ndir /usr/share/locale \
	"\$@"
