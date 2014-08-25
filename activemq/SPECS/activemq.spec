%define short_name activemq
%define os_user  activemq
%define os_group activemq

# do NOT repack jars
%define __jar_repack %{nil}
# work around build id note absence issue
%undefine _missing_build_ids_terminate_build

Name: apache-activemq
Version: 5.10.0
Release: 3%{?dist}
Summary: ActiveMQ Messaging Broker
Group: System Environment/Daemons
License: ASL 2.0
URL: http://activemq.apache.org/
Source0: http://www.apache.org/dist/activemq/%{name}/%{version}/%{name}-%{version}-bin.tar.gz
Patch0: activemq-rpm.patch

%description
Apache ActiveMQ ™ is the most popular and powerful open source messaging and
Integration Patterns server. Apache ActiveMQ is fast, supports many Cross
Language Clients and Protocols, comes with easy to use Enterprise Integration
Patterns and many advanced features while fully supporting JMS 1.1 and J2EE
1.4. Apache ActiveMQ is released under the Apache 2.0 License.


%package client
Summary: Client jar for Apache ActiveMQ
Group: System Environment/Libraries
BuildArch: noarch

%description client
Client jar for Apache ActiveMQ.


%package examples
Summary: Apache ActiveMQ examples
Group: System Environment/Libraries
BuildArch: noarch

%description examples
Examples for Apache ActiveMQ.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1


%build


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_javadir}
install -d %{buildroot}%{_datadir}/%{short_name}
install -d %{buildroot}/usr/bin
install -d %{buildroot}/etc/activemq
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/var/log/activemq
install -d %{buildroot}/var/run/activemq
install -d %{buildroot}/var/lib/activemq/data

mv * %{buildroot}%{_datadir}/%{short_name}

# move arch-specific wrapper binaries to parent directory
pushd %{buildroot}%{_datadir}/%{short_name}
    %ifarch i386 i686
        mv bin/linux-x86-32/wrapper bin
        mv bin/linux-x86-32/libwrapper.so bin
        mv bin/linux-x86-32/activemq %{buildroot}/etc/init.d
        mv bin/linux-x86-32/wrapper.conf %{buildroot}/etc/activemq
    %endif
    %ifarch x86_64
        mv bin/linux-x86-64/wrapper bin
        mv bin/linux-x86-64/libwrapper.so bin
        mv bin/linux-x86-64/activemq %{buildroot}/etc/init.d
        mv bin/linux-x86-64/wrapper.conf %{buildroot}/etc/activemq
    %endif
    rm -fr bin/linux-x86-32 
    rm -fr bin/linux-x86-64 
    rm -fr bin/macosx
    # Fix up permissions (rpmlint complains)
    find lib -perm 755 -type f -exec chmod -x '{}' \;
    find webapps -perm 755 -type f -exec chmod -x '{}' \;
    find examples/stomp/ruby -name \*.rb -type f -exec chmod +x '{}' \;
popd

# move all conf/* except DIRECTORY_MOVED to /etc/activemq
# http://stackoverflow.com/questions/670460/move-all-files-except-one
pushd %{buildroot}%{_datadir}/%{short_name}/conf
    ls -1 | grep -v ^DIRECTORY_MOVED | xargs -I{} mv {} %{buildroot}/etc/activemq
popd

# create activemq client binary symlinks in /usr/bin, thanks to
pushd %{buildroot}/usr/bin
    rd=`echo %{_datadir}/%{short_name} | cut -c2-`
    ln -s ../../$rd/bin/activemq-admin activemq-admin
    ln -s ../../$rd/bin/activemq activemq
popd

mv %{buildroot}%{_datadir}/%{short_name}/activemq-all-%{version}.jar %{buildroot}%{_javadir}
pushd %{buildroot}%{_javadir}
    for jar in *-%{version}*
    do
        ln -sf $jar `echo $jar|sed "s|-%{version}||g"`
    done
popd

# remove the empty activemq.log
pushd %{buildroot}%{_datadir}/%{short_name}/data
    [ -f activemq.log ] && rm -f activemq.log
popd


%clean
rm -rf %{buildroot}


%pre
# Add the "activemq" user and group
getent group %{os_group} > /dev/null || /usr/sbin/groupadd -g 92 -r %{os_group} 2> /dev/null || :
getent passwd %{os_user} > /dev/null || /usr/sbin/useradd -c "Apache ActiveMQ" -u 92 -g %{os_group} -s /bin/bash -r -d /var/lib/activemq %{os_user} 2>/dev/null || :


%post
[ -f /etc/init.d/activemq ] && /sbin/chkconfig --add activemq


%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/activemq ] && /etc/init.d/activemq stop
    [ -f /etc/init.d/activemq ] && /sbin/chkconfig --del activemq
fi


%files
%defattr(-,root,root,-)
%attr(0755,root,root) /etc/init.d/activemq
%attr(0755,root,root) /usr/bin/activemq
%attr(0755,root,root) /usr/bin/activemq-admin
%config(noreplace) %attr(644,%{os_user},%{os_group}) /etc/activemq/*
%attr(755,%{os_user},%{os_group}) %dir /var/log/activemq
%attr(755,%{os_user},%{os_group}) %dir /var/run/activemq
%attr(755,%{os_user},%{os_group}) /var/lib/activemq
%{_datadir}/%{short_name}/bin
%{_datadir}/%{short_name}/data
%{_datadir}/%{short_name}/LICENSE
%{_datadir}/%{short_name}/README.txt
%{_datadir}/%{short_name}/conf
%{_datadir}/%{short_name}/docs
%{_datadir}/%{short_name}/lib
%{_datadir}/%{short_name}/NOTICE
%{_datadir}/%{short_name}/webapps


%files client
%defattr(-,root,root,-)
%{_javadir}


%files examples
%defattr(-,root,root,-)
%{_datadir}/%{short_name}/examples
%{_datadir}/%{short_name}/webapps-demo


%changelog
* Mon Aug 25 2014 Justin Zhang <schnell18@gmail.com> - 5.10.0-3
- Move examples to its own package
* Fri Aug 22 2014 Justin Zhang <schnell18@gmail.com> - 5.10.0-2
- Move from /usr to /usr/share to be FHS compliant
* Thu Jul 31 2014 Justin Zhang <schnell18@gmail.com> - 5.10.0-1
- refactor for 5.10.0
