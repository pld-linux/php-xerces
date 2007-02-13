# TODO
# - doesn't compile
%define		_modname	xerces
Summary:	PHP XML Parser with validation
Summary(pl.UTF-8):	Analizator XML-a z kontrolą poprawności dla PHP
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
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	xerces-c-devel
BuildRequires:	sed >= 4.0
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension lets you create XML parsers and then define handlers
for different XML events. It can also validate documents with DTD and
XML-Schema.

%description -l pl.UTF-8
Moduł PHP umożliwiający parsowanie plików XML i obsługę zdarzeń
związanych z tymi plikami. Potrafi również sprawdzać poprawność
dokumentów w oparciu o DTD i XML-Schema.

%prep
%setup -q
%{__sed} -i -e 's/-version-info [^ ]*/-avoid-version/' Makefile.am

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

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{php_extensiondir}/xerces.so
