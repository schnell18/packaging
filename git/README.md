# Git RPM circular dependency
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

Please reference [this post][2] and [this][3] for more details.
[Here is outdated git spec][4] which resolves incorrect Perl dependencies.

[1]: http://pkgs.fedoraproject.org/cgit/git.git/tree/git.spec?h=f21
[2]: http://superuser.com/questions/518211/how-do-i-turn-off-the-perl-specific-parts-of-find-requires-when-building-an-rpm
[3]: http://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
[4]: https://github.com/repoforge/rpms/blob/master/specs/git/git.spec
