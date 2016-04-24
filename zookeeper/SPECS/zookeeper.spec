Name: zookeeper
Version: 3.4.8
Release: 1%{?dist}
Summary: High-performance coordination service for distributed applications.

Group: Applications/Databases
License: Apache License v2.0
URL: http://zookeeper.apache.org/

Source0: http://apache.fayea.com/zookeeper/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: zookeeper.init
Source2: zookeeper.logrotate
Source3: zoo.cfg
Source4: log4j.properties
Source5: java.env
Source6: zkEnv.sh
Source7: zookeeper.sysconfig

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel,gcc,make,libtool,autoconf,cppunit-devel
Requires: logrotate, java
Requires(post): chkconfig initscripts
Requires(pre): chkconfig initscripts
AutoReqProv: no

%description
ZooKeeper is a distributed, open-source coordination service for
distributed applications. It exposes a simple set of primitives that
distributed applications can build upon to implement higher level
services for synchronization, configuration maintenance, and groups and
naming. It is designed to be easy to program to, and uses a data model
styled after the familiar directory tree structure of file systems. It
runs in Java and has bindings for both Java and C.

Coordination services are notoriously hard to get right. They are
especially prone to errors such as race conditions and deadlock. The
motivation behind ZooKeeper is to relieve distributed applications the
responsibility of implementing coordination services from scratch.


%prep
%setup -q -n %{name}-%{version}

%build
pushd src/c
rm -rf aclocal.m4 autom4te.cache/ config.guess config.status config.log \
    config.sub configure depcomp install-sh ltmain.sh libtool \
    Makefile Makefile.in missing stamp-h1 compile
autoheader
libtoolize --force
aclocal
automake -a
autoconf
autoreconf
%configure
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}/lib
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}/data

install -p -D -m 755 bin/zkCli.sh %{buildroot}%{_bindir}/zkCli.sh
install -p -D -m 755 bin/zkServer.sh %{buildroot}%{_bindir}/zkServer.sh
install -p -D -m 755 bin/zkCleanup.sh %{buildroot}%{_bindir}/zkCleanup.sh
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_libexecdir}/zkEnv.sh
install -p -D -m 644 dist-maven/%{name}-%{version}.jar %{buildroot}%{_datadir}/%{name}/
install -p -D -m 644 lib/*.jar %{buildroot}%{_datadir}/%{name}/lib
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{makeinstall} -C src/c

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt NOTICE.txt README.txt
%dir %attr(0750, %{name}, %{name}) %{_localstatedir}/log/%{name}
%dir %attr(0750, %{name}, %{name}) %{_localstatedir}/lib/%{name}
%dir %attr(0750, %{name}, %{name}) %{_localstatedir}/lib/%{name}/data
%{_datadir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}
%{_libexecdir}/zkEnv.sh

# zookeeper-doc
%package doc
Summary: Documents for zookeeper
Group: Documentation
BuildArch: noarch

%description doc
The package contains API documents and recipes of zookeeper

%files doc
%defattr(-, root, root, -)
%doc docs recipes

# libzookeeper
%package -n libzookeeper
Summary: C client interface to zookeeper server
Group: Development/Libraries
BuildRequires: gcc

%description -n libzookeeper
The client supports two types of APIs -- synchronous and asynchronous.

Asynchronous API provides non-blocking operations with completion
callbacks and relies on the application to implement event multiplexing
on its behalf.

On the other hand, Synchronous API provides a blocking flavor of
zookeeper operations and runs its own event loop in a separate thread.

Sync and Async APIs can be mixed and matched within the same
application.

%files -n libzookeeper
%defattr(-, root, root, -)
%doc src/c/README src/c/LICENSE
%{_libdir}/libzookeeper_mt.so.*
%{_libdir}/libzookeeper_st.so.*

# libzookeeper-devel
%package -n libzookeeper-devel
Summary: Headers and static libraries for libzookeeper
Group: Development/Libraries
Requires: gcc

%description -n libzookeeper-devel
This package contains the libraries and header files needed for
developing with libzookeeper.

%files -n libzookeeper-devel
%defattr(-, root, root, -)
%{_includedir}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_localstatedir}/lib/%{name} -s /sbin/nologin %{name}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%changelog
* Sat Apr 23 2016 Justin Zhang <schnell18@gmail.com> - 3.4.8-1
- Bump up version to 3.4.8 and split zookeeper-doc package
* Mon Dec 8 2014 David Xie <david.scriptfan@gmail.com> - 3.4.6-1
- Bump version to 3.4.6
* Thu May 30 2013 Sam Kottler <shk@linux.com> - 3.4.5-1
- Updated to 3.4.5
* Tue Oct 2 2012 Sam Kottler <sam@kottlerdevelopment.com> - 3.3.2-1
- Initialize package creation
