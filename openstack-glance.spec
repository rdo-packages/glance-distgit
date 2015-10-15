%global release_name liberty
%global service glance

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-glance
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          11.0.0
Release:          1%{?dist}
Summary:          OpenStack Image Service

Group:            Applications/System
License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          http://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Patch0001: 0001-notify-calling-process-we-are-ready-to-serve.patch

Source1:          openstack-glance-api.service
Source2:          openstack-glance-registry.service
Source3:          openstack-glance-scrubber.service
Source4:          openstack-glance.logrotate

Source5:          glance-api-dist.conf
Source6:          glance-registry-dist.conf
Source7:          glance-cache-dist.conf
Source8:          glance-scrubber-dist.conf

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
Group:            Applications/System

Requires:         MySQL-python
Requires:         pysendfile
Requires:         python-anyjson
Requires:         python2-castellan
Requires:         python-crypto
Requires:         python-cryptography >= 1.0
Requires:         python-elasticsearch
Requires:         python-eventlet >= 0.17.4
Requires:         python-glance-store >= 0.9.1
Requires:         python-httplib2
Requires:         python-iso8601
Requires:         python-jsonschema
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-keystonemiddleware >= 2.0.0
Requires:         python-migrate >= 0.9.6
Requires:         python-netaddr
Requires:         python-oslo-concurrency >= 2.3.0
Requires:         python-oslo-config >= 2:2.3.0
Requires:         python-oslo-context >= 0.2.0
Requires:         python-oslo-db >= 2.4.1
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-log >= 1.8.0
Requires:         python-oslo-messaging >= 2.5.0
Requires:         python-oslo-middleware >= 2.8.0
Requires:         python-oslo-policy >= 0.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-service >= 0.7.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-oslo-vmware >= 0.11.1
Requires:         python-osprofiler
Requires:         python-paste-deploy
Requires:         python-pbr
Requires:         python-posix_ipc
Requires:         python-retrying
Requires:         python-routes
Requires:         python-semantic-version
Requires:         python-six >= 1.9.0
Requires:         python-sqlalchemy >= 0.9.9
Requires:         python-stevedore >= 1.5.0
Requires:         python-swiftclient >= 2.2.0
Requires:         python-taskflow >= 1.16.0
Requires:         python-webob
Requires:         python-wsme >= 0.7
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
Group:            Documentation

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    systemd-units
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-eventlet
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-stevedore
BuildRequires:    python-webob

%description      doc
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains documentation files for glance.

%prep
%setup -q -n glance-%{upstream_version}

%patch0001 -p1

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/db/sqlalchemy/migrate_repo/manage.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# Programmatically update defaults in example config
api_dist=%{SOURCE5}
registry_dist=%{SOURCE6}
cache_dist=%{SOURCE7}
scrubber_dist=%{SOURCE8}
for svc in api registry cache scrubber; do
  #  First we ensure all values are commented in appropriate format.
  #  Since icehouse, there was an uncommented keystone_authtoken section
  #  at the end of the file which mimics but also conflicted with our
  #  distro editing that had been done for many releases.
  sed -i '/^[^#[]/{s/^/#/; s/ //g}; /^#[^ ]/s/ = /=/' etc/glance-$svc.conf

  #  TODO: Make this more robust
  #  Note it only edits the first occurance, so assumes a section ordering in sample
  #  and also doesn't support multi-valued variables like dhcpbridge_flagfile.
  eval dist_conf=\$${svc}_dist
  while read name eq value; do
    test "$name" && test "$value" || continue
    sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/glance-$svc.conf
  done < $dist_conf
done

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/glance/tests

# Drop old glance CLI it has been deprecated
# and replaced glanceclient
rm -f %{buildroot}%{_bindir}/glance

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
sphinx-build -b man source build/man

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
rm -f %{buildroot}%{_sysconfdir}/glance*.conf
rm -f %{buildroot}%{_sysconfdir}/glance*.ini
rm -f %{buildroot}%{_sysconfdir}/logging.cnf.sample
rm -f %{buildroot}%{_sysconfdir}/policy.json
rm -f %{buildroot}%{_sysconfdir}/schema-image.json
rm -f %{buildroot}/usr/share/doc/glance/README.rst

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/glance
install -d -m 755 %{buildroot}%{_sharedstatedir}/glance/images
install -d -m 755 %{buildroot}%{_sysconfdir}/glance/metadefs

# Config file
install -p -D -m 640 etc/glance-api.conf %{buildroot}%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_datadir}/glance/glance-api-dist.conf
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_datadir}/glance/glance-api-dist-paste.ini
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_datadir}/glance/glance-registry-dist-paste.ini
install -p -D -m 640 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_datadir}/glance/glance-cache-dist.conf
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf

install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Move metadefs
install -p -D -m  640 etc/metadefs/*.json %{buildroot}%{_sysconfdir}/glance/metadefs/

# systemd services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-glance-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-glance-registry.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-glance-scrubber.service

# Logrotate config
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-glance

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Programmatically update defaults in sample config
# which is installed at /etc/$project/$program.conf
# TODO: Make this more robust
# Note it only edits the first occurance, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
for svc in api registry cache scrubber; do
  cfg=%{buildroot}%{_sysconfdir}/glance/glance-$svc.conf
  test -e $cfg || continue
  while read name eq value; do
    test "$name" && test "$value" || continue
    # Note some values in upstream glance config may not be commented
    # and if not, they might not match the default value in code.
    # So we comment out both froms to have dist config take precedence.
    sed -i "0,/^#* *$name *=/{s!^#* *$name *=.*!#$name=$value!}" $cfg
  done < %{buildroot}%{_datadir}/glance/glance-$svc-dist.conf
done

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
%{_bindir}/glance-artifacts
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-registry-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf
%{_datadir}/glance/glance-api-dist-paste.ini
%{_datadir}/glance/glance-registry-dist-paste.ini

%{_unitdir}/openstack-glance-api.service
%{_unitdir}/openstack-glance-registry.service
%{_unitdir}/openstack-glance-scrubber.service

%{_mandir}/man1/glance*.1.gz
%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/metadefs/*.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0750, glance, glance) %{_localstatedir}/log/glance

%files -n python-glance
%doc README.rst
%{python2_sitelib}/glance
%{python2_sitelib}/glance-*.egg-info

%files doc
%doc doc/build/html

%changelog
* Fri Oct 16 2015 Haikel Guemar <hguemar@fedoraproject.org> 1:11.0.0-1
- Update to upstream 11.0.0

* Fri Oct 09 2015 Alan Pevec <alan.pevec@redhat.com> 1:11.0.0-0.3.0rc2
- Update to upstream 11.0.0.0rc2

* Wed Sep 30 2015 Haikel Guemar <hguemar@fedoraproject.org> 11.0.0-0.1rc1
- Update to upstream 11.0.0.0rc1

* Wed Sep 30 2015 Haikel Guemar <hguemar@fedoraproject.org> 11.0.0-0.1
- Update to upstream 11.0.0.0rc1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2015.1.0-5
- logrotate: make it consistent with other services (RHBZ #1212478)

* Mon May 11 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2015.1.0-4
- logrotate: rotate logs when file > 10M (RHBZ #1212478)

* Mon May 04 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-3
- Update dependencies

* Sat May 02 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-2
- Deploy systemd notifications in api, registry and scrubber services.

* Thu Apr 30 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-1
- OpenStack Kilo release
