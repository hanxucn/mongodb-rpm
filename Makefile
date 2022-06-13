.ONESHELL:

SHELL := /bin/bash

NAME					:= mongod
CURRENT_BASE_VERSION	:= 1.8
PRE_BASE_VERSION		:= 1.6

WORKSPACE_PATH			:= $(shell realpath .)
DIST_PATH				:= $(WORKSPACE_PATH)/dist

UBUNTU_16_X8664_IMG		:= docker.io/library/ubuntu:16.04
UBUNTU_16_ARM64_IMG		:= arm64v8/ubuntu:16.04
UBUNTU_18_X8664_IMG		:= docker.io/library/ubuntu:18.04
UBUNTU_18_ARM64_IMG		:= arm64v8/ubuntu:18.04
BUILDER_X86_IMG			:= harbor.smartx.com/mongoup-builder:v0.1
BUILDER_ARM64_IMG		:= harbor.smartx.com/mongoup-builder-arm64:v0.1
CENTOS7_X8664_IMG		:= harbor.smartx.com/pyzbs_ci/centos:7.2.1511
CENTOS7_ARM64_IMG		:= harbor.smartx.com/pyzbs_ci/centos-arm64:7

# command variables
DOCKER_RUN				?= docker run --rm --network host -v $(WORKSPACE_PATH):$(WORKSPACE_PATH) -w $(WORKSPACE_PATH)


.PHONY:	pre_base_image
pre_base_image:
	docker build -t localhost/mongodb-base:$(PRE_BASE_VERSION) -f Dockerfile.base16 .


.PHONY: current_base_image
current_base_image:
	docker build -t localhost/mongodb-base:$(CURRENT_BASE_VERSION) -f Dockerfile.base18 .


.PHONY: amd64_pre_rpm
amd64_pre_rpm:
	docker build \
		--network host \
		--build-arg NAME=$(NAME) \
		--build-arg RELEASE=1 \
		--build-arg BASE_VERSION=16 \
		--build-arg RPM_TYPE=pre \
		-t $(BUILDER_X86_IMG) \
		-f docker/Dockerfile.x86_64 .

	echo "Copy rpm from docker image to workspace"
	$(DOCKER_RUN) $(BUILDER_X86_IMG) cp -rf /root/rpmbuild/RPMS $(DIST_PATH)

.PHONY: arm64_pre_rpm
arm64_pre_rpm:
	docker build \
		--network host \
		--build-arg NAME=$(NAME) \
		--build-arg RELEASE=1 \
		--build-arg BASE_VERSION=16 \
		--build-arg RPM_TYPE=pre \
		-t $(BUILDER_ARM64_IMG) \
		-f docker/Dockerfile.arm64 .

	echo "Copy rpm from docker image to workspace"
	$(DOCKER_RUN) $(BUILDER_ARM64_IMG) cp -rf /root/rpmbuild/RPMS $(DIST_PATH)

.PHONY: amd64_current_rpm
amd64_current_rpm:
	docker build \
		--network host \
		--build-arg NAME=$(NAME) \
		--build-arg RELEASE=1 \
		--build-arg BASE_VERSION=18 \
		--build-arg RPM_TYPE=current \
		-t $(BUILDER_X86_IMG) \
		-f docker/Dockerfile.x86_64 .

	echo "Copy rpm from docker image to workspace"
	$(DOCKER_RUN) $(BUILDER_X86_IMG) cp -rf /root/rpmbuild/RPMS $(DIST_PATH)

.PHONY: arm64_current_rpm
arm64_current_rpm:
	docker build \
		--network host \
		--build-arg NAME=$(NAME) \
		--build-arg RELEASE=1 \
		--build-arg BASE_VERSION=18 \
		--build-arg RPM_TYPE=current \
		-t $(BUILDER_ARM64_IMG) \
		-f docker/Dockerfile.arm64 .

	echo "Copy rpm from docker image to workspace"
	$(DOCKER_RUN) $(BUILDER_ARM64_IMG) cp -rf /root/rpmbuild/RPMS $(DIST_PATH)
