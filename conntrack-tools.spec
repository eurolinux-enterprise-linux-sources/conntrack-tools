Name:           conntrack-tools
Version:        1.4.3
Release:        1%{?dist}
Summary:        Manipulate netfilter connection tracking table and run High Availability
Group:          System Environment/Base
License:        GPLv2
URL:            http://netfilter.org
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
Source1:        conntrackd.service
Source2:        conntrackd.conf
BuildRequires:  libnfnetlink-devel >= 1.0.1, libnetfilter_conntrack-devel >= 1.0.4
BuildRequires:  libnetfilter_cttimeout-devel >= 1.0.0, libnetfilter_cthelper-devel >= 1.0.0
BuildRequires:  libmnl-devel >= 1.0.3, libnetfilter_queue-devel >= 1.0.2
BuildRequires:  pkgconfig bison flex
Provides:       conntrack = 1.0-1
Obsoletes:      conntrack < 1.0-1
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description
With conntrack-tools you can setup a High Availability cluster and
synchronize conntrack state between multiple firewalls.

The conntrack-tools package contains two programs:
- conntrack: the command line interface to interact with the connection
             tracking system.
- conntrackd: the connection tracking userspace daemon that can be used to
              deploy highly available GNU/Linux firewalls and collect
              statistics of the firewall use.

conntrack is used to search, list, inspect and maintain the netfilter
connection tracking subsystem of the Linux kernel.
Using conntrack, you can dump a list of all (or a filtered selection  of)
currently tracked connections, delete connections from the state table, 
and even add new ones.
In addition, you can also monitor connection tracking events, e.g. 
show an event message (one line) per newly established connection.

%prep
%setup -q

%build
# do not use --enable-cthelper --enable-cttimeout, it causes disabling of these features
%configure --disable-static
%{__make} %{?_smp_mflags}
chmod 644 doc/sync/primary-backup.sh
rm -f doc/sync/notrack/conntrackd.conf.orig doc/sync/alarm/conntrackd.conf.orig doc/helper/conntrackd.conf.orig

%install
%{__make} install DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/conntrackd/

%files
%doc COPYING AUTHORS TODO doc
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%{_mandir}/man8/*
%dir %{_libdir}/conntrack-tools
%{_libdir}/conntrack-tools/*

%post
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
%systemd_postun conntrackd.service 

%changelog
* Fri Aug 12 2016 Paul Wouters <pwouters@redhat.com> - 1.4.3-1
- Resolves: rhbz#1351701 conntrackd -d throws "ERROR: Helper support is disabled"

* Fri Aug 21 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-9
- Resolves: rhbz#1255578 conntrackd could neither be started nor be stopped

* Tue Aug 18 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-8
- Resolves: rhbz#CVE-2015-6496
- Fold in upstream patches since 1.4.2 release up to git 900d7e8
- Fold in upstream patch set of 2015-08-18 for coverity issues

* Thu May 21 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-7
- Resolves: rhbz#1122611 [BNE] Add conntrack-tools package to RHEL-7
