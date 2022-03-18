%define debug_package %{nil}
%define _unpackaged_files_terminate_build 0

Name:    mongodb-server
Version: %{_version}
Release: %{_release}.el7.smartx
Summary: %{_name}
License: SMARTX
URL:     http://www.smartx.com

Source0: mongo-binary.%{_version}.tar.gz
Source1: %{_name}.service
Source2: logrotate.conf
Source3: %{_name}.conf

Requires:   mongodb-base%{ubuntu_version}

%description
mongodb-server

%prep
#%setup -q

%install

install -d -m 777 %{buildroot}%{_localstatedir}/log/mongodb
install -d -m 755 %{buildroot}%{_sharedstatedir}/mongodb

install -d -m 755 %{buildroot}%{_datadir}/mongodb
install -c -m 755 %{SOURCE0} %{buildroot}%{_datadir}/mongodb/

install -d -m 755 %{buildroot}%{_unitdir}
install -c -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{_name}.service

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -c -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/mongodb

install -c -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{_name}.conf

touch %{buildroot}%{_localstatedir}/log/mongodb/mongod.log
%post

if [ $1 -eq 1 ]; then
    # install
    /bin/systemctl daemon-reload
    mkdir -p /opt/mongodb/%{_version}/
    tar xzf %{_datadir}/mongodb/mongo-binary.%{_version}.tar.gz -C /opt/mongodb/%{_version}/
    sed -i 's/mongo_version/%{_version}/g' %{_unitdir}/%{_name}.service
    sed -i 's/base_version/%{ubuntu_version}/g' %{_unitdir}/%{_name}.service
fi

if [ $1 -eq 2 ]; then
    # upgrade
    mkdir -p /opt/mongodb/%{_version}/
    tar xzf %{_datadir}/mongodb/mongo-binary.%{_version}.tar.gz -C /opt/mongodb/%{_version}/
    sed -i 's/mongo_version/%{_version}/g' %{_unitdir}/%{_name}.service
    sed -i 's/base_version/%{ubuntu_version}/g' %{_unitdir}/%{_name}.service
fi


%preun
if [ $1 -eq 0 ]; then
    # uninstall
    /bin/systemctl disable %{_name}.service
    /bin/systemctl stop %{_name}.service
fi


%files
%defattr(-,root,root,-)
%attr(0777,mongodb,root) %{_localstatedir}/log/mongodb
%attr(0755,mongodb,root) %{_sharedstatedir}/mongodb
%{_unitdir}/%{_name}.service
%{_datadir}/mongodb
%{_sysconfdir}/logrotate.d/mongodb
%{_sharedstatedir}/mongodb
%config(noreplace) %{_sysconfdir}/%{_name}.conf
