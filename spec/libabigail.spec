Name: libabigail
Version: 1.0.0
Release: 1%{?dist}
Summary: ABI analysis tool

License: LGPLv3+
URL: https://sourceware.org/libabigail/
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone git://sourceware.org/git/libabigail.git
#  cd libabigail && autoreconf -i && ./configure && make dist
Source0: %{name}-%{version}.tar.gz

BuildRequires: libtool, elfutils-devel, libxml2-devel, doxygen, python-sphinx
Requires: elfutils

%description
Libabigail aims at providing a C++ library for constructing, manipulating,
serializing and de-serializing ABI-relevant artifacts. The set of artifacts that
we are interested in is made of constructions like types, variables, functions 
and declarations of a given library or program.For a given program or library,
this set of constructions is called an ABI corpus. Provides library to
manipulate ABI corpora, compare them, provides detailed information about their 
differences and help build tools to infer interesting conclusions about these
difference.

%package -n libabigail-devel
Summary: Development package
Provides: libabigail-devel = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description -n libabigail-devel
Development package of libabigail


%package -n libabigail-man
Summary: Man page of libabigail tools
Provides: libabigail-man = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description -n libabigail-man
Man page for tools like abidiff, abidw, abilint provided by libabigail

%prep
%setup -q


%build
autoreconf -i
%configure
make %{?_smp_mflags}
pushd doc
make html-doc
pushd manuals
make html-doc
make man
popd
popd

%check
make check

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/libabigail.so.*
%{_datadir}/aclocal
%doc doc/manuals/html

%files -n libabigail-devel
%defattr(-,root,root,-)
%{_libdir}/libabigail.so
%{_libdir}/libabigail.a
%{_libdir}/libabigail.la
%{_libdir}/pkgconfig/libabigail.pc
%{_includedir}/*
%doc doc/api/

%files -n libabigail-man
%defattr(-,root,root,-)
%{_mandir}/man7/*

%changelog
* Wed Jan 14 2015 Sinny Kumari <ksinny@gmail.com> - 1.0.0-1
- Initial build of libabigail
