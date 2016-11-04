Summary: Kafka is a distributed publish/subscribe messaging system
Name: kafka
Version: 0.10.1.0
Release: 1%{?dist}
Group: Applications/Internet
License: Apache (v2)
Source0: kafka-%{version}.tgz
Source1: kafka.init
Source2: kafka.sysconfig
URL: http://kafka.apache.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Distribution: Niels Basjes
Packager: Justin Zhang <schnell18@gmail.com>

Requires: java >= 1.6
Requires(pre): shadow-utils
Requires: zookeeper >= 3.3.4

%description
It is designed to support the following

Persistent messaging with O(1) disk structures that provide constant
time performance even with many TB of stored messages.  High-throughput:
even with very modest hardware Kafka can support hundreds of thousands
of messages per second.  Explicit support for partitioning messages over
Kafka servers and distributing consumption over a cluster of consumer
machines while maintaining per-partition ordering semantics.  Support
for parallel data load into Hadoop.  Kafka is aimed at providing a
publish-subscribe solution that can handle all activity stream data and
processing on a consumer-scale web site. This kind of activity (page
views, searches, and other user actions) are a key ingredient in many of
the social feature on the modern web. This data is typically handled by
"logging" and ad hoc log aggregation solutions due to the throughput
requirements. This kind of ad hoc solution is a viable solution to
providing logging data to an offline analysis system like Hadoop, but is
very limiting for building real-time processing. Kafka aims to unify
offline and online processing by providing a mechanism for parallel load
into Hadoop as well as the ability to partition real-time consumption
over a cluster of machines.

See our web site for more details on the project.
(http://kafka.apache.org/)

%pre

# Create user and group
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || \
    useradd -r -g kafka -d /var/lib/kafka -s /bin/bash \
    -c "Kafka Account" kafka


exit 0

%preun
service kafka stop

%prep

%setup

%build
# Build package

%install

# Clean out any previous builds not on slash
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}/var/lib/%{name}
%{__cp} -R * %{buildroot}/var/lib/%{name}
rm -fr %{buildroot}/var/lib/%{name}/site-docs
rm -fr %{buildroot}/var/lib/%{name}/bin/windows
%{__mkdir_p} %{buildroot}/var/log/%{name}
%{__mkdir_p} %{buildroot}/etc/rc.d/init.d
%{__mkdir_p} %{buildroot}/etc/sysconfig
install -m 755 %{S:1} %{buildroot}/etc/rc.d/init.d/%{name}
install -m 755 %{S:2} %{buildroot}/etc/sysconfig/%{name}

# Simply create this oneliner in the spec file
%{__mkdir_p} %{buildroot}/etc/profile.d/
echo 'export PATH=${PATH}:/var/lib/kafka/bin' > %{buildroot}/etc/profile.d/kafka.sh

%files
%defattr(-,kafka,kafka)

%config /var/lib/%{name}/config
/var/lib/%{name}
/var/log/%{name}
/etc/rc.d/init.d/%{name}
/etc/sysconfig/%{name}
/etc/profile.d/kafka.sh

%clean
#used to cleanup things outside the build area and possibly inside.
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%changelog
* Fri Nov 4 2016 Justin Zhang<schnell18@gmail.com>
- Make FHS compliant
* Mon Sep 16 2013 Niels Basjes <kafka@basjes.nl>
- Refactoring the scripting
* Fri Mar 15 2013 Mark Poole <mpoole@apache.org>
- First build
