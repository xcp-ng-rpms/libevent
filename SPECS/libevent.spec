%global package_speccommit 47219eb4efa6c86cedf6d7801fdcb0c7ffdcaf6f
%global usver 2.0.21
%global xsver 5
%global xsrel %{xsver}%{?xscount}%{?xshash}

Name:           libevent
Version:        2.0.21
Release:        %{?xsrel}%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://sourceforge.net/projects/levent/
Source0: libevent-2.0.21-stable.tar.gz
Patch0: libevent-2.0.10-stable-configure.patch
Patch1: libevent-nonettests.patch

BuildRequires: doxygen

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%package doc
Summary: Development documentation for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}-devel, you will
need to install %{name}-doc.

%prep
%autosetup -p1 -n libevent-%{version}-stable

%build
%configure \
    --disable-dependency-tracking --disable-static --disable-openssl
make %{?_smp_mflags} all

# Create the docs
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/html
(cd doxygen/html; \
	install -p -m 644 *.* $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/html)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/sample
(cd sample; \
	install -p -m 644 *.c Makefile* $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/sample)

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*
%{_libdir}/libevent_pthreads-*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_includedir}/event2/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-devel-%{version}/html/*
%{_docdir}/%{name}-devel-%{version}/sample/*

%changelog
* Sat Sep 28 2024 Deli Zhang <deli.zhang@citrix.com> - 2.0.21-5
- First imported release

