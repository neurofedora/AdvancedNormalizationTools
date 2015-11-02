%global origname ANTs

# Name was discussed with upstream developers
# https://github.com/stnava/ANTs/issues/237
Name:           AdvancedNormalizationTools
Version:        2.1.0
Release:        1%{?dist}
Summary:        Advanced Normalization Tools (ANTs)

License:        BSD
URL:            http://stnava.github.io/%{origname}/
Source0:        https://github.com/stnava/ANTs/archive/v%{version}/%{origname}-%{version}.tar.gz
# https://github.com/stnava/ANTs/pull/236
Patch0:         0001-cmake-fixes-for-GITDIR-NOTFOUND.patch
# https://github.com/stnava/ANTs/issues/239
# https://github.com/stnava/ANTs/commit/ac0885a1a8791154f45cfd64d566a5dfe7d30583
Patch1:         0001-ENH-Alternate-input-type.-Necessary-for-other-platfo.patch
# I think it is Fedora's VTK specific case
Patch2:         0001-cmake-add-vtkFiltersStatisticsGnuR-dep-to-fix-undefi.patch
# https://github.com/stnava/ANTs/pull/240
Patch3:         0001-cmake-quote-optimization-flag-for-compiler-check.patch
# https://github.com/stnava/ANTs/pull/244
Patch4:         0001-cmake-add-multiarch-support.patch
# https://github.com/stnava/ANTs/pull/245
Patch5:         0001-rename-sa-to-adaBoostSegmentationRefinement.patch

BuildRequires:  gcc-c++ cmake
BuildRequires:  InsightToolkit-devel
BuildRequires:  gdcm-devel
BuildRequires:  vxl-devel
BuildRequires:  fftw-devel
BuildRequires:  git-core

%description
ANTs extracts information from complex datasets that include imaging
(Word Cloud). Paired with ANTsR (answer), ANTs is useful for managing,
interpreting and visualizing multidimensional data. ANTs is popularly
considered a state-of-the-art medical image registration and segmentation
toolkit. ANTsR is an emerging tool supporting standardized multimodality image
analysis.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -n %{origname}-%{version} -S git
rm -rf build/
mkdir -p build/
rm -rf .git/

%build
pushd build
  export ITK_DIR=%{_libdir}/cmake/InsightToolkit
  export GDCM_DIR=%{_datadir}/gdcm
  # TODO: testing requires external data
  %cmake ../ \
    -DANTS_SUPERBUILD=OFF \
    -DANTS_BUILD_DISTRIBUTE=ON \
    -DBUILD_TESTING=OFF \
    -DUSE_VTK=ON
  %make_build
popd

%install
pushd build
  %make_install
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING.txt
%doc README.md
%{_bindir}/*
%{_libdir}/libl_*.so.*

%files devel
%license COPYING.txt
%doc README.md
%{_libdir}/libl_*.so

%changelog
* Sat Oct 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.1.0-1
- Initial packaging
