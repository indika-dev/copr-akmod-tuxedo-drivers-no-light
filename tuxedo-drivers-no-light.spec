%global         modname                 tuxedo-drivers
%global         buildforkernels         akmod
%global         debug_package           %{nil}

Name:           tuxedo-drivers-no-light
Version:        4.13.1
Release:        37%{?dist}
Summary:        Tuxedo drivers akmod (no light version)
License:        GPL-2.0-or-later
URL:            https://gitlab.com%{modname}

# WICHTIG: Ein Akmod ist plattformunabhängig (enthält nur Sourcen)
BuildArch:      noarch

Source0:        %{url}/-/archive/v%{version}/tuxedo-drivers-v%{version}.tar.gz
Source1:        tuxedo-drivers-no-light-kmod.spec

BuildRequires:  kmodtool
# Diese werden benötigt, damit das Akmod auf dem Zielsystem bauen kann
Requires:       akmods
Requires:       %{name}-common = %{version}-%{release}

# Dynamische Erstellung der Akmod-Paketbeschreibungen
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} 2>/dev/null) }

%description
Tuxedo drivers as akmod package.

%package common
Summary:  Common configuration files for Tuxedo drivers
%description common
Contains udev rules and hwdb configurations.

%prep
%setup -q -n %{modname}-v%{version}

%build
# Bei einem Akmod wird im Copr-Build nichts kompiliert!

%install
# 1. Akmod-Sourcen vorbereiten
mkdir -p %{buildroot}%{_usrsrc}/akmods/
cp %{SOURCE0} %{buildroot}%{_usrsrc}/akmods/%{modname}-%{version}.tar.gz
# Kopiere das Child-SPEC (Steuerungsdatei)
cp %{SOURCE1} %{buildroot}%{_usrsrc}/akmods/%{modname}-kmod.spec

# 2. udev & hwdb Files (deine Logik)
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_udevhwdbdir}

cp 99-infinityflex-touchpanel-toggle.rules %{buildroot}%{_udevrulesdir}/
cp 99-z-tuxedo-systemd-fix.rules %{buildroot}%{_udevrulesdir}/
cp 61-sensor-tuxedo.hwdb %{buildroot}%{_udevhwdbdir}/
cp 61-keyboard-tuxedo.hwdb %{buildroot}%{_udevhwdbdir}/

# 3. Akmod Steuerungs-Dateien generieren
%{?akmod_install}

%files
# Das Hauptpaket kann leer sein oder Metadaten enthalten

%files common
%{_udevrulesdir}/*.rules
%{_udevhwdbdir}/*.hwdb

%files -n akmod-tuxedo-drivers-no-light
%{_usrsrc}/akmods/*

%files tuxedo-drivers-no-light-kmod
%{modname}-%{version}.tar.gz
%{name}-kmod.spec

%files tuxedo-drivers-no-light
