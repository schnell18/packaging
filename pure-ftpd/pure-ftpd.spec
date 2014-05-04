%global ftp_user ftpuser
%global ftp_group ftpgroup


Name:       pure-ftpd
Version:    1.0.36
Release:    1%{?dist}
Summary:    Lightweight, fast and secure FTP server

Group:      System Environment/Daemons
License:    BSD
URL:        http://www.pureftpd.org
Source0:    http://download.pureftpd.org/pub/pure-ftpd/releases/pure-ftpd-%{version}.tar.bz2
Source1:    pure-ftpd.init 
Source2:    pure-ftpd.logrotate
Source3:    pure-ftpd.xinetd
Source4:    pure-ftpd.pure-ftpwho.pam
Source5:    pure-ftpd.pure-ftpwho.consoleapp
Source6:    pure-ftpd.README.SELinux
Source7:    pure-ftpd.pureftpd.te
Source8:    pure-ftpd.conf.uploadscript
Source9:    pure-ftpd.ftp-hook
Patch2:     pure-ftpd-paminclude.patch
Provides:   ftpserver
BuildRequires:  pam-devel, perl, python, libcap-devel
%{!?_without_ldap:BuildRequires:  openldap-devel}
%{!?_without_mysql:BuildRequires: mysql-devel}
%{!?_without_pgsql:BuildRequires: postgresql-devel}
%{!?_without_tls:BuildRequires: openssl-devel}
# SELinux module
%if 0%{?fedora} == 5
BuildRequires: checkpolicy, selinux-policy >= 2.2.40, m4
%else
BuildRequires: checkpolicy, selinux-policy-devel
%endif

Requires(post):   chkconfig
Requires(preun):  chkconfig, initscripts
Requires(postun): initscripts
Requires:   logrotate, usermode


%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP server,
based upon Troll-FTPd. Unlike other popular FTP servers, it has no known
security flaw, it is really trivial to set up and it is especially designed
for modern Linux and FreeBSD kernels (setfsuid, sendfile, capabilities) .
Features include PAM support, IPv6, chroot()ed home directories, virtual
domains, built-in LS, anti-warez system, bandwidth throttling, FXP, bounded
ports for passive downloads, UL/DL ratios, native LDAP and SQL support,
Apache log files and more.
Rebuild switches:
--without ldap     disable ldap support
--without mysql    disable mysql support
--without pgsql    disable postgresql support
--without extauth  disable external authentication
--without tls      disable SSL/TLS


%package    selinux
Summary:    SELinux support for Pure-FTPD
Group:      System Environment/Daemons
Requires:   %{name} = %{version}
Requires(post): policycoreutils, initscripts, %{name}
Requires(preun): policycoreutils, initscripts, %{name}
Requires(postun): policycoreutils

%description selinux
This package adds SELinux enforcement to Pure-FTPD. Install it if you want
Pure-FTPd to be protected in the same way other FTP servers are in Fedora
(e.g. VSFTPd and ProFTPd)


%prep
%setup -q
%patch2 -p0 -b .paminclude
install -pm 644 %{SOURCE6} README.SELinux
mkdir selinux
cp -p %{SOURCE7} selinux/pureftpd.te


%build
%configure  \
            --sysconfdir=%{_sysconfdir}/%{name} \
            --with-capabilities \
            --with-sendfile \
            --with-cork \
            --with-paranoidmsg \
            --with-altlog \
            --with-puredb \
            %{!?_without_extauth:--with-extauth} \
            --with-pam \
            --with-cookie \
            --with-throttling \
            --with-ratios \
            --with-quotas \
            --with-ftpwho \
            --with-welcomemsg \
            --with-uploadscript \
            --with-virtualhosts \
            --with-virtualchroot \
            --with-diraliases \
            --with-peruserlimits \
            %{!?_without_ldap:--with-ldap} \
            %{!?_without_mysql:--with-mysql} \
            %{!?_without_pgsql:--with-pgsql} \
            --with-privsep \
            %{!?_without_tls:--with-tls --with-certfile=%{_sysconfdir}/pki/%{name}/%{name}.pem} \
            --with-rfc2640 \
            --without-bonjour \

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man8
install -d -m 755 $RPM_BUILD_ROOT%{_sbindir}
install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/ftp
%{!?_without_tls:install -d -m 700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/%{name}}

# Conf
install -p -m 755 configuration-file/pure-config.pl $RPM_BUILD_ROOT%{_sbindir}
install -p -m 644 configuration-file/pure-ftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p -m 755 configuration-file/pure-config.py $RPM_BUILD_ROOT%{_sbindir}
install -p -m 644 pureftpd-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p -m 644 pureftpd-mysql.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p -m 644 pureftpd-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
# install customized pure-fptd.conf w/ upload script enabled
install -p -m 644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/%{name}/%{name}-ftpd.conf
# install dummy FTP hook script
install -p -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_bindir}/pure-fptd-hook

# Man
install -p -m 644 man/pure-ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-ftpwho.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-mrtginfo.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-uploadscript.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-pw.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-pwconvert.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-statsdecode.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-quotacheck.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p -m 644 man/pure-authd.8 $RPM_BUILD_ROOT%{_mandir}/man8

# Init script
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# Pam 
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -p -m 644 pam/pure-ftpd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/

# Logrotate
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

# xinetd support
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}

# pure-ftpwho and non-root users
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/pure-ftpwho
install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/pure-ftpwho
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/pure-ftpwho

# SELinux support
cd selinux
echo "%{_sbindir}/pure-ftpd    system_u:object_r:ftpd_exec_t:s0" > pureftpd.fc
echo '%{_localstatedir}/log/pureftpd.log    system_u:object_r:xferlog_t:s0' >> pureftpd.fc
touch pureftpd.if
make -f %{_datadir}/selinux/devel/Makefile
install -p -m 644 -D pureftpd.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{name}/pureftpd.pp


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ "$1" -le "1" ]; then # fist install
    /sbin/chkconfig --add pure-ftpd
fi
%if 0%{!?_without_tls:1}
# TLS Certificate
if [ ! -f %{_sysconfdir}/pki/%{name}/%{name}.pem ]; then
  %{_sysconfdir}/pki/tls/certs/make-dummy-cert \
    %{_sysconfdir}/pki/%{name}/%{name}.pem
fi
%endif

%preun
if [ "$1" -lt "1" ]; then
    /sbin/service pure-ftpd stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del pure-ftpd
fi


%postun
if [ "$1" -ge "1" ]; then 
    /sbin/service pure-ftpd condrestart > /dev/null 2>&1 
fi


%post selinux
if [ "$1" -le "1" ]; then # Fist install
    semodule -i %{_datadir}/selinux/packages/%{name}/pureftpd.pp 2>/dev/null || :
    fixfiles -R pure-ftpd restore || :
    /sbin/service pure-ftpd condrestart > /dev/null 2>&1  || :
fi


%preun selinux
if [ "$1" -lt "1" ]; then # Final removal
    semodule -r pureftpd 2>/dev/null || :
    fixfiles -R pure-ftpd restore || :
    /sbin/service pure-ftpd condrestart > /dev/null 2>&1 || :
fi


%postun selinux
if [ "$1" -ge "1" ]; then # Upgrade
    # Replaces the module if it is already loaded
    semodule -i %{_datadir}/selinux/packages/%{name}/pureftpd.pp 2>/dev/null || :
    # no need to restart the daemon
fi


%files
%defattr(-, root, root, -)
%doc FAQ THANKS AUTHORS CONTACT HISTORY NEWS
%doc README README.Authentication-Modules README.Configuration-File
%doc README.Contrib README.Donations README.LDAP README.MySQL
%doc README.PGSQL README.TLS README.Virtual-Users
%doc contrib/pure-vpopauth.pl pureftpd.schema contrib/pure-stat.pl
%{_bindir}/pure-*
%{_sbindir}/pure-*
%config %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/pure-ftpwho
%config(noreplace) %{_sysconfdir}/security/console.apps/pure-ftpwho
%{!?_without_tls:%{_sysconfdir}/pki/%{name}}
%{_mandir}/man8/*
%dir /var/ftp/


%files selinux
%defattr(-, root, root, -)
%doc README.SELinux
%{_datadir}/selinux/packages/%{name}/pureftpd.pp


%changelog
* Sun May 04 2014 Justin Zhang <schnell18@gmail.com> - 1.0.36-1
- version 1.0.36
- customized to enable upload script

* Mon Mar 14 2011 Michal Ingeli <mi@v3.sk> - 1.0.30-1
- version 1.0.30
- security bug fix #683221 by upstream

* Wed Apr 28 2010 Aurelien Bompard <abompard@fedoraproject.org> -  1.0.29-2
- fix bug #586513

* Tue Mar 16 2010 Aurelien Bompard <abompard@fedoraproject.org> -  1.0.29-1
- version 0.1.29

* Fri Dec 04 2009 Aurelien Bompard <abompard@fedoraproject.org> -  1.0.27-1
- version 1.0.27

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.22-4
- use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.22-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 27 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.22-1
- version 1.0.22

* Wed Mar 04 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-20
- make pam and consolehelper's conf files noreplace

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.21-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-18
- Rebuild for mysql

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.21-17
- Rebuild for Python 2.6

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-16
- Rebuild for libcap.so.2 (bug 450086)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.21-15
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.0.21-14
- Rebuild for deps

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-13
- rebuild for BuildID

* Sat Dec 09 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-12
- rebuild

* Sat Dec 09 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-11
- rebuild

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-9
- rebuild

* Fri Aug 04 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-8
- BuildRequire selinux-policy-devel for FC6 onwards

* Fri Aug 04 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.0.21-7
- install README.SELinux with perms 644 to avoid depending on the
  buildsys' umask (bug 200844)

* Fri Jun 16 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-6
- add missing m4 BuildRequires

* Sun May 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-5
- add missing BuildRequires

* Sun May 14 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-4
- add SELinux support
- prevent the init script from displaying the config on startup

* Sun Apr 09 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-3
- fix mysql socket location (bug 188426)

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-2
- build option rendezvous has been renamed to bonjour
- add --with-cork
- see bug 182314 for more info, thanks to Jose Pedro Oliveira

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.0.21-1
- version 1.0.21

* Sun Nov 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-4
- rebuild
- i18n in init script

* Mon Aug 01 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-3
- build feature-complete by default
- add TLS support
- see bug #162849

* Wed Mar 23 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-2.fc4
- implement Jose's RFE in bug 151337: pure-ftpwho can be run
  by a normal user.
- change release tag for FC4

* Sun Mar 13 2005 Aurelien Bompard <gauret[AT]free.fr> 1.0.20-1
- adapt to Fedora Extras (drop Epoch, change Release tag)

* Wed Feb 16 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.9
- license is BSD, not GPL

* Mon Feb 14 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.8
- various fixes. See bug 1573 (fedora.us) for more info.

* Fri Feb 11 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.7
- fix init script
- require logrotate
- add rebuild switches to lower dependancies
- see bug 1573 (fedora.us) for more info.

* Fri Feb 04 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.6
- Add the "UseFtpUsers no" directive in the config file since we don't
  use it anymore

* Wed Feb 02 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.5
- various spec file improvements

* Mon Jan 31 2005 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.4
- add patch for x86_64 support
- implement wishes in bug 1573 from Jose Pedro Oliveira
- don't use the ftpusers file, and thus remove conflicts with other FTP servers
- rediff config patch

* Tue Nov 02 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.3
- add large file support

* Fri Sep 24 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.2
- redirect %%preun output to /dev/null
- add requirements to chkconfig for the scriptlets

* Sun Aug 01 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.20-0.fdr.1
- version 1.0.20 (bugfixes)

* Mon Jun 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.19-0.fdr.1
- version 1.0.19

* Tue May 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:1.0.18-0.fdr.1
- version 1.0.18
- spec file cleanups

* Sun Oct 19 2003 Aurelien Bompard <gauret[AT]free.fr> 1.0.16a-1
- Redhatize the Mandrake RPM
- version 1.0.16a
- improve ftpusers creation script

