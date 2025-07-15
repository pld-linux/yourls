Summary:	YOURLS: Your Own URL Shortener
Name:		yourls
Version:	1.7
Release:	0.3
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/YOURLS/YOURLS/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	171ea94dc65d1d4f8c7e857a8b650ae1
Source1:	apache.conf
Source2:	lighttpd.conf
Patch0:		config.patch
URL:		http://yourls.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
YOURLS stands for Your Own URL Shortener. It is a small set of PHP
scripts that will allow you to run your own URL shortening service (a
la TinyURL or bitly).

Running your own URL shortener is fun, geeky and useful: you own your
data and don't depend on third party services. It's also a great way
to add branding to your short URLs, instead of using the same public
URL shortener everyone uses.

%prep
%setup -q -n YOURLS-%{version}
mv user/config{-sample,}.php

%patch -P0 -p1

# do not obfuscate
rm user/index.html
rm user/plugins/index.html
rm user/languages/index.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT{%{_appdir}/user,%{_sysconfdir}}/config.php
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/user

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md CONTRIBUTING.md LICENSE.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
