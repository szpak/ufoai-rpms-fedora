#TODO: remove in 2.5 final
%define		devModifier	-dev

Name:		ufoai
Version:	2.5
Release:	0.1.2013117git%{?dist}
Summary:	UFO: Alien Invasion

Group:		Amusements/Games
License:	GPLv2+
URL:		http://ufoai.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}%{devModifier}-source.tar.bz2
Source1:	%{name}-wrapper.sh
Source2:	uforadiant-wrapper.sh
Patch0:		ufoai-2.5-desktop-files.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	desktop-file-utils curl-devel freealut-devel gettext
BuildRequires:	libjpeg-devel libogg-devel libpng-devel
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libXxf86dga-devel libXxf86vm-devel
BuildRequires:	lua-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
# in RPMFusion-free; substituted with libtheora-devel
#BuildRequires:	xvidcore-devel

Requires:	opengl-games-utils
Requires:	%{name}-common = %{version}
Requires:	%{name}-data = %{version}
Requires:	%{name}-data-server = %{version}


%package common
Summary:	UFO: Alien Invasion shared files


# Temporarily disabled - tetex-latex needs hundreds of sub packages
#%package doc
#Summary:	UFO: Alien Invasion user manual
#Group:		Documentation
#License:	GFDL
#BuildRequires:	tetex-latex


%package server
Summary:	UFO: Alien Invasion dedicated server
Requires:	%{name}-data-server = %{version}
Requires:	%{name}-common = %{version}


%package tools
Summary:	UFO: Alien Invasion developer tools
Group:		Development/Tools


%package uforadiant
Summary:	UFO: Alien Invasion map editor
Group:		Development/Tools
BuildRequires:	gtkglext-devel
BuildRequires:	gtksourceview2-devel
Requires:	%{name}-tools


%description
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment. You are in command of a small special unit which
has been founded to face the alien strike force. To be successful on
the long run, you will also have to have a research team study the
aliens and their technologies in order to learn as much as possible
about their technology, their goals and the aliens themselves.


%description common
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment.

This package contains files common both to the client and the server.


# Temporarily disabled - tetex-latex needs hundreds of sub packages
#%description doc
#UFO: ALIEN INVASION is a strategy game featuring tactical combat
#against hostile alien forces which are about to infiltrate earth at
#this very moment.
#
#This package contains the user manual for the game.


%description server
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment.

This package contains the UFO:AI dedicated server.


%description tools
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment.

This package contains the developer tools.


%description uforadiant
UFO: ALIEN INVASION is a strategy game featuring tactical combat
against hostile alien forces which are about to infiltrate earth at
this very moment.

This package contains the UFORadiant map editor.


%prep
%setup -q -n %{name}-%{version}%{devModifier}-source
# ufoai-2.5-desktop-files.patch - fix executable and icon names
%patch0 -p1
sed -i -e "/maps.mk/d" Makefile
sed -i -e "/models.mk/d" Makefile
# we don't use any of the installers
#sed -i -e "/install.mk/d" Makefile
#TODO: Disable also "mojo install"
#TODO: Add license file also in other packages - always GPLv2+?

%build
# don't use %%configure, UFOAI doesn't like default configure options
./configure \
	--disable-dependency-tracking \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--datadir=%{_datadir}/%{name} \
	--libdir=%{_libdir}/%{name} \
	--localedir=%{_datarootdir}/locale \
	--enable-ufoded \
	--enable-uforadiant \
	--enable-ufo2map \
	--enable-ufomodel \
	--enable-release

make %{?_smp_mflags}
make %{?_smp_mflags} lang

# Temporarily disabled - tetex-latex needs hundreds of sub packages
# build documentation
#make %{?_smp_mflags} manual

# build uforadiant
make %{?_smp_mflags} uforadiant


%install
rm -rf %{buildroot}
# we don't use
#   make install_exec DESTDIR=%%{buildroot}
# simply because it does not work ...

### client
install -D -m 0755 ufo %{buildroot}%{_bindir}/ufo
install -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}
install -D -m 0644 debian/ufo.6 %{buildroot}%{_mandir}/man6/ufo.6
mkdir -p -m 0755 %{buildroot}%{_datadir}/locale
cp -pr base/i18n/* %{buildroot}%{_datadir}/locale/
%find_lang %{name}
install -D -m 0644 debian/%{name}.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm
desktop-file-install --dir=%{buildroot}%{_datadir}/applications debian/ufoai.desktop

### install common
install -D -m 0755 base/game.so %{buildroot}%{_libdir}/%{name}/game.so

## install doc
mkdir -p -m 0755 %{buildroot}%{_docdir}/%{name}-%{version}
# Temporarily disabled - tetex-latex needs hundreds of sub packages
#cp -pr README COPYING src/docs/tex/*.pdf %{buildroot}%{_docdir}/%{name}-%{version}/
cp -pr README COPYING %{buildroot}%{_docdir}/%{name}-%{version}/

### install server
install -D -m 0755 ufoded %{buildroot}%{_bindir}
install -D -m 0644 debian/ufoded.6 %{buildroot}%{_mandir}/man6/ufoded.6
install -D -m 0644 debian/ufoded.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/ufoded.xpm
desktop-file-install --dir=%{buildroot}%{_datadir}/applications debian/ufoded.desktop

### install tools
install -D -m 0755 ufo2map %{buildroot}%{_bindir}
install -D -m 0644 debian/ufo2map.6 %{buildroot}%{_mandir}/man6/ufo2map.6
install -D -m 0755 ufomodel %{buildroot}%{_bindir}
install -D -m 0755 ufoslicer %{buildroot}%{_bindir}
install -D src/tools/blender/md2tag_export.py %{buildroot}%{_datadir}/%{name}/tools/md2tag_export.py
## not available in our sources
##install -D -m 0644 contrib/scripts/bashcompletion/ufo2map %%{buildroot}%%{_sysconfdir}/bash_completion.d/ufo2map
##install -D -m 0644 contrib/scripts/bashcompletion/ufomodel %%{buildroot}%%{_sysconfdir}/bash_completion.d/ufomodel

### install uforadiant
install -D -m 0755 radiant/uforadiant %{buildroot}%{_bindir}/uforadiant
install -p -m 0755 %{SOURCE2} %{buildroot}%{_bindir}
install -D -m 0644 debian/uforadiant.6 %{buildroot}%{_mandir}/man6/uforadiant.6
mkdir -p -m 0755 %{buildroot}%{_datadir}/%{name}/radiant
cp -p radiant/*.xml %{buildroot}%{_datadir}/%{name}/radiant/
cp -p radiant/mapdef.template %{buildroot}%{_datadir}/%{name}/radiant/
cp -pr radiant/bitmaps %{buildroot}%{_datadir}/%{name}/radiant
cp -pr radiant/prefabs %{buildroot}%{_datadir}/%{name}/radiant
cp -pr radiant/sourceviewer %{buildroot}%{_datadir}/%{name}/radiant
cp -pr radiant/i18n/* %{buildroot}%{_datadir}/locale/
%find_lang uforadiant
install -D -m 0644 debian/uforadiant.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/uforadiant.xpm
desktop-file-install --dir=%{buildroot}%{_datadir}/applications debian/uforadiant.desktop

%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%post server
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%post uforadiant
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun server
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun uforadiant
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
# we need to use full path so %%doc does not the cleanup
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/COPYING
%{_bindir}/ufo
%{_bindir}/ufoai-wrapper.sh
%{_datadir}/applications/ufoai.desktop
%{_datadir}/icons/hicolor/32x32/apps/ufoai.xpm
%doc %{_mandir}/man6/ufo.6*


%files common
%defattr(-,root,root,-)
%{_libdir}/%{name}/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/


# Temporarily disabled - tetex-latex needs hundreds of sub packages
#%files doc
#%defattr(-,root,root,-)
#%dir %{_docdir}/%{name}-%{version}
#%lang(en) %doc %{_docdir}/%{name}-%{version}/ufo-manual_EN.pdf


%files server
%defattr(-,root,root,-)
%{_bindir}/ufoded
%{_datadir}/applications/ufoded.desktop
%{_datadir}/icons/hicolor/32x32/apps/ufoded.xpm
%doc %{_mandir}/man6/ufoded.6*


%files tools
%defattr(-,root,root,-)
%{_bindir}/ufo2map
%{_bindir}/ufomodel
%{_bindir}/ufoslicer
%dir %{_datadir}/%{name}/
# not available in our sources
#%%{_sysconfdir}/bash_completion.d/
%doc %{_mandir}/man6/ufo2map.6*
%{_datadir}/%{name}/tools/


%files uforadiant -f uforadiant.lang
%defattr(-,root,root,-)
%{_bindir}/uforadiant
%{_bindir}/uforadiant-wrapper.sh
%{_datadir}/applications/uforadiant.desktop
%{_datadir}/icons/hicolor/32x32/apps/uforadiant.xpm
%{_datadir}/%{name}/radiant/
%doc %{_mandir}/man6/uforadiant.6*


%changelog
* Sun Nov 24 2013 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 2.5-0.1.2013117git
- Update to 2.5-dev (doc package temporarily disabled)

* Fri Jun 29 2012 Karel Volny <kvolny@redhat.com> 2.4-1
- Version bump
- Changelog: http://ufoai.org/wiki/index.php/Changelog/2.4
- Fixed duplicate packaging of md2tag_export.py
- Added ufoslicer to -tools

* Tue May 15 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-5
- Fix FTBFS

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 17 2011 Karel Volny <kvolny@redhat.com> 2.3.1-2
- Fixes RPMFusion bug #1555 (dependency typo for uforadiant)
- Fixes uforadiant install paths
- Adds patch for appPath issue, see
  https://sourceforge.net/tracker/?func=detail&aid=3219962&group_id=157793&atid=805242

* Mon Mar 14 2011 Karel Volny <kvolny@redhat.com> 2.3.1-1
- Version bump
- Fixes RPMFusion bug #1546
- See the release annoucement for list of changes:
  http://ufoai.ninex.info/wiki/index.php/News/2010#UFO:_Alien_Invasion_2.3_released
- .spec cleanup
- Adds workaround for crash on Intel cards

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.3-2
- Rebuilt for gcc bug

* Tue Sep 14 2010 Karel Volny <kvolny@redhat.com> 2.3-1
- Version bump
- Fixes RPMFusion bug #1305
- Adjusted BuildRequires
- Split Radiant (the map editor), tools, server and common subpackages
- Install manpages and other goodies from debian subdirectory
- Removed ufoded wrapper, no longer needed

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.2.1-4
- rebuild for new F11 features

* Thu Dec 11 2008 Karel Volny <kvolny@redhat.com> 2.2.1-3
- Fixed unowned directories (bug #225)

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.2.1-2
- rebuild

* Mon Jun 09 2008 Karel Volny <kvolny@redhat.com> 2.2.1-1
- Version bump
- Fixes Livna bug #1931
- Configure with --enable-release

* Tue Feb 26 2008 Karel Volny <kvolny@redhat.com> 2.2-5
- Added patch to allow setting fs_libdir, fixes Livna bug #1882

* Tue Feb 19 2008 Karel Volny <kvolny@redhat.com> 2.2-4
- Changed BuildRequires of the doc subpackage to tetex-latex instead of tetex

* Mon Feb 18 2008 Karel Volny <kvolny@redhat.com> 2.2-3
- Fixed BuildRequires to include SDL_mixer-devel

* Mon Feb 04 2008 Karel Volny <kvolny@redhat.com> 2.2-2
- Merged in ufoai-doc as a subpackage
- Added gtk-update-icon-cache to %%post and %%postun

* Tue Jan 22 2008 Karel Volny <kvolny@redhat.com> 2.2-1
- Version bump
- Added BuildRequires: curl-devel
- Changed language file handling
- Use bundled icons
- Added ufoded wrapper and menu entry

* Mon Jan 07 2008 Karel Volny <kvolny@redhat.com> 2.1.1-3
- Marked localisation files
- Some fixes according the comment #18 to bug #412001:
- Added BuildRequires: freealut-devel libXxf86vm-devel libXxf86dga-devel
- Improved .desktop file
- Added fix for mixed encoding within the file CONTRIBUTORS

* Thu Dec 06 2007 Karel Volny <kvolny@redhat.com> 2.1.1-2
- Split the game, data and additional music into separate packages
- Added wrapper script to use correct command line parameters and OpenGL Wrapper
- Added ufoai.desktop as a separate file

* Tue Dec 04 2007 Karel Volny <kvolny@redhat.com> 2.1.1-1
- Initial release for Fedora 8
