%define dtdver 20030619
%define mltype mathml20
%define sgmlbase %{_datadir}/sgml

Name:    docbook-dtd-%{mltype}
Version: 1.0
Release:  %mkrel 3
Group  : Publishing
Summary: XHTML 1.1 plus MathML 2.0 document type definition
License: Distributable
URL    : http://numexp.sourceforge.net/

# tar.gz at http://www.w3.org/Math/DTD/mathml2.tgz
Source0  : mathml2.tar.bz2
Patch0   : %{name}-sysid-base.patch.bz2
BuildArch: noarch

BuildRequires: libxml2-utils
Requires: sgml-common >= 0.6.3-2mdk

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -q -n mathml2

# CRLF -> LF
find -type f -print0 | xargs -r -0 perl -pi -e 's/\r//g'

%patch0 -p1

%build

%install
[ -z "$RPM_BUILD_ROOT" -o "$RPM_BUILD_ROOT" = "/" ] || rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT%{sgmlbase}/docbook/%{mltype}-dtd-%{dtdver}
mkdir -p $DESTDIR
cp -a html iso8879 iso9573-13 mathml $DESTDIR/
cp -a mathml2.dtd xhtml-math11-f.dtd *.mod $DESTDIR/

ln -s %{mltype}-dtd-%{dtdver} $RPM_BUILD_ROOT%{sgmlbase}/docbook/%{mltype}-dtd

# create subcatalog
SUBCATALOG="%{_sysconfdir}/xml/mathml.cat"
SGMLDIR="%{sgmlbase}/docbook/%{mltype}-dtd"

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xml
xmlcatalog --create > $RPM_BUILD_ROOT$SUBCATALOG

xmlcatalog --noout --add "rewriteSystem" \
	"http://www.w3.org/Math/DTD/mathml2/" \
	"file://$SGMLDIR/" \
	$RPM_BUILD_ROOT$SUBCATALOG

xmlcatalog --noout --add "public" \
	"-//W3C//DTD MathML 2.0//EN" \
	"$SGMLDIR/mathml2.dtd" \
	$RPM_BUILD_ROOT$SUBCATALOG

xmlcatalog --noout --add "public" \
	"-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN" \
	"$SGMLDIR/xhtml-math11-f.dtd" \
	$RPM_BUILD_ROOT$SUBCATALOG

xmlcatalog --noout --add "public" \
	"-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN" \
	"$SGMLDIR/xhtml-math11-f.dtd" \
	$RPM_BUILD_ROOT$SUBCATALOG


%clean
[ -z "$RPM_BUILD_ROOT" -o "$RPM_BUILD_ROOT" = "/" ] || rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%{sgmlbase}/docbook/%{mltype}-dtd
%{sgmlbase}/docbook/%{mltype}-dtd-%{dtdver}
%{_sysconfdir}/xml/mathml.cat

%post
CATALOG="%{_sysconfdir}/xml/catalog"
SUBCATALOG="%{_sysconfdir}/xml/mathml.cat"
# test xmlcatalog is available before using it...
[ -f "$CATALOG" -a -f "$SUBCATALOG" ] || exit 0

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//W3C//DTD MathML 2.0//EN" \
	"file://$SUBCATALOG" "$CATALOG"
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//W3C//DTD XHTML 1.1 plus MathML 2.0" \
	"file://$SUBCATALOG" "$CATALOG"
%{_bindir}/xmlcatalog --noout --add "delegateSystem" \
	"http://www.w3.org/Math/DTD/mathml2"  \
	"file://$SUBCATALOG" "$CATALOG"
%{_bindir}/xmlcatalog --noout --add "delegateURI" \
	"http://www.w3.org/Math/DTD/mathml2" \
	"file://$SUBCATALOG" "$CATALOG"

%preun
CATALOG=%{_sysconfdir}/xml/catalog
SUBCATALOG="%{_sysconfdir}/xml/mathml.cat"
# test xmlcatalog is available before using it...
[ -f "$CATALOG" -a -f "$SUBCATALOG" ] || exit 0
# Do not remove if upgrade
[ "$1" = "0" ] || exit 0

%{_bindir}/xmlcatalog --noout --del \
	"file://$SUBCATALOG" $CATALOG
 
