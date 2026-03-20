# copied partially from https://github.com/gladion136/tuxedo-drivers-kmod

%global         modname                 tuxedo-drivers
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%global         buildforkernels         akmod
%global         AkmodsBuildRequires     make gcc sed gawk

%define no-git-info %(echo "")
# extract all chars from "git" until next point or the end is reached
%define git_suffix %(echo %{release} | grep -o 'git\.[0-9]*\.[a-z0-9]*')
# extract only hash
%define git_hash %(echo %{release} | grep -o 'git\.[0-9]*\.[a-z0-9]*' | sed 's/git\.//g')
# assign standard value if suffix or hash are empty
%define safe_git_suffix %{?git_suffix}%{!?git_suffix:no-git-info}
%define safe_git_hash %{?git_hash}%{!?git_hash:no-git-info}

%if 0%{?fedora}
%global         debug_package           %{nil}
%endif

Name:           %{modname}-no-light-kmod
Version:        4.13.1
Release:        3%{?dist}
Summary:        Tuxedo drivers not enabling light on touchpad as akmod
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://github.com/tuxedocomputers/tuxedo-drivers
# Source0:        tuxedo-drivers-no-light-kmod.spec
# Source1:        tuxedo-drivers-no-light-kmod.spec.in
# Source2:        %{modname}-v%{version}.tar.gz

BuildRequires: kmodtool
BuildRequires: kernel-devel
BuildRequires: make
BuildRequires: gcc
BuildRequires: systemd-rpm-macros

Provides: %{modname}-no-light = %{version}
Obsoletes: %{modname}-no-light < 4.0.0

%description
Tuxedo drivers as kmod

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -q -c -T -a 0
cp %{_sourcedir}/%{name}-%{version}/%{name}.spec %{_sourcedir}
cp %{_sourcedir}/%{name}-%{version}/%{name}.spec.in %{_sourcedir}
cp %{_sourcedir}/%{name}-%{version}/%{modname}-v%{version}.tar.gz %{_sourcedir}

%build

%install
# copy the spec file for the final akmod to the spec directory
mkdir -p %{_specdir}
cp %{_sourcedir}/%{name}.spec.in %{_specdir}/%{name}.spec

# generate the akmod with the newly copied spec file
%{?akmod_install}

%files
%{_usrsrc}/akmods/*.src.rpm
%{_usrsrc}/akmods/%{name}.latest

%changelog
* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-3
- prepared for initial build by tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-2
- prepare for initial build (stefan.maassen@posteo.de)
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-1
- initial build by tito

