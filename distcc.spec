%define	name    distcc 
%define version 2.18.3
%define release %mkrel 4
%define masqdir %{_libdir}/%{name}/bin

Name:           %{name}
Summary:	Program to distribute compilation of C or C++ 
Group:		Development/C
Version:        %{version}
Release:        %{release}
License: 	GPL
URL:		http://distcc.samba.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:        http://distcc.samba.org/ftp/distcc/%{name}-%{version}.tar.bz2
Source1:	xinetd.d-distcc.bz2
Source2:        %{name}d.init.bz2
BuildRequires:	gtk+2-devel popt-devel
Requires:	%{name}-client %{name}-daemon

%description
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile. 

This package does not contains any files, this is a meta package
used to ease the installation of distcc.

%package	client
Group:		Development/C
Summary:	Program to distribute compilation of C or C++

%description	client
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This is the client, who should be installed on the machine who
act as a master.

%package        masq
Group:          System/Servers
Requires:       %{name}-client
Summary:        Masquerade directory for enabling distcc by default

%description    masq
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contains the masquerade directories that can be used to make
most compiles use distcc by default when configured for parallel builds.

%package	daemon-common
Group:		System/Servers
Requires: 	gcc-c++
Summary:	Program to distribute compilation of C or C++
Requires(pre):		rpm-helper
Requires(postun):		rpm-helper
Requires:	%{name}-masq
Requires:       %{name}-daemon

%description daemon-common
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contain the common files for the daemon, installed on the
slaves nodes of the cluster.

%package	daemon-standalone
Group:		System/Servers
Requires: 	gcc-c++
Summary:	Program to distribute compilation of C or C++
Requires(post):		rpm-helper
Requires(postun):		rpm-helper
Obsoletes:      %{name}-daemon
Provides:       %{name}-daemon
Requires:	%{name}-daemon-common
Conflicts:	daemon-xinetd

%description daemon-standalone
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contain the standalone %{name} daemon, installed on the
slaves nodes of the cluster. 

%package	daemon-xinetd
Group:		System/Servers
Requires: 	gcc-c++ xinetd
Summary:	Program to distribute compilation of C or C++
Requires(pre):		rpm-helper
Requires(post):		rpm-helper
Obsoletes:      %{name}-daemon
Provides:       %{name}-daemon
Requires:	%{name}-daemon-common
Conflicts:	daemon-standalone

%description daemon-xinetd
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contain the xinetd %{name} daemon, installed on the slaves
nodes of the cluster. 

%package	gnome-monitor
Group:		Monitoring
Requires:	%{name}-client
Buildrequires:	libglade2.0-devel libgnome2-devel libgnomeui2-devel
Summary:	Program to monitor distibuted compilation of distcc

%description	gnome-monitor
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contain a graphical version of the distcc monitor.

%prep
%setup -q
bzcat %{SOURCE1} > xinetd.d-distcc
bzcat %{SOURCE2} > %{name}d.init

%build
%configure2_5x --enable-gnome --with-gnome
%make

cat <<EOF > %{name}.sh
if [ -f %{_sysconfdir}/sysconfig/ccache ]; then
    . %{_sysconfdir}/sysconfig/ccache
fi

if [ -f %{_sysconfdir}/sysconfig/distcc ]; then
    . %{_sysconfdir}/sysconfig/distcc
fi

if [ "\$USE_DISTCC_DEFAULT" = "yes" ]; then
  if [ "\$USE_CCACHE_DEFAULT" = "yes" ]; then
      if [ -z "\$CCACHE_PREFIX" ]; then
          export CCACHE_PREFIX=%{_bindir}/distcc
      fi
  else
      export PATH=%{masqdir}:\$PATH
  fi
fi
EOF
cat <<EOF > %{name}.csh
if ( -f %{_sysconfdir}/sysconfig/ccache ) then
    eval \`sed -n 's/^\([^#]*\)=\([^#]*\)/set \1=\2;/p' < %{_sysconfdir}/sysconfig/ccache
endif

if ( -f %{_sysconfdir}/sysconfig/distcc ) then
    eval \`sed -n 's/^\([^#]*\)=\([^#]*\)/set \1=\2;/p' < %{_sysconfdir}/sysconfig/distcc
endif

if ( "\$USE_DISTCC_DEFAULT" == "yes" ) then
  if ( "\$USE_CCACHE_DEFAULT" == "yes" ) then
      if ( "\$path" !~ *%{_libdir}/ccache/bin* ) then
          setenv CCACHE_PREFIX %{_bindir}/distcc
      endif
  else
      setenv path = ( %{masqdir} \$path )
  endif
fi
EOF

cat <<EOF > %{name}.sysconfig
USE_DISTCC_DEFAULT=yes
DISTCC_HOSTS=localhost
DISTCC_LOG=%{_var}/log/%{name}d.log
DISTCC_VERBOSE=1
TMPDIR=%{_var}/lib/%{name}d
EOF

cat << EOF > %{name}.logrotate
%{_var}/log/%{name}d.log {
    missingok
    monthly
    compress
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
%{makeinstall}
install -m644 xinetd.d-distcc -D $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
echo localhost > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hosts

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{name}d

mkdir -p $RPM_BUILD_ROOT%{masqdir}
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{masqdir}/gcc
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{masqdir}/cc
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{masqdir}/g++
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{masqdir}/c++
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{masqdir}/%{_target_platform}-gcc

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=Distcc monitor
Comment=Distcc monitor
Exec=distccmon-gnome
Icon=%{name}
Terminal=false
Type=Application
Categories=System;X-MandrivaLinux-System-Monitoring
EOF

install -m755 %{name}.sh -D $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.sh
install -m755 %{name}.csh -D $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.csh
install -m644 %{name}.sysconfig -D $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -m755 %{name}d.init -D %{buildroot}%{_initrddir}/%{name}d

mkdir -p $RPM_BUILD_ROOT%{_var}/log
touch $RPM_BUILD_ROOT%{_var}/log/%{name}d.log

install -m644 %{name}.logrotate -D $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}d

%pre daemon-common
%_pre_useradd %{name}d %{_localstatedir}/%{name}d /sbin/nologin
%create_ghostfile %{_var}/log/%{name}d.log distccd adm 0644

%post daemon-standalone
%_post_service %{name}d

%preun daemon-standalone
%_preun_service %{name}d

%pre daemon-xinetd

%post daemon-xinetd
# check that /etc/services has been already patched with ditscc port
CHECK_PORT=`grep distcc %{_sysconfdir}/services`
if [ -z "$CHECK_PORT" ]; then
	echo " " >> %{_sysconfdir}/services
	echo "distcc            3632/tcp # distcc port for daemon" >> %{_sysconfdir}/services
	else
	perl -pi -e 's/distcc.*/distcc                3632\/tcp \# distcc port for daemon/' %{_sysconfdir}/services
fi

# restarting xinetd service
service xinetd condrestart

%postun daemon-common
%_postun_userdel %{name}d

%postun daemon-xinetd
# restarting xinetd service
service xinetd condrestart

%post gnome-monitor
%update_menus

%postun gnome-monitor
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

# (misc) here to generate a empty rpm, who require the 2 others
%files 

%files client
%defattr(644,root,root,755)
%doc README* INSTALL AUTHORS doc/*
%{_mandir}/man1/%{name}.1*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/hosts
%defattr(755,root,root,755)
%{_bindir}/%{name}
%{_bindir}/%{name}mon-text
%{_mandir}/man1/%{name}mon-text.*

%files masq
%defattr(644,root,root,755)
%attr(0755,root,root) %{masqdir}

%files gnome-monitor
%defattr(-,root,root)
%{_datadir}/applications/mandriva-%{name}.desktop
%{_bindir}/%{name}mon-gnome
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.desktop
#%_datadir/*.glade*

%files daemon-common
%defattr(-,root,root)
%{_bindir}/%{name}d*
%{_mandir}/man1/%{name}d.1*
%defattr(-,distccd,distccd)
%{_localstatedir}/%{name}d
%attr(0640,distccd,adm) %ghost %{_var}/log/%{name}d.log
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}d

%files daemon-standalone
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%config(noreplace) %{_initrddir}/%{name}d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files daemon-xinetd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}

