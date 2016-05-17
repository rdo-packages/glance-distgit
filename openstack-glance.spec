%global release_name liberty
%global service glance

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-glance
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          XXX
Release:          XXX
Summary:          OpenStack Image Service

License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          https://launchpad.net/glance/%{release_name}/%{version}/+download/glance-%{version}.tar.gz

Source001:         openstack-glance-api.service
Source002:         openstack-glance-glare.service
Source003:         openstack-glance-registry.service
Source004:         openstack-glance-scrubber.service
Source010:         openstack-glance.logrotate

Source021:         glance-api-dist.conf
Source022:         glance-cache-dist.conf
Source023:         glance-glare-dist.conf
Source024:         glance-registry-dist.conf
Source025:         glance-scrubber-dist.conf

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    intltool

Requires(pre):    shadow-utils
Requires:         python-glance = %{epoch}:%{version}-%{release}
Requires:         python-glanceclient >= 1:0
Requires:         openstack-utils

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images. The Image Service API server
provides a standard REST interface for querying information about virtual disk
images stored in a variety of back-end stores, including OpenStack Object
Storage. Clients can register new virtual disk images with the Image Service,
query for information on publicly available disk images, and use the Image
Service's client library for streaming virtual disk images.

This package contains the API and registry servers.

%package -n       python-glance
Summary:          Glance Python libraries

Requires:         pysendfile
Requires:         python-anyjson
Requires:         python2-castellan >= 0.3.1
Requires:         python-crypto
Requires:         python-cryptography >= 1.0
Requires:         python-eventlet >= 0.17.4
Requires:         python-futurist >= 0.11.0
Requires:         python-glance-store >= 0.13.0
Requires:         python-httplib2
Requires:         python-jsonschema
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-keystonemiddleware >= 4.0.0
Requires:         python-migrate >= 0.9.6
Requires:         python-netaddr
Requires:         python-oslo-concurrency >= 3.5.0
Requires:         python-oslo-config >= 2:3.7.0
Requires:         python-oslo-context >= 0.2.0
Requires:         python-oslo-db >= 4.1.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 1.14.0
Requires:         python-oslo-messaging >= 4.0.0
Requires:         python-oslo-middleware >= 3.0.0
Requires:         python-oslo-policy >= 0.5.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-service >= 1.0.0
Requires:         python-oslo-utils >= 3.5.0
Requires:         python-oslo-vmware >= 0.11.1
Requires:         python-osprofiler
Requires:         python-paste-deploy
Requires:         python-pbr
Requires:         python-posix_ipc
Requires:         python-retrying
Requires:         python-routes
Requires:         python-semantic-version
Requires:         python-six >= 1.9.0
Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-stevedore >= 1.5.0
Requires:         python-swiftclient >= 2.2.0
Requires:         python-taskflow >= 1.26.0
Requires:         python-webob >= 1.2.3
Requires:         python-wsme >= 0.8
Requires:         pyOpenSSL
Requires:         pyxattr

#test deps: python-mox python-nose python-requests
#test and optional store:
#ceph - glance.store.rdb
#python-boto - glance.store.s3
Requires:         python-boto

%description -n   python-glance
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the glance Python library.

%package doc
Summary:          Documentation for OpenStack Image Service

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    systemd-units
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python2-castellan >= 0.3.1
BuildRequires:    python-crypto
BuildRequires:    python-cryptography >= 1.0
BuildRequires:    python-eventlet
BuildRequires:    python-futurist
BuildRequires:    python-glance-store >= 0.13.0
BuildRequires:    python-httplib2
BuildRequires:    python-keystoneauth1
BuildRequires:    python-keystonemiddleware >= 4.0.0
BuildRequires:    python-oslo-config >= 2:3.7.0
BuildRequires:    python-oslo-concurrency >= 3.5.0
BuildRequires:    python-oslo-context >= 0.2.0
BuildRequires:    python-oslo-db >= 4.1.0
BuildRequires:    python-oslo-log >= 1.14.0
BuildRequires:    python-oslo-messaging >= 4.0.0
BuildRequires:    python-oslo-policy >= 0.5.0
BuildRequires:    python-osprofiler
BuildRequires:    python-paste-deploy
BuildRequires:    python-routes
BuildRequires:    python-semantic-version
BuildRequires:    python-sqlalchemy >= 1.0.10
BuildRequires:    python-stevedore
BuildRequires:    python-taskflow >= 1.26.0
BuildRequires:    python-webob >= 1.2.3
BuildRequires:    python-wsme >= 0.8
# Required to compile translation files
BuildRequires:    python-babel

%description      doc
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains documentation files for glance.

%package -n python-%{service}-tests
Summary:        Glance tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the Glance test files.


%prep
%setup -q -n glance-%{upstream_version}

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/db/sqlalchemy/migrate_repo/manage.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
PYTHONPATH=. oslo-config-generator --config-dir=etc/oslo-config-generator/

# Build
%{__python2} setup.py build

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
#TODO(apevec) debug sphinx build failures in DLRN buildroot
#             not reproducible locally
#%{__python2} setup.py build_sphinx
#%{__python2} setup.py build_sphinx --builder man
#mkdir -p %{buildroot}%{_mandir}/man1
#install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
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
install -p -D -m 640 etc/glance-glare.conf %{buildroot}%{_sysconfdir}/glance/glance-glare.conf
install -p -D -m 644 %{SOURCE23} %{buildroot}%{_datadir}/glance/glance-glare-dist.conf
install -p -D -m 644 etc/glance-glare-paste.ini %{buildroot}%{_datadir}/glance/glance-glare-dist-paste.ini
##
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 %{SOURCE24} %{buildroot}%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_datadir}/glance/glance-registry-dist-paste.ini
##
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf

install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Move metadefs
install -p -D -m  640 etc/metadefs/*.json %{buildroot}%{_sysconfdir}/glance/metadefs/

# systemd services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-glance-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-glance-glare.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-glance-registry.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-glance-scrubber.service

# Logrotate config
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-glance

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

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
%systemd_post openstack-glance-glare.service
%systemd_post openstack-glance-registry.service
%systemd_post openstack-glance-scrubber.service


%preun
%systemd_preun openstack-glance-api.service
%systemd_preun openstack-glance-glare.service
%systemd_preun openstack-glance-registry.service
%systemd_preun openstack-glance-scrubber.service

%postun
%systemd_postun_with_restart openstack-glance-api.service
%systemd_postun_with_restart openstack-glance-glare.service
%systemd_postun_with_restart openstack-glance-registry.service
%systemd_postun_with_restart openstack-glance-scrubber.service

%files
%doc README.rst
%{_bindir}/glance-api
%{_bindir}/glance-control
%{_bindir}/glance-glare
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-glare-dist.conf
%{_datadir}/glance/glance-registry-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf
%{_datadir}/glance/glance-api-dist-paste.ini
%{_datadir}/glance/glance-glare-dist-paste.ini
%{_datadir}/glance/glance-registry-dist-paste.ini

%{_unitdir}/openstack-glance-api.service
%{_unitdir}/openstack-glance-glare.service
%{_unitdir}/openstack-glance-registry.service
%{_unitdir}/openstack-glance-scrubber.service

#%{_mandir}/man1/glance*.1.gz
%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-glare.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/metadefs/*.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0750, glance, glance) %{_localstatedir}/log/glance

%files -n python-glance -f %{service}.lang
%doc README.rst
%{python2_sitelib}/glance
%{python2_sitelib}/glance-*.egg-info
%exclude %{python2_sitelib}/glance/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%files doc
#%doc doc/build/html

%changelog
