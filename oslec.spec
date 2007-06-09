#
# Conditional build:
%bcond_without  dist_kernel     	# allow non-distribution kernel
%define	no_install_post_strip	1

%define	_rel	0.1

Summary:	Open Source Line Echo Canceller (OSLEC)
Name:		oslec
Version:	20070608
Release:	%{_rel}
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	1fb5834740944a4ded9ce2556da63ff3
URL:		http://www.rowetel.com/ucasterisk/oslec.html
Requires:	dialog
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oslec is an open source high performance line echo canceller. It works
well on lines where the built-in Zaptel echo canceller fails. No
tweaks like rxgain/txgain or fxotrain are required. Oslec is supplied
as GPL licensed C source code and is free as in speech.

%package -n kernel%{_alt_kernel}-misc-oslec
Summary:	oslec - Linux kernel module
Summary(pl.UTF-8):	oslec - moduł jądra Linuksa
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
License:	GPL v2
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-misc-oslec
oslec - Linux kernel module.

%description -n kernel%{_alt_kernel}-misc-oslec -l pl.UTF-8
oslec - moduł jądra Linuksa.

%prep
%setup -q
sed -i "s|#include <echo.h>|#include <$PWD/spandsp-0.0.3/src/spandsp/echo.h>|" kernel/oslec_wrap.c

%build
%build_kernel_modules -C kernel -m oslec

%install
rm -rf $RPM_BUILD_ROOT

install -D kernel/oslec-ctrl-panel.sh $RPM_BUILD_ROOT%{_sbindir}/oslec-ctrl-panel.sh

%install_kernel_modules -m kernel/oslec -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n kernel%{_alt_kernel}-misc-oslec
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-oslec
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_sbindir}/oslec-ctrl-panel.sh

%files -n kernel%{_alt_kernel}-misc-oslec
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/oslec*
