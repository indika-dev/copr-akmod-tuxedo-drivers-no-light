# copied partially from https://github.com/gladion136/tuxedo-drivers-kmod

%global         modname                 tuxedo-drivers
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%global         buildforkernels         akmod
%global         AkmodsBuildRequires     make gcc sed gawk

%define no-git-info %(echo "")
%define releasenumber %(echo %{release} | grep -o '[0-9]*' | head -1 )
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

Name:           %{modname}-no-light
Version:        4.13.1
Release:        15%{?dist}
Summary:        Tuxedo drivers not enabling light on touchpad as akmod
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://github.com/tuxedocomputers/tuxedo-drivers
Source0:        https://github.com/indika-dev/copr-akmod-%{name}/archive/refs/tags/%{name}-%{version}-%{releasenumber}.tar.gz
Source1:        https://github.com/tuxedocomputers/tuxedo-drivers/archive/refs/tags/v4.13.1.tar.gz
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
curl -LO https://github.com/indika-dev/copr-akmod-%{name}/archive/refs/tags/%{name}-%{version}-%{releasenumber}.tar.gz
mkdir -p %{_sourcedir}
ls -alR %{_sourcedir}
tar xvzf %{name}-%{version}-%{releasenumber}.tar.gz --strip-components=1 -C %{_sourcedir}
ls -alR %{_sourcedir}

%build

%install
# copy the spec file for the final akmod to the spec directory
mkdir -p %{_specdir}
cp %{_sourcedir}/%{modname}-no-light-kmod.spec.in %{_specdir}/%{name}.spec
cp %{_sourcedir}/%{modname}-v%{version}.tar.gz %{_specdir}/%{name}.spec

# generate the akmod with the newly copied spec file
%{?akmod_install}

pushd %{buildroot}%{_usrsrc}/akmods/
  # Findet das frisch gebaute SRPM (z.B. tuxedo-drivers-kmod-4.1.1-1.fc40.src.rpm)
  NEW_SRPM=$(ls *.src.rpm | head -n 1)
  # Erstellt den Softlink (z.B. tuxedo-drivers.latest -> ...)
  ln -s "$NEW_SRPM" %{name}.latest
popd

%files
%{_usrsrc}/akmods/*.src.rpm
%{_usrsrc}/akmods/%{name}.latest

%changelog
* Sun Mar 22 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-15
- prepare for initial build (stefan.maassen@posteo.de)

* Sun Mar 22 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-14
- prepare for initial build (stefan.maassen@posteo.de)
- prepare for initial build (stefan.maassen@posteo.de)

* Sun Mar 22 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-13
- new package built with tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-12
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-11
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-10
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-9
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-8
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-7
- prepare for initial build (stefan.maassen@posteo.de)
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-6
- new package built with tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-5
- prepare for initial build by tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-4
- prepare for initial build by tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-3
- prepared for initial build by tito

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-2
- prepare for initial build (stefan.maassen@posteo.de)
- prepare for initial build (stefan.maassen@posteo.de)

* Fri Mar 20 2026 Stefan Maaßen <stefan.maassen@posteo.de> 4.13.1-1
- initial build by tito

