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
This spec file is based [tischda][1] and refactor to support build on
both 32 and 64 bit machines. Major changes are:
- Use %ifarch to support 32 and 64 bit architectures
- Install to /usr/activemq instead of /usr/share/activemq
- Move data directory to /var/lib/activemq/data
- Make /var/lib/activemq home direcotry of user activemq
- Enhance post-install scriptlet
- Cleaner code

[1]: https://github.com/tischda/almira-rpm/tree/master/packages/apache-activemq


