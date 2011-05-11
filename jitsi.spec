# TODO
# - ensure all is really built
# - cc/cflags for native build (find source first (currently prebuild libs used))
%define		subver	3464
%define		rel		0.9
Summary:	A Java VoIP and Instant Messaging client
Name:		jitsi
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	LGPL 2.1
Group:		Applications/Communications
URL:		http://www.jitsi.org/
Source0:	http://download.jitsi.org/jitsi/src/sip-communicator-src-%{version}-beta1-nightly.build.%{subver}.zip
# Source0-md5:	7f91e55a23c736e517471f80b4602513
Source1:	%{name}.desktop
Source2:	%{name}.sh
BuildRequires:	ant
BuildRequires:	ant-nodeps
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
Jitsi (SIP Communicator) is an audio/video Internet phone and instant
messenger that supports some of the most popular instant messaging and
telephony protocols such as SIP, Jabber, AIM/ICQ, MSN, Yahoo!
Messenger, Bonjour, IRC, RSS and soon others like IAX.

Jitsi (SIP Communicator) is completely Open Source / Free Software,
and is freely available under the terms of the GNU Lesser General
Public License.

%prep
%setup -q -n sip-communicator

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

%build
# source code not US-ASCII
export LC_ALL=en_US
%ant rebuild

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{lib,sc-bundles},%{_libdir}/%{name}}

cp -p sc-bundles/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles
cp -p sc-bundles/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/sc-bundles

cp -p lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -p lib/logging.properties lib/felix.client.run.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -p lib/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

## arch dependant libs
install -d $RPM_BUILD_ROOT%{_libdir}
%ifarch %{x8664}
install -p lib/native/linux-64/* $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif
%ifarch %{ix86}
install -p lib/native/linux/* $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif

install -p %{name}.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

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
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/lib*.so
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}.svg
