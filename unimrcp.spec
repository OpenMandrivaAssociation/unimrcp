%define name unimrcp
%define develname %mklibname %{name} -d
%define libname %mklibname %{name}

Name: %{name}
Version: 1.0.0
Release: 5

Summary: Media Resource Control Protocol Stack
License: Apache
Group: System/Servers
Url: http://unimrcp.org

Source0: http://unimrcp.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: %{name}server.service

BuildRequires: pkgconfig
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: expat-devel
BuildRequires: libunimrcp-deps-devel
BuildRequires: pocketsphinx-devel
BuildRequires: sphinxbase-devel
BuildRequires: pkgconfig(sndfile)
#BuildRequires: flite-devel >= 1.3.9

Requires: lib%{name}
Requires: libunimrcp-deps
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

%package -n %{libname}
Summary: Media Resource Control Protocol Stack shared librarries
Group: System/Libraries
Provides: lib%{name} = %{version}-%{release}

%description -n %{libname}
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.
This package contains UniMRCP shared libraries

%package -n %{develname}
Summary: Media Resource Control Protocol Stack develnameopment
Group: Development/C
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Requires: lib%{name} = %{version}-%{release}, pkgconfig

%description -n %{develname}
UniMRCP is an open source cross-platform MRCP implementation, which provides
everything required for MRCP client and server side deployment.
UniMRCP encapsulates SIP/MRCPv2, RTSP, SDP and RTP stacks inside and provides
MRCP version independent user level interface for the integration.
This package contains development part of UniMRCP.

%prep
%setup -q

%build
[ ! -x ./bootstrap ] || ./bootstrap

perl -pi -w -e 's/lib\/pkgconfig/pkgconfig/g' configure
perl -pi -w -e 's/^confdir=([\W])\$\{prefix\}/confdir=$1\$\(DESTDIR\)\$\{prefix\}/g' configure
perl -pi -w -e 's/^logdir=([\W])\$\{prefix\}/logdir=$1\$\(DESTDIR\)\$\{prefix\}/g' configure
perl -pi -w -e 's/^datadir=([\W])\$\{prefix\}/datadir=$1\$\(DESTDIR\)\$\{prefix\}/g' configure

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --with-apr=%{_datadir}/unimrcp-deps \
    --with-apr-util=%{_datadir}/unimrcp-deps \
    --with-sofia-sip=%{_datadir}/unimrcp-deps/lib \
    --with-sphinxbase=%{_libdir} \
    --with-pocketsphinx=%{_libdir} \
    --enable-pocketsphinx-plugin \
    --disable-static
#    --enable-flite-plugin \

%install
%makeinstall_std

install -d -m0775 %{buildroot}%{_sysconfdir}/%{name}
mv -f %{buildroot}/usr/conf %{buildroot}%{_sysconfdir}/%{name}/
mv -f %{buildroot}/usr/data %{buildroot}%{_sysconfdir}/%{name}/
mv -f %{buildroot}/usr/log %{buildroot}%{_sysconfdir}/%{name}/
mv -f %{buildroot}/usr/plugin %{buildroot}%{_sysconfdir}/%{name}/

install -D -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}server.service

%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/conf/*.xml
%config(noreplace) %{_sysconfdir}/%{name}/conf/*.xsd
%config(noreplace) %{_sysconfdir}/%{name}/conf/client-profiles/*.xml
%{_bindir}/*
%{_sysconfdir}/%{name}/plugin
%{_sysconfdir}/%{name}/data
%{_sysconfdir}/%{name}/log
%attr(0644,root,root) %{_unitdir}/%{name}server.service

%files -n %{libname}
%{_libdir}/*.so
%{_libdir}/*.so.*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
