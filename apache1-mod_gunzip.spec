%define		mod_name	gunzip
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: On-the-fly decompression of HTML documents
Summary(es):	Descompresión instantanea de archivos HTML para Apache
Summary(pl):	Modu³ do apache: dekompresuje dokumenty HTML w locie
Summary(pt_BR):	Descompressão "On-the-fly" de arquivos HTML para o Apache
Name:		apache-mod_%{mod_name}
Version:	1
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://sep.hamburg.com/mod_%{mod_name}.tar.gz
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
BuildRequires:	zlib-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
Apache module: On-the-fly decompression of HTML documents.

%description -l es
Descompresión instantanea de archivos HTML para Apache.

%description -l pl
Modu³ do apache: dekompresuje dokumenty HTML w locie.

%description -l pt_BR
Descompressão "On-the-fly" de arquivos HTML para o Apache.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	%{_sysconfdir}/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
