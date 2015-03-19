%global perl_vendorlib %(eval $(perl -V:vendorlib); echo $vendorlib)
%global gitolite_homedir /var/lib/%{name}

%define os_user git

Name:           gitolite3
Epoch:          1
Version:        3.6.2
Release:        1%{?dist}
Summary:        Highly flexible server for git directory version tracker

Group:          Applications/System
License:        GPLv2 and CC-BY-SA
URL:            http://github.com/sitaramc/gitolite
Source0:        https://github.com/sitaramc/gitolite/archive/v%{version}.tar.gz

BuildArch:      noarch
Provides:       perl(%{name}) = %{version}-%{release}
Requires:       git
Requires:       openssh-clients
Requires:       perl(:MODULE_COMPAT_%(eval $(%{__perl} -V:version); echo $version))
Requires(pre):  shadow-utils
AutoReqProv:    no

%description
Gitolite allows a server to host many git repositories and provide access
to many developers, without having to give them real userids on the server.
The essential magic in doing this is ssh's pubkey access and the authorized
keys file, and the inspiration was an older program called gitosis.

Gitolite can restrict who can read from (clone/fetch) or write to (push) a
repository. It can also restrict who can push to what branch or tag, which
is very important in a corporate environment. Gitolite can be installed
without requiring root permissions, and with no additional software than git
itself and perl. It also has several other neat features described below and
elsewhere in the doc/ directory.


%prep
%setup -qn gitolite-%{version}

%build
#This page intentionally left blank.

%install
rm -rf $RPM_BUILD_ROOT

# Directory structure
install -d $RPM_BUILD_ROOT%{gitolite_homedir}
install -d $RPM_BUILD_ROOT%{gitolite_homedir}/.ssh
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{perl_vendorlib}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

# Code
cp -pr src/lib/Gitolite $RPM_BUILD_ROOT%{perl_vendorlib}
echo "%{version}-%{release}" >src/VERSION
cp -a src/* $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s %{_datadir}/%{name}/gitolite $RPM_BUILD_ROOT%{_bindir}/gitolite
ln -s %{_datadir}/%{name}/gitolite-shell $RPM_BUILD_ROOT%{_bindir}/gitolite-shell

# empty authorized_keys file
touch $RPM_BUILD_ROOT%{gitolite_homedir}/.ssh/authorized_keys


%pre
getent group %{os_user} >/dev/null || groupadd -r %{os_user}
getent passwd %{os_user} >/dev/null || \
useradd -r -g %{os_user} -d %{gitolite_homedir} -s /bin/sh \
        -c "git repository hosting" %{os_user}
exit 0

%post
cat <<EOF
Please perform the following post-install setup
1)  run "su - %{os_user}" to get a login shell on the gitolite
    user
2)  run "gitolite setup -a admin ." where admin is your gitolite admin
username.

On whatever machine your key came from (maybe your
workstation or another account on the same server):

3)  run "git clone gitolite@<name.or.ip>:gitolite-admin" to
    start adding users and repos.

EOF

%files
%{_bindir}/*
%{perl_vendorlib}/*
%{_datadir}/%{name}
# make homedir non world readable
%attr(750,%{os_user},%{os_user}) %dir %{gitolite_homedir}
%attr(750,%{os_user},%{os_user}) %dir %{gitolite_homedir}/.ssh
%config(noreplace) %attr(640,%{os_user},%{os_user}) %{gitolite_homedir}/.ssh/authorized_keys
%doc COPYING README.markdown CHANGELOG


%changelog
* Wed Oct 29 2014 Justin Zhang <schnell18@gmail.com> - 1:3.6.1-1
- Set git user home directory to /var/lib/gitolite3

* Wed Oct 23 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.5.3.1-1
- Latest upstream.

* Wed Oct 16 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.5.3-1
- Latest upstream.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:3.5.2-2
- Perl 5.18 rebuild

* Wed Jul 10 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.5.2-1
- Latest upstream.

* Thu Mar 28 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.5.1-1
- Latest upstream.

* Mon Mar 25 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.5-1
- Latest upstream.

* Tue Mar 05 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.4-1
- Latest upstream.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Jon Ciesla <limburgher@gmail.com> - 1:3.3-1
- Latest upstream.

* Mon Nov 19 2012 Jon Ciesla <limburgher@gmail.com> - 1:3.2-1
- Latest upstream.

* Wed Oct 10 2012 Jon Ciesla <limburgher@gmail.com> - 1:3.1-1
- 3.1, rewuiring Epoch bump.

* Tue Oct 09 2012 Jon Ciesla <limburgher@gmail.com> - 3.04-4
- Patch for directory traversal bug.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 3.04-2
- Perl 5.16 rebuild

* Wed Jun 27 2012 Jon Ciesla <limburgher@gmail.com> - 3.04-1
- Latest upstream, docs now includable.

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 3.03-3
- Perl 5.16 rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 3.03-2
- Perl 5.16 rebuild

* Wed May 23 2012 Jon Ciesla <limburgher@gmail.com> - 3.03-1
- Latest upstream.

* Mon May 21 2012 Jon Ciesla <limburgher@gmail.com> - 3.02-1
- Latest upstream.

* Tue May 15 2012 Jon Ciesla <limburgher@gmail.com> - 3.01-2
- Added license file, fixed duplicate files, dropped defattr.
- Dropped clean and buildroot.
- Added script to generate tarball in comments.

* Thu May 03 2012 Jon Ciesla <limburgher@gmail.com> - 3.01-1
- Initial packaging based on gitolite 2.3-2.
