%define short_name sonar
%define os_user  sonar
%define os_group sonar

# do NOT repack jars
%define __jar_repack %{nil}
# work around build id note absence issue
%undefine _missing_build_ids_terminate_build

Name:    sonarqube
Version: 4.5.1
Release: 1%{?dist}
Summary: Open source platform for continuous inspection of code quality.
Group: System Environment/Daemons
License: LGPL 3.0
URL: http://www.sonarqube.org
Source0: http://dist.sonar.codehaus.org/%{name}-%{version}.zip
Source1: context.xml
Patch0: sonar-rpm.patch

%description
SonarQube has got a very efficient way of navigating, a balance between
high-level view, dashboard, TimeMachine and defect hunting tools. This
enables to quickly uncover projects and / or components that are in
Technical Debt to establish action plans.  SonarQube is a web-based
application. Rules, alerts, thresholds, exclusions, settings… can be
configured online. By leveraging its database, SonarQube not only allows
to combine metrics altogether but also to mix them with historical
measures.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1


%build


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_javadir}
install -d %{buildroot}%{_datadir}/%{short_name}
install -d %{buildroot}/etc/sonar
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/var/log/sonar
install -d %{buildroot}/var/run/sonar
install -d %{buildroot}/var/lib/sonar
install -d %{buildroot}/var/lib/sonar/web

mv conf/*     %{buildroot}/etc/%{short_name}
mv COPYING    %{buildroot}%{_datadir}/%{short_name}
mv bin        %{buildroot}%{_datadir}/%{short_name}
mv lib        %{buildroot}%{_datadir}/%{short_name}
mv data       %{buildroot}/var/lib/sonar
mv extensions %{buildroot}/var/lib/sonar
mv logs       %{buildroot}/var/lib/sonar
mv temp       %{buildroot}/var/lib/sonar
mv web/deploy %{buildroot}/var/lib/sonar/web
mv web        %{buildroot}%{_datadir}/%{short_name}
cp %{SOURCE1} %{buildroot}%{_datadir}/%{short_name}/web/META-INF

# move arch-specific wrapper binaries to parent directory
pushd %{buildroot}%{_datadir}/%{short_name}
    %ifarch i386 i686
        mv bin/linux-x86-32/wrapper bin
        mv bin/linux-x86-32/lib/libwrapper.so bin
        mv bin/linux-x86-32/sonar.sh %{buildroot}/etc/init.d/sonar
    %endif
    %ifarch x86_64
        mv bin/linux-x86-64/wrapper bin
        mv bin/linux-x86-64/lib/libwrapper.so bin
        mv bin/linux-x86-64/sonar.sh %{buildroot}/etc/init.d/sonar
    %endif
    rm -fr bin/linux-*
    rm -fr bin/solaris-*
    rm -fr bin/macosx-*
    rm -fr bin/windows-*
    ln -sf ../../../etc/sonar conf
    ln -sf ../../../var/lib/sonar/data data
    ln -sf ../../../var/lib/sonar/extensions extensions
    ln -sf ../../../var/lib/sonar/temp temp
    ln -sf ../../../var/lib/sonar/logs logs
    pushd web
        ln -sf ../../../../var/lib/sonar/web/deploy deploy
    popd
popd

%clean
rm -rf %{buildroot}


%pre
# Add the "sonar" user and group
getent group %{os_group} > /dev/null || /usr/sbin/groupadd -g 92 -r %{os_group} 2> /dev/null || :
getent passwd %{os_user} > /dev/null || /usr/sbin/useradd -c "SonarQube" -u 92 -g %{os_group} -s /bin/bash -r -d /var/lib/sonar %{os_user} 2>/dev/null || :


%post
[ -f /etc/init.d/sonar ] && /sbin/chkconfig --levels 345 sonar on


%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/sonar ] && /etc/init.d/sonar stop
    [ -f /etc/init.d/sonar ] && /sbin/chkconfig --del sonar
fi


%files
%defattr(-,root,root,-)
%attr(0755,root,root) /etc/init.d/sonar
%config(noreplace) %attr(644,%{os_user},%{os_group}) /etc/sonar/*
%attr(755,%{os_user},%{os_group}) %dir /var/log/sonar
%attr(755,%{os_user},%{os_group}) %dir /var/run/sonar
%attr(755,%{os_user},%{os_group}) /var/lib/sonar/*
%{_datadir}/%{short_name}/bin
%{_datadir}/%{short_name}/data
%{_datadir}/%{short_name}/COPYING
%{_datadir}/%{short_name}/conf
%{_datadir}/%{short_name}/extensions
%{_datadir}/%{short_name}/lib
%{_datadir}/%{short_name}/logs
%{_datadir}/%{short_name}/temp
%{_datadir}/%{short_name}/web


%changelog
* Tue Dec 16 2014 Justin Zhang <schnell18@gmail.com> - 4.5.1-1
- Create spec for SonarQube 4.5.1
