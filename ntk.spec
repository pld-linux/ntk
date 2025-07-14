Summary:	Fast Light Tool Kit fork from the NON project
Name:		ntk
Version:	1.3.1000
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	https://git.tuxfamily.org/non/fltk.git/snapshot/fltk-%{version}.tar.bz2
# Source0-md5:	6948491e6fab7777b2975b509099c072
Patch0:		link.patch
URL:		http://non.tuxfamily.org/wiki/NTK
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	fontconfig
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NTK is a fork of FLTK 1.3.0 which adds graphics rendering via Cairo,
support for transparent/overlapping widgets, streamlining of
internals, and some new/improved widgets.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n fltk-%{version}

%patch -P0 -p1

%build
CC="%{__cc}" \
CXX="%{__cxx}" \
CPP="%{__cpp}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
LINKFLAGS="%{rpmldflags}" \
./waf configure \
	--prefix="%{_prefix}" \
	--libdir="%{_libdir}" \
	--destdir="$RPM_BUILD_ROOT"

./waf build -v

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT \
./waf install

rm $RPM_BUILD_ROOT%{_libdir}/libntk.a{,.1}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libntk.a.%{version} $RPM_BUILD_ROOT%{_libdir}/libntk.a
rm $RPM_BUILD_ROOT%{_libdir}/libntk_images.a{,.1}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libntk_images.a.%{version} $RPM_BUILD_ROOT%{_libdir}/libntk_images.a

# library not built
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/%{name}_gl.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS README
%attr(755,root,root) %{_bindir}/ntk-chtheme
%attr(755,root,root) %{_bindir}/ntk-fluid
%attr(755,root,root) %{_libdir}/libntk.so.1.*
%ghost %attr(755,root,root) %{_libdir}/libntk.so.1
%attr(755,root,root) %{_libdir}/libntk_images.so.1.*
%ghost %attr(755,root,root) %{_libdir}/libntk_images.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libntk.so
%attr(755,root,root) %{_libdir}/libntk_images.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc
#%{_pkgconfigdir}/%{name}_gl.pc
%{_pkgconfigdir}/%{name}_images.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libntk.a
%{_libdir}/libntk_images.a
