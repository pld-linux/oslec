#
# Conditional build:
%bcond_without  dist_kernel     	# allow non-distribution kernel
#
%define		rel	1
Summary:	Open Source Line Echo Canceller (OSLEC)
Summary(pl.UTF-8):	Open Source Line Echo Canceller (OSLEC) - usuwanie echa
Name:		oslec
Version:	0.2
Release:	%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	 http://www.rowetel.com/ucasterisk/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	554a0d44d2b4bac27ca1cc29fc55f69b
Patch0:		%{name}-build.patch
URL:		http://www.rowetel.com/ucasterisk/oslec.html
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.379
Requires:	dialog
# build broken (ppc, sparc) or nothing built (alpha)
ExcludeArch:	ppc sparc alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oslec is an open source high performance line echo canceller. It works
well on lines where the built-in Zaptel echo canceller fails. No
tweaks like rxgain/txgain or fxotrain are required. Oslec is supplied
as GPL licensed C source code and is free as in speech.

%description -l pl.UTF-8
Oslec to mający otwarte źródła i wysoką wydajność moduł do usuwania
echa z linii. Działa dobrze na liniach, na których zawodzi wbudowane
narzędzie Zaptela do usuwania echa. Nie są wymagane sztuczki typu
rxgain/txgain czy fxotrain. Oslec jest wolnodostępny, rozpowszechniany
na licencji GPL z kodem źródłowym w C.

%package -n kernel%{_alt_kernel}-misc-oslec
Summary:	oslec - Linux kernel module
Summary(pl.UTF-8):	oslec - moduł jądra Linuksa
Release:	%{rel}@%{_kernel_ver_str}
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
%patch0 -p1

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
