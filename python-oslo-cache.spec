%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

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
Version:        1.28.1
Release:        1%{?dist}
Summary:        Cache storage for Openstack projects

License:        ASL 2.0
URL:            http://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  git

%package -n python2-%{pkg_name}
Summary:        Cache storage for Openstack projects
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-urllib3
# Required for tests
BuildRequires:  python2-hacking
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-log
# Required to compile translation files
BuildRequires:  python2-babel
%if 0%{?fedora} > 0
BuildRequires:  python2-memcached
BuildRequires:  python2-pymongo
BuildRequires:  python2-dogpile-cache >= 0.6.2
%else
BuildRequires:  python-memcached
BuildRequires:  python-pymongo
BuildRequires:  python-dogpile-cache >= 0.6.2
%endif

Requires:       python2-six
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-utils >= 3.33.0
%if 0%{?fedora} > 0
Requires:       python2-dogpile-cache >= 0.6.2
Requires:       python2-memcached
%else
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-memcached
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}


%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Documentation for the OpenStack Oslo Cache library

BuildRequires:  python2-sphinx
BuildRequires:  python2-oslo-config
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-oslo-sphinx
BuildRequires:  python2-fixtures
BuildRequires:  dos2unix

%description doc
Documentation for the OpenStack Oslo cache library.
%endif

%package  -n python2-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python2-%{pkg_name} = %{version}-%{release}
Requires:  python2-hacking
Requires:  python2-mock
Requires:  python2-oslotest
%if 0%{?fedora} > 0
Requires:  python2-pymongo
%else
Requires:  python-pymongo
%endif

%description -n python2-%{pkg_name}-tests
Tests for the OpenStack Oslo Cache library

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        Cache storage for Openstack projects
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Required for tests
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-memcached
BuildRequires:  python3-pymongo

Requires:       python3-dogpile-cache >= 0.6.2
Requires:       python3-six
Requires:       python3-oslo-config >= 2:5.1.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-memcached
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%package  -n python3-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-pymongo

%description -n python3-%{pkg_name}-tests
Tests for the OpenStack Oslo Cache library
%endif

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
#doc
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_cache/locale

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif
%if 0%{?with_doc}
dos2unix doc/build/html/_static/jquery.js
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_cache/locale/*/LC_*/oslo_cache*po
rm -f %{buildroot}%{python2_sitelib}/oslo_cache/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_cache/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_cache/locale
%endif

# Find language files
%find_lang oslo_cache --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{python2_sitelib}/oslo_cache
%{python2_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python2_sitelib}/oslo_cache/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_cache/tests

%files -n python-%{pkg_name}-lang -f oslo_cache.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{python3_sitelib}/oslo_cache
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/oslo_cache/tests

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_cache/tests
%endif

%changelog
* Thu Jun 06 2019 RDO <dev@lists.rdoproject.org> 1.28.1-1
- Update to 1.28.1

* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 1.28.0-1
- Update to 1.28.0

