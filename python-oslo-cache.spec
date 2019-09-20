# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# NOTE(ykarel) disable doc as doc depends on etcd3gw which is
# not packaged.
%global with_doc 0

%global pypi_name oslo.cache
%global pkg_name oslo-cache

%global common_desc \
oslo.cache aims to provide a generic caching mechanism for OpenStack projects \
by wrapping the dogpile.cache library. The dogpile.cache library provides \
support memoization, key value storage and interfaces to common caching \
backends such as Memcached.

Name:           python-oslo-cache
Version:        XXX
Release:        XXX
Summary:        Cache storage for Openstack projects

License:        ASL 2.0
URL:            http://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%package -n python%{pyver}-%{pkg_name}
Summary:        Cache storage for Openstack projects
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-urllib3
# Required for tests
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-stestr
# Required to compile translation files
BuildRequires:  python%{pyver}-babel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python%{pyver}-memcached
BuildRequires:  python%{pyver}-dogpile-cache >= 0.6.2
%else
BuildRequires:  python-memcached
BuildRequires:  python-dogpile-cache >= 0.6.2
%endif

Requires:       python%{pyver}-six >= 1.11.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python%{pyver}-dogpile-cache >= 0.6.2
Requires:       python%{pyver}-memcached
%else
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-memcached
%endif
Requires:       python%{pyver}-%{pkg_name}-lang = %{version}-%{release}


%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Documentation for the OpenStack Oslo Cache library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  dos2unix

%description doc
Documentation for the OpenStack Oslo cache library.
%endif

%package  -n python%{pyver}-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-stestr

%description -n python%{pyver}-%{pkg_name}-tests
Tests for the OpenStack Oslo Cache library

%package  -n python%{pyver}-%{pkg_name}-lang
Summary:   Translation files for Oslo cache library

%description -n python%{pyver}-%{pkg_name}-lang
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
%{pyver_build}

%if 0%{?with_doc}
#doc
%{pyver_bin} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif
# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_cache/locale

%install
%{pyver_install}
%if 0%{?with_doc}
dos2unix doc/build/html/_static/jquery.js
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
%if %{pyver} == 3
rm -rf %{buildroot}%{python2_sitelib}/oslo_cache/locale
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*/LC_*/oslo_cache*po
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_cache/locale %{buildroot}%{_datadir}/locale
%else
rm -rf %{buildroot}%{python3_sitelib}/oslo_cache/locale
rm -f %{buildroot}%{python2_sitelib}/oslo_cache/locale/*/LC_*/oslo_cache*po
rm -f %{buildroot}%{python2_sitelib}/oslo_cache/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_cache/locale %{buildroot}%{_datadir}/locale
%endif

# Find language files
%find_lang oslo_cache --all-name

%check
PYTHON=python%{pyver} stestr-%{pyver} --test-path ./oslo_cache/tests run --black-regex 'oslo_cache.tests.test_cache_backend_mongo'

%files -n python%{pyver}-%{pkg_name}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{pyver_sitelib}/oslo_cache
%{pyver_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{pyver_sitelib}/oslo_cache/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_cache/tests

%files -n python%{pyver}-%{pkg_name}-lang -f oslo_cache.lang
%license LICENSE

%changelog
