Name:           fcgiwrap
Version:        1.1.0
Release:        1%{?dist}
Summary:        Simple FastCGI wrapper for CGI scripts
Group:          System Environment/Daemons
License:        BSD-like
URL:            http://nginx.localdomain.pl/wiki/FcgiWrap
Source0:        https://github.com/gnosek/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         Makefile.in.patch
BuildRequires:  autoconf automake fcgi-devel pkgconfig systemd-devel
Requires:       fcgi


%description
This package provides a simple FastCGI wrapper for CGI scripts with
following features:
 - very lightweight (84KB of private memory per instance)
 - fixes broken CR/LF in headers
 - handles environment in a sane way (CGI scripts get HTTP-related env.
   vars from FastCGI parameters and inherit all the others from
   environment of fcgiwrap )
 - no configuration, so you can run several sites off the same
   fcgiwrap pool
 - passes CGI stderr output to stderr stream of cgiwrap or FastCGI
 - support systemd socket activation, launcher program like spawn-fcgi
   is no longer required on systemd-enabled distributions


%prep
%setup -q
%patch0 -p1 -b .orig

%build
autoreconf -i
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/fcgiwrap
%{_mandir}/man8/*
%{_unitdir}/*.service
%{_unitdir}/*.socket


%post
# enable socket activation for fcgiwrap
/usr/bin/systemctl enable fcgiwrap.socket
/usr/bin/systemctl start fcgiwrap.socket
cat <<BANNER
==================================================
FCGI service fcgiwrap is ready!!!
==================================================
BANNER


%preun
# stop and disable socket activation for fcgiwrap
/usr/bin/systemctl stop fcgiwrap.socket
/usr/bin/systemctl disable fcgiwrap.socket


%changelog
* Tue Apr 22 2014 Justin Zhang <schnell18[AT]gmail.com> - 1.1.0-1
- version 1.1.0
- Create RPM spec file for the fcgiwrap
