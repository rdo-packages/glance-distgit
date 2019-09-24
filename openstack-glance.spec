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

%global release_name liberty
%global service glance
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global common_desc \
OpenStack Image Service (code-named Glance) provides discovery, registration, \
and delivery services for virtual disk images. The Image Service API server \
provides a standard REST interface for querying information about virtual disk \
images stored in a variety of back-end stores, including OpenStack Object \
Storage. Clients can register new virtual disk images with the Image Service, \
query for information on publicly available disk images, and use the Image \
Service's client library for streaming virtual disk images.

Name:             openstack-glance
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          OpenStack Image Service

License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source001:         openstack-glance-api.service
Source003:         openstack-glance-registry.service
Source004:         openstack-glance-scrubber.service
Source010:         openstack-glance.logrotate

Source021:         glance-api-dist.conf
Source022:         glance-cache-dist.conf
Source024:         glance-registry-dist.conf
Source025:         glance-scrubber-dist.conf
Source026:         glance-swift.conf

Source030:         glance-sudoers
Source031:         glance-rootwrap.conf

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    intltool
# Required for config generation
BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-alembic
BuildRequires:    python%{pyver}-cursive
BuildRequires:    python%{pyver}-defusedxml
BuildRequires:    python%{pyver}-eventlet
BuildRequires:    python%{pyver}-futurist
BuildRequires:    python%{pyver}-glance-store >= 1.0.0
BuildRequires:    python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-middleware >= 3.31.0
BuildRequires:    python%{pyver}-oslo-policy >= 1.30.0
BuildRequires:    python%{pyver}-oslo-utils >= 3.33.0
BuildRequires:    python%{pyver}-oslo-upgradecheck >= 0.1.0
BuildRequires:    python%{pyver}-osprofiler
BuildRequires:    python%{pyver}-requests
BuildRequires:    python%{pyver}-routes
BuildRequires:    python%{pyver}-oslo-messaging >= 5.29.0
BuildRequires:    python%{pyver}-taskflow >= 2.16.0
BuildRequires:    python%{pyver}-wsme >= 0.8.0
BuildRequires:    python%{pyver}-castellan >= 0.17.0

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-httplib2
BuildRequires:    python-paste-deploy
%else
BuildRequires:    python%{pyver}-httplib2
BuildRequires:    python%{pyver}-paste-deploy
%endif


Requires(pre):    shadow-utils
Requires:         python%{pyver}-glance = %{epoch}:%{version}-%{release}
Requires:         python%{pyver}-glanceclient >= 1:2.8.0

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
BuildRequires: systemd

%description
%{common_desc}

This package contains the API and registry servers.

%package -n       python%{pyver}-glance
Summary:          Glance Python libraries
%{?python_provide:%python_provide python%{pyver}-glance}

Requires:         python%{pyver}-cursive
Requires:         python%{pyver}-cryptography >= 2.1
Requires:         python%{pyver}-debtcollector >= 1.2.0
Requires:         python%{pyver}-defusedxml >= 0.5.0
Requires:         python%{pyver}-eventlet >= 0.22.0
Requires:         python%{pyver}-futurist >= 1.2.0
Requires:         python%{pyver}-glance-store >= 1.0.0
Requires:         python%{pyver}-iso8601 >= 0.1.11
Requires:         python%{pyver}-jsonschema
Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-keystonemiddleware >= 4.17.0
Requires:         python%{pyver}-oslo-concurrency >= 3.26.0
Requires:         python%{pyver}-oslo-config >= 2:5.2.0
Requires:         python%{pyver}-oslo-context >= 2.19.2
Requires:         python%{pyver}-oslo-db >= 4.27.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-log >= 3.36.0
Requires:         python%{pyver}-oslo-messaging >= 5.29.0
Requires:         python%{pyver}-oslo-middleware >= 3.31.0
Requires:         python%{pyver}-oslo-policy >= 1.30.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-oslo-vmware >= 0.11.1
Requires:         python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:         python%{pyver}-osprofiler
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-routes
Requires:         python%{pyver}-six >= 1.10.0
Requires:         python%{pyver}-sqlalchemy >= 1.0.10
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-swiftclient >= 2.2.0
Requires:         python%{pyver}-taskflow >= 2.16.0
Requires:         python%{pyver}-webob >= 1.8.1
Requires:         python%{pyver}-wsme >= 0.8.0
Requires:         python%{pyver}-os-brick >= 1.8.0
Requires:         python%{pyver}-alembic >= 0.8.10
Requires:         python%{pyver}-os-win >= 3.0.0
Requires:         python%{pyver}-castellan >= 0.17.0

%if 0%{?rhosp} == 0 || 0%{?rhel} > 7
Requires:         python%{pyver}-pyOpenSSL
%else
Requires:         python-pyOpenSSL
%endif # rhosp

# Handle python2 exception
%if %{pyver} == 2
Requires:         pysendfile
Requires:         python-httplib2
Requires:         python-migrate >= 0.11.0
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-retrying
Requires:         python-sqlparse
Requires:         pyxattr
%else
Requires:         python%{pyver}-pysendfile
Requires:         python%{pyver}-httplib2
Requires:         python%{pyver}-migrate >= 0.11.0
Requires:         python%{pyver}-paste
Requires:         python%{pyver}-paste-deploy
Requires:         python%{pyver}-retrying
Requires:         python%{pyver}-sqlparse
Requires:         python%{pyver}-pyxattr
%endif


#test deps: python-mox python-nose python-requests
#test and optional store:
#ceph - glance.store.rdb
#python-boto - glance.store.s3
Requires:         python%{pyver}-boto

%description -n   python%{pyver}-glance
%{common_desc}

This package contains the glance Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Image Service

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-sphinxcontrib-apidoc
BuildRequires:    graphviz
# Required to build module documents
BuildRequires:    python%{pyver}-boto
BuildRequires:    python%{pyver}-cryptography >= 2.1
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-keystonemiddleware
BuildRequires:    python%{pyver}-oslo-concurrency >= 3.26.0
BuildRequires:    python%{pyver}-oslo-context >= 2.19.2
BuildRequires:    python%{pyver}-oslo-db >= 4.27.0
BuildRequires:    python%{pyver}-sqlalchemy >= 1.0.10
BuildRequires:    python%{pyver}-stevedore
BuildRequires:    python%{pyver}-webob >= 1.8.1
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-psutil
BuildRequires:    python%{pyver}-testresources
# Required to compile translation files
BuildRequires:    python%{pyver}-babel

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    pyxattr
%else
BuildRequires:    python%{pyver}-pyxattr
%endif



%description      doc
%{common_desc}

This package contains documentation files for glance.
%endif

%package -n python%{pyver}-%{service}-tests
Summary:        Glance tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains the Glance test files.


%prep
%autosetup -n glance-%{upstream_version} -S git

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/db/sqlalchemy/migrate_repo/manage.py glance/cmd/status.py
# Until cleared upstream: https://github.com/openstack/glance/blob/master/setup.cfg#L30
sed -i '/rootwrap.conf/d' setup.cfg

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
PYTHONPATH=. oslo-config-generator-%{pyver} --config-dir=etc/oslo-config-generator/
# Build
%{pyver_build}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/%{service}/locale

%install
%{pyver_install}

%if 0%{?with_doc}
export PYTHONPATH=.
# FIXME(ykarel) remove warning is error flag until we have Sphinx >= 1.8.2
sphinx-build-%{pyver} -b html doc/source doc/build/html
%endif

# Fix hidden-file-or-dir warnings
%if 0%{?with_doc}
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif
rm -f %{buildroot}/usr/share/doc/glance/README.rst

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/glance
install -d -m 755 %{buildroot}%{_sharedstatedir}/glance/images
install -d -m 755 %{buildroot}%{_sysconfdir}/glance/metadefs

# Config file
install -p -D -m 640 etc/glance-api.conf %{buildroot}%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_datadir}/glance/glance-api-dist.conf
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_datadir}/glance/glance-api-dist-paste.ini
##
install -p -D -m 640 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datadir}/glance/glance-cache-dist.conf
##
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 %{SOURCE24} %{buildroot}%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_datadir}/glance/glance-registry-dist-paste.ini
##
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf
##
install -p -D -m 644 %{SOURCE26} %{buildroot}%{_sysconfdir}/glance/glance-swift.conf
##
install -p -D -m 644 etc/glance-image-import.conf.sample %{buildroot}%{_sysconfdir}/glance/glance-image-import.conf

install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json
install -p -D -m 640 %{SOURCE31} %{buildroot}%{_sysconfdir}/glance/rootwrap.conf
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Move metadefs
install -p -D -m  640 etc/metadefs/*.json %{buildroot}%{_sysconfdir}/glance/metadefs/

# systemd services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-glance-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-glance-registry.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-glance-scrubber.service

# Logrotate config
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-glance

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Install sudoers
install -p -D -m 440 %{SOURCE30} %{buildroot}%{_sysconfdir}/sudoers.d/glance

# Symlinks to rootwrap config files
mkdir -p %{buildroot}%{_sysconfdir}/glance/rootwrap.d
for filter in %{_datarootdir}/os-brick/rootwrap/*.filters; do
  ln -s $filter %{buildroot}%{_sysconfdir}/glance/rootwrap.d
done
for filter in %{_datarootdir}/glance_store/*.filters; do
  test -f $filter && ln -s $filter %{buildroot}%{_sysconfdir}/glance/rootwrap.d
done

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Cleanup
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}

%pre
getent group glance >/dev/null || groupadd -r glance -g 161
getent passwd glance >/dev/null || \
useradd -u 161 -r -g glance -d %{_sharedstatedir}/glance -s /sbin/nologin \
-c "OpenStack Glance Daemons" glance
exit 0

%post
# Initial installation
%systemd_post openstack-glance-api.service
%systemd_post openstack-glance-registry.service
%systemd_post openstack-glance-scrubber.service


%preun
%systemd_preun openstack-glance-api.service
%systemd_preun openstack-glance-registry.service
%systemd_preun openstack-glance-scrubber.service

%postun
%systemd_postun_with_restart openstack-glance-api.service
%systemd_postun_with_restart openstack-glance-registry.service
%systemd_postun_with_restart openstack-glance-scrubber.service

%files
%doc README.rst
%{_bindir}/glance-api
%{_bindir}/glance-wsgi-api
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator
%{_bindir}/glance-status

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-registry-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf
%{_datadir}/glance/glance-api-dist-paste.ini
%{_datadir}/glance/glance-registry-dist-paste.ini

%{_unitdir}/openstack-glance-api.service
%{_unitdir}/openstack-glance-registry.service
%{_unitdir}/openstack-glance-scrubber.service

%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-swift.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-image-import.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/rootwrap.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/metadefs/*.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%{_sysconfdir}/glance/rootwrap.d/
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0750, glance, glance) %{_localstatedir}/log/glance
%config(noreplace) %{_sysconfdir}/sudoers.d/glance

%files -n python%{pyver}-glance -f %{service}.lang
%doc README.rst
%{pyver_sitelib}/glance
%{pyver_sitelib}/glance-*.egg-info
%exclude %{pyver_sitelib}/glance/tests

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
