# Introduction
This git spec is based [the copy of fedora project][1]. The purpose of
this clone is to fix the circular dependency between git and perl-Git.

# Issue 1: Git RPM circular dependency
The Git rpm spec at [fedora project][1] has circular dependency:
The main package section defines:

    Requires:       less
    Requires:       openssh-clients
    Requires:       perl(Error)
    Requires:       perl(Term::ReadKey)
    Requires:       perl-Git = %{version}-%{release}
    Requires:       rsync
    Requires:       zlib >= 1.2

And the 'perl-Git' sub pacakge also defines:

    %package -n perl-Git
    Summary:        Perl interface to Git
    Group:          Development/Libraries
    %if %{noarch_sub}
    BuildArch:      noarch
    %endif
    Requires:       git = %{version}-%{release}
    BuildRequires:  perl(Error), perl(ExtUtils::MakeMaker)
    Requires:       perl(Error)


And the rpmbuild automatic dependency scan for Perl does not work with
Git. Git include contrib Perl script that use the Git.pm. But that does
not mandate a dependency on perl(Git). We need filter this dependency by
adding:

    %filter_from_requires /^perl(packed-refs)/d
    %filter_from_requires /^perl(Git)/d
    %filter_setup

This will modify the find requires command at runtime to:

    Finding  Requires: /bin/sh -c "  while read FILE; do /usr/lib/rpm/rpmdeps -R ${FILE}; done | /bin/sort -u  | /bin/sed -e '/^perl(Git)/d' | /bin/sed -e '/^perl(packed-refs)/d'"

Please reference [this post][2] and [this][3] for more details.
[Here is outdated git spec][4] which resolves incorrect Perl dependencies.

# Issue 2: asciidoc package is absent on RHEL 6.5
The asciidoc is required to build the git 2.0.4 rpm. However, it does
not seem to exist in the official RHEL 6.5 repository. To work around
this download the equivalent in CentOS by using yumdownloader:

    yumdownloader asciidoc
    scp asciidoc-xxx-noarch.rpm <your_rhel65_host>

The yumdownloader is part of yumutils package.  If you do not have it
installed, run this command:

    yum install -y yumutils.noarch

# Issue 3: emacs-git rpm build on RHEL 6.5
## Symptom
Rebuild the source RPM on RHEL 6.5 64 bit gets:

    + make -C contrib/emacs
    make: Entering directory `/root/rpmbuild/BUILD/git-2.0.4/contrib/emacs'
    emacs -batch -f batch-byte-compile git.el
    emacs: error while loading shared libraries: libotf.so.0: cannot open shared object file: No such file or directory
    make: *** [git.elc] Error 127
    make: Leaving directory `/root/rpmbuild/BUILD/git-2.0.4/contrib/emacs'
    error: Bad exit status from /var/tmp/rpm-tmp.EjjQw0 (%build)

## Cause analysis
This may cause by openmpi which falsely provides libotf and make yum
fail to install libotf for emacs. See this [defect report][5] for more
details.

## Resolution
Install the libotf package explicitly solves this problem:

    sudo yum install libotf

[1]: http://pkgs.fedoraproject.org/cgit/git.git/tree/git.spec?h=f21
[2]: http://superuser.com/questions/518211/how-do-i-turn-off-the-perl-specific-parts-of-find-requires-when-building-an-rpm
[3]: http://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
[4]: https://github.com/repoforge/rpms/blob/master/specs/git/git.spec
[5]: https://bugzilla.redhat.com/show_bug.cgi?id=806031
