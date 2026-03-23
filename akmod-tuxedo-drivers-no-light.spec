%global         modname                 tuxedo-drivers
%global         buildforkernels         akmod
%global         debug_package           %{nil}

%define releasenumber %(echo %{release} | grep -o '[0-9]*' | head -1 )

Name:           tuxedo-drivers-no-light
Version:        4.13.1
Release:        68%{?dist}
Summary:        Tuxedo drivers akmod (no light version)
License:        GPL-2.0-or-later
URL:            https://github.com/indika-dev/copr-akmod-tuxedo-drivers-no-light

# WICHTIG: Ein Akmod ist plattformunabhängig (enthält nur Sourcen)
# BuildArch:      noarch
Source0:        https://github.com/tuxedocomputers/tuxedo-drivers/archive/refs/tags/v4.13.1.tar.gz
Source1:        tuxedo-drivers-no-light-kmod.spec.in

BuildRequires:  kmodtool
# Diese werden benötigt, damit das Akmod auf dem Zielsystem bauen kann
Requires:       akmods

# Dynamische Erstellung der Akmod-Paketbeschreibungen
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} 2>/dev/null) }

%description
Tuxedo drivers as akmod package.

%prep
%setup -q -n %{modname}-%{version}

%build
# Bei einem Akmod wird im Copr-Build nichts kompiliert!

%install
# 1. Akmod-Sourcen vorbereiten
mkdir -p %{buildroot}%{_usrsrc}/akmods
# Kopiere das Child-SPEC (Steuerungsdatei)
cp %{SOURCE1} %{_specdir}/%{name}.spec

# 2. udev & hwdb Files (deine Logik)
mkdir -p %{buildroot}/usr/lib/udev/rules.d/
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d/
mkdir -p %{buildroot}/etc/modules-load.d/

install -D -m 644 tuxedo_keyboard.conf %{buildroot}/etc/modules-load.d/tuxedo_keyboard.conf
install -D -m 644 99-infinityflex-touchpanel-toggle.rules %{buildroot}/usr/lib/udev/rules.d/
install -D -m 644 99-z-tuxedo-systemd-fix.rules %{buildroot}/usr/lib/udev/rules.d/
install -D -m 644 61-sensor-tuxedo.hwdb %{buildroot}/usr/lib/udev/hwdb.d/
install -D -m 644 61-keyboard-tuxedo.hwdb %{buildroot}/usr/lib/udev/hwdb.d/

# 3. Akmod Steuerungs-Dateien generieren
%{?akmod_install}
mkdir -p %{buildroot}%{_usrsrc}/akmods/%{modname}-%{version}
tar xzf %{SOURCE0} --strip-components=1 -C %{buildroot}%{_usrsrc}/akmods/%{modname}-%{version}

%files
/%{_usrsrc}/akmods/%{name}-kmod-%{version}-1%{dist}.src.rpm
/etc/modules-load.d/*.conf
/usr/lib/udev/rules.d/*.rules
/usr/lib/udev/hwdb.d/*.hwdb

