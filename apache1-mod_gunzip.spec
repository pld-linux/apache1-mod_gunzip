%define		mod_name	gunzip
Summary:	Apache module: On-the-fly decompression of HTML documents
Summary(pl):	Modu³ do apache: dekompresuje dokumenty HTML w locie
Name:		apache-mod_%{mod_name}
Version:	1
Release:	0.1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://sep.hamburg.com/mod_%{mod_name}.tar.gz
Copyright:	GPL
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache-devel
BuildRequires:	zlib-devel
Prereq:		/usr/sbin/apxs
Requires:	apache
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
Apache module: On-the-fly decompression of HTML documents.

%description -l pl
Modu³ do apache: dekompresuje dokumenty HTML w locie.

%prep 
%setup -q -n mod_%{mod_name}

%build
/usr/sbin/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT


install -d $RPM_BUILD_ROOT%{_pkglibdir}

install -m755 mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

strip --strip-unneeded $RPM_BUILD_ROOT%{_pkglibdir}/* 

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
