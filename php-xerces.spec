Summary:	PHP XML Parser with validation
Summary(pl):	Parser XML z kontrol± poprawno¶ci dla PHP
Name:		php-xerces
Version:	0.5
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ggodlewski.host.sk/download/php-xerces/%{name}-%{version}.tar.gz
# Source0-md5:	ccd6688e01a88a3a14735205ce254083
URL:		http://ggodlewski.host.sk/php/xerces
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	xerces-c-devel
BuildRequires:	php-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php

%description
This extension lets you create XML parsers and then
define handlers for different XML events.
It can also validate documents with DTD and XML-Schema.

%description -l pl
Modu³ PHP umo¿liwiaj±cy parsowanie plików XML i obs³ugê zdarzeñ
zwi±zanych z tymi plikami.
Potrafi równie¿ sprawdzaæ poprawno¶æ dokumentów w oparciu
o DTD i XML-Schema.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove xerces %{_sysconfdir}/php.ini
fi

%post
%{_sbindir}/php-module-install install xerces %{_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{_libdir}/php/*
