%define svnrelease 1798
%define name unimrcp
%define devel %mklibname %{name} -d
%define libs %mklibname %{name}

Name: %{name}
Version: 0.%svnrelease
Release: %mkrel 0

Summary: Media Resource Control Protocol Stack
License: Apache
Group: System/Servers
Url: http://unimrcp.org
BuildRoot: %{_tmppath}/%{name}-%{version}

Source: %{name}.tar.gz
Source1: %{name}server.init

BuildRequires: libexpat-devel
BuildRequires: libunimrcp-deps-devel
BuildRequires: pocketsphinx-devel
BuildRequires: sphinxbase-devel
#BuildRequires: flite-devel >= 1.3.9

Requires: libunimrcp
Requires: libunimrcp-deps
Requires: pocketsphinx-libs
#Requires: flite

%description
Media Resource Control Protocol (MRCP) allows to control media processing
resources over the network using distributed client/server architecture.
Media processing resources include:
- Speech Synthesizer (TTS)
- Speech Recognizer (ASR)
- Speaker Verifier (SV)
- Speech Recorder (SR)
MRCP is not a stand alone protocol and it relies on various VoIP protocols
such as:
- SIP (MRCPv2), RTSP (MRCPv1) session management
- SDP offer/answer model
- RTP media streaming
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.

%package -n %{libs}
Summary: Media Resource Control Protocol Stack shared librarries
Group: System/Libraries

%package -n %{devel}
Summary: Media Resource Control Protocol Stack development
Group: Development/C
Requires: libunimrcp = %version-%release

%description -n %{libs}
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.
This package contains UniMRCP shared libraries

%description -n %{devel}
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.
This package contains development part of UniMRCP.

%prep
%setup -q -n %{name}

%build
[ ! -x ./bootstrap ] || ./bootstrap

perl -pi -w -e 's/lib\/pkgconfig/pkgconfig/g' configure

%configure2_5x \
    LDFLAGS=-rpath=%{_datadir}/unimrcp-deps/lib \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --with-apr=%{_datadir}/unimrcp-deps \
    --with-apr-util=%{_datadir}/unimrcp-deps \
    --with-sofia-sip=%{_datadir}/unimrcp-deps/lib \
    --with-sphinxbase=%{_libdir} \
    --with-pocketsphinx=%{_libdir} \
    --enable-pocketsphinx-plugin
#    --enable-flite-plugin \

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std DESTDIR=%{buildroot} install

install -d -m1775 %{buildroot}%{_sysconfdir}/%{name}/conf/client-profiles
install -m0664 conf/client-profiles/*.xml %{buildroot}%{_sysconfdir}/%{name}/conf/client-profiles/
install -m0664 conf/*.xsd %{buildroot}%{_sysconfdir}/%{name}/conf/
install -m0664 conf/*.xml %{buildroot}%{_sysconfdir}/%{name}/conf/
install -m0664 plugins/mrcp-pocketsphinx/conf/*.xml %{buildroot}%{_sysconfdir}/%{name}/conf/

install -d -m1775 %{buildroot}%{_datadir}/%{name}
install -m0664 data/*.pcm %{buildroot}%{_datadir}/%{name}/
install -m0664 data/*.xml %{buildroot}%{_datadir}/%{name}/
install -m0664 data/grammar.* %{buildroot}%{_datadir}/%{name}/
mv -f %{buildroot}/usr/plugin %{buildroot}%{_sysconfdir}/%{name}/

install -d -m1775 %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}server

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/conf/*.xml
%config(noreplace) %{_sysconfdir}/%{name}/conf/*.xsd
%config(noreplace) %{_sysconfdir}/%{name}/conf/client-profiles/*.xml
%{_bindir}/*
%{_sysconfdir}/%{name}/plugin
%{_sysconfdir}/rc.d/init.d/*
%{_datadir}/%{name}

%files -n %{libs}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.so.*

%files -n %{devel}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
