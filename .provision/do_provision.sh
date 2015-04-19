function install_pre_requisite_warez() {
    yum install -y gcc rpm-build
}

function setup_rpmbuild_env() {
    # setup rpmbuild macros by copying /tmp/macros.rpmbuild
    # which is provisioned by the file provisioner, to /etc/rpm
    mkdir -p /home/devel/rpmbuild/{SOURCES,SPECS,SRPMS,RPMS,BUILD}
    mv /tmp/macros.rpmbuild /etc/rpm
    chmod 664 /etc/rpm/macros.rpmbuild
    chown root:root /etc/rpm/macros.rpmbuild
}

########## MAIN BLOCK ##########
echo "Make sure pre-requisite softwares are installed..."
install_pre_requisite_warez
echo "Setting up rpmbuild environment..."
setup_rpmbuild_env

# vim: set ai nu nobk expandtab sw=4 tw=72 ts=4 syntax=sh :
