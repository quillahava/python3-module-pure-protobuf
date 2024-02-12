%define pypi_name pure-protobuf

Name:           python3-module-%pypi_name
Version:        2.3.0
Release:        alt1
Summary:        Python implementation of Protocol Buffers with dataclass-based schemaʼs

Group:          Development/Python3

License:        MIT
URL:            https://github.com/eigenein/protobuf.git
Source0:        %{name}-%{version}.tar
Patch0:         %{name}-%{version}-without-dynamic-versioning.patch

BuildRequires(pre): rpm-build-python3

BuildRequires:      git
BuildRequires:      python3-dev
BuildRequires:      python3(setuptools)
BuildRequires:      python3(wheel)
BuildRequires:      python3-module-poetry
BuildRequires:      python3-module-hatchling

Requires: python3-module-typing_extensions
Requires: python3-module-get-annotations

Provides: python3(gi.repository.GdkPixbuf)
Provides: python3(pure_protobuf.dataclasses_)
Provides: python3(pure_protobuf.types)
%py3_provides %pypi_name

BuildArch:      noarch

%description
pure-protobuf leverages the standard dataclasses module for defining message types, offering a modern alternative to the traditional approach. This method is recommended for new projects due to its simplicity and integration with Python's features. Compatible with Python 3.6 and later versions, the dataclasses interface streamlines the process of structuring your data. While the legacy interface remains accessible through pure_protobuf.legacy, it is considered deprecated and is not recommended for future use. This documentation aims to guide you in utilizing pure-protobuf effectively, aligning closely with the standard developer guide and presupposing a basic understanding of Protocol Buffers.

%prep
%setup -v
%autopatch -p1

%build
%pyproject_build

%install
%pyproject_install
install -Dm644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE


%files
%doc README.md CONTRIBUTING.md
%_licensedir/%name/LICENSE
%python3_sitelibdir/*

%changelog
* Thu Feb 8 2024 Aleksandr A. Voyt <vojtaa@basealt.ru> 2.3.0-alt1
- First package version

