#
# spec file for package bareos-macros
#
# Copyright (c) 2022 SUSE LLC
#

%define appname bareos
%if 0%{?sle_version} <= 120500
%define _rpmmacrodir /usr/lib/rpm/macros.d
%endif
%define macrosfile %{_rpmmacrodir}/macros.%{appname}
Name:           %{appname}-macros
Version:        0.1.1
Release:        0
Group:          Development/Tools/Building
Summary:        Macros to help with Bareos packaging
License:        AGPL-3.0
URL:            https://suse.com
Source:         %{appname}.macros
BuildArch:      noarch

%description
This package contains RPM macros used during the Bareos build process. Users do not need to install this.

%prep

%build

%install
install -Dpm0644 %{SOURCE0} %{buildroot}%{macrosfile}

%files
%attr(0644, -, -) %{macrosfile}

%changelog

