%define debug_package %{nil}
%define _unpackaged_files_terminate_build 0

Name:    %{name}
Version: %{_version}
Release: %{_release}.el7.smartx
Summary: %{name}
License: SMARTX
URL:     http://www.smartx.com

Source0: podman-mongodb-base.%{_version}.aarch64.tar.gz


%description
mongodb base image


%prep
#%setup -q

%install

install -d -m 755 %{buildroot}%{_datadir}/mongodb
install -c -m 755 %{SOURCE0} %{buildroot}%{_datadir}/mongodb/podman-mongodb-base.%{_version}.aarch64.tar.gz

%post

if [ $1 -eq 1 ]; then
    # install

    podman load < %{_datadir}/mongodb/podman-mongodb-base.%{_version}.aarch64.tar.gz
fi

if [ $1 -eq 2 ]; then
    # upgrade
    image_id=$(podman images -a | grep localhost/mongodb-base | awk '{print $3}')
    podman rmi -f $image_id
    podman load < %{_datadir}/mongodb/podman-mongodb-base.%{_version}.aarch64.tar.gz
fi


%preun
if [ $1 -eq 0 ]; then
    # uninstall
    image_id=$(podman images -a | grep localhost/mongodb-base | awk '{print $3}')
    podman rmi -f $image_id
fi


%files
%{_datadir}/mongodb/podman-mongodb-base.%{_version}.aarch64.tar.gz
