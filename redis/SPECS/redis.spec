Name:             redis
Version:          2.8.17
Release:          1%{?dist}
Summary:          An advanced key-value cache and in-memory database

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
Source0:          http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
Patch0:           redis.conf.patch

BuildRequires:    tcl >= 8.5

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an open source, BSD licensed, advanced key-value cache and store. It
is often referred to as a data structure server since keys can contain strings,
hashes, lists, sets, sorted sets, bitmaps and hyperloglogs. You can run atomic
operations on these types, like appending to a string; incrementing the value
in a hash; pushing an element to a list; computing set intersection, union and
difference; or getting the member with highest ranking in a sorted set. In
order to achieve its outstanding performance, Redis works with an in-memory
dataset. Depending on your use case, you can persist it either by dumping the
dataset to disk every once in a while, or by appending each command to a log.
Persistence can be optionally disabled, if you just need a feature-rich,
networked, in-memory cache. Redis also supports trivial-to-setup master-slave
asynchronous replication, with very fast non-blocking first synchronization,
auto-reconnection with partial resynchronization on net split.

%prep
%setup -q
%patch0 -p0 -b .orig

%build
make %{?_smp_mflags} \
  DEBUG='' \
  CFLAGS='%{optflags}' \
  V=1 \
  all

%check
# make test

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add redis

%pre
getent group redis &> /dev/null || groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin \
-c 'Redis Server' redis &> /dev/null
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README MANIFESTO
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
%{_initrddir}/%{name}

%changelog
* Tue Oct 28 2014 Justin Zhang <schnell18@gmail.com> - 2.8.17-1
- Update to redis 2.8.17

* Sat Mar 31 2012 Silas Sewell <silas@sewell.org> - 2.4.10-1
- Update to redis 2.4.10

* Fri Feb 24 2012 Silas Sewell <silas@sewell.org> - 2.4.8-2
- Disable ppc64 for now
- Enable verbose builds

* Fri Feb 24 2012 Silas Sewell <silas@sewell.org> - 2.4.8-1
- Update to redis 2.4.8

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-2
- Remove google-perftools-devel

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-1
- Update to redis 2.2.5

* Tue Oct 19 2010 Silas Sewell <silas@sewell.ch> - 2.0.3-1
- Update to redis 2.0.3

* Fri Oct 08 2010 Silas Sewell <silas@sewell.ch> - 2.0.2-1
- Update to redis 2.0.2
- Disable checks section for el5

* Fri Sep 11 2010 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Update to redis 2.0.1

* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Update to redis 2.0.0

* Thu Sep 02 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-3
- Add Fedora build flags
- Send all scriplet output to /dev/null
- Remove debugging flags
- Add redis.conf check to init script

* Mon Aug 16 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-2
- Don't compress man pages
- Use patch to fix redis.conf

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
