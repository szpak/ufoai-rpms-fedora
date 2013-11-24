#!/bin/sh

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK UFO:AI

confdir="$HOME/.ufoai/2.5-dev/base"
conffile="$confdir/config.cfg"

if glxinfo | grep "renderer string" | grep Intel &> /dev/null ; then
    if [ -f $conffile ]; then
        if grep r_programs $conffile | grep 1 &> /dev/null ; then
            zenity --warning --text "You have GLSL Shaders enabled in your ufoai configuration file while using Intel OpenGL driver. This can cause X Server crash on some cards. In that case turn the option off (Options => Video => GLSL Shaders)."
        fi
    else
        mkdir -p $confdir
        echo 'set r_programs "0" a' > $conffile
        zenity --info --text "Intel OpenGL driver detected. Disabling GLSL Shaders due to possible game or X Server crash."
    fi
fi

#Fix full screen mode in multi monitor environments - http://ufoai.org/forum/index.php/topic,7931.msg60347.html#msg60347 
SDL_VIDEO_FULLSCREEN_HEAD=0 exec ufo \
	+set fs_i18ndir /usr/share/locale \
	"\$@"
