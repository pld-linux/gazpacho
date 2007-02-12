Summary:	Building Interfaces the easy way
Summary(pl.UTF-8):   Tworzenie interfejsów w łatwy sposób
Name:		gazpacho
Version:	0.6.5
Release:	1
License:	LGPL
Group:		Development/Building
Source0:	http://ftp.acc.umu.se/pub/GNOME/sources/gazpacho/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	853d2df3bcf3205848e695177bdba6a8
Patch0:		%{name}-desktop.patch
URL:		http://gazpacho.sicem.biz/
BuildRequires:	python-devel
BuildRequires:	sed >= 4.0
Requires:	python-pygtk-gtk >= 1:2.6.0
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautocompressdoc	AUTHORS CONTRIBUTORS COPYING

%description
This program allows you to create the Graphical User Interface (GUI)
of your GTK+ program in a visual way. It started as a Glade-3 clone
but now it is more complete and featured than its ancestor. It tries
to be compatible with libglade but it can handle some widgets that
still lack support in libglade.

%description -l pl.UTF-8
Ten program pozwala tworzyć graficzny interfejs użytkownika (GUI) dla
programów GTK+ w sposób wizualny. Z początku był klonem Glade-3, ale w
chwili obecnej jest bardziej zaawansowany od swojego przodka. Gazpacho
stara się być kompatybilnym z libglade, choć zawiera kilka kontrolek
wciąż nie wspieranych przez libglade.

%prep
%setup -q
%patch0 -p1

sed -i	-e "s/from gazpacho import application//" \
	-e "s/application.__version__/'%{version}'/" \
	setup.py

sed -i	-e "s@return self._variables\['docs_dir'\]\[0\]@return '/usr/share/doc/%{name}-%{version}/'@" gazpacho/environ.py

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_pixmapsdir}}

python setup.py install \
	--optimize=2 \
	--root $RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{py_sitescriptdir}/gazpacho -name '*.py' -exec rm -f {} \;

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install pixmaps/gazpacho-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/gazpacho.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%postun
if [ $1 = 0 ]; then
    umask 022
    [ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
# do not remove COPYING -- needed at runtime
%doc AUTHORS COPYING CONTRIBUTORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/gazpacho
%{py_sitescriptdir}/gazpacho
%{_desktopdir}/*.desktop
%{_examplesdir}/%{name}-%{version}
%{_pixmapsdir}/*.png
