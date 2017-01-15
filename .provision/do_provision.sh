function enable_local_repo {
# install nginx yum repo
cat <<'EOF' > /etc/yum.repos.d/nginx.repo
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
EOF
}

function config_nginx {
cat <<'EOF' > /etc/nginx/conf.d/yum.conf
server {
    listen 80;
    server_name 192.168.33.40;

    location / {
        root         /var/www/yum;
        autoindex    on;
        access_log   /var/log/nginx/access_yum.log;
        error_log    /var/log/nginx/error_yum.log error;
        expires      30d;
    }

}
EOF
}

function install_pre_requisite_warez() {
    yum install -y gcc rpm-build
}

function setup_rpmbuild_env() {
    # setup rpmbuild macros by copying /tmp/macros.rpmbuild
    # which is provisioned by the file provisioner, to /etc/rpm
    mkdir -p /home/devel/rpmbuild/{SOURCES,SPECS,SRPMS,RPMS,BUILD}
    chown -R devel:devel /home/devel/rpmbuild
    mv /tmp/macros.rpmbuild /etc/rpm
    chmod 664 /etc/rpm/macros.rpmbuild
    chown root:root /etc/rpm/macros.rpmbuild
}

function setup_rpmbot_repo() {
    if [[ ! -f /etc/yum.repos.d/nginx.repo ]]; then
        enable_local_repo
    fi

    # check if nginx is installed
    rpm -q                                           \
        --queryformat "%{name} %{version} installed" \
        nginx
    if [[  $? != 0 ]]; then
        yum install -y nginx createrepo
    fi

    yum install -y nginx
    chkconfig --level 345 nginx on
    if [[ ! -f /etc/nginx/conf.d/yum.conf ]]; then
        if [[ ! -d /var/www/yum ]]; then
            mkdir -p /var/www/yum
        fi
        config_nginx
    fi
    service nginx start
}

########## MAIN BLOCK ##########
echo "Make sure pre-requisite softwares are installed..."
install_pre_requisite_warez
echo "Setting up rpmbuild environment..."
setup_rpmbuild_env
echo "Setting up rpmbot yum repo..."
setup_rpmbot_repo
# vim: set ai nu nobk expandtab sw=4 tw=72 ts=4 syntax=sh :
