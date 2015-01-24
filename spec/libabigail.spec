%global date 20150114
%global git_revision 63c81f0
%global checkout %{date}git%{git_revision}

Name: libabigail
Version: 1.0
Release: 0.3.%{checkout}%{?dist}
Summary: Set of ABI analysis tools

License: LGPLv3+
URL: https://sourceware.org/libabigail/
# This tarball was constructed from pulling the source code of
# libabigail from its Git repository by doing:
#    git clone git://sourceware.org/git/libabigail.git
#    pushd libabigail
#    git archive --prefix %%{name}-%%{version}/ -o %%{name}-%%{version}.tar.gz %%{git_revision} 
Source0: %{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: elfutils-devel
BuildRequires: libxml2-devel
BuildRequires: doxygen
BuildRequires: python-sphinx python-sphinx-latex
BuildRequires: texinfo
BuildRequires: dos2unix

%description
The libabigail package comprises four command line utilities: abidiff,
abicompat, abidw and abilint.  The abidiff command line tool compares
the ABI of two ELF shared libraries and emits meaningful textual
reports about changes impacting exported functions, variables and
their types.  abicompat checks if a subsequent version of a shared
library is still compatible with an applicatipon that is linked
against it.  abidw emits an XML representation of the ABI of a given
ELF shared library. abilint checks that a given XML representation of
the ABI of a shared library is correct.

Install libabigail if you need to compare the ABI of ELF shared
libraries.

%package devel
Summary: Shared library and header files to write ABI analysis tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains a shared library and the associated header files
that are necessary to develop applications that use the C++ Libabigail
library.  The library provides facilities to analyze and compare
application binary interfaces of shared libraries in the ELF format.


%package doc
Summary: Man pages, texinfo files and html manuals of libabigail
Requires(post): info
Requires(preun): info

%description doc
This package contains documentation for the libabigail tools in the
form of man pages, texinfo documentation and API documentation in html
format.

%prep
%setup -q

%build
autoreconf -i
%configure --disable-silent-rules --disable-zip-archive
make %{?_smp_mflags}
pushd doc
make html-doc
pushd manuals
make html-doc
make man
make info
popd
popd

%install
%make_install

# Install man and texinfo files as they are not installed by the
# default 'install' target of the makefile.
make -C doc/manuals install-man-and-info-doc DESTDIR=%{buildroot}
dos2unix doc/manuals/html/_static/jquery.js

%check
make check
if [ $1 -eq 0 ]; then
  cat tests/test-suite.log
fi

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/abicompat
%{_bindir}/abidiff
%{_bindir}/abidw
%{_bindir}/abilint
%{_libdir}/libabigail.so.0
%{_libdir}/libabigail.so.0.0.0
%doc AUTHORS ChangeLog
%license COPYING-LGPLV3

%files devel
%{_libdir}/libabigail.so
%exclude %{_libdir}/libabigail.a
%exclude %{_libdir}/libabigail.la
%{_libdir}/pkgconfig/libabigail.pc
%{_includedir}/*
%{_datadir}/aclocal/abigail.m4

%files doc
%license COPYING-LGPLV3
%doc doc/manuals/html/*
%{_mandir}/man7/*
%{_infodir}/abigail.info*

%post doc
/usr/sbin/install-info %{_infodir}/abigail.info* %{_infodir}/dir 2>/dev/null || :

%preun doc
if [ $1 -eq 0 ]; then
  /usr/sbin/install-info --delete %{_infodir}/abigail.info* %{_infodir}/dir 2>/dev/null || :
fi

%changelog
* Sat Jan 24 2015 SInny Kumari <ksinny@gmail.com> - 1.0-0.3.20150114git63c81f0
- Specify only sub-packgae name instead of giving full package name
- Add info as post and preun Requires for doc sub-package

* Fri Jan 23 2015 Sinny Kumari <ksinny@gmail.com> - 1.0-0.2.20150114git63c81f0
- Add python-sphinx-latex as BuildRequires
- Use license instead of doc macro for license file installation
- Update checkout value

* Sun Jan 18 2015 Sinny Kumari <ksinny@gmail.com> - 1.0-0.1.git.63c81f0
- Initial build of the libabigail package using source code from git
  revision 63c81f0.
