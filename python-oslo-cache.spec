%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pifpaf
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

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

License:        Apache-2.0
URL:            http://launchpad.net/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core

%package -n python3-%{pkg_name}
Summary:        Cache storage for Openstack projects

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:       python-%{pkg_name}-lang = %{version}-%{release}


%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for the OpenStack Oslo Cache library

%description -n python-%{pkg_name}-doc
Documentation for the OpenStack Oslo cache library.
%endif

%package  -n python3-%{pkg_name}-tests
Summary:        Tests for the OpenStack Oslo Cache library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-%{pkg_name}+dogpile = %{version}-%{release}
Requires:  python3-%{pkg_name}+etcd3gw = %{version}-%{release}
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
#doc
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_cache/locale --domain oslo_cache

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*/LC_*/oslo_cache*po
rm -f %{buildroot}%{python3_sitelib}/oslo_cache/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_cache/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_cache --all-name

%check
%tox -e %{default_toxenv}

%pyproject_extras_subpkg -n python3-%{pkg_name} dogpile etcd3gw

%files -n python3-%{pkg_name}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{python3_sitelib}/oslo_cache
%{python3_sitelib}/%{pypi_name}-%{upstream_version}.dist-info
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
# REMOVEME: error caused by commit https://opendev.org/openstack/oslo.cache/commit/a7200161b056a7febce470b06817f8ddc1c65e41
