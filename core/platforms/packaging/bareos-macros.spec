#
# spec file for package bareos-macros
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
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

