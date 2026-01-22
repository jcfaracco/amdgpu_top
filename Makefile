srpm:
	#dnf install -y rpmdevtools git
	git remote add upstream https://github.com/Umio-Yasuno/amdgpu_top.git
	git fetch --tags upstream
	$(eval TAG := $(shell git describe --tags --abbrev=0 | cut -dv -f2))
	cd .. && tar --exclude=amdgpu_top/.git --exclude=amdgpu_top/target -czf amdgpu_top-$(TAG).tar.gz --transform 's,^amdgpu_top,amdgpu_top-$(TAG),' amdgpu_top
	mv ../amdgpu_top-$(TAG).tar.gz .
