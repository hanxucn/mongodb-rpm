#!/usr/bin/env bash

base_version=$1
rpm_type=$2
arch=$3

mkdir -p SOURCE
mkdir -p /usr/share/mongodb/base

podman build -t mongodb-base:$base_version -f Dockerfile.base${base_version} .

podman save --compress --format oci-archive -o /usr/share/mongodb/base/podman-mongodb-base-${base_version}.tar.gz localhost/mongodb-base:${base_version}


rpmbuild --verbose \
         --define "_topdir `pwd`" \
         --define "_name mongod" \
         --define "_release 1" \
         --define "base_version $base_version" \
         --bb ./mongodb-${rpm_type}.spec
