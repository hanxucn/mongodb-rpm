%define debug_package %{nil}
%define _unpackaged_files_terminate_build 0

Name:    mongodb-server
Version: 5.0.6
Release: %{_release}.smartx
Summary: %{_name}
License: SMARTX
URL:     http://www.smartx.com

Source0: mongo-binary-4.2.19.tar.gz
Source1: mongo-binary-4.4.13.tar.gz
Source2: mongo-binary-5.0.6.tar.gz
Source3: %{_name}.service
Source4: logrotate.conf
Source5: %{_name}.conf
Source6: podman-mongodb-base-%{base_version}.tar.gz

Requires:   podman

%description
mongodb-server

%prep
#%setup -q

%install

install -d -m 777 %{buildroot}%{_localstatedir}/log/mongodb
install -d -m 755 %{buildroot}%{_sharedstatedir}/mongodb

install -d -m 755 %{buildroot}%{_datadir}/mongodb/binary/
install -c -m 755 %{SOURCE0} %{buildroot}%{_datadir}/mongodb/binary/
install -c -m 755 %{SOURCE1} %{buildroot}%{_datadir}/mongodb/binary/
install -c -m 755 %{SOURCE2} %{buildroot}%{_datadir}/mongodb/binary/

install -d -m 755 %{buildroot}%{_unitdir}
install -c -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{_name}.service

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -c -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/mongodb

install -c -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/%{_name}.conf

install -d -m 755 %{buildroot}%{_datadir}/mongodb/base/
install -c -m 755 %{SOURCE6} %{buildroot}%{_datadir}/mongodb/base/podman-mongodb-base-%{base_version}.tar.gz

touch %{buildroot}%{_localstatedir}/log/mongodb/mongod.log
%post

if [ $1 -eq 1 ]; then
    # install
    /bin/systemctl daemon-reload

    podman load < %{_datadir}/mongodb/base/podman-mongodb-base-%{base_version}.tar.gz
    mkdir -p /opt/mongodb/5.0.6/
    tar xzf %{_datadir}/mongodb/binary/mongo-binary-5.0.6.tar.gz -C /opt/mongodb/5.0.6/
    sed -i 's/mongo_version/5.0.6/g' %{_unitdir}/%{_name}.service
    sed -i 's/base_version/%{base_version}/g' %{_unitdir}/%{_name}.service
fi

if [ $1 -eq 2 ]; then
    # upgrade

    old_images=($(podman images localhost/mongodb-base --format '{{ .ID }}'))
    for old_image in "${old_images[@]}"; do
        podman rmi -f $old_image
    done
    podman load < %{_datadir}/mongodb/base/podman-mongodb-base-%{base_version}.tar.gz

    mongo_current=(4.2.19 4.4.13 5.0.6)
    for mongo_v in "${mongo_current[@]}"; do
        mkdir -p /opt/mongodb/${mongo_v}/
        tar xzf %{_datadir}/mongodb/binary/mongo-binary-${mongo_v}.tar.gz -C /opt/mongodb/${mongo_v}/
    done
    sed -i 's/base_version/%{base_version}/g' %{_unitdir}/%{_name}.service
fi


%preun
if [ $1 -eq 0 ]; then
    # uninstall
    /bin/systemctl disable %{_name}.service
    /bin/systemctl stop %{_name}.service
    old_images=($(podman images localhost/mongodb-base --format '{{ .ID }}'))
    for old_image in "${old_images[@]}"; do
        podman rmi -f $old_image
    done
fi


%files
%defattr(-,root,root,-)
#%attr(0777,100999,100999) %{_localstatedir}/log/mongodb
#%attr(0755,100999,100999) %{_sharedstatedir}/mongodb
%{_unitdir}/%{_name}.service
%{_datadir}/mongodb/binary/mongo-binary-4.2.19.tar.gz
%{_datadir}/mongodb/binary/mongo-binary-4.4.13.tar.gz
%{_datadir}/mongodb/binary/mongo-binary-5.0.6.tar.gz
%{_datadir}/mongodb/base/podman-mongodb-base-%{base_version}.tar.gz
%{_sysconfdir}/logrotate.d/mongodb
%{_sharedstatedir}/mongodb
%config(noreplace) %{_sysconfdir}/%{_name}.conf
