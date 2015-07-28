# Created by pyp2rpm-1.1.2
%global pypi_name oslo.cache

Name:           python-oslo-cache
Version:        0.2.0
Release:        1%{?dist}
Summary:        Cache storage for Openstack projects

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-sphinx

Requires:       python-babel
Requires:       python-dogpile-cache
Requires:       python-six
Requires:       python-oslo-config
Requires:       python-oslo-i18n
Requires:       python-oslo-log
Requires:       python-oslo-utils
Requires:       python-memcached


%description
oslo.cache aims to provide a generic caching mechanism for OpenStack projects 
by wrapping the dogpile.cache library. The dogpile.cache library provides
support memoization, key value storage and interfaces to common caching
backends such as Memcached.

%package doc
Summary:        Documentation for the OpenStack Oslo Cache library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-fixtures
BuildRequires:  dos2unix

%description doc
Documentation for the OpenStack Oslo cache library.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Let RPM handle the dependencies
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

rm -f {test-,}requirements.txt


%build
%{__python2} setup.py build
#doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
dos2unix doc/build/html/_static/jquery.js

%files
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{python2_sitelib}/oslo_cache
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Fri Jul 10 2015 Chandan Kumar <chkumar246@gmail.com> - 0.2.0-1
- Initial package.
