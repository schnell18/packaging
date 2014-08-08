# Introduction
This packages the nice-looking [bash-git-prompt][1] into an RPM to ease
the installation.

This package will automatically enable the git prompt in bash after
install. It will disable the git prompt accordingly after uninstall.

# Instruction to build the rpm
* clone the this repository
* copy the SPECS/bash-git-prompt.spec to ~/rpmbuild/SPECS
* change directory to ~/rpmbuild/SOURCES
* download upstream source from [bash-git-prompt github][1]
* change directory to ~/rpmbuild/SPECS
* run "rpmbuild -ba bash-git-prompt.spec"
* enjoy the rpm

[1]: https://github.com/magicmonty/bash-git-prompt.git
