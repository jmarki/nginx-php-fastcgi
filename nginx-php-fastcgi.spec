%define nginx_user      nginx
%define nginx_group      nginx
%define nginx_home      %{_localstatedir}/www/nginx
%define nginx_confdir   %{_sysconfdir}/nginx
%define nginx_sockdir   %{_localstatedir}/run/%{name}

Name:           nginx-php-fastcgi
Version:        0.2
Release:        3%{?dist}
Summary:        PHP-CGI daemon for nginx, using FastCGI
Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            http://github.com/jmarki/nginx-php-fastcgi
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:           php-cli, gawk, nginx
# for /usr/sbin/useradd
Requires(pre):      shadow-utils
Requires(post):     chkconfig
# for /sbin/service
Requires(preun):    chkconfig, initscripts
Requires(postun):   initscripts

Source0:    https://github.com/jmarki/nginx-php-fastcgi/%{name}-%{version}.tar.gz

%description
PHP-CGI daemon for Nginx [engine x], using FastCGI

%prep
%setup -q -n %{name}

%build

%install
rm -rf %{buildroot}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
%{__install} -p -d -m 0775 %{buildroot}%{nginx_sockdir}
%{__install} -p -d -m 0755 %{buildroot}%{_initrddir}
%{__install} -p -m 0644 php-fastcgi.conf %{buildroot}%{nginx_confdir}/conf.d/
%{__install} -p -m 0644 %{name}.conf %{buildroot}%{nginx_confdir}/
%{__install} -p -m 0644 fastcgi_params_php %{buildroot}%{nginx_confdir}/conf.d/
%{__install} -p -m 0755 %{name}.init %{buildroot}%{_initrddir}/%{name}

%clean
rm -rf %{buildroot}

%pre
if [ $1 == 1 ]; then
    %{_sbindir}/useradd -c "Nginx user" -s /bin/false -r -d %{nginx_home} %{nginx_group} 2>/dev/null || :
fi

%post
if [ $1 == 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 == 2 ]; then
    /sbin/service %{name} upgrade || :
fi

%files
%defattr(-,root,root,-)
%attr(0755,%{nginx_user},%{nginx_group}) %{nginx_sockdir}
%attr(0755,-,-) %{_initrddir}/%{name}
%attr(0755,-,-) %{nginx_confdir}
%attr(0644,-,-) %{nginx_confdir}/%{name}.conf
%attr(0644,-,-) %{nginx_confdir}/conf.d/php-fastcgi.conf
%attr(0644,-,-) %{nginx_confdir}/conf.d/fastcgi_params_php
%config(noreplace) %{nginx_confdir}/%{name}.conf
%config(noreplace) %{nginx_confdir}/conf.d/php-fastcgi.conf
%config(noreplace) %{nginx_confdir}/conf.d/fastcgi_params_php


%changelog
* Tue Dec 27 2012 Koo Jun Hao <junhao82 at jmarki dot net> - 0.2-3
- bugfix in spec file

* Tue Dec 27 2012 Koo Jun Hao <junhao82 at jmarki dot net> - 0.2
- released version 0.2

* Tue May 10 2011 Koo Jun Hao <junhao82 at jmarki dot net> - 0.2
- changed to use the more standard /var/www/nginx directory instead

* Thu May 05 2011 Koo Jun Hao <junhao82 at jmarki dot net> - 0.1-1
- modified from Nginx spec file from Fedora EPEL repository
- initial commit of init files and configuration for PHP-CGI on nginx
