Introduction
============

Collections of customized or home-brew spec files for some open source
softwares. This project includes a Vagrantfile to facilitate preparation
of RPM build environment. The vagrant box is built from a minimal CentOS
7 image. The exact instructions to build this box are located at [the
vmbot github project][1]

RPM spec catalog
================

* fcgiwrap:  spec file to install and enable fcgiwrap as a systemd service
* gitolite3: repack to remove the SVN dependency and use 'git' as hosting user
* pure-fptd: repack to enable upload script and use upstream version 1.0.36
* ngix:      repack to enable LDAP authentication via nginx-auth-ldap
* activemq:  repack activemq 5.10.0
* git:       repack git 2.3.4(based on fedora 21), fix circular dependencies
* cgit:      repack cgit 2.1.0(based on epel7), cut down docs for docker
* bash-git-prompt: create RPM package for the nice-looking [bash-git-prompt][2]
* redis:     upgrade to redis 2.8.17 based on the spec file from fedora project
* sonarqube: spec file to install SonarQube out-of-box

Regenerate the RPM
==================
To regenerate the RPM, you first down the source rpm in the SOURCES
directory and type command like:

    rpmbuild --rebuild <src_rpm_file>

The generated RPM is located at ~/rpmbuild/RPMS/{x86\_64,i686}/.

Issues
======
Sonar temp directory not writable:

    2014.12.16 23:31:11 INFO  app[o.s.p.m.JavaProcessLauncher] Launch
    process[search]:
    /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.71.x86_64/jre/bin/java
    -Djava.awt.headless=true -Xmx256m -Xms256m -Xss256k
    -Djava.net.preferIPv4Stack=true -XX:+UseParNewGC -XX:+UseConcMarkSweepGC
    -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly
    -XX:+HeapDumpOnOutOfMemoryError -Djava.io.tmpdir=/usr/share/sonar/temp
    -cp ./lib/common/*:./lib/search/* org.sonar.search.SearchServer
    /tmp/sq-process3858771298897868443properties
    Exception in thread "main" java.lang.IllegalStateException: Temp
    directory is not writable: /usr/share/sonar/temp
        at
    org.sonar.process.MinimumViableSystem.checkWritableDir(MinimumViableSystem.java:60)
        at
    org.sonar.process.MinimumViableSystem.checkWritableTempDir(MinimumViableSystem.java:52)
        at
    org.sonar.process.MinimumViableSystem.check(MinimumViableSystem.java:45)
        at org.sonar.search.SearchServer.<init>(SearchServer.java:63)
        at org.sonar.search.SearchServer.main(SearchServer.java:260)
    Caused by: java.io.IOException: Permission denied

sonar is not FHS friendly, the code assume the sonar home dir is
writable which is not true for RPM managed Java application
The embedded tomcat web server does not follow symbol link by default.
Add a context.xml to META-INF sub folder w/ following context resolves
the problem:

    <?xml version="1.0" encoding="UTF-8"?>
    <Context path="/" allowLinking="true"/>
    </Context>

[1]: https://github.com/schnell18/vmbot.git
[2]: https://github.com/magicmonty/bash-git-prompt
