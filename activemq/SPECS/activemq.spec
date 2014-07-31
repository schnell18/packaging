%define amqhome /usr/share/activemq
%define amqhome_rd usr/share/activemq
%define os_user  activemq
%define os_group activemq

# work around build id note absence issue
%undefine _missing_build_ids_terminate_build
%define __jar_repack %{nil}

Name: apache-activemq
Version: 5.10.0
Release: 1%{?dist}
Summary: ActiveMQ Messaging Broker
Group: System Environment/Daemons
License: ASL 2.0
URL: http://activemq.apache.org/
Source0: http://www.apache.org/dist/activemq/%{name}/%{version}/%{name}-%{version}-bin.tar.gz
Patch0: activemq-rpm.patch

%description
ActiveMQ Messaging Broker.


%package client
Summary: Client jar for Apache ActiveMQ
Group: System Environment/Libraries

%description client
Client jar for Apache ActiveMQ.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1


%build


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_javadir}
install -d %{buildroot}%{amqhome}
install -d %{buildroot}/usr/bin
install -d %{buildroot}/etc/activemq
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/var/run/activemq
install -d %{buildroot}/var/lib/activemq/data

mv * %{buildroot}%{amqhome}

# move arch-specific wrapper binaries to parent directory
pushd %{buildroot}%{amqhome}
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
    find webapps -perm 755 -type f -exec chmod -x '{}' \;
    find examples/stomp/ruby -name \*.rb -type f -exec chmod +x '{}' \;
popd

# move all conf/* except README to /etc/activemq
# http://stackoverflow.com/questions/670460/move-all-files-except-one
pushd %{buildroot}%{amqhome}/conf
    ls -1 | grep -v ^README | xargs -I{} mv {} %{buildroot}/etc/activemq
popd

# create activemq client binary symlinks in /usr/bin, thanks to
pushd %{buildroot}/usr/bin
    ln -s ../../%{amqhome_rd}/bin/activemq-admin activemq-admin
    ln -s ../../%{amqhome_rd}/bin/activemq activemq
popd

mv %{buildroot}%{amqhome}/activemq-all-%{version}.jar %{buildroot}%{_javadir}
pushd %{buildroot}%{_javadir}
    for jar in *-%{version}*
    do
        ln -sf ${jar} `echo $jar|sed "s|-%{version}||g"`
    done
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
%config(noreplace) %attr(644,root,root) /etc/activemq/*
%attr(0755,root,root) /etc/init.d/activemq
%attr(0755,root,root) /usr/bin/activemq
%attr(0755,root,root) /usr/bin/activemq-admin
%attr(755,%{os_user}, %{os_group}) %dir /var/run/activemq
%attr(755,%{os_user}, %{os_group}) /var/lib/activemq
%{amqhome}


%files client
%defattr(-,root,root,-)
%{_javadir}


%changelog
* Thu Jul 31 2014 Justin Zhang <dos.7182@gmail.com> - 5.10.0-1
- refactor for 5.10.0
