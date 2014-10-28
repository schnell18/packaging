Introduction
============

Collections of customized or home-brew spec files for some open source
softwares.

RPM spec catalog
================

* fcgiwrap:  spec file to install and enable fcgiwrap as a systemd service
* gitolite3: repack to remove the SVN dependency and use 'git' as hosting user
* pure-fptd: repack to enable upload script and use upstream version 1.0.36
* ngix:      repack to enable LDAP authentication via nginx-auth-ldap
* activemq:  repack activemq 5.10.0
* git:       repack git 2.1.0(based on fedora 21), fix circular dependencies
* bash-git-prompt: create RPM package for the nice-looking [bash-git-prompt][1]
* redis:     upgrade to redis 2.8.17 based on the spec file from fedora project

Regenerate the RPM
==================
To regenerate the RPM, you first down the source rpm in the SOURCES
directory and type command like:

    rpmbuild --rebuild <src_rpm_file>

The generated RPM is located at ~/rpmbuild/RPMS/{x86\_64,i686}/.

[1]: https://github.com/magicmonty/bash-git-prompt
