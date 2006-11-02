# TODO
# - doesn't compile
%define		_modname	xerces
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	PHP XML Parser with validation
Summary(pl):	Analizator XML-a z kontrol± poprawno¶ci dla PHP
Name:		php-xerces
Version:	0.8
Release:	1.1
License:	Apache
Group:		Libraries
Source0:	http://ggodlewski.host.sk/download/php-xerces/%{name}-%{version}.tar.gz
# Source0-md5:	8e9bbebe6c918d83fc608231e53a04aa
URL:		http://ggodlewski.host.sk/php/xerces/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.322
BuildRequires:	xerces-c-devel
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension lets you create XML parsers and then define handlers
for different XML events. It can also validate documents with DTD and
XML-Schema.

%description -l pl
Modu³ PHP umo¿liwiaj±cy parsowanie plików XML i obs³ugê zdarzeñ
zwi±zanych z tymi plikami. Potrafi równie¿ sprawdzaæ poprawno¶æ
dokumentów w oparciu o DTD i XML-Schema.

%prep
%setup -q

sed -e 's/-version-info [^ ]*/-avoid-version/' Makefile.am > Makefile.am.tmp
mv -f Makefile.am.tmp Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{extensionsdir}/xerces.so
