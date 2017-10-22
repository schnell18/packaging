Name:       nicstat
Version:    1.95
Release:    1%{?dist}
Summary:    Print network traffic statistics
Group:      System Environment/Daemons
License:    Artistic
URL:        https://sourceforge.net/projects/nicstat/
BuildRequires: glibc-devel
Source0:    %{name}-%{version}.tar.gz
Source1:    Makefile


%description
Prints out network statistics for all network cards (NICs), including
packets, kilobytes per second, average packet sizes and more

%prep
%setup -q
cp %{SOURCE1} %{_builddir}/%{name}-%{version}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -d 755 %{buildroot}%{_bindir}
install -d 755 %{buildroot}%{_mandir}/man1
install -m 755 -p nicstat %{buildroot}%{_bindir}
install -m 755 -p enicstat %{buildroot}%{_bindir}
install -m 444 -p nicstat.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(4511, root, root) %{_bindir}/nicstat
%attr(755, root, root) %{_bindir}/enicstat
%doc %{_mandir}/man1/nicstat.1.gz

%changelog
* Sun Oct 22 2017 Justin Zhang <schnell18[AT]gmail.com> - 1.95-1
- version 1.95
- Create RPM packaging files
