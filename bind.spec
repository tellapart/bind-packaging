#%define debug_package %{nil}
%define posix_threads 0
%{?!SDB:    %define SDB         1}
%{?!LIBBIND:%define LIBBIND	1}
%{?!efence: %define efence      0}
%{?!test:   %define test        0}
%{?!WITH_DBUS: %define WITH_DBUS 1} # + dynamic forwarder table management with D-BUS 
# Usage: export RPM='/usr/bin/rpmbuild --define "test 1"'; make $arch;
Summary: The Berkeley Internet Name Domain (BIND) DNS (Domain Name System) server.
Name: bind
License: BSD-like
Version: 9.3.1
Release: 22
Epoch:   24
Url: http://www.isc.org/products/BIND/
Buildroot: %{_tmppath}/%{name}-root
Group: System Environment/Daemons
Source: ftp://ftp.isc.org/isc/bind9/%{version}/bind-%{version}.tar.gz
#Source1: bind-manpages-2.tar.bz2 
# Finally, ISC are distributing man named.conf(5) and nslookup(8) !
Source1: named.sysconfig
Source2: named.init
Source3: named.logrotate
Source4: keygen.c
Source5: rfc1912.txt
Source6: bind-chroot.tar.gz
Source7: bind-9.3.1rc1-sdb_tools-Makefile.in
Source8: dnszone.schema
Source9: libbind-man.tar.gz
Source10: named-dbus.conf
Source11: named.service
Source12: README.sdb_pgsql
# http://www.venaas.no/ldap/bind-sdb/dnszone-schema.txt
Patch: bind-9.2.0rc3-varrun.patch
Patch1: bind-9.2.1-key.patch
Patch2: bind-9.3.1beta2-openssl-suffix.patch
Patch3: bind-posixthreads.patch
Patch4: bind-bsdcompat.patch
Patch5: bind-nonexec.patch
Patch6: bind-9.2.2-nsl.patch
Patch7: bind-9.2.4rc7-pie.patch
Patch8: bind-9.3.0-handle-send-errors.patch
Patch9: bind-9.3.0-missing-dnssec-tools.patch
Patch10: bind-9.3.1rc1-no-libtool-for-PIEs.patch
Patch11: bind-9.3.1rc1-sdbsrc.patch
Patch12: bind-9.3.1rc1-sdb.patch
Patch13: bind-9.3.1rc1-fix_libbind_includedir.patch
Patch14: libbind-9.3.1rc1-fix_h_errno.patch
Patch15: bind-9.3.1.dbus.patch
Patch16: bind-9.3.1-redhat_doc.patch
Patch17: bind-9.3.1-fix_sdb_ldap.patch
Patch18: bind-9.3.1-reject_resolv_conf_errors.patch
Patch19: bind-9.3.1-next_server_on_referral.patch
Patch20: bind-9.3.1-no_servfail_stops.patch
Patch21: bind-9.3.1-fix_sdb_pgsql.patch
Patch22: bind-9.3.1-sdb_dbus.patch
Patch23: bind-9.3.1-dbus_archdep_libdir.patch
Patch24: bind-9.3.1-t_no_default_lookups.patch
Patch25: bind-9.3.1-fix_no_dbus_daemon.patch
Patch26: bind-9.3.1-flush-cache.patch
Patch27: bind-9.3.1-dbus_restart.patch
Requires(pre,preun): shadow-utils
Requires(post,preun): chkconfig
Requires(post): textutils, fileutils, sed, grep
Requires: bind-libs = %{epoch}:%{version}-%{release}, bind-utils = %{epoch}:%{version}-%{release},  glibc  >= 2.2, /bin/usleep
#Requires: kernel >= 2.4
#Requires: glibc  >= 2.3.2-5
%if %{SDB}
%if %{WITH_DBUS}
BuildRequires: openssl-devel gcc dbus-devel glibc-devel >= 2.2.5-26 glibc-kernheaders >= 2.4-7.10 libtool pkgconfig tar openldap-devel postgresql-devel
%else
BuildRequires: openssl-devel gcc glibc-devel >= 2.2.5-26 glibc-kernheaders >= 2.4-7.10 libtool pkgconfig tar openldap-devel postgresql-devel
%endif
%else
%if %{WITH_DBUS}
BuildRequires: openssl-devel gcc dbus-devel glibc-devel >= 2.2.5-26 glibc-kernheaders >= 2.4-7.10 libtool pkgconfig tar
%else
BuildRequires: openssl-devel gcc glibc-devel >= 2.2.5-26 glibc-kernheaders >= 2.4-7.10 libtool pkgconfig tar
%endif
%endif

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named),
which resolves host names to IP addresses; a resolver library
(routines for applications to use when interfacing with DNS); and
tools for verifying that the DNS server is operating properly.

%package libs
Summary: Libraries used by various DNS packages
Group: Applications/System

%description libs
Contains libraries used by both the bind server package as well as the utils packages.

%package utils
Summary: Utilities for querying DNS name servers.
Group: Applications/System
Requires: bind-libs = %{epoch}:%{version}-%{release}

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name System) name servers to find out information about Internet
hosts. These tools will provide you with the IP addresses for given
host names, as well as other information about registered domains and
network addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%package devel
Summary: Include files and libraries needed for bind DNS development.
Group: Development/Libraries
Requires: bind-libs = %{epoch}:%{version}-%{release}

%description devel
The bind-devel package contains all the include files and the library
required for DNS (Domain Name System) development for BIND versions
9.x.x.

%if %{LIBBIND}

%package libbind-devel
Summary: Include files and library needed to use the BIND resolver library.
Group: Development/Libraries
Requires: bind-libs = %{epoch}:%{version}-%{release}

%description libbind-devel
The bind-libbind-devel package contains the libbind BIND resolver library,
compatible with that from ISC BIND 8, and the /usr/include/bind include files
necessary to develop software that uses it.

%endif

%package chroot
Summary: A chrooted tree for the BIND nameserver
Group: System Environment/Daemons
Prefix: /var/named/chroot
Requires: bind = %{epoch}:%{version}-%{release}

%description chroot
This package contains a tree of files which can be used as a
chroot(2) jail for the named(8) program from the BIND package.
Based off code from Jan "Yenya" Kasprzak <kas@fi.muni.cz>

%if %{SDB}

%package sdb
Summary: The Berkeley Internet Name Domain (BIND) DNS (Domain Name System) server with database backends.
Group: System Environment/Daemons
Requires: bind-libs = %{epoch}:%{version}-%{release}, bind-utils = %{epoch}:%{version}-%{release},  glibc  >= 2.2, /bin/usleep

%description sdb
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named),
which resolves host names to IP addresses; a resolver library
(routines for applications to use when interfacing with DNS); and
tools for verifying that the DNS server is operating properly.

BIND SDB (Simplified Database Backend) provides named_sdb, the DNS 
name server compiled to include support for using alternative Zone Databases 
stored in an LDAP server (ldapdb), a postgreSQL database (pgsqldb), or in the 
filesystem (dirdb), in addition  to the standard in-memory RBT (Red Black Tree) 
zone database. 

%endif

%prep
%setup -q -n %{name}-%{version}
%patch -p1 -b .varrun
%patch1 -p1 -b .key
%patch2 -p1 -b .openssl_suffix
#%if %{posix_threads}
#%patch3 -p1 -b .posixthreads
#%endif
# This patch is no longer required and would not work anyway (see BZ 87525).
%patch4 -p1 -b .bsdcompat
%patch5 -p1 -b .nonexec
%patch6 -p1 
%patch7 -p1 -b .pie
#%patch8 -p1 -b .handle_send_errors
# This patch is now in ISC bind-9.3.1x
%patch9 -p1 -b .missing_dnssec_tools
%patch10 -p1 -b .no-libtool-for-PIEs
%if %{SDB}
%patch11 -p1 -b .sdbsrc
# BUILD 'Simplified Database Backend' (SDB) version of named: named_sdb
cp -rfp bin/named bin/named_sdb
# SDB ldap
cp -fp contrib/sdb/ldap/ldapdb.[ch] bin/named_sdb
# SDB postgreSQL
cp -fp contrib/sdb/pgsql/pgsqldb.[ch] bin/named_sdb
# SDB Berkeley DB - needs to be ported to DB4!
#cp -fp contrib/sdb/bdb/bdb.[ch] bin/named_sdb
# SDB dir
cp -fp contrib/sdb/dir/dirdb.[ch] bin/named_sdb
# SDB tools
mkdir -p bin/sdb_tools
cp -fp %{SOURCE7} bin/sdb_tools/Makefile.in
#cp -fp contrib/sdb/bdb/zone2bdb.c bin/sdb_tools
cp -fp contrib/sdb/ldap/{zone2ldap.1,zone2ldap.c} bin/sdb_tools
cp -fp contrib/sdb/pgsql/zonetodb.c bin/sdb_tools
%patch12 -p1 -b .sdb
%endif
%if %{LIBBIND}
%patch13 -p1 -b .fix_libbind_includedir
%patch14 -p1 -b .fix_h_errno
%endif
%if %{WITH_DBUS}
%patch15 -p1 -b .dbus
%else
%patch16 -p1 -b .redhat_doc
%endif
%if %{SDB}
%patch17 -p1 -b .fix_sdb_ldap
%endif
%patch18 -p1 -b .reject_resolv_conf_errors
%patch19 -p1 -b .next_server_on_referral
%patch20 -p1 -b .no_servfail_stops
%patch21 -p1 -b .fix_sdb_pgsql
%if %{WITH_DBUS}
%if %{SDB}
cp -fp bin/named/{dbus_mgr.c,dbus_service.c,log.c,server.c} bin/named_sdb
cp -fp bin/named/include/named/{dbus_mgr.h,dbus_service.h,globals.h,server.h,log.h,types.h} bin/named_sdb/include/named
%patch22 -p1 -b .sdb_dbus
%endif
%patch23 -p1 -b .dbus_archdep_libdir
%endif
%patch24 -p1 -b .-t_no_default_lookups
%patch25 -p1 -b .fix_no_dbus_daemon
%patch26 -p1 -b .flush_cache
%patch27 -p1 -b .dbus_restart
%build
libtoolize --copy --force; aclocal; autoconf
cp -f /usr/share/libtool/config.{guess,sub} .
export CFLAGS="$RPM_OPT_FLAGS"
%if %{WITH_DBUS}
%ifarch s390x x86_64 ppc64
# every 64-bit arch EXCEPT ia64 has dbus architecture dependant
# includes in  /usr/lib64/dbus-1.0/include
export DBUS_ARCHDEP_LIBDIR=lib64
%endif
%endif
if pkg-config openssl ; then
	export CFLAGS="$CFLAGS `pkg-config --cflags openssl`"
	export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I openssl`"
	export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
#export CFLAGS="-g $CFLAGS"
%if %{efence}
export LDFLAGS=-lefence
%endif
%if %{LIBBIND}
%configure --with-libtool --localstatedir=/var \
	--enable-threads \
	--enable-ipv6 \
	--with-pic \
	--with-openssl=/usr \
	--enable-libbind
%else
%configure --with-libtool --localstatedir=/var \
	--enable-threads \
	--enable-ipv6 \
	--with-pic \
	--with-openssl=/usr
%endif
make %{?_smp_mflags}
if [ $? -ne 0 ]; then
   exit $?;
fi;
cp %{SOURCE5} doc/rfc
gzip -9 doc/rfc/*

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/etc/{rc.d/init.d,logrotate.d}
mkdir -p ${RPM_BUILD_ROOT}/usr/{bin,lib,sbin,include}
mkdir -p ${RPM_BUILD_ROOT}/var/named
mkdir -p ${RPM_BUILD_ROOT}/var/named/slaves
mkdir -p ${RPM_BUILD_ROOT}/var/named/data
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/{man1,man5,man8}
mkdir -p ${RPM_BUILD_ROOT}/var/run/named
#chroot
mkdir -p ${RPM_BUILD_ROOT}/%{prefix}
tar --no-same-owner -zxvf %{SOURCE6} --directory ${RPM_BUILD_ROOT}/%{prefix} 
# these are required to prevent them being erased during upgrade of previous
# versions that included them (bug #130121):
touch ${RPM_BUILD_ROOT}/%{prefix}/etc/named.conf
touch ${RPM_BUILD_ROOT}/%{prefix}/etc/rndc.key
touch ${RPM_BUILD_ROOT}/%{prefix}/dev/null
touch ${RPM_BUILD_ROOT}/%{prefix}/dev/random
#end chroot
make DESTDIR=$RPM_BUILD_ROOT install
install -c -m 640 bin/rndc/rndc.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -c -m 755 contrib/named-bootconf/named-bootconf.sh $RPM_BUILD_ROOT/usr/sbin/named-bootconf
install -c -m 755 %SOURCE2 $RPM_BUILD_ROOT/etc/rc.d/init.d/named
install -c -m 644 %SOURCE3 $RPM_BUILD_ROOT/etc/logrotate.d/named
touch $RPM_BUILD_ROOT%{_sysconfdir}/rndc.key
cat << __EOF > $RPM_BUILD_ROOT%{_sysconfdir}/rndc.key
key "rndckey" {
        algorithm       hmac-md5;
        secret "@KEY@";
};
__EOF
%{__cc} $RPM_OPT_FLAGS -o $RPM_BUILD_ROOT/usr/sbin/dns-keygen %{SOURCE4}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/named
#mv $RPM_BUILD_ROOT/usr/share/man/man8/named.conf.* $RPM_BUILD_ROOT/usr/share/man/man5
%if %{SDB}
mkdir -p $RPM_BUILD_ROOT/etc/openldap/schema
install -c -m 644 %{SOURCE8} $RPM_BUILD_ROOT/etc/openldap/schema/dnszone.schema
cp -fp %{SOURCE12} contrib/sdb/pgsql/
%endif
%if %{LIBBIND}
gunzip < %{SOURCE9} | (cd $RPM_BUILD_ROOT/usr/share; tar -xpf -) 
%endif
%if %{WITH_DBUS}
mkdir -p $RPM_BUILD_ROOT/etc/dbus-1/system.d
mkdir -p $RPM_BUILD_ROOT/usr/share/dbus-1/services
cp -fp %{SOURCE10} $RPM_BUILD_ROOT/etc/dbus-1/system.d/named.conf
cp -fp %{SOURCE11} $RPM_BUILD_ROOT/usr/share/dbus-1/services/named.service
%endif
%if %{test}
if [ "`whoami`" = 'root' ]; then
   set -e
   chmod -R a+rwX .
   pushd bin/tests
   pushd system
   ./ifconfig.sh up
   popd
   make test
   e=$?   
   pushd system
   ./ifconfig.sh down	
   popd
   popd
   if [ "$e" -ne 0 ]; then
      echo "ERROR: this build of BIND failed 'make test'. Aborting."
      exit $e;
   fi;
else
   echo 'test==1 : only root can run the tests (they require an ifconfig).';   
fi
:;
%endif
# Files required to run test-suite outside of build tree:
cp -fp config.h $RPM_BUILD_ROOT/%{_includedir}/bind9
cp -fp lib/dns/include/dns/forward.h $RPM_BUILD_ROOT/%{_includedir}/dns
cp -fp lib/isc/unix/include/isc/keyboard.h $RPM_BUILD_ROOT/%{_includedir}/isc
cp -fp lib/isc/include/isc/hash.h $RPM_BUILD_ROOT/%{_includedir}/isc
# exit 0;
# uncomment to prevent stripping / debuginfo
:;

%pre
/usr/sbin/groupadd -g 25 named >/dev/null 2>&1 || :;
/usr/sbin/useradd -c "Named" -u 25 -g named \
	-s /sbin/nologin -r -d /var/named named >/dev/null 2>&1 || :;

%post
if [ "$1" -eq 1 ]; then
	/sbin/chkconfig --add named
	if [ -f /etc/named.boot -a ! -f /etc/named.conf ]; then
	  if [ -x /usr/sbin/named-bootconf ]; then
		cat /etc/named.boot | /usr/sbin/named-bootconf > /etc/named.conf
	    	chmod 644 /etc/named.conf
	  fi
	fi
	if grep -q '@KEY@' /etc/rndc.key; then
	  sed -e "s/@KEY@/`/usr/sbin/dns-keygen`/" /etc/rndc.key >/etc/rndc.key.tmp
	  mv -f /etc/rndc.key.tmp /etc/rndc.key
	fi
	if [ ! -s /etc/named.conf ]; then	
	   echo -e '// Default named.conf generated by install of bind-'%{version}'-'%{release}'\noptions {\n\tdirectory "/var/named";\n\tdump-file "/var/named/data/cache_dump.db";\n\tstatistics-file "/var/named/data/named_stats.txt";\n};\ninclude "/etc/rndc.key";\n' > /etc/named.conf;
	fi;
        [ -d /selinux ] && [ -x /sbin/restorecon ] && /sbin/restorecon /etc/rndc.key /etc/rndc.conf /etc/named.conf >/dev/null 2>&1
	chmod 0640 /etc/rndc.conf /etc/rndc.key
	chown root:named /etc/rndc.conf /etc/rndc.key /etc/named.conf
	/sbin/ldconfig
fi
:;

%preun
if [ "$1" = 0 ]; then
   /etc/rc.d/init.d/named stop >/dev/null 2>&1 || :;
   /usr/sbin/userdel named 2>/dev/null || :;
   /usr/sbin/groupdel named 2>/dev/null || :;
   /sbin/chkconfig --del named || :;
fi
:;

%postun
if [ "$1" -ge 1 ]; then
   /etc/rc.d/init.d/named condrestart >/dev/null 2>&1 || :   	   
fi;
/sbin/ldconfig

%postun utils
# because bind-utils depends on bind, it gets uninstalled first,
# so bind's preun's 'service named stop' will fail (no rndc).
if [ $1 = 0 ]; then
   if [ -f /var/lock/subsys/named ]; then
      /etc/rc.d/init.d/named stop >/dev/null  2>&1 || :;
   fi;
fi;
:;

%triggerpostun -- bind < 8.2.2_P5-15
/sbin/chkconfig --add named
/sbin/ldconfig
:;

%triggerpostun -n bind -- bind <= 24:9.3.1-11
if [ "$1" -gt 0 ]; then
# bind <= 22:9.3.0-2:
# These versions of bind installed named service at order 55 in 
# runlevel startup order, after programs like  nis / ntp / nfs 
# which may need its services if using no nameservers in resolv.conf.
# bind <= 24:9.3.1-11:
# These versions ran bind with order 11 in runlevel 2, after syslog
# at order 12 . BIND should run after syslog and now has order '- 13 87'.
# 
   rl=()
   for l in 0 1 2 3 4 5 6; 
   do
	if chkconfig --level=$l named; then
	   rl=(${rl[@]} 1)
	else
	   rl=(${rl[@]} 0)
	fi
   done
   chkconfig --del named
   chkconfig --add named
   let l=0;
   for s in ${rl[@]};
   do
       if [ "$s" = "1" ]; then
          chkconfig --level=$l named on;
       else
          chkconfig --level=$l named off;
       fi;
       let l='l+1';
   done;
fi
:;

%clean
rm -rf ${RPM_BUILD_ROOT}
# ${RPM_BUILD_DIR}/%{name}-%{version}
:;

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CHANGES COPYRIGHT README
%doc doc/arm doc/misc
%if %{WITH_DBUS}
%doc doc/README.DBUS
%attr(644,root,root) %config /etc/dbus-1/system.d/named.conf
%attr(644,root,root) %config /usr/share/dbus-1/services/named.service
%endif
%config(noreplace) /etc/logrotate.d/named
%attr(754,root,root) %config /etc/rc.d/init.d/named
%config(noreplace) /etc/sysconfig/named
%verify(not size,not md5) %config(noreplace) %attr(0640,root,named) /etc/rndc.conf
%verify(not size,not md5) %config(noreplace) %attr(0640,root,named) /etc/rndc.key

%{_sbindir}/dnssec*
%{_sbindir}/lwresd
%{_sbindir}/named
%{_sbindir}/named-bootconf
%{_sbindir}/named-check*
%{_sbindir}/rndc*
%{_sbindir}/dns-keygen

%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/dnssec*.8*
%{_mandir}/man8/named-checkconf.8*
%{_mandir}/man8/named-checkzone.8*
%{_mandir}/man8/rndc-confgen.8*

%attr(750,root,named) %dir /var/named
%attr(770,named,named) %dir /var/named/slaves
%attr(770,named,named) %dir /var/named/data
%attr(770,named,named) %dir /var/run/named

%files libs
%defattr(-,root,root)
%{_libdir}/*so*
%{_libdir}/*.la

%files utils
%defattr(-,root,root)
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_mandir}/man1/host.1*
%{_mandir}/man8/nsupdate.8*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*

%files devel
%defattr(-,root,root)
%{_libdir}/libbind9.a
%{_libdir}/libdns.a
%{_libdir}/libisc.a
%{_libdir}/libisccc.a
%{_libdir}/libisccfg.a
%{_libdir}/liblwres.a
%{_includedir}/bind9
%{_includedir}/dns
%{_includedir}/dst
%{_includedir}/isc
%{_includedir}/isccc
%{_includedir}/isccfg
%{_includedir}/lwres
%{_mandir}/man3/lwres*
%{_bindir}/isc-config.sh
%doc doc/draft doc/rfc 

%if %{LIBBIND}

%files libbind-devel
%defattr(-,root,root)
%{_libdir}/libbind.*
%{_includedir}/bind
%{_mandir}/man3/libbind-*
%{_mandir}/man7/libbind-*
%{_mandir}/man5/libbind-*

%post libbind-devel -p /sbin/ldconfig

%postun libbind-devel -p /sbin/ldconfig

%endif

%files chroot
%defattr(-,root,root)
%attr(750,root,named) %dir %prefix
%attr(750,root,named) %dir %prefix/dev
%attr(750,root,named) %dir %prefix/etc
%attr(750,root,named) %dir %prefix/var
%attr(770,root,named) %dir  %prefix/var/run
%attr(770,named,named) %dir %prefix/var/tmp
%attr(770,named,named) %dir %prefix/var/run/named
%attr(750,root,named) %dir  %prefix/var/named
%attr(770,named,named) %dir %prefix/var/named/slaves
%attr(770,named,named) %dir %prefix/var/named/data
%ghost %prefix/etc/named.conf
%ghost %prefix/etc/rndc.key
%ghost %prefix/dev/null
%ghost %prefix/dev/random

%if %{SDB}

%files sdb
%defattr(-,root,named)
%{_sbindir}/named_sdb
%config /etc/openldap/schema/dnszone.schema
%{_sbindir}/zone2ldap
%{_sbindir}/ldap2zone
%{_sbindir}/zonetodb
%{_mandir}/man1/zone2ldap.1*
%doc contrib/sdb/ldap/README.ldap contrib/sdb/ldap/INSTALL.ldap contrib/sdb/pgsql/README.sdb_pgsql

%post sdb
if [ "$1" -ge 1 ]; then
   # check that dnszone.schema is installed in OpenLDAP's slapd.conf
   if [ -x /usr/sbin/named_sdb ] && [ -f /etc/openldap/slapd.conf ]; then
   # include the LDAP dnszone.schema in slapd.conf:
      if ! /bin/egrep -q '^include.*\dnszone.schema' /etc/openldap/slapd.conf; then
         tf=`/bin/mktemp /tmp/XXXXXX`
         let n=`/bin/grep -n '^include.*\.schema' /etc/openldap/slapd.conf | /usr/bin/tail -1 | /bin/sed 's/:.*//'`
         if [ "$n" -gt 0 ]; then
   	    /bin/cp -fp /etc/openldap/slapd.conf /etc/openldap/slapd.conf.rpmsave;
	    /usr/bin/head -$n /etc/openldap/slapd.conf > $tf
            echo 'include         /etc/openldap/schema/dnszone.schema' >> $tf
            let n='n+1'
            /usr/bin/tail +$n /etc/openldap/slapd.conf >> $tf
            /bin/mv -f $tf /etc/openldap/slapd.conf;
            /bin/chmod --reference=/etc/openldap/slapd.conf.rpmsave /etc/openldap/slapd.conf
            [ -d /selinux ] && [ -x /sbin/restorecon ] && /sbin/restorecon /etc/openldap/slapd.conf >/dev/null 2>&1
            [ -x /etc/init.d/ldap ] && /etc/init.d/ldap condrestart >/dev/null 2>&1
         fi
         rm -f $tf >/dev/null 2>&1 || :;
      fi;
   fi;
fi;
:;

%preun sdb
if [ "$1" -eq 0 ] && [ -x /usr/sbin/named_sdb ] && [ -f /etc/openldap/slapd.conf ]; then
   if /bin/egrep -q '^include.*\dnszone.schema' /etc/openldap/slapd.conf; then
      tf=`/bin/mktemp /tmp/XXXXXX`
      /bin/egrep -v '^include.*dnszone\.schema' /etc/openldap/slapd.conf > $tf
      /bin/mv -f $tf /etc/openldap/slapd.conf;
      rm -f $tf >/dev/null 2>&1
      [ -d /selinux ] && [ -x /sbin/restorecon ] && /sbin/restorecon /etc/openldap/slapd.conf >/dev/null 2>&1
      [ -x /etc/init.d/ldap ] && /etc/init.d/ldap condrestart >/dev/null 2>&1 || :;
   fi;
fi;
:;

%endif # SDB

%post chroot
safe_replace()
{
   f1=$1;
   f2=$2;
   o=$3;
   g=$4;
   m=$5;
   dc=$6;
   if /usr/bin/test "x" =  "x$f1" -o "x" =  "x$f2" -o "$f1" =  "$f2"; then
      return 1;
   fi;
   if /usr/bin/test -r $f1 -a -s $f1 -a '!' -L $f1; then  
      if /usr/bin/test -r $f2 -a -s $f2 -a '!' -L $f2; then
         /bin/mv $f1 $f1'.rpmsave' >/dev/null 2>&1 || :;
         /bin/mv $f2 $f1 > /dev/null 2>&1 || :;         
      else
         /bin/rm -f $f2 > /dev/null 2>&1 || :;
      fi;
      /bin/mv $f1 $f2 > /dev/null 2>&1 || :;
      /bin/ln -s $f2 $f1 > /dev/null 2>&1 || :;
   else
      /bin/rm -f $f1 > /dev/null 2>&1 || :;
      if /usr/bin/test -r $f2 -a -s $f2; then
         /bin/ln -s $f2 $f1 > /dev/null 2>&1 || :;
      else
	 if /usr/bin/test "x$dc" != "x"; then 
	    echo  $dc > $f2;
	    /bin/ln -s $f2 $f1 > /dev/null 2>&1 || :;
	 else
	    return 2;
         fi;
      fi;
   fi;
   chown $o':'$g $f2;
   chmod $m $f2;
   return 0;
}
if /usr/bin/test -r /etc/sysconfig/named && /bin/egrep -q '^ROOTDIR=' /etc/sysconfig/named; then 
  :;
else 
  echo ROOTDIR="%{prefix}" >>/etc/sysconfig/named;
fi
if /usr/bin/test -r /etc/localtime; then 
   /bin/cp -fp /etc/localtime "%{prefix}/etc/localtime"
fi
safe_replace /etc/rndc.key "%{prefix}/etc/rndc.key" root named 644 '';
r=$?;
if /usr/bin/test "$r" -eq 2; then
   /bin/rm -f /etc/rndc.key
   echo -e 'key "rndckey" {\nalgorithm       hmac-md5;\nsecret "'`/usr/sbin/dns-keygen`'"\n};' > /etc/rndc.key;
   safe_replace /etc/rndc.key "%{prefix}/etc/rndc.key" root named 644 '';
fi;
default_ndc='include "/etc/rndc.key";'
if [ -f /etc/named.custom ]; then
   default_ndc='include "/etc/rndc.key";\ninclude "/etc/named.custom";'
   safe_replace /etc/named.custom "%{prefix}/etc/named.custom" root named 644 '' || :;
fi
safe_replace /etc/named.conf "%{prefix}/etc/named.conf" root named 644  "$default_ndc"
/usr/bin/find /var/named -xdev -type f | /bin/egrep -v '/var/named/chroot' | while read f; 
do
   d=`/usr/bin/dirname $f`;
   if test '!' -d "%{prefix}$d"; then
	mkdir -p "%{prefix}$d"; 
	chown named:named "%{prefix}$d";
	chmod 655 "%{prefix}$d";
   fi;
   safe_replace $f "%{prefix}$f" named named 644 '' || :;
done
[ ! -e "%{prefix}/dev/random" ] && mknod "%{prefix}/dev/random" c 1 8
[ ! -e "%{prefix}/dev/zero" ] && mknod "%{prefix}/dev/zero" c 1 5
[ ! -e "%{prefix}/dev/null" ] && mknod "%{prefix}/dev/null" c 1 3
chmod a+r "%{prefix}/dev/random" "%{prefix}/dev/null" "%{prefix}/dev/" 
chown root:named "%{prefix}/var/named"
chown named:named "%{prefix}/var/named/slaves"
chown named:named "%{prefix}/var/named/data"
/etc/init.d/named condrestart >/dev/null 2>&1 || :;
[ -d /selinux ] && [ -x /sbin/restorecon ] && /sbin/restorecon -R %{prefix} >/dev/null 2>&1
:;

%preun chroot
if [ "$1" = "0" ]; then
	/usr/bin/find /var/named/chroot -xdev -type f | while read f;
	do
	  F=`echo $f | sed 's#/var/named/chroot##'`;
	  if /usr/bin/test -L $F && test `/usr/bin/readlink $F` = $f; then
	     /bin/rm -f $F;
	     /bin/mv $f $F; 
	  fi;
	done
	if test -r /etc/sysconfig/named && grep -q '^ROOTDIR=' /etc/sysconfig/named; then		
          named_tmp=`/bin/mktemp /tmp/XXXXXX`
	  grep -v '^ROOTDIR='%{prefix} /etc/sysconfig/named > $named_tmp	
	  mv -f $named_tmp /etc/sysconfig/named
	  [ -d /selinux ] && [ -x /sbin/restorecon ] && /sbin/restorecon /etc/sysconfig/named
	fi
	/etc/init.d/named condrestart >/dev/null 2>&1 || :;
fi
:;

%triggerpostun -n bind-chroot -- bind-chroot
# Fix mess left by bind-chroot-9.2.2's %preun (bug 131803)
if [ "$1" -gt 0 ]; then
   if test -r /etc/sysconfig/named && grep -q '^ROOTDIR=' /etc/sysconfig/named; then
      :;
   else
      echo 'ROOTDIR='%{prefix} >> /etc/sysconfig/named
      /etc/init.d/named condrestart >/dev/null 2>&1 || :;
   fi;
fi;
:;

%changelog
* Sun Nov 13 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-22
- fix bug 172632 - remove .la files
- ship namedGetForwarders and namedSetForwarders scripts
- fix detection of -D option in chroot

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> - 24:9.3.1-21
- rebuilt with new openssl

* Wed Oct 19 2005 Jason Vas Dias <jvdias@redhat.com> - 24.9.3.1-20
- Allow the -D enable D-BUS option to be used within bind-chroot .
- fix bug 171226: supply some documentation for pgsql SDB .

* Thu Oct 06 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-18
- fix bug 169969: do NOT call dbus_svc_dispatch() in dbus_mgr_init_dbus() -
      task->state != task_ready and will cause Abort in task.c if process
      is waiting for NameOwnerChanged to do a SetForwarders

* Wed Oct 05 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-16
- Fix reconnecting to dbus-daemon after it stops & restarts .

* Tue Sep 27 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-14
- When forwarder nameservers are changed with D-BUS, flush the cache.

* Mon Sep 26 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-12
- fix bug 168302: use %{__cc} for compiling dns-keygen
- fix bug 167682: bind-chroot directory permissions
- fix issues with -D dbus option when dbus service not running or disabled

* Tue Aug 30 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-12
- fix bug 167062: named should be started after syslogd by default

* Mon Aug 22 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-11
- fix bug 166227: host: don't do default AAAA and MX lookups with '-t a' option

* Tue Aug 16 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-10
- Build with D-BUS patch by default; D-BUS support enabled with named -D option
- Enable D-BUS for named_sdb also 
- fix sdb pgsql's zonetodb.c: must use isc_hash_create() before dns_db_create()
- update fix for bug 160914 : test for RD=1 and ARCOUNT=0 also before trying next server 
- fix named.init script to handle named_sdb properly
- fix named.init script checkconfig() to handle named '-c' option
  and make configtest, test, check configcheck synonyms 

* Tue Jul 19 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-8
- fix named.init script bugs 163598, 163409, 151852(addendum)

* Tue Jul 12 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-7
- fix bug 160914: resolver utilities should try next server on empty referral
                  (now that glibc bug 162625 is fixed)
		  host and nslookup now by default try next server on SERVFAIL
		  (host now has '-s' option to disable, and nslookup given
                   '[no]fail' option similar to dig's [no]fail option).
- rebuild and re-test with new glibc & gcc (all tests passed).

* Tue May 31 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-6
- fix bug 157950: dig / host / nslookup should reject invalid resolv.conf
                  files and not use uninitialized garbage nameserver values
                  (ISC bug 14841 raised).

* Mon May 23 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-4_FC4
- Fix SDB LDAP

* Mon May 16 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-4 
- Fix bug 157601: give named.init a configtest function
- Fix bug 156797: named.init should check SELinux booleans.local before booleans
- Fix bug 154335: if no controls in named.conf, stop named with -TERM sig, not rndc
- Fix bug 155848: add NOTES section to named.8 man-page with info on all Red Hat 
                  BIND quirks and SELinux DDNS / slave zone file configuration
- D-BUS patches NOT applied until dhcdbd is in FC

* Sun May 15 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-4_dbus
- Enhancement to allow dynamic forwarder table management and 
- DHCP forwarder auto-configuration with D-BUS

* Thu Apr 14 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-2_FC4
- Rebuild for bind-sdb libpq.so.3 dependency
- fix bug 150981: don't install libbind man-pages if no libbind
- fix bug 151852: mount proc on $ROOTDIR/proc to allow sysconf(...)
  to work and correct number of CPUs to be determined

* Fri Mar 11 2005 Jason Vas Dias <jvdias@redhat.com> - 24:9.3.1-1_FC4
- Upgrade to ISC BIND 9.3.1 (final release) released today.

* Wed Mar  9 2005 Jason Vas Dias <jvdias@redhat.com> - 22.9.3.1rc1-5
- fix bug 150288: h_errno not being accessed / set correctly in libbind 
- add libbind man-pages from bind-8.4.6

* Mon Mar  7 2005 Jason Vas Dias <jvdias@redhat.com> - 22:9.3.1rc1-4
- Rebuild with gcc4 / glibc-2.3.4-14.
 
* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> - 22:9.3.1rc1-3
- configure with --with-pic to get PIC libraries

* Sun Feb 20 2005 Jason Vas Dias <jvdias@redhat.com> - 22:9.3.1rc1-2
- fix bug 149183: don't use getifaddrs() .

* Wed Feb 16 2005 Jason Vas Dias <jvdias@redhat.com> - 22:9.3.1rc1-1
- Upgrade to 9.3.1rc1
- Add Simplified Database Backend (SDB) sub-package ( bind-sdb )
-     add named_sdb - ldap + pgsql + dir database backend support with 
-     'ENABLE_SDB' named.sysconfig option
- Add BIND resolver library & includes sub-package ( libbind-devel)
- fix bug 147824 / 147073 / 145664: ENABLE_ZONE_WRITE in named.init
- fix bug 146084 : shutup restorecon

* Tue Jan 11 2005 Jason Vas Dias <jvdias@redhat.com> - 22:9.3.0-2
- Fix bug 143438: named.init will now make correct ownership of $ROOTDIR/var/named
-                 based on 'named_write_master_zones' SELinux boolean.
- Fix bug 143744: dig & nsupdate IPv6 timeout  (dup of 140528)

* Mon Nov 29 2004 Jason Vas Dias <jvdias@redhat.com> - 9.3.0-1
- Upgrade BIND to 9.3.0 in Rawhide / FC4 (bugs 134529, 133654...)
 
* Mon Nov 29 2004 Jason Vas Dias <jvdias@redhat.com> - 20:9.2.4-4
- Fix bugs 140528 and 141113:
- 2 second timeouts when IPv6 not configured and root nameserver's
- AAAA addresses are queried

* Mon Oct 18 2004 Jason Vas Dias <jvdias@redhat.com> - 20:9.2.4-2
- Fix bug 136243: bind-chroot %post must run restorecon -R %{prefix}
- Fix bug 135175: named.init must return non-zero if named is not run
- Fix bug 134060: bind-chroot %post must use mktemp, not /tmp/named
- Fix bug 133423: bind-chroot %files entries should have been %dirs

* Thu Sep 23 2004 Jason Vas Dias <jvdias@redhat.com> - 20:9.2.4-1
- BIND 9.2.4 (final release) released - source code actually
- identical to 9.2.4rc8, with only version number change.

* Mon Sep 20 2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc8-14
- Upgrade to upstream bind-9.2.4rc8 .
- Progress: Finally! Hooray! ISC bind now distributes:
- o named.conf(5) and nslookup(8) manpages 
-    'bind-manpages.bz2' source can now disappear
-    (could this have something to do with ISC bug I raised about this?)
- o 'deprecation_msg' global has vanished 
-     bind-9.2.3rc3-deprecation_msg_shut_up.diff.bz2 can disappear

* Mon Sep 20 2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc8-14
- Fix bug 106572/132385: copy /etc/localtime to chroot on start

* Fri Sep 10 2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc7-12_EL3
- Fix bug 132303: if ROOTDIR line was replaced after upgrade from
- bind-chroot-9.2.2-21, restart named

* Wed Sep 8  2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc7-11_EL3
- Fix bug 131803: replace ROOTDIR line removed by broken 
- bind-chroot 9.2.2-21's '%postun'; added %triggerpostun for bind-chroot

* Tue Sep 7  2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc7-10_EL3
- Fix bugs 130121 & 130981 for RHEL-3
 
* Mon Aug 30 2004 Jason Vas Dias <jvdias@redhat.com> - 10:9.2.4rc7-10
- Fix bug 130121: add '%ghost' entries for files included in previous
- bind-chroot & not in current - ie. named.conf, rndc.key, dev/* - 
- that RPM removed after upgrade .

* Thu Aug 26 2004 Jason Vas Dias <jvdias@redhat.com> 
- Fix bug 130981: add '-t' option to named-checkconf invocation in
- named.init if chroot installed.

* Wed Aug 25 2004 Jason Vas Dias <jvdias@redhat.com>
- Remove resolver(5) manpage now in man-pages (bug 130792); 
- Don't create /dev/ entries in bind-chroot if already there (bug 127556);
- fix bind-devel Requires (bug 130919)
- Set default location for dumpdb & stats files to /var/named/data

* Tue Aug 24 2004 Jason Vas Dias <jvdias@redhat.com>
- Fix devel Requires for bug 130738 & fix version

* Tue Aug 24 2004 Jason Vas Dias <jvdias@redhat.com>
- Fix errors on clean install if named group does not exist
- (bug 130777)

* Thu Aug 19 2004 Jason Vas Dias <jvdias@redhat.com>
- Upgrade to bind-9.2.4rc7; applied initscript fix
- for bug 102035.

* Mon Aug  9 2004 Jason Vas Dias <jvdias@redhat.com>
- Fixed bug 129289: bind-chroot install / deinstall
- on install, existing config files 'safe_replace'd
- with links to chroot copies; on uninstall, moved back.

* Fri Aug  6 2004 Jason Vas Dias <jvdias@redhat.com>
- Fixed bug 129258: "${prefix}/var/tmp" typo in spec

* Wed Jul 28 2004 Jason Vas Dias <jvdias@redhat.com>
- Fixed bug 127124 : 'Requires: kernel >= 2.4' 
- causes problems with Linux VServers

* Tue Jul 27 2004 Jason Vas Dias <jvdias@redhat.com>
- Fixed bug 127555 : chroot tar missing var/named/slaves

* Fri Jul 16 2004 Jason Vas Dias <jvdias@redhat.com>
- Upgraded to ISC version 9.2.4rc6

* Fri Jul 16 2004 Jason Vas Dias <jvdias@redhat.com>
- Fixed named.init generation of error messages on
- 'service named stop' and 'service named reload'
- as per bug 127775

* Thu Jun 23 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-19
- Bump for rhel 3.0  U3

* Thu Jun 23 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-18
- remove disable-linux-caps

* Wed Jun 16 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-17
- Update RHEL3 to latest bind 

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 8 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-15
- Remove device files from chroot,  Named uses the system one

* Fri Mar 26 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-14
- Move RFC to devel package 

* Fri Mar 26 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-13
- Fix location of restorecon

* Thu Mar 25 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-12
- Tighten security on config files.  Should be owned by root 

* Thu Mar 25 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-11
- Update key patch to include conf-keygen

* Tue Mar 23 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-10
- fix chroot to only happen once.
- fix init script to do kill insteall of killall

* Mon Mar 15 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-9
- Add fix for SELinux security context

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 28 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- run ldconfig for libs subrpm

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Tue Feb 17 2004 Daniel Walsh <dwalsh@redhat.com> 9.2.3-7
- Add COPYRIGHT

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 30 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.3-5
- Add defattr to libs

* Mon Dec 29 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.3-4
- Break out library package

* Mon Dec 22 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.3-3
- Fix condrestart

* Wed Nov 12 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.3-2
- Move libisc and libdns to bind from bind-util

* Tue Nov 11 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.3-1
- Move to 9.2.3

* Mon Oct 27 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-10
- Add PIE support

* Fri Oct 17 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-9
- Add /var/named/slaves directory

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against libnsl, not needed for Linux

* Wed Oct 8 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-6
- Fix local time in log file

* Tue Oct 7 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-5
- Try again 

* Mon Oct 6 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-4
- Fix handling of chroot -/dev/random

* Thu Oct 2 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-3
- Stop hammering stuff on update of chroot environment

* Mon Sep 29 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-2
- Fix chroot directory to grab all subdirectories

* Wed Sep 24 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2.P3-1
- New patch to support for "delegation-only"

* Wed Sep 17 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-23
- patch support for "delegation-only"

* Wed Jul 30 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-22
- Update to build on RHL

* Wed Jul 30 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-21
- Install libraries as exec so debug info will be pulled

* Sat Jul 19 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-20
- Remove BSDCOMPAT (BZ 99454)

* Tue Jul 15 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-19
- Update to build on RHL

* Tue Jul 15 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-18
- Change protections on /var/named and /var/chroot/named

* Tue Jun 17 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-17
- Update to build on RHL

* Tue Jun 17 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-16
- Update to build on RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 22 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-14
- Update to build on RHEL

* Tue Apr 22 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-13
- Fix config description of named.conf in chroot
- Change named.init script to check for existence of /etc/sysconfig/network

* Fri Apr 18 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-12
- Update to build on RHEL

* Fri Apr 18 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-11
- Update to build on RHEL

* Fri Apr 18 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-10
- Fix echo OK on starting/stopping service

* Fri Mar 28 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-9
- Update to build on RHEL

* Fri Mar 28 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-8
- Fix echo on startup

* Tue Mar 25 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-7
- Fix problems with chroot environment
- Eliminate posix threads

* Mon Mar 24 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-6
- Fix build problems

* Fri Mar 14 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-5
- Fix build on beehive

* Thu Mar 13 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-4
- build bind-chroot kit

* Tue Mar 11 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-3
- Change configure to use proper threads model

* Fri Mar 7 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-2
- update to 9.2.2

* Tue Mar 4 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.2-1
- update to 9.2.2

* Tue Jan 24 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.1-16
- Put a sleep in restart to make sure stop completes

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 7 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.1-14
- Separate /etc/rndc.key to separate file

* Tue Jan 7 2003 Nalin Dahyabhai <nalin@redhat.com> 9.2.1-13
- Use openssl's pkgconfig data, if available, at build-time.

* Mon Jan 6 2003 Daniel Walsh <dwalsh@redhat.com> 9.2.1-12
- Fix log rotate to use service named reload
- Change service named reload to give success/failure message [73770]
- Fix File checking [75710]
- Begin change to automatically run in CHROOT environment

* Tue Dec 24 2002 Daniel Walsh <dwalsh@redhat.com> 9.2.1-10
- Fix startup script to work like all others.

* Mon Dec 16 2002 Daniel Walsh <dwalsh@redhat.com> 9.2.1-9
- Fix configure to build on x86_64 platforms

* Wed Aug 07 2002 Karsten Hopp <karsten@redhat.de>
- fix #70583,  doesn't build on IA64 

* Tue Jul 30 2002 Karsten Hopp <karsten@redhat.de> 9.2.1-8
- bind-utils shouldn't require bind

* Mon Jul 22 2002 Karsten Hopp <karsten@redhat.de> 9.2.1-7
- fix name of pidfine in logrotate script (#68842)
- fix owner of logfile in logrotate script (#41391)
- fix nslookup and named.conf man pages (output on stderr)
  (#63553, #63560, #63561, #54889, #57457)
- add rfc1912 (#50005)
- gzip all rfc's
- fix typo in keygen.c (#54870)
- added missing manpages (#64065)
- shutdown named properly with rndc stop (#62492)
- /sbin/nologin instead of /bin/false (#68607)
- move nsupdate to bind-utils (where the manpage already was) (#66209, #66381)
- don't kill initscript when rndc fails (reload)    (#58750)


* Mon Jun 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.1-5
- Fix #65975

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.1-2
- Move libisccc, lib isccfg and liblwres from bind-utils to bind,
  they're not required if you aren't running a nameserver.

* Fri May 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 9.2.1 release

* Thu Mar 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-8
- Merge 30+ bug fixes from 9.2.1rc1 code

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-7
- Don't exit if /etc/named.conf doesn't exist if we're running
  chroot (#60868)
- Revert Elliot's changes, we do require specific glibc/glibc-kernheaders
  versions or bug #58335 will be back. "It compiles, therefore it works"
  isn't always true.

* Thu Feb 28 2002 Elliot Lee <sopwith@redhat.com> 9.2.0-6
- Fix BuildRequires (we don't need specific glibc/glibc-kernheaders 
versions).
- Use _smp_mflags

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-4
- rebuild, require recent autoconf, automake (#58335)

* Fri Jan 25 2002 Tim Powers <timp@redhat.com>
- rebuild against new libssl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-1
- 9.2.0

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc10.2
- 9.2.0rc10

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc8.2
- Fix up rndc.conf (#55574)

* Thu Oct 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc8.1
- rc8
- Enforce --enable-threads

* Mon Oct 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc7.1
- 9.2.0rc7
- Use rndc status for "service named status", it's supposed to actually
  work in 9.2.x.

* Wed Oct  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc5.1
- 9.2.0rc5
- Fix rpm --rebuild with ancient libtool versions (#53938, #54257)

* Tue Sep 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc4.1
- 9.2.0rc4

* Fri Sep 14 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.2.0-0.rc3.1
- 9.2.0rc3
- remove ttl patch, I don't think we need this for 8.0.
- remove dig.1.bz2 from the bind8-manpages tar file, 9.2 has a new dig man page
- add lwres* man pages to -devel

* Mon Sep  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-4
- Make sure /etc/rndc.conf isn't world-readable even after the
  %post script inserted a random key (#53009)

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-3
- Add build dependencies (#49368)
- Make sure running service named start several times doesn't create
  useless processes (#47596)
- Work around the named parent process returning 0 even if the config
  file is broken (it's parsed later by the child processes) (#45484)

* Mon Jul 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-2
- Don't use rndc status, it's not yet implemented (#48839)

* Sun Jul 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 9.1.3 release

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc3.1
- Fix up rndc configuration and improve security (#46586)

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc2.2
- Sync with caching-nameserver-7.1-6

* Mon Jun 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc2.1
- Update to rc2

* Fri Jun  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc1.3
- Remove resolv.conf(5) man page, it's now in man-pages

* Thu May 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc1.2
- Add named.conf man page from bind 8.x (outdated, but better than nothing,
  #42732)
- Rename the rndc key (#42895)
- Add dnssec* man pages

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.3-0.rc1.1
- 9.1.3rc1
- s/Copyright/License/

* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.2-1
- 9.1.2 final. No changes between 9.1.2-0.rc1.1 and this one, except for
  the version number, though.

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.2-0.rc1.1
- 9.1.2rc1

* Thu Mar 29 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.1-1
- 9.1.1

* Thu Mar 15 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.0-10
- Merge fixes from 9.1.1rc5

* Sun Mar 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 9.1.0-9
- Work around bind 8 -> bind 9 migration problem when using buggy zone files:
  accept zones without a TTL, but spew out a big fat warning. (#31393)

* Thu Mar  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add fixes from rc4

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- killall -HUP named if rndc reload fails (#30113)

* Tue Feb 27 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Merge some fixes from 9.1.1rc3

* Tue Feb 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't use the standard rndc key from the documentation, instead, create a random one
  at installation time (#26358)
- Make /etc/rndc.conf readable by user named only, it contains secret keys

* Tue Feb 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.1 probably won't be out in time, revert to 9.1.0 and apply fixes
  from 9.1.1rc2
- bind requires bind-utils (#28317)

* Tue Feb 13 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to rc2, fixes 2 more bugs
- Fix build with glibc >= 2.2.1-7

* Thu Feb  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 9.1.1rc1; fixes 17 bugs (14 of them affecting us;
  1 was fixed in a Red Hat patch already, 2 others are portability
  improvements)

* Wed Feb  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Remove initscripts 5.54 requirement (#26489)

* Mon Jan 29 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add named-checkconf, named-checkzone (#25170)

* Mon Jan 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use echo, not gprintf

* Wed Jan 24 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix problems with $GENERATE
  Patch from Daniel Roesen <droesen@entire-systems.com>
  Bug #24890

* Thu Jan 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.0 final

* Sat Jan 13 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.0rc1
- i18nify init script
- bzip2 source to save space

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix %%postun script

* Tue Jan  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.0b3

* Mon Jan  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add named.conf man page from bind8 (#23503)

* Sun Jan  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Make /etc/rndc.conf and /etc/sysconfig/named noreplace
- Make devel require bind = %%{version} rather than just bind

* Sun Jan  7 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix init script for real

* Sat Jan  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix init script when ROOTDIR is not set

* Thu Jan  4 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add hooks for setting up named to run chroot (RFE #23246)
- Fix up requirements

* Fri Dec 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.0b2

* Wed Dec 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move run files to /var/run/named/ - /var/run isn't writable
  by the user we're running as. (Bug #20665)

* Tue Dec 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix reverse lookups (#22272)
- Run ldconfig in %post utils

* Tue Dec 12 2000 Karsten Hopp <karsten@redhat.de>
- fixed logrotate script (wrong path to kill)
- include header files in -devel package
- bugzilla #22049, #19147, 21606

* Fri Dec  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.1.0b1 (9.1.0 is in our timeframe and less buggy)

* Mon Nov 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.0.1

* Mon Oct 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix initscript (Bug #19956)
- Add sample rndc.conf (Bug #19956)
- Fix build with tar 1.13.18

* Tue Oct 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add some missing man pages (taken from bind8) (Bug #18794)

* Sun Sep 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.0.0 final

* Wed Aug 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rc5
- fix up nslookup

* Thu Aug 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rc4

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 9.0.0rc1

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
