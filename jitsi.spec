# TODO
# - ensure all is really built
# - cc/cflags for native build
%define		subver	3464
%define		rel		0.1
Summary:	A Java VoIP and Instant Messaging client
Name:		jitsi
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	LGPL
Group:		Applications/Communications
URL:		http://www.jitsi.org/
Source0:	http://download.jitsi.org/jitsi/src/sip-communicator-src-%{version}-beta1-nightly.build.%{subver}.zip
# Source0-md5:	7f91e55a23c736e517471f80b4602513
Source1:	%{name}.desktop
Source2:	%{name}.sh
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	jdk
BuildRequires:	unzip
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
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

# docs
cp -p resources/install/doc/readme.txt README
cp -p resources/install/doc/License.txt LICENSE

%build
# source code not US-ASCII
export LC_ALL=en_US
%ant rebuild

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/sc-bundles
cp -p sc-bundles/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/sc-bundles

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/sc-bundles/os-specific
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/sc-bundles/os-specific/linux
cp -p sc-bundles/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/sc-bundles/os-specific/linux

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/lib
cp -p lib/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/lib

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/lib/os-specific/linux
cp -p lib/os-specific/linux/*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/lib/os-specific/linux

## arch dependant libs
install -d $RPM_BUILD_ROOT%{_libdir}
%ifarch %{x8664}
install -p lib/native/linux-64/* $RPM_BUILD_ROOT%{_libdir}
%endif
%ifarch %{ix86}
install -p lib/native/linux/* $RPM_BUILD_ROOT%{_libdir}
%endif

install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}

# Icon
install -D -p resources/install/linux/sc-logo.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install -D -p resources/images/logo/sc_logo.svg $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.svg

# Desktop menu entry
install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/mozembed-linux-gtk1.2
%attr(755,root,root) %{_libdir}/mozembed-linux-gtk2
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_pixmapsdir}/%{name}.svg
