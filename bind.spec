Summary: A DNS (Domain Name System) server.
Name: bind
Version: 8.2.2_P5
Release: 26
Copyright: distributable
Group: System Environment/Daemons
Source0: ftp://ftp.isc.org/isc/bind/src/%{version}/bind-%{version}-src.tar.gz
Source1: ftp://ftp.isc.org/isc/bind/src/%{version}/bind-%{version}-doc.tar.gz
Source2: ftp://ftp.isc.org/isc/bind/src/%{version}/bind-%{version}-contrib.tar.gz
Source3: named.init
Source4: named.logrotate
Url: http://www.isc.org/bind.html
Patch0: bind-8.2.2-rh.patch
Patch1: bind-8.1.2-nonlist.patch
Patch2: bind-8.1.2-fds.patch
Patch3: bind-8.2-glibc21.patch
Patch4: bind-8.2-host.patch
Patch5: bind-8.8.2p5-hostmx.patch
Patch6: bind-8.8.2p5-ttl.patch
Patch7: bind-8.2.2_P5-restart.patch
Buildroot: %{_tmppath}/%{name}-root
Prereq: /sbin/chkconfig, sh-utils, /bin/cat, /bin/chmod, /usr/sbin/useradd, perl

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named), 
which resolves host names to IP addresses, and a resolver library 
(routines for applications to use when interfacing with DNS).  A DNS 
server allows clients to name resources or objects and share the 
information with other network machines.  The named DNS server can be 
used on workstations as a caching name server, but is generally only 
needed on one machine for an entire network.  Note that the 
configuration files for making BIND act as a simple caching nameserver 
are included in the caching-nameserver package.  

Install the bind package if you need a DNS server for your network.  If
you want bind to act a caching name server, you will also need to install
the caching-nameserver package.

%package utils
Summary: Utilities for querying DNS name servers.
Group: Applications/System

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name Service) name servers to find out information about Internet hosts.
These tools will provide you with the IP addresses for given host names,
as well as other information about registered domains and network 
addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%package devel
Summary: Include files and libraries needed for bind DNS development.
Group: Development/Libraries
Requires: bind

%description devel
The bind-devel package contains all the include files and the 
library required for DNS (Domain Name Service) development for 
BIND versions 8.x.x.

You should install bind-devel if you want to develop bind DNS
applications. If you install bind-devel, you'll also need to install
bind.

%prep
%setup -q -c -a 1 -a 2
%patch0 -p0 -b .rh
%patch1 -p0 -b .nonlist
%patch2 -p1 -b .fds
%patch3 -p1 -b .glibc21
%patch4 -p1 -b .host
%patch5 -p1 -b .mx
%patch6 -p1 -b .ttl
%patch7 -p1 -b .restart

rm -f compat/include/sys/cdefs.h

%build

# XXX hack around egcs -m486 bug (#3413, #3485)
%ifarch i386
RPM_OPT_FLAGS="`echo $RPM_OPT_FLAGS | sed -e 's|-m486||'`"
%endif

unset RPM_OPT_FLAGS

# Work around a bind bug: SYSTYPE is always set to bsdos
find src -name Makefile | xargs -n 1 perl -pi -e "s/^SYSTYPE=.*/SYSTYPE=linux/g"
find src -name Makefile | xargs -n 1 perl -pi -e "s/^SYSTYPE =.*/SYSTYPE=linux/g"
find src -name Makefile | xargs -n 1 perl -pi -e "s/^CDEBUG=.*/CDEBUG=$RPM_OPT_FLAGS/g"
find src -name Makefile | xargs -n 1 perl -pi -e "s/^CDEBUG =.*/CDEBUG=$RPM_OPT_FLAGS/g"

make -C src
make clean all -C src SUBDIRS=../doc/man

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/etc/{rc.d/init.d,logrotate.d}
mkdir -p ${RPM_BUILD_ROOT}/usr/{bin,lib,sbin}
mkdir -p ${RPM_BUILD_ROOT}/var/named
MANBASE=`echo %{_mandir} | sed -e "s,/man$,,"`
mkdir -p ${RPM_BUILD_ROOT}/usr/man/{man1,man3,man5,man7,man8}
mkdir -p ${RPM_BUILD_ROOT}${MANBASE}

make DESTDIR=$RPM_BUILD_ROOT install -C src
make DESTDIR=$RPM_BUILD_ROOT INSTALL=install install -C src SUBDIRS=../doc/man
if test "$MANBASE" != "/usr"; then
	rm -rf $RPM_BUILD_ROOT%{_mandir}
	mv ${RPM_BUILD_ROOT}/usr/man $RPM_BUILD_ROOT$MANBASE
fi
install -c -m 755 src/bin/named-bootconf/Grot/named-bootconf.pl $RPM_BUILD_ROOT/usr/sbin/named-bootconf
install -c -m 755 %SOURCE3 $RPM_BUILD_ROOT/etc/rc.d/init.d/named
install -c -m 644 %SOURCE4 $RPM_BUILD_ROOT/etc/logrotate.d/named
ln -s resolver.5 $RPM_BUILD_ROOT%{_mandir}/man5/resolv.conf.5

%pre
/usr/sbin/useradd -c "Named" -u 25 \
	-s /bin/false -r -d /var/named named 2>/dev/null || :

%post
/sbin/chkconfig --add named
if [ -f /etc/named.boot -a ! -f /etc/named.conf ]; then
  if [ -x /usr/sbin/named-bootconf ]; then
    cat /etc/named.boot | /usr/sbin/named-bootconf > /etc/named.conf
    chmod 644 /etc/named.conf
  fi
fi

%preun
if [ $1 = 0 ]; then
   /usr/sbin/userdel named 2>/dev/null || :
   /usr/sbin/groupdel named 2>/dev/null || :
   /sbin/chkconfig --del named
   [ -f /var/lock/subsys/named ] && /sbin/service named stop >/dev/null 2>&1 || :
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
   /sbin/service named condrestart >/dev/null 2>&1 || :
fi

%triggerpostun -- bind < 8.2.2_P5-15
/sbin/chkconfig --add named

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc src/README src/INSTALL src/Version src/CHANGES 
%doc src/TODO
%doc doc/bog doc/html doc/misc doc/notes doc/rfc doc/tmac
%config /etc/logrotate.d/named
%config /etc/rc.d/init.d/named

/usr/sbin/dnskeygen
/usr/sbin/irpd
/usr/sbin/named
/usr/sbin/named-bootconf
/usr/sbin/named-xfer
/usr/sbin/ndc

%{_mandir}/man1/dnskeygen.1*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man7/hostname.7*
%{_mandir}/man8/named.8*
%{_mandir}/man8/ndc.8*
%{_mandir}/man8/named-bootconf.8*
%{_mandir}/man8/named-xfer.8*

%attr(-,named,named) %dir /var/named
     
%files utils
%defattr(-,root,root)
/usr/bin/addr
/usr/bin/dig
/usr/bin/dnsquery
/usr/bin/host
/usr/bin/nslookup
/usr/bin/nsupdate
/usr/lib/nslookup.help
%{_mandir}/man1/dig.1*
%{_mandir}/man1/dnsquery.1*
%{_mandir}/man1/host.1*
%{_mandir}/man5/irs.conf.5*
%{_mandir}/man5/resolver.5*
%{_mandir}/man5/resolv.conf.5*
%{_mandir}/man8/nslookup.8*
%{_mandir}/man8/nsupdate.8*

%files devel
%defattr(-,root,root)
/usr/lib/bind
%{_mandir}/man3/hesiod.3*
%{_mandir}/man3/inet_cidr.3*
%{_mandir}/man3/tsig.3*

%changelog
* Mon Oct 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Remove mkservdb - there's no such thing on Linux (Bug #19195)
  (We've always shipped this; glad it went unnoticed for so long. :) )

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- change the init script to take condrestart, not cond-restart
- add sh-utils, /bin/cat, perl, /bin/chmod, /usr/sbin/useradd as prereqs for
  the %pre and %post scripts

* Sun Jul 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't prereq /etc/init.d

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul  9 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add "exit 0" for uninstall case

* Fri Jul  7 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add prereq init.d and cleanup install section

* Fri Jun 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the init script

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- make libbind.a and nslookup.help readable again by setting INSTALL_LIB to ""

* Mon Jun 26 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix up the initscript (Bug #13033)
- Fix build with current glibc (Bug #12755)
- /etc/rc.d/init.d -> /etc/init.d
- use %%{_mandir} rather than /usr/share/man

* Mon Jun 19 2000 Bill Nottingham <notting@redhat.com>
- fix conflict with man-pages
- remove compatibilty chkconfig links
- initscript munging

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify logrotate setup to use PID file
- temporarily disable optimization by unsetting $RPM_OPT_FLAGS at build-time
- actually bump the release this time

* Sun Jun  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance

* Mon Apr 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- clean up restart patch

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- provide /var/named (fix for bugs #9847, #10205)
- preserve args when restarted via ndc(8) (bug #10227)
- make resolv.conf(5) a link to resolver(5) (bug #10245)
- fix SYSTYPE bug in all makefiles
- move creation of named user from %%post into %%pre

* Mon Feb 28 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix TTL (patch from ISC, Bug #9820)

* Wed Feb 16 2000 Bernhard Rosenkränzer <bero@redhat.com>
- fix typo in spec (it's %post, without a leading blank) introduced in -6
- change SYSTYPE to linux

* Sat Feb 11 2000 Bill Nottingham <notting@redhat.com>
- pick a standard < 100 uid/gid for named

* Thu Feb 04 2000 Elliot Lee <sopwith@redhat.com>
- Pass named a '-u named' parameter by default, and add/remove user.

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix host mx bug (Bug #9021)

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
- man pages are compressed

* Wed Jan 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- It's /usr/bin/killall, not /usr/sbin/killall (Bug #8063)

* Mon Jan 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up location of named-bootconf.pl and make it executable
  (Bug #8028)
- bind-devel requires bind

* Mon Nov 15 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to 8.2.2-P5

* Wed Nov 10 1999 Bill Nottingham <notting@redhat.com>
- update to 8.2.2-P3

* Tue Oct 12 1999 Cristian Gafton <gafton@redhat.com>
- add patch to stop a cache only server from complaining about lame servers
  on every request.

* Fri Sep 24 1999 Preston Brown <pbrown@redhat.com>
- use real stop and start in named.init for restart, not ndc restart, it has
  problems when named has changed during a package update... (# 4890)

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %preun, not %postun

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Mon Jul 26 1999 Bill Nottingham <notting@redhat.com>
- fix installed chkconfig links to match init file

* Sat Jul  3 1999 Jeff Johnson <jbj@redhat.com>
- conflict with new (in man-1.24) man pages (#3876,#3877).

* Tue Jun 29 1999 Bill Nottingham <notting@redhat.com>
- fix named.logrotate (wrong %SOURCE)

* Fri Jun 25 1999 Jeff Johnson <jbj@redhat.com>
- update to 8.2.1.
- add named.logrotate (#3571).
- hack around egcs-1.1.2 -m486 bug (#3413, #3485).
- vet file list.

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- don't run by default

* Sun May 30 1999 Jeff Johnson <jbj@redhat.com>
- nslookup fixes (#2463).
- missing files (#3152).

* Sat May  1 1999 Stepan Kasal <kasal@math.cas.cz>
- nslookup patched:
  to count numRecords properly
  to fix subsequent calls to ls -d
  to parse "view" and "finger" commands properly
  the view hack updated for bind-8 (using sed)

* Wed Mar 31 1999 Bill Nottingham <notting@redhat.com>
- add ISC patch
- add quick hack to make host not crash
- add more docs

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add probing information in the init file to keep linuxconf happy
- dont strip libbind

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Mar 17 1999 Preston Brown <pbrown@redhat.com>
- removed 'done' output at named shutdown.

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- version 8.2

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- patch to use the __FDS_BITS macro
- build for glibc 2.1

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- change named.restart to /usr/sbin/ndc restart

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- install man pages correctly.
- change K10named to K45named.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- don't start if /etc/named.conf doesn't exist.

* Sat Aug  8 1998 Jeff Johnson <jbj@redhat.com>
- autmagically create /etc/named.conf from /etc/named.boot in %post
- remove echo in %post

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- merge in 5.1 mods

* Sun Apr 12 1998 Manuel J. Galan <manolow@step.es>
- Several essential modifications to build and install correctly.
- Modified 'ndc' to avoid deprecated use of '-'

* Mon Dec 22 1997 Scott Lampert <fortunato@heavymetal.org>
- Used buildroot
- patched bin/named/ns_udp.c to use <libelf/nlist.h> for include
  on Redhat 5.0 instead of <nlist.h>

