%define		mod_name	gunzip
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: On-the-fly decompression of HTML documents
Summary(es):	Descompresión instantanea de archivos HTML para Apache
Summary(pl):	Modu³ do apache: dekompresuje dokumenty HTML w locie
Summary(pt_BR):	Descompressão "On-the-fly" de arquivos HTML para o Apache
Name:		apache1-mod_%{mod_name}
Version:	1
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://sep.hamburg.com/mod_%{mod_name}.tar.gz
# Source0-md5:	9f549047abccccf6570333bb0313d2cd
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel
BuildRequires:	zlib-devel
Requires(post,preun):	%{apxs}
Requires:	apache1
Obsoletes:	apache-mod_%{mod_name} <= %{version}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
