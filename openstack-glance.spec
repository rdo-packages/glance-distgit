%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

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
Source004:         openstack-glance-scrubber.service
Source010:         openstack-glance.logrotate

Source021:         glance-api-dist.conf
Source022:         glance-cache-dist.conf
Source025:         glance-scrubber-dist.conf
Source026:         glance-swift.conf

Source030:         glance-sudoers
Source031:         glance-rootwrap.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    intltool
# Required for config generation
BuildRequires:    openstack-macros
BuildRequires:    python3-alembic
BuildRequires:    python3-cursive
BuildRequires:    python3-defusedxml
BuildRequires:    python3-eventlet
BuildRequires:    python3-futurist
BuildRequires:    python3-glance-store >= 1.0.0
BuildRequires:    python3-oslo-config >= 2:8.1.0
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-middleware >= 3.31.0
BuildRequires:    python3-oslo-policy >= 1.30.0
BuildRequires:    python3-oslo-utils >= 3.33.0
BuildRequires:    python3-oslo-upgradecheck >= 0.1.0
BuildRequires:    python3-osprofiler
BuildRequires:    python3-requests
BuildRequires:    python3-routes
BuildRequires:    python3-oslo-messaging >= 5.29.0
BuildRequires:    python3-taskflow >= 2.16.0
BuildRequires:    python3-wsme >= 0.8.0
BuildRequires:    python3-castellan >= 0.17.0
# Required for tests
BuildRequires:    python3-stestr
BuildRequires:    python3-oslo-reports
BuildRequires:    python3-ddt
BuildRequires:    python3-cryptography >= 2.1
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-mock
BuildRequires:    python3-openstacksdk >= 0.56.0
BuildRequires:    python3-oslo-concurrency >= 4.5.1
BuildRequires:    python3-oslo-context >= 2.19.2
BuildRequires:    python3-oslo-db >= 4.27.0
BuildRequires:    python3-oslo-limit >= 1.6.0
BuildRequires:    python3-sqlalchemy >= 1.4.18
BuildRequires:    python3-stevedore
BuildRequires:    python3-webob >= 1.8.1
BuildRequires:    python3-oslotest
BuildRequires:    python3-psutil
BuildRequires:    python3-testresources
BuildRequires:    python3-retrying
BuildRequires:    python3-boto3
BuildRequires:    python3-swiftclient

BuildRequires:    python3-httplib2
BuildRequires:    python3-paste-deploy
BuildRequires:    qemu-img


Requires(pre):    shadow-utils
Requires:         python3-glance = %{epoch}:%{version}-%{release}
# Install glanceclient as a dependency for convenience
Requires:         python3-glanceclient >= 1:2.8.0
Requires:         qemu-img

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
BuildRequires: systemd

%description
%{common_desc}

This package contains the API server.

%package -n       python3-glance
Summary:          Glance Python libraries
%{?python_provide:%python_provide python3-glance}

Requires:         python3-cursive >= 0.2.1
Requires:         python3-cryptography >= 2.6.1
Requires:         python3-debtcollector >= 1.19.0
Requires:         python3-defusedxml >= 0.6.0
Requires:         python3-eventlet >= 0.25.1
Requires:         python3-futurist >= 1.2.0
Requires:         python3-glance-store >= 2.3.0
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-jsonschema >= 3.2.0
Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-keystoneclient >= 3.8.0
Requires:         python3-keystonemiddleware >= 5.1.0
Requires:         python3-oslo-concurrency >= 4.5.1
Requires:         python3-oslo-config >= 2:8.1.0
Requires:         python3-oslo-context >= 2.22.0
Requires:         python3-oslo-db >= 5.0.0
Requires:         python3-oslo-i18n >= 5.0.0
Requires:         python3-oslo-limit >= 1.6.0
Requires:         python3-oslo-log >= 4.5.0
Requires:         python3-oslo-messaging >= 5.29.0
Requires:         python3-oslo-middleware >= 3.31.0
Requires:         python3-oslo-policy >= 3.11.0
Requires:         python3-oslo-reports >= 1.18.0
Requires:         python3-oslo-utils >= 4.7.0
Requires:         python3-oslo-vmware >= 0.11.1
Requires:         python3-oslo-upgradecheck >= 1.3.0
Requires:         python3-osprofiler >= 1.4.0
Requires:         python3-pbr >= 3.1.1
Requires:         python3-prettytable >= 0.7.1
Requires:         python3-routes >= 2.3.1
Requires:         python3-sqlalchemy >= 1.3.14
Requires:         python3-stevedore >= 1.20.0
Requires:         python3-taskflow >= 4.0.0
Requires:         python3-webob >= 1.8.1
Requires:         python3-wsme >= 0.8.0
Requires:         python3-os-brick >= 1.8.0
Requires:         python3-alembic >= 0.9.6
Requires:         python3-os-win >= 4.0.1
Requires:         python3-castellan >= 0.17.0

%if 0%{?rhosp} == 0 || 0%{?rhel} > 7
Requires:         python3-pyOpenSSL >= 17.1.0
%else
Requires:         python-pyOpenSSL
%endif # rhosp

Requires:         python3-pysendfile
Requires:         python3-httplib2 >= 0.9.1
Requires:         python3-paste >= 2.0.2
Requires:         python3-paste-deploy >= 1.5.0
Requires:         python3-retrying >= 1.2.3
Requires:         python3-sqlparse >= 0.2.2
Requires:         python3-pyxattr


#test deps: python-mox python-nose python-requests
#test and optional store:
#ceph - glance.store.rdb

%description -n   python3-glance
%{common_desc}

This package contains the glance Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Image Service

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-sphinxcontrib-apidoc
BuildRequires:    graphviz
BuildRequires:    python3-boto
# Required to compile translation files
BuildRequires:    python3-babel

BuildRequires:    python3-pyxattr



%description      doc
%{common_desc}

This package contains documentation files for glance.
%endif

%package -n python3-%{service}-tests
Summary:        Glance tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python3-%{service}-tests
%{common_desc}

This package contains the Glance test files.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n glance-%{upstream_version} -S git

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/cmd/status.py
# Until cleared upstream: https://github.com/openstack/glance/blob/master/setup.cfg#L30
sed -i '/rootwrap.conf/d' setup.cfg

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
PYTHONPATH=. oslo-config-generator --config-dir=etc/oslo-config-generator/
# Build
%{py3_build}

# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale --domain glance

%install
%{py3_install}

%if 0%{?with_doc}
export PYTHONPATH=.
# FIXME(ykarel) remove warning is error flag until we have Sphinx >= 1.8.2
sphinx-build -b html doc/source doc/build/html
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
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-api-paste.ini
##
install -p -D -m 640 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datadir}/glance/glance-cache-dist.conf
##
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf
##
install -p -D -m 644 %{SOURCE26} %{buildroot}%{_sysconfdir}/glance/glance-swift.conf
##
install -p -D -m 644 etc/glance-image-import.conf.sample %{buildroot}%{_sysconfdir}/glance/glance-image-import.conf

install -p -D -m 640 %{SOURCE31} %{buildroot}%{_sysconfdir}/glance/rootwrap.conf
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Move metadefs
install -p -D -m  640 etc/metadefs/*.json %{buildroot}%{_sysconfdir}/glance/metadefs/

# systemd services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-glance-api.service
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
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Cleanup
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}

%check
stestr run

%pre
getent group glance >/dev/null || groupadd -r glance -g 161
getent passwd glance >/dev/null || \
useradd -u 161 -r -g glance -d %{_sharedstatedir}/glance -s /sbin/nologin \
-c "OpenStack Glance Daemons" glance
exit 0

%post
# Initial installation
%systemd_post openstack-glance-api.service
%systemd_post openstack-glance-scrubber.service


%preun
%systemd_preun openstack-glance-api.service
%systemd_preun openstack-glance-scrubber.service

%postun
%systemd_postun_with_restart openstack-glance-api.service
%systemd_postun_with_restart openstack-glance-scrubber.service

%files
%doc README.rst
%{_bindir}/glance-api
%{_bindir}/glance-wsgi-api
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator
%{_bindir}/glance-status

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf

%{_unitdir}/openstack-glance-api.service
%{_unitdir}/openstack-glance-scrubber.service

%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-swift.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-image-import.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/rootwrap.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/metadefs/*.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%{_sysconfdir}/glance/rootwrap.d/
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0750, glance, glance) %{_localstatedir}/log/glance
%config(noreplace) %{_sysconfdir}/sudoers.d/glance

%files -n python3-glance -f %{service}.lang
%doc README.rst
%{python3_sitelib}/glance
%{python3_sitelib}/glance-*.egg-info
%exclude %{python3_sitelib}/glance/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
