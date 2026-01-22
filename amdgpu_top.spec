Name:           amdgpu_top
Version:        0.11.0
Release:        1%{?dist}
Summary:        Tool to displays AMDGPU usage and performance counters

%global debug_package %{nil}

License:        MIT
URL:            https://github.com/Umio-Yasuno/amdgpu_top
Source0:        %{name}-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

%if 0%{?fedora}
BuildRequires:  rust >= 1.70
BuildRequires:  cargo
%endif
%if 0%{?epel}
BuildRequires:  rust >= 1.70
BuildRequires:  cargo
%endif
BuildRequires:  libdrm-devel >= 2.4.110
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  gcc
BuildRequires:  clang

# Runtime dependencies
Requires:       libdrm >= 2.4.110

%description
amdgpu_top is a tool that displays AMD GPU utilization, similar to nvidia-smi
or intel_gpu_top. The tool displays information gathered from performance 
counters (GRBM, GRBM2), sensors, fdinfo, gpu_metrics and AMDGPU driver.

Features:
- Simple TUI mode (like nvidia-smi, rocm-smi)
- Full TUI mode with detailed monitoring
- GUI mode with graphical interface
- JSON output for automation/scripting
- Process monitoring and memory usage tracking
- Performance counter access
- GPU metrics and sensor data

%prep
%autosetup

%build
# Build with all features enabled
cargo build --release --locked --no-default-features --features="libdrm_link,tui,gui,json"

%install
# Install main binary
install -Dm755 target/release/amdgpu_top %{buildroot}%{_bindir}/amdgpu_top

# Install desktop files
install -Dm644 assets/amdgpu_top.desktop %{buildroot}%{_datadir}/applications/amdgpu_top.desktop
install -Dm644 assets/amdgpu_top-tui.desktop %{buildroot}%{_datadir}/applications/amdgpu_top-tui.desktop

# Install metainfo
install -Dm644 assets/io.github.umio_yasuno.amdgpu_top.metainfo.xml %{buildroot}%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml

# Install man page if it exists
if [ -f docs/amdgpu_top.1 ]; then
    install -Dm644 docs/amdgpu_top.1 %{buildroot}%{_mandir}/man1/amdgpu_top.1
fi

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/amdgpu_top
%{_datadir}/applications/amdgpu_top.desktop
%{_datadir}/applications/amdgpu_top-tui.desktop
%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml
%{_mandir}/man1/amdgpu_top.1*

%changelog
* Tue Sep 02 2025 Julio Faracco <jfaracco@redhat.com> - 0.11.0-1
- fix Appstream metainfo by @malfisya
- fix the process to get gpu_metrics when resuming from suspended state
- stop monitoring when no VRAM-using processes are found
- fix getting sensors when resuming monitoring
- stop reading PC (GRBM, GRBM2) for RDNA 4 dGPU when no VRAM-using processes are found
- add exclude process names (amdgpu_top, steamwebhelper) for no_process_using_vram
- add memory_vendor to AppDeviceInfo
- fix DevicePath::init when libdrm_amdgpu is None (#133)
- fix combination of --single/--single-gpu and --pci options (#134)
- reorder the device path list if a device is specified in the options
- add support for FCLK (Fabric Clock) DPM
- update vram usage when pre-dropping device handle
- update logic for dropping device handle
- add supports_gpu_metrics field to AppDeviceInfo
- fix get_rocm_version for TheRock
- remove dependency on anyhow
- [XDNA] update bindings for 32bit targets
- [TUI] do not display average_socket_power if gpu_metrics_v3_0
- [TUI] clear gpu_metrics_view when metrics is None
- [TUI] check stapm_limit and current_stapm_limit
- [SMI] print the suspended state
- [SMI] print PCI power state
- [SMI] set FdInfoSortType::GTT when the device is APU
- [SMI] print junction temp instead of edge temp, if junction temp is available
- [SMI] add memory temp.
- [SMI] remove ECC status
- [SMI] update layout for the suspending device
- [GUI] do not display average_socket_power if gpu_metrics_v3_0
- [GUI] add tab_gui mode
- [GUI] set striped to side panel
- [JSON] add some info to json_info dump (#137)
