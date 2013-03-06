# TODO
# - ensure all is really built
# - cc/cflags for native build (find source first (currently prebuild libs used))
#   - currently packages bundled libs: libcrypto.so.1.0.0(OPENSSL_1.0.0)(64bit) is needed by jitsi-2.0-0.4506.10553.0.1.x86_64
# - sync with resources/install/rpm/SPECS/jitsi.spec
%define		subver	4506.10553
%define		rel		0.1
Summary:	Open Source Video Calls and Chat
Name:		jitsi
Version:	2.0
Release:	0.%{subver}.%{rel}
License:	LGPL 2.1
Group:		Applications/Communications
URL:		http://www.jitsi.org/
Source0:	https://download.jitsi.org/jitsi/src/%{name}-src-%{version}.%{subver}.zip
# Source0-md5:	5d79c2c5e71be44fabd9dec45a4c1d52
# TODO use resources/install/debian/jitsi.desktop.tmpl
Source1:	%{name}.desktop
# TODO: sync with resources/install/debian/jitsi.sh.tmpl
Source2:	%{name}.sh
Patch0:		dbus-lib64.patch
Patch1:		jawt-link.patch
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	jpackage-utils
Obsoletes:	sip-communicator
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jitsi is an audio/video Internet phone and instant messenger that
supports some of the most popular instant messaging and telephony
protocols such as SIP, Jabber, AIM/ICQ, MSN, Yahoo! Messenger,
Bonjour, RSS and counting.

Jitsi is completely Open Source / Free Software, and is freely
available under the terms of the GNU Lesser General Public License.

%prep
%setup -qc
mv jitsi/* .
#%patch0 -p1
#%patch1 -p1

install -p %{SOURCE2} .
%if "%{_lib}" != "lib"
%{__sed} -i -e 's,/usr/lib,%{_libdir},' %{name}.sh
%endif

# gtk+1
%{__rm} -v lib/native/linux*/*mozembed*gtk1.2*

# libgtkembedmoz.so not satisfiable right now
# too old xulrunner?, xulrunner-libs 1.8 contained it
%{__rm} -v lib/native/linux*/libmozembed-linux-gtk2.so
%{__rm} -v lib/native/linux*/mozembed-linux-gtk2

# docs
cp -p resources/install/doc/readme.txt README
cp -p resources/install/doc/License.txt LICENSE

# this does not work, need each of them as separate tag: <compilerarg value="-O2" />
#%{__sed} -i -e 's,-O3,%{rpmcflags},' src/native/build.xml
#%{__sed} -i -e 's,-O2,%{rpmcflags},' src/native/build.xml

%build
%{__sed} -e 's,_PACKAGE_NAME_,%{name},g;s,_APP_NAME_,%{name},g' \
	resources/install/debian/jitsi.1.tmpl > %{name}.1

# copy the launcher script
cp resources/install/debian/jitsi.sh.tmpl $RPM_BUILD_ROOT%{_bindir}/jitsi
sed -i -e "s/_PACKAGE_NAME_/jitsi/" $RPM_BUILD_ROOT/usr/bin/jitsi

#      TODO 'ant ffmpeg' to compile ffmpeg shared library
#      TODO 'ant portaudio' to compile jnportaudio shared library
#      TODO 'ant speex' to compile jspeex shared library

%if 0
%ant \
	screencapture jawtrenderer g722 hid hwaddressretriever \
	video4linux2 galagonotification
%endif

# source code not US-ASCII
export LC_ALL=en_US
%ant -Dlabel=%{subver} rebuild

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_datadir}/%{name}/{lib,sc-bundles},%{_libdir}/%{name}}

cp -p sc-bundles/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles
cp -p sc-bundles/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles

# remove all slicks
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles/*-slick.jar
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles/slick*.jar

cp -p lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -a lib/bundle $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/bundle/junit.jar
cp -p lib/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -p resources/install/logging.properties lib/felix.client.run.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/

# arch dependant libs
install -d $RPM_BUILD_ROOT%{_libdir}
%ifarch %{x8664}
install -p lib/native/linux-64/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif
%ifarch %{ix86}
install -p lib/native/linux/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif

install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -p %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Desktop Entry
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -p resources/install/linux/sc-logo.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -p resources/images/logo/sc_logo.svg $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.svg
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}.svg
