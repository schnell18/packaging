# Instruction to build RPM
This document is a brief description of how to build Apache ActiveMQ
RPM from scratch.

## RPM build setup
Make sure you have rpmbuild tool installed before attempting to build
the RPM. You can check if rpmbuild is available by running the following
command:

    rpm -q rpm-build

You can run the command below to install the rpmbuild tool:

    sudo yum install -y rpm-build

Then you create the directory layout for RPM build by using the
following command:

    mkdir -p ~/rpmbuild/{BUILD,RPMS,S{OURCE,PEC,RPM}S}

## Get prinstine source of ActiveMQ
Download the tarball distribution of ActiveMQ from Apache website or
mirrors. Then move the tarball into ~/rpmbuild/SOURCES. Here is the
sample commands to accomplish this goal:

    cd ~/rpmbuild/SOURCES
    wget http://apache.dataguru.cn/activemq/5.10.0/apache-activemq-5.10.0-bin.tar.gz

## Get spec file and patch for ActiveMQ
Then you download the the spec file and patch from this page or clone
this repository to your computer. You copy the SOURCES/activemq-rpm.patch 
to the ~/rpmbuild/SOURCES directory. And copy the SPECS/activemq.spec to
~/rpmbuild/SPECS. The patch is only tested ok with ActiveMQ 5.10.0. It
might work with 5.9.x as well.

After you complete above steps, the directory layout under ~/rpmbuild
looks like this:

    ~/rpmbuild
    ├── BUILD
    ├── RPMS
    ├── SRPMS
    ├── SOURCES
    │   ├── activemq-rpm.patch
    │   └── apache-activemq-5.10.0-bin.tar.gz
    └── SPECS
        └── activemq.spec

## Run the rpmbuild
You are now ready to kick off the build. You follow these command to
initiate the build:

    cd ~/rpmbuild/SPECS
    rpmbuild -ba activemq.spec

After the build is completed, you can find the result rpm under
~/rpmbuild/RPMS/i686 (on 32 bit OS) or ~/rpmbuild/RPMS/x86\_64 (on 64
bit OS).


# spec file changes
This spec file is based [tischda][1] and refactored to make activemq
follow common Linux convention and to support build on both 32 and 64
bit machines. Major changes are:
- Use %ifarch to support 32 and 64 bit architectures
- Install to /usr/activemq instead of /usr/share/activemq
- Move data directory to /var/lib/activemq/data
- Move logs to /var/log/activemq
- Make /var/lib/activemq home direcotry of user activemq
- Enhance post-install scriptlet
- Cleaner code

# Issues resolved
## Issue 1: rpmbuild fails on build id note absence
### symptom
The rpmbuild of the [original spec file][1] emits error message like: 

    extracting debug info from /home/justin/rpmbuild/BUILDROOT/apache-activemq-5.10.0-1.el6.i386/usr/share/activemq/bin/linux-x86-32/wrapper
    *** ERROR: No build ID note found in /home/justin/rpmbuild/BUILDROOT/apache-activemq-5.10.0-1.el6.i386/usr/share/activemq/bin/linux-x86-32/wrapper
    error: Bad exit status from /var/tmp/rpm-tmp.bvvcqU (%install)

And the build fails.

### cause
The wrapper binary shipped by Apache does not have build id note. However,
the rpmbuild mandates the build id and fails the build on absence.

### resolution
The fix is set the "_missing_build_ids_terminate_build" which was
introduced in this [ticket][2] like this:

    %undefine _missing_build_ids_terminate_build

Someone suggests:

    %global _missing_build_ids_terminate_build 0

but it does not work as the command to extract debug info is defined as:

%global __debug_install_post                                 \
    %{_rpmconfigdir}/find-debuginfo.sh                       \
    %{?_missing_build_ids_terminate_build:--strict-build-id} \
    %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"  \
    %{nil}

even if the _missing_build_ids_terminate_build is zero the expression
%?{_missing_build_ids_terminate_build} still evaluates to true

### tips
Running "rpm --showrc" displays all macro definitions, which is a great
aid to diagnose the rpmbuild errors.

## Issue 2: unnecesary jar repack
### symptom
brp-java-repack-jars takes too long to complete

### cause
Running this program is inherently slow according to [this blog][3].
There is no negative impact if the jar repack is not perform so long as
the jars have no jni DSO and are not compiled using GCJ.

### resolution
Re-define the following marco in the spec to disable jar repack:

    %define __jar_repack %{nil}

[1]: https://github.com/tischda/almira-rpm/tree/master/packages/apache-activemq
[2]: https://bugzilla.redhat.com/show_bug.cgi?id=279871
[3]: http://swaeku.github.io/blog/2013/08/05/how-to-disable-brp-java-repack-jars-during-rpm-build/
