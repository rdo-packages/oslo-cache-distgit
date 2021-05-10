%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global pypi_name oslo.cache
%global pkg_name oslo-cache

%global common_desc \
oslo.cache aims to provide a generic caching mechanism for OpenStack projects \
by wrapping the dogpile.cache library. The dogpile.cache library provides \
support memoization, key value storage and interfaces to common caching \
backends such as Memcached.

Name:           python-oslo-cache
Version:        2.3.1
Release:        1%{?dist}
Summary:        Cache storage for Openstack projects

License:        ASL 2.0
URL:            http://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%package -n python3-%{pkg_name}
Summary:        Cache storage for Openstack projects
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-urllib3
# Required for tests
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-log
BuildRequires:  python3-stestr
BuildRequires:  python3-dogpile-cache >= 0.6.2
# Required to compile translation files
BuildRequires:  python3-babel
BuildRequires:  python3-memcached

Requires:       python3-etcd3gw >= 0.2.0
Requires:       python3-six >= 1.11.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-dogpile-cache >= 0.6.2
Requires:       python3-memcached
Requires:       python-%{pkg_name}-lang = %{version}-%{release}


%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for the OpenStack Oslo Cache library

BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-oslo-config
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-etcd3gw
BuildRequires:  python3-fixtures

%description -n python-%{pkg_name}-doc
Documentation for the OpenStack Oslo cache library.
%endif

%package  -n python3-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-stestr

%description -n python3-%{pkg_name}-tests
Tests for the OpenStack Oslo Cache library

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo cache library

%description -n python-%{pkg_name}-lang
Translation files for Oslo cache library

%description
%{common_desc}


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Let RPM handle the dependencies
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
rm -f {test-,}requirements.txt


%build
%{py3_build}

%if 0%{?with_doc}
#doc
sphinx-build -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif
# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_cache/locale

%install
%{py3_install}
# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*/LC_*/oslo_cache*po
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_cache/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_cache --all-name

%check
PYTHON=python3 stestr-3 --test-path ./oslo_cache/tests run --black-regex 'oslo_cache.tests.test_cache_backend_mongo'

%files -n python3-%{pkg_name}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{python3_sitelib}/oslo_cache
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/oslo_cache/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_cache/tests

%files -n python-%{pkg_name}-lang -f oslo_cache.lang
%license LICENSE

%changelog
* Wed Feb 17 2021 RDO <dev@lists.rdoproject.org> 2.3.1-1
- Update to 2.3.1

* Fri Apr 24 2020 RDO <dev@lists.rdoproject.org> 2.3.0-1
- Update to 2.3.0

