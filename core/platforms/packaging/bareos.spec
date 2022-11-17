#
# spec file for package bareos
#
# Copyright (c) 2022 SUSE LLC
# Copyright (c) 2013-2021 Bareos GmbH & Co KG
# Copyright (c) 2011-2012 Bruno Friedmann (Ioda-Net) and Philipp Storz (dass IT)
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

%bareos_conditionals
Name:           bareos
Version:        21.1.4
Release:        0%{?dist}
Group:          Productivity/Archiving/Backup
License:        AGPL-3.0
BuildRoot:      %{_tmppath}/%{name}-root
URL:            https://www.bareos.org/
Vendor:         The Bareos Team

# Defaults
%define client_only 0
%define build_qt_monitor 1
%define glusterfs 0
%define droplet 1
%define have_git 1
%define ceph 0
%define install_suse_fw 0
%define firewalld 0
%define systemd_support 0
%define python_plugins 1

# <= SUSE Linux Enterprise 12.x / openSUSE Leap 42.x
%if 0%{?suse_version} <= 1315
%define build_qt_monitor 0
%define install_suse_fw 1
%define _fwdefdir   %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services
%endif

# >= SUSE Linux Enterprise 12.x / openSUSE Leap 42.x
%if 0%{?suse_version} >= 1315
%define systemd_support 1
%endif

# >= SUSE Linux Enterprise 12
%if 0%{?sle_version} >= 120000
%global ceph 1
%endif

# >= SUSE Linux Enterprise 15.x / openSUSE Leap 15.x
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%define firewalld 1
%endif

%if "%{_sharedstatedir}" == "/usr/com"
%define _sharedstatedir /var/lib/
%endif

# rhel/centos 6 must not be built with libtirpc installed
%if 0%{?rhel} == 6
BuildConflicts: libtirpc-devel
%endif

# fedora 28: rpc was removed from libc
%if 0%{?fedora} >= 28 || 0%{?rhel} > 7 || 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150300
BuildRequires: rpcgen
BuildRequires: libtirpc-devel
%endif

%if 0%{?rhel_version} >= 700 || 0%{?centos_version} >= 700
%define glusterfs 1
%define systemd_support 1
%endif

%if 0%{?rhel_version} >= 700 && !0%{?centos_version}
%define ceph 1
%endif

%if 0%{?centos} >= 8
%define ceph 1
%endif

%if 0%{?suse_version} > 1500
BuildRequires: gcc12 gcc12-c++
%else
%if 0%{?sle_version} >= 120500
BuildRequires: gcc11 gcc11-c++
%endif
%endif

BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  lzo-devel
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(openssl)

%if 0%{?systemd_support}
BuildRequires: systemd
# see https://en.opensuse.org/openSUSE:Systemd_packaging_guidelines
%if 0%{?suse_version} >= 1315
BuildRequires: systemd-rpm-macros
BuildRequires: libudev-devel
#BuildRequires: pkgconfig(libsystemd)
#BuildRequires: pkgconfig(systemd)
%endif
%{?systemd_requires}
%endif

%if 0%{?glusterfs}
BuildRequires: glusterfs-devel glusterfs-api-devel
%endif

%if 0%{?ceph}
  %if 0%{?sle_version} >= 120200
BuildRequires: libcephfs-devel
BuildRequires: librados-devel
  %else
# the rhel macro is set in docker, but not in obs
    %if 0%{?rhel} == 7
BuildRequires: librados2-devel
BuildRequires: libcephfs1-devel
    %else
      %if 0%{?rhel} == 8
BuildRequires: librados-devel
BuildRequires: libradosstriper-devel
BuildRequires: libcephfs-devel
      %else
BuildRequires: ceph-devel
      %endif
    %endif
  %endif
%endif

%if 0%{?have_git}
BuildRequires: git-core
%endif

Source0: %{name}-%{version}.tar.gz
%if 0%{?suse_version}
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
Source1: system-user-%{name}.conf
%endif
Source2: permissions.%{name}-fd.easy
Source3: permissions.%{name}-fd.secure
Source4: permissions.%{name}-fd.paranoid
%endif
%if 0%{?firewalld}
Source5: firewall.bareos-dir.xml
Source6: firewall.bareos-fd.xml
Source7: firewall.bareos-sd.xml
%endif

BuildRequires: pam-devel

BuildRequires: cmake >= 3.12
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: glibc
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: perl
BuildRequires: readline-devel
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: libacl-devel
BuildRequires: pkgconfig
BuildRequires: lzo-devel
BuildRequires: logrotate
BuildRequires: postgresql-devel
BuildRequires: openssl
BuildRequires: libcap-devel
BuildRequires: mtx

%if 0%{?build_qt_monitor}
%if 0%{?suse_version}
BuildRequires: libqt5-qtbase-devel
%else

%if 0%{?centos_version} > 700 || 0%{?rhel_version} > 700 || 0%{?fedora} >= 29
BuildRequires: qt5-qtbase-devel
%else
BuildRequires: qt-devel
%endif

%endif
%endif


%if 0%{?python_plugins}
%if 0%{?centos_version} >= 800 || 0%{?rhel_version} >= 800 || 0%{?fedora} >= 31
BuildRequires: python2-devel >= 2.6
BuildRequires: python3-devel >= 3.4
%else
BuildRequires: python-devel >= 2.6
BuildRequires: python3-devel >= 3.4
%endif
%endif

%if 0%{?suse_version}
BuildRequires: bareos-macros
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
BuildRequires: sysuser-tools
%sysusers_requires
%endif

%if 0%{?firewalld}
BuildRequires: firewall-macros
%endif

%if 0%{?suse_version} <= 1315 && 0%{?sle_version} >= 120500
BuildRequires: distribution-release
%else
%if 0%{?sle_version}
BuildRequires: sles-release
%else
BuildRequires: suse-release
%endif
%endif
BuildRequires: pwdutils
BuildRequires: update-desktop-files
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(json-c)

%if 0%{?suse_version}
# link identical files
BuildRequires: fdupes
BuildRequires: libjansson-devel
BuildRequires: lsb-release
%endif

%else
# non suse

BuildRequires: passwd


# Some magic to be able to determine what platform we are running on.
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}

BuildRequires: redhat-lsb

# older versions require additional release packages
%if 0%{?rhel_version}   && 0%{?rhel_version} <= 600
BuildRequires: redhat-release
%endif

%if 0%{?centos_version} && 0%{?centos_version} <= 600
BuildRequires: redhat-release
%endif

%if 0%{?fedora_version}
BuildRequires: fedora-release
%endif

%if 0%{?rhel_version} >= 600 || 0%{?centos_version} >= 600 || 0%{?fedora_version} >= 14
BuildRequires: jansson-devel
%endif
%else
# non suse, non redhat: eg. mandriva.

BuildRequires: lsb-release

%endif

%endif

# dependency tricks for vixdisklib
# Note: __requires_exclude only works for dists with rpm version >= 4.9
#       SLES12 has suse_version 1315, SLES11 has 1110
%if 0%{?rhel_version} >= 700 || 0%{?centos_version} >= 700 || 0%{?fedora_version} >= 16 || 0%{?suse_version} >= 1315
%global __requires_exclude ^(.*libvixDiskLib.*|.*CXXABI_1.3.9.*)$

%else
%define _use_internal_dependency_generator 0
%define our_find_requires %{_builddir}/%{name}-%{version}/find_requires
%endif

Summary:    Backup Archiving REcovery Open Sourced - metapackage
Requires:   %{name}-director = %{version}
Requires:   %{name}-storage = %{version}
Requires:   %{name}-client = %{version}

%define dscr %{bareos_dscr_long}


%description
%{dscr}

# Notice : Don't try to change the order of package declaration
# You will have side effect with PreReq

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%package -n system-user-%{name}
Summary:    System user and group for Bareos
Group:      System/Fhs
BuildArch:  noarch
%endif

%package    bconsole
Summary:    Bareos administration console (CLI)
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}

%package    client
Summary:    Bareos client Meta-All-In-One package
Group:      Productivity/Archiving/Backup
BuildArch:  noarch
Requires:   %{name}-bconsole = %{version}
Requires:   %{name}-filedaemon = %{version}
%if 0%{?suse_version}
Recommends: %{name}-traymonitor = %{version}
%endif

%package    director
Summary:    Bareos Director daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}
Requires:   %{name}-database-common = %{version}
Requires:   %{name}-database-tools
%if 0%{?suse_version}
Requires(pre): pwdutils
# Don't use this option on anything other then SUSE derived distributions
# as Fedora & others don't know this tag
Recommends: logrotate
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
Requires:   system-user-%{name}
%endif
%else
Requires(pre): shadow-utils
%endif
Provides:   %{name}-dir

%package    storage
Summary:    Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}
Provides:   %{name}-sd
%if 0%{?suse_version}
Requires(pre): pwdutils
Recommends: bareos-tools
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
Requires:   system-user-%{name}
%endif
%else
Requires(pre): shadow-utils
# Recommends would be enough, however only supported by Fedora >= 24.
Requires: bareos-tools
%endif

%if 0%{?droplet}
%package    storage-droplet
Summary:    Object Storage support (through libdroplet) for the Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common  = %{version}
Requires:   %{name}-storage = %{version}
%endif

%if 0%{?glusterfs}
%package    storage-glusterfs
Summary:    GlusterFS support for the Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common  = %{version}
Requires:   %{name}-storage = %{version}
Requires:   glusterfs
%endif

%if 0%{?ceph}
%package    storage-ceph
Summary:    CEPH support for the Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common  = %{version}
Requires:   %{name}-storage = %{version}
%endif

%package    storage-tape
Summary:    Tape support for the Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common  = %{version}
Requires:   %{name}-storage = %{version}
Requires:   mtx
%if !0%{?suse_version}
Requires:   mt-st
%endif

%package    storage-fifo
Summary:    FIFO support for the Bareos Storage backend
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common  = %{version}
Requires:   %{name}-storage = %{version}

%package    filedaemon
Summary:    Bareos File daemon (backup and restore client)
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}
Provides:   %{name}-fd
%if 0%{?suse_version}
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
Requires:   system-user-%{name}
%endif
Requires(pre): pwdutils
Requires(post): permissions
Requires(verify):permissions
%else
Requires(pre): shadow-utils
%endif

%package    common
Summary:    Common files, required by multiple Bareos packages
Group:      Productivity/Archiving/Backup
Requires:   openssl
%if 0%{?suse_version}
Requires(pre): pwdutils
%else
Requires(pre): shadow-utils
%endif
Provides:   %{name}-libs

%package    database-common
Summary:    Generic abstraction libs and files to connect to a database
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}
Requires:   %{name}-database-backend = %{version}
Requires:   openssl
Provides:   %{name}-sql

%package    database-postgresql
Summary:    Libs & tools for postgresql catalog
Group:      Productivity/Archiving/Backup
Requires:   %{name}-database-common = %{version}
Provides:   %{name}-catalog-postgresql
Provides:   %{name}-database-backend

%package    database-tools
Summary:    Bareos CLI tools with database dependencies
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}
Requires:   %{name}-database-common = %{version}
Provides:   %{name}-dbtools

%package    tools
Summary:    Bareos CLI tools (bcopy, bextract, bls, bregex, bwild)
Group:      Productivity/Archiving/Backup
Requires:   %{name}-common = %{version}

%if 0%{build_qt_monitor}
%package    traymonitor
Summary:    Bareos Tray Monitor (QT)
Group:      Productivity/Archiving/Backup
# Added to by pass the 09 checker rules (conflict with bareos-tray-monitor.conf)
# This is mostly wrong cause the two binaries can use it!
Conflicts:  %{name}-tray-monitor-gtk
Provides:   %{name}-tray-monitor-qt
%endif

%package    devel
Summary:    Devel headers
Group:      Development/Languages/C and C++
Requires:   %{name}-common = %{version}
Requires:   zlib-devel
Requires:   libacl-devel
Requires:   postgresql-devel
Requires:   libcap-devel
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora_version}
Requires:   openssl-devel
%else
Requires:   libopenssl-devel
%endif

%package    regress-config
Summary:    Required files for bareos-regress
Group:      Development/Languages/C and C++
Requires:   %{name}-common = %{version}

%if 0%{?python_plugins}
%package    director-python2-plugin
Summary:    Python plugin for Bareos Director daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-director = %{version}
Requires:   bareos-director-python-plugins-common = %{version}
Provides:   bareos-director-python-plugin

%package    director-python3-plugin
Summary:    Python plugin for Bareos Director daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-director = %{version}
Requires:   bareos-director-python-plugins-common = %{version}
Provides:   bareos-director-python-plugin

%package    director-python-plugins-common
Summary:    Python plugin for Bareos Director daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-director = %{version}


%package    filedaemon-python2-plugin
Summary:    Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugins-common = %{version}
Provides:   bareos-filedaemon-python-plugin

%package    filedaemon-python3-plugin
Summary:    Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugins-common = %{version}
Provides:   bareos-filedaemon-python-plugin

%package    filedaemon-python-plugins-common
Summary:    Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}

%package    filedaemon-ldap-python-plugin
Summary:    LDAP Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugin = %{version}
Requires:   python-ldap

%package    filedaemon-ovirt-python-plugin
Summary:    Ovirt Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugin = %{version}

%package    filedaemon-libcloud-python-plugin
Summary:    Libcloud Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugin = %{version}

%package    filedaemon-postgresql-python-plugin
Summary:    PostgreSQL Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugin = %{version}

%package    filedaemon-percona-xtrabackup-python-plugin
Summary:    Percona xtrabackup Python plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   bareos-filedaemon-python-plugin = %{version}
#Requires:   python-percona

%package    storage-python2-plugin
Summary:    Python plugin for Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-storage = %{version}
Requires:   bareos-storage-python-plugins-common = %{version}
Provides:   bareos-storage-python-plugin

%package    storage-python3-plugin
Summary:    Python plugin for Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-storage = %{version}
Requires:   bareos-storage-python-plugins-common = %{version}
Provides:   bareos-storage-python-plugin

%package    storage-python-plugins-common
Summary:    Python plugin for Bareos Storage daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-storage = %{version}

# vmware switch is set via --define="vmware 1" in build script when
# vix disklib is detected

%if 0%{?vmware}
# VMware Plugin BEGIN

%package -n     bareos-vadp-dumper
Summary:        VADP Dumper - vStorage APIs for Data Protection Dumper program
Group:          Productivity/Archiving/Backup
Requires:       bareos-vmware-vix-disklib

%description -n bareos-vadp-dumper
Uses vStorage API to connect to VMWare and dump data like virtual disks snapshots
to be used by other programs.


%package -n     bareos-vmware-plugin
Summary:        Bareos VMware plugin
Group:          Productivity/Archiving/Backup
Requires:       bareos-vadp-dumper
Requires:       bareos-filedaemon-python-plugin >= 15.2

%description -n bareos-vmware-plugin
Uses the VMware API to take snapshots of running VMs and takes
full and incremental backup so snapshots. Restore of a snapshot
is currently supported to the origin VM.

%package -n     bareos-vmware-plugin-compat
Summary:        Bareos VMware plugin compatibility
Group:          Productivity/Archiving/Backup
Requires:       bareos-vmware-plugin

%description -n bareos-vmware-plugin-compat
Keeps bareos/plugins/vmware_plugin subdirectory, which have been used in Bareos <= 16.2.

# VMware Plugin END
%endif

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%description -n system-user-%{name}
This package provides the system user and group used by various Bareos components.
%endif

%description director-python2-plugin
%{dscr}

This package contains the python plugin for the director daemon

%description director-python3-plugin
%{dscr}

This package contains the python 3 plugin for the director daemon

%description director-python-plugins-common
%{dscr}

This package contains the common files for the python 2 and python 3 director plugins.

%description filedaemon-python2-plugin
%{dscr}

This package contains the python plugin for the file daemon

%description filedaemon-python3-plugin
%{dscr}

This package contains the python 3 plugin for the file daemon

%description filedaemon-python-plugins-common
%{dscr}

This package contains the common files for the python 2 and python 3 filedaemon plugins.

%description filedaemon-ldap-python-plugin
%{dscr}

This package contains the LDAP python plugin for the file daemon

%description filedaemon-ovirt-python-plugin
%{dscr}

This package contains the Ovirt python plugin for the file daemon

%description filedaemon-libcloud-python-plugin
%{dscr}

This package contains the Libcloud python plugin for the file daemon

%description filedaemon-postgresql-python-plugin
%{dscr}

This package contains the PostgreSQL python plugin for the file daemon
%description filedaemon-percona-xtrabackup-python-plugin
%{dscr}

This package contains the Percona python plugin for the file daemon

%description storage-python2-plugin
%{dscr}

This package contains the python plugin for the storage daemon

%description storage-python3-plugin
%{dscr}

This package contains the python 3 plugin for the storage daemon

%description storage-python-plugins-common
%{dscr}

This package contains the common files for the python 2 and python 3 storage plugins.
%endif

%if 0%{?glusterfs}
%package    filedaemon-glusterfs-plugin
Summary:    GlusterFS plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}
Requires:   glusterfs

%description filedaemon-glusterfs-plugin
%{dscr}

This package contains the GlusterFS plugin for the file daemon

%endif

%if 0%{?ceph}
%package    filedaemon-ceph-plugin
Summary:    CEPH plugin for Bareos File daemon
Group:      Productivity/Archiving/Backup
Requires:   bareos-filedaemon = %{version}

%description filedaemon-ceph-plugin
%{dscr}

This package contains the CEPH plugins for the file daemon

%endif

%package webui
Summary:       Bareos Web User Interface
Group:         Productivity/Archiving/Backup
BuildArch:     noarch

# ZendFramework 2.4 says it required php >= 5.3.23.
# However, it works on SLES 11 with php 5.3.17
# while it does not work with php 5.3.3 (RHEL6).
Requires: php >= 5.3.17

Requires: php-bz2
Requires: php-ctype
Requires: php-curl
Requires: php-date
Requires: php-dom
Requires: php-fileinfo
Requires: php-filter
Requires: php-gettext
Requires: php-gd
Requires: php-hash
Requires: php-iconv
Requires: php-intl
Requires: php-json

%if !0%{?suse_version}
Requires: php-libxml
%endif

Requires: php-mbstring
Requires: php-openssl
Requires: php-pcre
Requires: php-reflection
Requires: php-session
Requires: php-simplexml
Requires: php-spl
Requires: php-xml
Requires: php-xmlreader
Requires: php-xmlwriter
Requires: php-zip

%if 0%{?suse_version} || 0%{?sle_version}
BuildRequires: apache2
# /usr/sbin/apxs2
BuildRequires: apache2-devel
BuildRequires: mod_php_any
%define _apache_conf_dir /etc/apache2/conf.d/
%define www_daemon_user  wwwrun
%define www_daemon_group www
Requires: apache
Recommends: mod_php_any
%else
BuildRequires: httpd
# apxs2
BuildRequires: httpd-devel
%define _apache_conf_dir /etc/httpd/conf.d/
%define www_daemon_user  apache
%define www_daemon_group apache
%if 0%{?fedora_version} >= 33
Requires:   php-fpm
%else
Requires:   mod_php
%endif
Requires:   httpd
%endif



%description webui
%{dscr}

This package contains the webui (Bareos Web User Interface).

%description client
%{dscr}

This package is a meta package requiring the packages
containing the fd and the console.

This is for client only installation.

%description bconsole
%{dscr}

This package contains the bconsole (the CLI interface program)

%description director
%{dscr}

This package contains the Director Service (Bareos main service daemon)

%description storage
%{dscr}

This package contains the Storage Daemon
(Bareos service to read and write data from/to media)

%description storage-tape
%{dscr}

This package contains the Storage Daemon tape support
(Bareos service to read and write data from/to tape media)

%if 0%{?droplet}
%description storage-droplet
%{dscr}

This package contains the Storage backend for Object Storage (through libdroplet).
%endif

%if 0%{?glusterfs}
%description storage-glusterfs
%{dscr}

This package contains the Storage backend for GlusterFS.
%endif

%if 0%{?ceph}
%description storage-ceph
%{dscr}

This package contains the Storage backend for CEPH.
%endif

%description storage-fifo
%{dscr}

This package contains the Storage backend for FIFO files.
This package is only required, when a resource "Archive Device = fifo"
should be used by the Bareos Storage Daemon.

%description filedaemon
%{dscr}

This package contains the File Daemon
(Bareos client daemon to read/write data from the backed up computer)

%description common
%{dscr}

This package contains the shared libraries that are used by multiple daemons and tools.

%description database-common
%{dscr}

This package contains the shared libraries that abstract the catalog interface

%description database-postgresql
%{dscr}

This package contains the shared library to access postgresql as catalog db.

%description database-tools
%{dscr}

This package contains Bareos database tools.

%description tools
%{dscr}

This package contains Bareos tools.

%if 0%{?build_qt_monitor}
%description traymonitor
%{dscr}

This package contains the tray monitor (QT based).
%endif

%description devel
%{dscr}

This package contains bareos development files.

%description regress-config
%{dscr}

This package contains required files for Bareos regression testing.


%prep
# this is a hack so we always build in "bareos" and not in "bareos-version"
%setup -c -n bareos -q
mv bareos-*/* .
find . -type f -name '.*' -delete
find ./webui/tests/regress -type f -execdir sed -i -e '0,/#\!\/.*\/.*/d' {} +
find . -type f -execdir sed -i -e 's?%{_bindir}/env python?%{_bindir}/python3?' -e 's?%{_bindir}/env python2?%{_bindir}/python2?' -e 's?%{_bindir}/env python3?%{_bindir}/python3?' -e 's?%{_bindir}/env perl?%{_bindir}/perl?' -e 's?%{_bindir}/env bash?%{_bindir}/bash?' {} +

%build
# Cleanup defined in Fedora Packaging:Guidelines
# and required repetitive local build of at least CentOS 5.
if [ "%{?buildroot}" -a "%{?buildroot}" != "/" ]; then
    rm -rf "%{?buildroot}"
fi
%if !0%{?suse_version}
export PATH=$PATH:/usr/lib64/qt5/bin:/usr/lib/qt5/bin
%endif
export MTX=/usr/sbin/mtx

%bareos_build

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%sysusers_generate_pre %{SOURCE1} %{name} system-user-%{name}.conf
%endif

%check
%bareos_test

%install
for directory in \
  %{_datadir}/applications %{_datadir}/pixmaps %{_docdir}/%{name}         \
  %{bareos_backend_dir} %{bareos_working_dir} %{bareos_plugin_dir}        \
  %{_libdir}/%{name}/plugins/vmware_plugin %{_localstatedir}/log/%{name}  \
  ;                                                                       \
do install -dm 755 "%{buildroot}$directory" ; done

%bareos_install
%bareos_cleanup

cleanup misc
%if 0%{?client_only}
cleanup client
%endif
%if 0%{?install_suse_fw} == 0
cleanup suse_fw
%endif
%if 0%{?systemd_support}
cleanup systemd
%endif
%if ! 0%{?vmware}
cleanup vmware
%endif
%if ! 0%{?python_plugins}
cleanup python_plugins
%endif
%if ! 0%{?glusterfs}
cleanup glusterfs
%endif
%if ! 0%{?build_qt_monitor}
cleanup qtmonitor
%endif
%if %{without vanilla_config}
cleanup vanillaconfig
%endif

# remove links to libraries
# for i in #{buildroot}/#{_libdir}/libbareos*; do printf "$i: "; readelf -a $i | grep SONAME; done
find %{buildroot}%{bareos_library_dir} -type l -name "libbareos*.so" -maxdepth 1 -delete


# install tray monitor
# #if 0#{?build_qt_monitor}
# #if 0#{?suse_version} > 1010
# disables, because suse_update_desktop_file complains
# that there are two desktop file (applications and autostart)
# ##suse_update_desktop_file bareos-tray-monitor System Backup
# #endif
# #endif

# install systemd service files
%if 0%{?systemd_support}
install -vdm755 %{buildroot}%{_unitdir}
for service in \
  bareos-dir bareos-fd bareos-sd ; \
do \
  install -vm644 "core/platforms/systemd/$service.service" %{buildroot}%{_unitdir} \
%if 0%{?suse_version}
  ; ln -fs '%{_sbindir}/service' "%{buildroot}%{_sbindir}/rc$service" \
%endif
; done
%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
install -vd %{buildroot}%{_sysusersdir}
install -vm644 %{SOURCE1} %{buildroot}%{_sysusersdir}
%endif
%endif

%if 0%{?suse_version}
install -vd %{buildroot}%{_sysconfdir}/permissions.d
for permset in easy secure paranoid ; \
do install -vm644 "%{_sourcedir}/permissions.%{name}-fd.$permset" "%{buildroot}%{_sysconfdir}/permissions.d/%{name}-fd.$permset" ; done
%if 0%{?firewalld}
install -vd %{buildroot}%{_prefix}/lib/firewalld/services
for fwservice in bareos-dir bareos-sd bareos-fd ; \
do install -vm644 "%{_sourcedir}/firewall.$fwservice.xml" "%{buildroot}%{_prefix}/lib/firewalld/services/$fwservice.xml" ; done
%endif
%endif

echo "This meta package emulates the former bareos-client package" > %{buildroot}%{_docdir}/%{name}/README.bareos-client
echo "This is a meta package to install a full bareos system" > %{buildroot}%{_docdir}/%{name}/README.bareos

for directory in %{_datadir}/%{name}-webui/tests/selenium \
%if 0%{?python_plugins}
%{bareos_library_dir}/plugins \
%endif
; do recursive_chmodx "$directory" py ; done
recursive_chmodx %{bareos_script_dir} sh

# these already exist in /usr/bin
for binary in bconsole bregex bsmtp bwild ; \
do rm "%{buildroot}%{_sbindir}/$binary" ; done

mv %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-dir %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-director

rm %{buildroot}%{_datadir}/%{name}-webui/tests/selenium/README.md
find %{buildroot}%{_datadir}/%{name}-webui/tests -size 0 -delete

%fdupes %{buildroot}%{_datadir}


%files
%defattr(-, root, root)
%{_docdir}/%{name}/README.bareos

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%files -n system-user-%{name}
%defattr(-,root,root,-)
%{_sysusersdir}/system-user-%{name}.conf
%endif

%files webui
%defattr(-,root,root,-)
%doc webui/README.md webui/LICENSE
%doc webui/doc/README-TRANSLATION.md
%{_datadir}/%{name}-webui/
# attr(-, #daemon_user, #daemon_group) #{_datadir}/#{name}/data
%dir /etc/bareos-webui
%config(noreplace) /etc/bareos-webui/directors.ini
%config(noreplace) /etc/bareos-webui/configuration.ini
%if %{with vanilla_config}
%config %attr(644,root,root) /etc/bareos/bareos-dir.d/console/admin.conf.example
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/profile/webui-admin.conf
%config %attr(644,root,root) /etc/bareos/bareos-dir.d/profile/webui-limited.conf.example
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/profile/webui-readonly.conf
%endif
%config(noreplace) %{bareos_apache_conf_dir}/bareos-webui.conf

%files client
%defattr(-, root, root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README.bareos-client


%if 0%{?vmware}
# VMware Plugin BEGIN

%files -n bareos-vadp-dumper
%defattr(-,root,root)
%{_sbindir}/bareos_vadp_dumper*
%doc core/src/vmware/LICENSE.vadp

%files -n bareos-vmware-plugin
%defattr(-,root,root)
%dir %{_libdir}/bareos/
%{_sbindir}/vmware_cbt_tool.py
%{bareos_plugin_dir}/BareosFdPluginVMware.py*
%{bareos_plugin_dir}/bareos-fd-vmware.py*
%doc core/src/vmware/LICENSE core/src/vmware/README.md

%files -n bareos-vmware-plugin-compat
%defattr(-,root,root)
%{_libdir}/bareos/plugins/vmware_plugin/

#VMware Plugin END
%endif
%files bconsole
# console package
%defattr(-, root, root)
%if %{with vanilla_config}
%attr(0640, root, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bconsole.conf
%endif
%{_bindir}/bconsole
%{_mandir}/man1/bconsole.1.gz

%if !0%{?client_only}

%files director
# dir package (bareos-dir)
%defattr(-, root, root)
%if 0%{?suse_version}
%if !0%{?systemd_support}
%{_sysconfdir}/init.d/bareos-dir
%endif
%{_sbindir}/rcbareos-dir
%if 0%{?install_suse_fw}
# use noreplace if user has adjusted its list of IP
%attr(0644, root, root) %config(noreplace) %{_fwdefdir}/bareos-dir
%endif
%if 0%{?firewalld}
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/services
%{_prefix}/lib/firewalld/services/bareos-dir.xml
%endif
%else
%if !0%{?systemd_support}
%{_sysconfdir}/rc.d/init.d/bareos-dir
%endif
%endif
%if %{with vanilla_config}
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/catalog/MyCatalog.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/client/bareos-fd.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/console/bareos-mon.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/director/bareos-dir.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/Catalog.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/LinuxAll.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/SelfTest.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) "%{_sysconfdir}/%{name}/bareos-dir.d/fileset/Windows All Drives.conf"
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/job/backup-bareos-fd.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/job/BackupCatalog.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/jobdefs/DefaultJob.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/job/RestoreFiles.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/messages/Daemon.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/messages/Standard.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/pool/Differential.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/pool/Full.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/pool/Incremental.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/pool/Scratch.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/profile/operator.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/schedule/WeeklyCycleAfterBackup.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/schedule/WeeklyCycle.conf
%attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-dir.d/storage/File.conf
%attr(0750, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir-export/
%endif
%if 0%{?build_qt_monitor} && %{with vanilla_config}
%attr(0755, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/tray-monitor.d/director
%attr(0644, %{bareos_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/tray-monitor.d/director/Director-local.conf
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-director
%attr(0775, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_localstatedir}/log/%{name}
# we do not have any dir plugin but the python plugin
#%%{bareos_plugin_dir}/*-dir.so
%{bareos_script_dir}/delete_catalog_backup
%{bareos_script_dir}/make_catalog_backup
%{bareos_script_dir}/make_catalog_backup.pl
%{_sbindir}/bareos-dir
%dir %{_docdir}/%{name}
%{_mandir}/man8/bareos-dir.8.gz
%{_mandir}/man8/bareos.8.gz
%if 0%{?systemd_support}
%{_unitdir}/bareos-dir.service
%endif

%{bareos_script_dir}/query.sql

%files storage
# sd package (bareos-sd, bls, btape, bcopy, bextract)
%defattr(-, root, root)
%if %{with vanilla_config}
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/autochanger
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/device
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/director
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/ndmp
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/messages
%attr(0750, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-sd.d/storage
%attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-sd.d/device/FileStorage.conf
%attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-sd.d/director/bareos-dir.conf
%attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-sd.d/director/bareos-mon.conf
%attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-sd.d/messages/Standard.conf
%attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-sd.d/storage/bareos-sd.conf
%endif
%if 0%{?build_qt_monitor} && %{with vanilla_config}
%attr(0755, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/tray-monitor.d/storage
%attr(0644, %{bareos_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/tray-monitor.d/storage/StorageDaemon-local.conf
%endif
%if 0%{?suse_version}
%if !0%{?systemd_support}
%{_sysconfdir}/init.d/bareos-sd
%endif
%{_sbindir}/rcbareos-sd
%if 0%{?install_suse_fw}
# use noreplace if user has adjusted its list of IP
%attr(0644, root, root) %config(noreplace) %{_fwdefdir}/bareos-sd
%endif
%if 0%{?firewalld}
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/services
%{_prefix}/lib/firewalld/services/bareos-sd.xml
%endif
%else
%if !0%{?systemd_support}
%{_sysconfdir}/rc.d/init.d/bareos-sd
%endif
%endif
%{_sbindir}/bareos-sd
%{bareos_script_dir}/disk-changer
%{bareos_plugin_dir}/autoxflate-sd.so
%{_mandir}/man8/bareos-sd.8.gz
%if 0%{?systemd_support}
%{_unitdir}/bareos-sd.service
%endif
%attr(0775, %{bareos_storage_daemon_user}, %{bareos_daemon_group}) %dir /var/lib/%{name}/storage

%files storage-tape
# tape specific files
%defattr(-, root, root)
%{bareos_backend_dir}/libbareossd-gentape*.so
%{bareos_backend_dir}/libbareossd-tape*.so
%{bareos_script_dir}/mtx-changer
%if %{with vanilla_config}
%config(noreplace) %{_sysconfdir}/%{name}/mtx-changer.conf
%endif
%{_mandir}/man8/bscrypto.8.gz
%{_mandir}/man8/btape.8.gz
%{_sbindir}/bscrypto
%{_sbindir}/btape
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/storage/Tape.conf.example
%config %attr(0640, %{bareos_storage_daemon_user},  %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-sd.d/autochanger/autochanger-0.conf.example
%config %attr(0640, %{bareos_storage_daemon_user},  %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-sd.d/device/tapedrive-0.conf.example
%endif
%{bareos_plugin_dir}/scsicrypto-sd.so
%{bareos_plugin_dir}/scsitapealert-sd.so

%files storage-fifo
%defattr(-, root, root)
%{bareos_backend_dir}/libbareossd-fifo*.so
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/storage/NULL.conf.example
%config %attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group})  %{_sysconfdir}/%{name}/bareos-sd.d/device/NULL.conf.example
%endif

%if 0%{?droplet}
%files storage-droplet
%defattr(-, root, root)
%{bareos_backend_dir}/libbareossd-chunked*.so
%{bareos_backend_dir}/libbareossd-droplet*.so
%{bareos_library_dir}/libbareosdroplet.so*
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user},%{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/storage/S3_Object.conf.example
%config %attr(0640, %{bareos_storage_daemon_user},%{bareos_daemon_group})  %{_sysconfdir}/%{name}/bareos-sd.d/device/S3_ObjectStorage.conf.example
%dir %{_sysconfdir}/%{name}/bareos-sd.d/device/droplet/
%config %attr(0640, %{bareos_storage_daemon_user},%{bareos_daemon_group})  %{_sysconfdir}/%{name}/bareos-sd.d/device/droplet/*.example
%endif
%endif

%if 0%{?glusterfs}
%files storage-glusterfs
%defattr(-, root, root)
%{bareos_backend_dir}/libbareossd-gfapi*.so
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/storage/Gluster.conf.example
%config %attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group})  %{_sysconfdir}/%{name}/bareos-sd.d/device/GlusterStorage.conf.example
%endif
%endif

%if 0%{?ceph}
%files storage-ceph
%defattr(-, root, root)
%{bareos_backend_dir}/libbareossd-rados*.so
%{bareos_backend_dir}/libbareossd-cephfs*.so
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/storage/Rados.conf.example
%config %attr(0640, %{bareos_storage_daemon_user}, %{bareos_daemon_group})  %{_sysconfdir}/%{name}/bareos-sd.d/device/RadosStorage.conf.example
%endif
%endif

# not client_only
%endif

%files filedaemon
# fd package (bareos-fd, plugins)
%defattr(-, root, root)
%if %{with vanilla_config}
%attr(0750, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-fd.d/
%attr(0750, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-fd.d/client
%attr(0750, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-fd.d/director
%attr(0750, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-fd.d/messages
%attr(0640, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-fd.d/client/myself.conf
%attr(0640, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-fd.d/director/bareos-dir.conf
%attr(0640, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-fd.d/director/bareos-mon.conf
%attr(0640, %{bareos_file_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/bareos-fd.d/messages/Standard.conf
%endif
%if 0%{?build_qt_monitor} && %{with vanilla_config}
%attr(0755, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/tray-monitor.d/client
%attr(0644, %{bareos_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/tray-monitor.d/client/FileDaemon-local.conf
%endif
%if 0%{?suse_version}
%config %{_sysconfdir}/permissions.d/%{name}-fd.*
%verify(not mode caps) %attr(0750, root, %{bareos_daemon_group}) %{_sbindir}/%{name}-fd
%if !0%{?systemd_support}
%{_sysconfdir}/init.d/bareos-fd
%endif
%{_sbindir}/rcbareos-fd
%if 0%{?install_suse_fw}
# use noreplace if user has adjusted its list of IP
%attr(0644, root, root) %config(noreplace) %{_fwdefdir}/bareos-fd
%endif
%if 0%{?firewalld}
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/services
%{_prefix}/lib/firewalld/services/bareos-fd.xml
%endif
%else
%if !0%{?systemd_support}
%{_sysconfdir}/rc.d/init.d/bareos-fd
%endif
%{_sbindir}/bareos-fd
%endif
%{bareos_plugin_dir}/bpipe-fd.so
%{_mandir}/man8/bareos-fd.8.gz
# tray monitor
%if 0%{?systemd_support}
%{_unitdir}/bareos-fd.service
%endif

%files common
# common shared libraries (without db)
%defattr(-, root, root)
%attr(0755, root, %{bareos_daemon_group})           %dir %{_sysconfdir}/%{name}
%if !0%{?client_only}
# these directories belong to bareos-common,
# as other packages may contain configurations for the director.
%if %{with vanilla_config}
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/catalog
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/client
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/console
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/counter
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/director
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/fileset
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/job
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/jobdefs
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/messages
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/pool
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/profile
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/schedule
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/storage
%attr(0750, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/bareos-dir.d/user
%endif
# tray monitor configurate is installed by the target daemons
%if 0%{?build_qt_monitor} && %{with vanilla_config}
%attr(0755, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/tray-monitor.d
%endif
%endif
%dir %{bareos_backend_dir}
%{bareos_library_dir}/libbareosfastlz.so*
%{bareos_library_dir}/libbareos.so*
%{bareos_library_dir}/libbareosfind.so*
%{bareos_library_dir}/libbareoslmdb.so*
%if !0%{?client_only}
%{bareos_library_dir}/libbareosndmp.so*
%{bareos_library_dir}/libbareossd.so*
%endif
# generic stuff needed from multiple bareos packages
%dir /usr/lib/%{name}/
%dir %{bareos_script_dir}
%{bareos_script_dir}/bareos-config
%{bareos_script_dir}/bareos-config-lib.sh
%{bareos_script_dir}/bareos-explorer
%{bareos_script_dir}/btraceback.gdb
%if "%{_libdir}" != "/usr/lib/"
%dir %{_libdir}/%{name}/
%endif
%dir %{bareos_plugin_dir}
%if !0%{?client_only}
%{_bindir}/bsmtp
%endif
%{_sbindir}/btraceback
%if !0%{?client_only}
%{_mandir}/man1/bsmtp.1.gz
%endif
%{_mandir}/man8/btraceback.8.gz
%attr(0770, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{bareos_working_dir}
%attr(0775, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_localstatedir}/log/%{name}
%doc core/AGPL-3.0.txt core/LICENSE core/README.*
#TODO: cmake does not create build directory
#doc build/

%if !0%{?client_only}

%files database-common
# catalog independent files
%defattr(-, root, root)
%{bareos_library_dir}/libbareossql*.so.*
%{bareos_library_dir}/libbareoscats*.so.*
%dir %{bareos_script_dir}/ddl
%dir %{bareos_script_dir}/ddl/creates
%dir %{bareos_script_dir}/ddl/drops
%dir %{bareos_script_dir}/ddl/grants
%dir %{bareos_script_dir}/ddl/updates
%{bareos_script_dir}/create_bareos_database
%{bareos_script_dir}/drop_bareos_database
%{bareos_script_dir}/drop_bareos_tables
%{bareos_script_dir}/grant_bareos_privileges
%{bareos_script_dir}/make_bareos_tables
%{bareos_script_dir}/update_bareos_tables
%{bareos_script_dir}/ddl/versions.map

%files database-postgresql
# postgresql catalog files
%defattr(-, root, root)
%{bareos_script_dir}/ddl/*/postgresql*.sql
%{bareos_backend_dir}/libbareoscats-postgresql.so*

%files database-tools
# dbtools with link to db libs (dbcheck, bscan, dbcopy)
%defattr(-, root, root)
%{_sbindir}/bareos-dbcheck
%{_sbindir}/bscan
%{_mandir}/man8/bareos-dbcheck.8.gz
%{_mandir}/man8/bscan.8.gz

%files tools
# tools without link to db libs (bwild, bregex)
%defattr(-, root, root)
%{_bindir}/bregex
%{_bindir}/bwild
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/bpluginfo
%{_mandir}/man1/bwild.1.gz
%{_mandir}/man1/bregex.1.gz
%{_mandir}/man8/bcopy.8.gz
%{_mandir}/man8/bextract.8.gz
%{_mandir}/man8/bls.8.gz
%{_mandir}/man8/bpluginfo.8.gz

%if 0%{?build_qt_monitor}
%files traymonitor
%defattr(-,root, root)
%if %{with vanilla_config}
%attr(0755, %{bareos_daemon_user}, %{bareos_daemon_group}) %dir %{_sysconfdir}/%{name}/tray-monitor.d/monitor
%attr(0644, %{bareos_daemon_user}, %{bareos_daemon_group}) %config(noreplace) %{_sysconfdir}/%{name}/tray-monitor.d/monitor/bareos-mon.conf
%endif
%config %{_sysconfdir}/xdg/autostart/bareos-tray-monitor.desktop
%{_bindir}/bareos-tray-monitor
%{_mandir}/man1/bareos-tray-monitor.1.gz
/usr/share/applications/bareos-tray-monitor.desktop
/usr/share/pixmaps/bareos-tray-monitor.png
%endif

# client_only
%endif

%if 0%{?python_plugins}
%files filedaemon-python2-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python-fd.so
%{python2_sitelib}/bareosfd*.so

%files filedaemon-python3-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python3-fd.so
%{python3_sitelib}/bareosfd*.so

%files filedaemon-python-plugins-common
%defattr(-, root, root)
%{bareos_plugin_dir}/bareos-fd-local-fileset.py*
%{bareos_plugin_dir}/BareosFdPluginBaseclass.py*
%{bareos_plugin_dir}/BareosFdPluginLocalFileset.py*
%{bareos_plugin_dir}/BareosFdPluginLocalFilesBaseclass.py*
%{bareos_plugin_dir}/BareosFdWrapper.py*

%files filedaemon-ldap-python-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/bareos-fd-ldap.py*
%{bareos_plugin_dir}/BareosFdPluginLDAP.py*
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/plugin-ldap.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/backup-ldap.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/restore-ldap.conf.example
%endif

%files filedaemon-ovirt-python-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/bareos-fd-ovirt.py*
%{bareos_plugin_dir}/BareosFdPluginOvirt.py*
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/plugin-ovirt.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/backup-ovirt.conf.example
%endif

%files filedaemon-libcloud-python-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/bareos-fd-libcloud.py*
%{bareos_plugin_dir}/BareosFdPluginLibcloud.py*
%{bareos_plugin_dir}/BareosLibcloudApi.py*
%dir %{bareos_plugin_dir}/bareos_libcloud_api
%{bareos_plugin_dir}/bareos_libcloud_api/*

#attr(0640, #{director_daemon_user}, #{daemon_group}) #{_sysconfdir}/#{name}/bareos-dir.d/fileset/plugin-libcloud.conf.example
#attr(0640, #{director_daemon_user}, #{daemon_group}) #{_sysconfdir}/#{name}/bareos-dir.d/job/backup-libcloud.conf.example

%files filedaemon-postgresql-python-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/BareosFdPluginPostgres.py*
%{bareos_plugin_dir}/bareos-fd-postgres.py*

%files filedaemon-percona-xtrabackup-python-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/bareos-fd-percona-xtrabackup.py*
%{bareos_plugin_dir}/BareosFdPluginPerconaXtraBackup.py*
##attr(0640, #{director_daemon_user}, #{daemon_group}) #{_sysconfdir}/#{name}/bareos-dir.d/fileset/plugin-percona-xtrabackup.conf.example
##attr(0640, #{director_daemon_user}, #{daemon_group}) #{_sysconfdir}/#{name}/bareos-dir.d/job/backup-percona-xtrabackup.conf.example
##attr(0640, #{director_daemon_user}, #{daemon_group}) #{_sysconfdir}/#{name}/bareos-dir.d/job/restore-percona-xtrabackup.conf.example
%{bareos_plugin_dir}/BareosFdPluginMariabackup.py
%{bareos_plugin_dir}/bareos-fd-mariabackup.py

%files director-python2-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python-dir.so
%{python2_sitelib}/bareosdir*.so

%files director-python3-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python3-dir.so
%{python3_sitelib}/bareosdir*.so

%files director-python-plugins-common
%defattr(-, root, root)
%{bareos_plugin_dir}/BareosDirPluginBaseclass.py*
%{bareos_plugin_dir}/bareos-dir-class-plugin.py*
%{bareos_plugin_dir}/BareosDirWrapper.py*

%files storage-python2-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python-sd.so
%{python2_sitelib}/bareossd*.so

%files storage-python3-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/python3-sd.so
%{python3_sitelib}/bareossd*.so

%files storage-python-plugins-common
%defattr(-, root, root)
%{bareos_plugin_dir}/BareosSdPluginBaseclass.py*
%{bareos_plugin_dir}/BareosSdWrapper.py*
%{bareos_plugin_dir}/bareos-sd-class-plugin.py*

# python_plugins
%endif

%if 0%{?glusterfs}
%files filedaemon-glusterfs-plugin
%defattr(-, root, root)
%{bareos_script_dir}/bareos-glusterfind-wrapper
%{bareos_plugin_dir}/gfapi-fd.so
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/plugin-gfapi.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/BackupGFAPI.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/RestoreGFAPI.conf.example
%endif
%endif

%if 0%{?ceph}
%files filedaemon-ceph-plugin
%defattr(-, root, root)
%{bareos_plugin_dir}/cephfs-fd.so
%{bareos_plugin_dir}/rados-fd.so
%if %{with vanilla_config}
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/plugin-cephfs.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/BackupCephfs.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/RestoreCephfs.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/fileset/plugin-rados.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/BackupRados.conf.example
%config %attr(0640, %{bareos_director_daemon_user}, %{bareos_daemon_group}) %{_sysconfdir}/%{name}/bareos-dir.d/job/RestoreRados.conf.example
%endif
%endif

%files regress-config
%defattr(-, root, root)
%{bareos_script_dir}/%{name}
%{bareos_script_dir}/bareos-ctl-*
%{_sbindir}/btestls

#
# Define some macros for updating the system settings.
#
%if ! 0%{?suse_version}
# non suse, systemd

%define add_service_start() \
/bin/systemctl daemon-reload >/dev/null 2>&1 || true \
/bin/systemctl enable %1.service >/dev/null 2>&1 || true \
%nil

%define stop_on_removal() \
test -n "$FIRST_ARG" || FIRST_ARG=$1 \
if test "$FIRST_ARG" = "0" ; then \
  /bin/systemctl stop %1.service > /dev/null 2>&1 || true \
fi \
%nil

%define restart_on_update() \
test -n "$FIRST_ARG" || FIRST_ARG=$1 \
if test "$FIRST_ARG" -ge 1 ; then \
  /bin/systemctl try-restart %1.service >/dev/null 2>&1 || true \
fi \
%nil

%endif


%post webui
%if 0%{?suse_version} >= 1315
a2enmod setenv &> /dev/null || true
a2enmod rewrite &> /dev/null || true
%endif

%if 0%{?suse_version} >= 1315
# 1315:
#   SLES12 (PHP 7)
#   openSUSE Leap 42.1 (PHP 5)
if php -v | grep -q "PHP 7"; then
  a2enmod php7 &> /dev/null || true
else
  a2enmod php5 &> /dev/null || true
fi
%else
a2enmod php5 &> /dev/null || true
%endif

%post director
%if %{with vanilla_config}
%{bareos_script_dir}/bareos-config initialize_local_hostname
%{bareos_script_dir}/bareos-config initialize_passwords
%{bareos_script_dir}/bareos-config initialize_database_driver
%endif
%if 0%{?suse_version} >= 1315
%service_add_post bareos-dir.service
%if 0%{?firewalld}
%firewalld_reload
%endif
%else
%add_service_start bareos-dir
%endif

%post storage
%if %{with vanilla_config}
%{bareos_script_dir}/bareos-config setup_sd_user
%{bareos_script_dir}/bareos-config initialize_local_hostname
%{bareos_script_dir}/bareos-config initialize_passwords
%endif
%if 0%{?suse_version} >= 1315
%service_add_post bareos-sd.service
%if 0%{?firewalld}
%firewalld_reload
%endif
%else
%add_service_start bareos-sd
%endif

%post filedaemon
%if %{with vanilla_config}
%{bareos_script_dir}/bareos-config initialize_local_hostname
%{bareos_script_dir}/bareos-config initialize_passwords
%endif
%if 0%{?suse_version} >= 1315
%set_permissions %{_sbindir}/%{name}-fd
%service_add_post bareos-fd.service
%if 0%{?firewalld}
%firewalld_reload
%endif
%else
%add_service_start bareos-fd
%endif

%if 0%{?suse_version}
%verifyscript filedaemon
%verify_permissions -e %{_sbindir}/%{name}-fd
%endif

%post bconsole
%if %{with vanilla_config}
%{bareos_script_dir}/bareos-config initialize_local_hostname
%{bareos_script_dir}/bareos-config initialize_passwords
%endif

%post common
/sbin/ldconfig

%postun common
/sbin/ldconfig

%post database-common
/sbin/ldconfig

%postun database-common
/sbin/ldconfig

%post database-postgresql
/sbin/ldconfig

%postun database-postgresql
/sbin/ldconfig

%if 0%{?build_qt_monitor}

%post traymonitor
%{bareos_script_dir}/bareos-config initialize_local_hostname
%{bareos_script_dir}/bareos-config initialize_passwords

%endif


%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%pre -f %{name}.pre director
%else
%pre director
%create_group %{bareos_daemon_group}
%create_user  %{bareos_director_daemon_user}
%endif
%if 0%{?suse_version} >= 1315
%service_add_pre bareos-dir.service
%endif

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%pre -f %{name}.pre storage
%else
%pre storage
%create_group %{bareos_daemon_group}
%create_user  %{bareos_storage_daemon_user}
%endif
%if 0%{?suse_version} >= 1315
%service_add_pre bareos-sd.service
%endif

%if 0%{?sle_version} >= 150000 || 0%{?suse_version} > 1500
%pre -f %{name}.pre filedaemon
%else
%pre filedaemon
%create_group %{bareos_daemon_group}
%create_user  %{bareos_storage_daemon_user}
%endif
%if 0%{?suse_version} >= 1315
%service_add_pre bareos-fd.service
%endif

%if ! 0%{?suse_version} >= 150200
%pre common
%create_group %{bareos_daemon_group}
%create_user  %{bareos_daemon_user}
%endif

%preun director
%if 0%{?suse_version} >= 1315
%service_del_preun bareos-dir.service
%else
%stop_on_removal bareos-dir
%endif

%preun storage
%if 0%{?suse_version} >= 1315
%service_del_preun bareos-sd.service
%else
%stop_on_removal bareos-sd
%endif

%preun filedaemon
%if 0%{?suse_version} >= 1315
%service_del_preun bareos-fd.service
%else
%stop_on_removal bareos-fd
%endif

%postun director
# to prevent aborting jobs, no restart on update
%if 0%{?suse_version} >= 1315
%service_del_postun bareos-dir.service
%endif

%postun storage
# to prevent aborting jobs, no restart on update
%if 0%{?suse_version} >= 1315
%service_del_postun bareos-sd.service
%endif

%postun filedaemon
%if 0%{?suse_version} >= 1315
%service_del_postun bareos-fd.service
%else
%restart_on_update bareos-fd
%endif

%changelog
