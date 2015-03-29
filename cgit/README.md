# Introduction
This git spec is based [the copy of fedora project][1]. The purpose of
this clone is to cut down unnecessary documentation files to make cgit
as small as possible in order to produce the smallest docker image.

And the rpmbuild automatic dependency scan is too strict on the Perl
script shipped by cgit. We should ignore this dependency by adding:

    %filter_from_requires /^perl(Digest::MD5)/d
    %filter_setup

This will modify the find requires command at runtime to:

    Finding  Requires: /bin/sh -c "  while read FILE; do /usr/lib/rpm/rpmdeps -R ${FILE}; done | /bin/sort -u  | /bin/sed -e '/^perl(Digest::MD5)/d'"

# Instructions to get latest pristine source
As of the spec for cgit 0.11.2, we need git 2.3.4. The commands to
download cgit and git are listed as follows:

    # get pristine source of Git 2.3.4
    curl https://www.kernel.org/pub/software/scm/git/git-2.3.4.tar.xz \
         -o git-2.3.4.tar.xz
    # get pristine source of cgit 0.11.2
    curl http://git.zx2c4.com/cgit/snapshot/cgit-0.11.2.tar.xz \
         -o cgit-0.11.2.tar.xz

[1]: http://pkgs.fedoraproject.org/cgit/cgit.git/
