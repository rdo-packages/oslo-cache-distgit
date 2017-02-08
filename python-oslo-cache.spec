%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global pypi_name oslo.cache
%global pkg_name oslo-cache

Name:           python-oslo-cache
Version:        1.17.0
Release:        1%{?dist}
Summary:        Cache storage for Openstack projects

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch
 

%package -n python2-%{pkg_name}
Summary:        Cache storage for Openstack projects
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# Required for documentation build
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-config
BuildRequires:  python-dogpile-cache >= 0.6.1
BuildRequires:  python-oslo-log
# Required for tests
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-oslotest
BuildRequires:  python-memcached
BuildRequires:  python-pymongo
# Required to compile translation files
BuildRequires:  python-babel

Requires:       python-babel
Requires:       python-dogpile-cache >= 0.6.1
Requires:       python-six
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-oslo-log
Requires:       python-oslo-utils
Requires:       python-memcached
Requires:       python-%{pkg_name}-lang = %{version}-%{release}


%description -n python2-%{pkg_name}
oslo.cache aims to provide a generic caching mechanism for OpenStack projects 
by wrapping the dogpile.cache library. The dogpile.cache library provides
support memoization, key value storage and interfaces to common caching
backends such as Memcached.

%package doc
Summary:        Documentation for the OpenStack Oslo Cache library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-fixtures
BuildRequires:  dos2unix

%description doc
Documentation for the OpenStack Oslo cache library.

%package  -n python2-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python-%{pkg_name} = %{version}-%{release}
Requires:  python-hacking
Requires:  python-mock
Requires:  python-oslotest
Requires:  python-pymongo

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

Requires:       python3-babel
Requires:       python3-dogpile-cache
Requires:       python3-six
Requires:       python3-oslo-config
Requires:       python3-oslo-i18n
Requires:       python3-oslo-log
Requires:       python3-oslo-utils
Requires:       python3-memcached
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
oslo.cache aims to provide a generic caching mechanism for OpenStack projects 
by wrapping the dogpile.cache library. The dogpile.cache library provides
support memoization, key value storage and interfaces to common caching
backends such as Memcached.

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
oslo.cache aims to provide a generic caching mechanism for OpenStack projects 
by wrapping the dogpile.cache library. The dogpile.cache library provides
support memoization, key value storage and interfaces to common caching
backends such as Memcached.


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
#doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_cache/locale

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif
dos2unix doc/build/html/_static/jquery.js

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

%files doc
%doc doc/build/html
%license LICENSE

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
* Wed Feb 08 2017 Alfredo Moralejo <amoralej@redhat.com> 1.17.0-1
- Update to 1.17.0

