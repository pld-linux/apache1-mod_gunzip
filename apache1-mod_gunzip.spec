%define		mod_name	gunzip
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: On-the-fly decompression of HTML documents
Summary(es):	Descompresi�n instantanea de archivos HTML para Apache
Summary(pl):	Modu� do apache: dekompresuje dokumenty HTML w locie
Summary(pt_BR):	Descompress�o "On-the-fly" de arquivos HTML para o Apache
Name:		apache1-mod_%{mod_name}
Version:	1
Release:	2
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://sep.hamburg.com/mod_%{mod_name}.tar.gz
# Source0-md5:	9f549047abccccf6570333bb0313d2cd
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_gunzip <= 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: On-the-fly decompression of HTML documents.

%description -l es
Descompresi�n instantanea de archivos HTML para Apache.

%description -l pl
Modu� do apache: dekompresuje dokumenty HTML w locie.

%description -l pt_BR
Descompress�o "On-the-fly" de arquivos HTML para o Apache.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
