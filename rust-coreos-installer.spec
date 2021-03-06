# Generated by rust2rpm 12
%bcond_without check
%global __cargo_skip_build 0

%global crate coreos-installer

Name:           rust-%{crate}
Version:        0.1.2
Release:        3%{?dist}
Summary:        Installer for Fedora CoreOS and RHEL CoreOS

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            https://crates.io/crates/coreos-installer
Source:         %{crates_source}

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  systemd-rpm-macros

%global _description %{expand:
coreos-installer installs Fedora CoreOS or RHEL CoreOS to bare-metal
machines (or, occasionally, to virtual machines).
}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}

# Since `rust-coreos-installer` creates a `coreos-installer`
# subpackage with a newer version number, which supersedes the
# deprecated `coreos-installer` package (https://src.fedoraproject.org/rpms/coreos-installer),
# an explicit `Obsoletes:` for `coreos-installer` is not necessary.

# Obsolete dracut modules as they are not provided in this package.
Obsoletes:      coreos-installer-dracut < 0.0.1

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%doc README.md
%{_bindir}/coreos-installer

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
# Install binaries, units, targets, generators for running via systemd
install -D -m 0750 -t %{buildroot}%{_libexecdir} systemd/coreos-installer-service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-reboot.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-noreboot.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer.target
install -D -m 0750 -t %{buildroot}%{_systemdgeneratordir} systemd/coreos-installer-generator

%package     -n %{crate}-systemd
Summary:     Systemd service files for %{crate}
Requires:   %{crate} = %{version}-%{release}

%description -n %{crate}-systemd
Systemd service files for %{crate}

%files       -n %{crate}-systemd
%{_libexecdir}/*
%{_unitdir}/*
%{_systemdgeneratordir}/*

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Josh Stone <jistone@redhat.com> - 0.1.2-2
- Remove the nix downgrade.

* Wed Jan 08 2020 Dusty Mabe <dusty@dustymabe.com> - 0.1.2-1
- Bump to new upstream release 0.1.2
    - Release notes: https://github.com/coreos/coreos-installer/releases/tag/v0.1.2
- Update spec file to include systemd units from upstream
    - These were added upstream in https://github.com/coreos/coreos-installer/pull/119

* Fri Dec 20 17:57:28 UTC 2019 Robert Fairley <rfairley@redhat.com> - 0.1.1-1
- Initial package
