%define srcname requests-scitokens
%define version 0.1.0
%define release 1

# -- metadata ---------------

BuildArch: noarch
License:   ASL 2.0
Name:      python-%{srcname}
Packager:  Duncan Macleod <macleoddm@cardiff.ac.uk>
Prefix:    %{_prefix}
Release:   %{release}%{?dist}
Source0:   %pypi_source
Summary:   SciTokens auth plugin for python3-requests
Url:       https://github.com/duncanmmacleod/requests-scitokens
Vendor:    Duncan Macleod <macleoddm@cardiff.ac.uk>
Version:   %{version}

# -- build requirements -----

# static build requirements
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
BuildRequires: pyproject-rpm-macros
%endif
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}dist(pip)
BuildRequires: python%{python3_pkgversion}dist(setuptools)
BuildRequires: python%{python3_pkgversion}dist(wheel)

# test requirements
BuildRequires: python%{python3_pkgversion}dist(pytest)
BuildRequires: python%{python3_pkgversion}dist(requests) >= 2.20.0
BuildRequires: python%{python3_pkgversion}dist(scitokens) >= 1.7.4

# -- packages ---------------

# src.rpm
%description
requests-scitokens adds optional SciTokens authorisation support
for the python3-requests HTTP library.

%package -n python%{python3_pkgversion}-%{srcname}
Summary: %{summary}
Requires: python%{python3_pkgversion}dist(requests) >= 2.20.0
Requires: python%{python3_pkgversion}dist(scitokens) >= 1.7.4
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
requests-scitokens adds optional SciTokens authorisation support
for the python3-requests HTTP library.
This package provides the Python %{python3_version} library.

# -- build ------------------

%prep
%autosetup -n %{srcname}-%{version}
# for RHEL < 9 hack together setup.{cfg,py} for old setuptools
%if 0%{?rhel} > 0 || 0%{?rhel} < 9
cat > setup.cfg <<EOF
[metadata]
name = %{srcname}
version = %{version}
author-email = %{packager}
description = %{summary}
license = %{license}
license_files = LICENSE
url = %{url}
[options]
packages = find:
python_requires = >=3.6
install_requires =
	requests >= 2.20.0
	scitokens >= 1.7.4
EOF
cat > setup.py <<EOF
from setuptools import setup
setup()
EOF
%endif

%build
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_wheel
%else
%py3_build_wheel
%endif

%install
%if 0%{?rhel} == 0 || 0%{?rhel} >= 9
%pyproject_install
%else
%py3_install_wheel requests_scitokens-%{version}*.whl
%endif

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
%python3 -m pip show requests-scitokens
%pytest --verbose -ra --pyargs requests_scitokens

# -- files ------------------

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog --------------

%changelog
* Tue Feb 13 2024 Duncan Macleod <macleoddm@cardiff.ac.uk> - 0.1.0-1
- first release
