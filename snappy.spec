# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: snappy
Epoch: 100
Version: 1.2.1
Release: 1%{?dist}
Summary: Fast compression/decompression library
License: BSD-3-Clause
URL: https://github.com/google/snappy/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: lz4-devel
BuildRequires: lzo-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel

%description
Snappy is a compression/decompression library. It does not aim for
maximum compression, or compatibility with any other compression
library; instead, it aims for very high speeds and reasonable
compression.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p build
pushd build && \
    cmake \
        .. \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DSNAPPY_BUILD_BENCHMARKS=OFF \
        -DSNAPPY_BUILD_TESTS=OFF && \
popd
pushd build && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
popd

%install
pushd build && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libsnappy1
Summary: Fast compression/decompression library

%description -n libsnappy1
Snappy is a compression/decompression library. It does not aim for
maximum compression, or compatibility with any other compression
library; instead, it aims for very high speeds and reasonable
compression.

%package -n snappy-devel
Summary: Fast compression/decompression library (development files)
Requires: libsnappy1 = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description -n snappy-devel
This package contains the development files required to build programs
against Snappy.

%post -n libsnappy1 -p /sbin/ldconfig
%postun -n libsnappy1 -p /sbin/ldconfig

%files
%license COPYING

%files -n libsnappy1
%{_libdir}/*.so.*

%files -n snappy-devel
%dir %{_libdir}/cmake/Snappy/
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/cmake/Snappy/*
%{_libdir}/pkgconfig/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n snappy-devel
Summary: Fast compression/decompression library (development files)
Requires: snappy = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description -n snappy-devel
This package contains the development files required to build programs
against Snappy.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/*.so.*

%files -n snappy-devel
%dir %{_libdir}/cmake/Snappy/
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/cmake/Snappy/*
%{_libdir}/pkgconfig/*
%endif

%changelog
