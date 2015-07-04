%define masqdir %{_libexecdir}/%{name}/bin
%define	prerel	rc1
%define	_disable_ld_no_undefined 1

Name:           distcc
Summary:	Program to distribute compilation of C or C++ 
Group:		Development/C
Version:        3.2
Release:        %{?prerel:0.%{prerel}.}1
License: 	GPLv2+
URL:		http://distcc.org
Source0:        https://github.com/distcc/distcc/archive/%{name}-%{version}%{?prerel}.tar.gz
Source1:	hosts.sample
Source2:        distccd.service
Source3:	xinetd.d-distcc
Source4:	distcc.sh
Source5:	distcc.csh
Source6:	distccd.sysconfig
Patch0:		distcc-3.2rc1-logrotate-mdkconf.patch
Patch1:		distcc-3.2rc1-desktop-utf8.patch
BuildRequires:	pkgconfig(avahi-client) pkgconfig(popt)
BuildRequires:	pkgconfig(python2) krb5-devel
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
Requires(post):	rpm-helper
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
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
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
BuildRequires:	pkgconfig(gtk+-x11-2.0) pkgconfig(pango)
BuildRequires:	pkgconfig(libgnomeui-2.0) pkgconfig(libgnome-2.0)
Summary:	Program to monitor distibuted compilation of distcc

%description	gnome-monitor
distcc is a program to distribute compilation of C or C++ code across
several machines on a network. distcc should always generate the same
results as a local compile, is simple to install and use, and is often
two or more times faster than a local compile.

This package contain a graphical version of the distcc monitor.

%prep
%setup -q -n %{name}-%{version}%{?prerel}
%patch0 -p1 -b .logrotate~
%patch1 -p1 -b .utf8~
chmod o+r -R .

%build
%configure	--with-gnome \
		--with-avahi \
		--with-auth \
		--disable-Werror
# XXX: for some reason --no-undefined causes problem when linking with python3...
LDSHARED='%{__cc} -pthread -shared' %make

%install
%makeinstall_std

# Move desktop & icon files to right directories
mkdir -p %{buildroot}%{_datadir}/applications
mv %{buildroot}%{_datadir}/%{name}/*.desktop %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_iconsdir}
mv %{buildroot}%{_datadir}/%{name}/*.png %{buildroot}%{_iconsdir}

install -p -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/%{name}/hosts
install -p -m644 %{SOURCE2} -D %{buildroot}%{_unitdir}/distccd.service
install -p -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/xinetd.d/%{name}
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -p -m644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh
install -p -m644 %{SOURCE6} -D %{buildroot}%{_sysconfdir}/sysconfig/distccd
install -p -m644 contrib/redhat/logrotate -D %{buildroot}%{_sysconfdir}/logrotate.d/distccd

rm -r %{buildroot}%{_docdir}/%{name}

mkdir -p %{buildroot}%{_localstatedir}/lib/distccd

mkdir -p %{buildroot}%{masqdir}
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/gcc
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/cc
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/g++
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/c++
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/%{_target_platform}-gcc
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/%{_target_platform}-g++
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/clang
ln -s %{_bindir}/%{name} %{buildroot}%{masqdir}/clang++

mkdir -p %{buildroot}%{_logdir}
touch %{buildroot}%{_logdir}/distccd.log

%pre daemon-common
%_pre_useradd distccd %{_localstatedir}/lib/distccd /sbin/nologin
%create_ghostfile %{_logdir}/distccd.log distccd adm 0644

%post daemon-standalone
%_post_service distccd

%preun daemon-standalone
%_preun_service distccd


%post daemon-xinetd
service xinetd condrestart

%postun daemon-common
%_postun_userdel distccd

%postun daemon-xinetd
service xinetd condrestart

# (misc) here to generate a empty rpm, who require the 2 others
%files 

%files client
%doc README* AUTHORS doc/*
%{_mandir}/man1/distcc.1*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/distcc/hosts
%{_bindir}/distcc
%{_bindir}/distccmon-text
%{_bindir}/lsdistcc
%{_bindir}/pump
%{_mandir}/man1/distccmon-text.1*
%{_mandir}/man1/include_server.1*
%{_mandir}/man1/pump.1*


%files masq
%{masqdir}

%files gnome-monitor
%{_datadir}/applications/distccmon-gnome.desktop
%{_iconsdir}/distccmon-gnome-icon.png
%{_bindir}/distccmon-gnome

%files daemon-common
%{_bindir}/distccd*
%{_mandir}/man1/distccd.1*
%attr(-,distccd,distccd) %{_localstatedir}/lib/distccd
%attr(0640,distccd,adm) %ghost %{_logdir}/distccd.log
%config(noreplace) %{_sysconfdir}/logrotate.d/distccd
%config(noreplace) %{_sysconfdir}/default/distcc
%config(noreplace) %{_sysconfdir}/distcc/*allow*
%{python_sitearch}/include_server*

%files daemon-standalone
%{_sysconfdir}/profile.d/%{name}.*sh
%{_unitdir}/distccd.service
%config(noreplace) %{_sysconfdir}/sysconfig/distccd

%files daemon-xinetd
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
