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
BuildRequires:    pyproject-rpm-macros
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

# optional requirements we include
Requires:         python3-pyxattr
Requires:         python3-pysendfile


%description -n   python3-glance
%{common_desc}

This package contains the glance Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Image Service

Requires:         %{name} = %{epoch}:%{version}-%{release}

# Manual adding because of issue with xattr
BuildRequires:    python3-pyxattr

%description      doc
%{common_desc}

This package contains documentation files for glance.
%endif

%package -n python3-%{service}-tests
Summary:        Glance tests
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
sed -i '/^xattr.*/d' test-requirements.txt
sed -i '/^doc8.*/d' test-requirements.txt
sed -i '/^pysendfile.*/d' test-requirements.txt
sed -i '/^hacking.*/d' test-requirements.txt
sed -i '/^whereto.*/d' doc/requirements.txt
sed -i '/^xattr.*/d' doc/requirements.txt
sed -i '/^os-api-ref.*/d' doc/requirements.txt
sed -i '/.*whereto.*/d' tox.ini

%generate_buildrequires
%if 0%{?with_doc}
%pyproject_buildrequires -t -e %{default_toxenv},docs
%else
%pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
# Generate i18n files
%{__python3} setup.py compile_catalog -d %{service}/locale --domain glance
rm -f %{service}/locale/*/LC_*/%{service}*po

%pyproject_wheel
PYTHONPATH=. oslo-config-generator --config-dir=etc/oslo-config-generator/

%install
%pyproject_install

%pyproject_save_files %{service}

%if 0%{?with_doc}
%tox -e docs
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
mv %{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Cleanup
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}

%check
%tox -e %{default_toxenv}

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

%files -n python3-glance -f %{service}.lang -f %{pyproject_files}
%doc README.rst
%exclude %{python3_sitelib}/glance/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
