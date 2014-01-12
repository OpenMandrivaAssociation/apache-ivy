%{?_javapackages_macros:%_javapackages_macros}
Name:           apache-ivy
Version:        2.3.0
Release:        3.1%{?dist}
Summary:        Java-based dependency manager


License:        ASL 2.0
URL:            http://ant.apache.org/ivy/
Source0:        http://www.apache.org/dist/ant/ivy/%{version}/%{name}-%{version}-src.tar.gz
BuildArch:      noarch

Provides:       ivy = %{version}-%{release}

BuildRequires:  ant
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jsch
BuildRequires:  jakarta-oro
BuildRequires:  java-devel >= 1.5
BuildRequires:  jpackage-utils
Requires:       jpackage-utils
Requires:       jakarta-oro
Requires:       jsch
Requires:       ant
Requires:       jakarta-commons-httpclient

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%package javadoc
Summary:        API Documentation for ivy

Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
JavaDoc documentation for %{name}

%prep
%setup -q

# Fix messed-up encodings
for F in RELEASE_NOTES README LICENSE NOTICE CHANGES.txt
do
        sed 's/\r//' $F |iconv -f iso8859-1 -t utf8 >$F.utf8
        touch -r $F $F.utf8
        mv $F.utf8 $F
done
rm -fr src/java/org/apache/ivy/plugins/signer/bouncycastle

%build
# Remove prebuilt documentation
rm -rf doc build/doc

# How to properly disable a plugin?
# we disable vfs plugin since commons-vfs is not available
rm -rf src/java/org/apache/ivy/plugins/repository/vfs \
        src/java/org/apache/ivy/plugins/resolver/VfsResolver.java
sed '/vfs.*=.*org.apache.ivy.plugins.resolver.VfsResolver/d' -i \
        src/java/org/apache/ivy/core/settings/typedef.properties

# Craft class path
mkdir -p lib
build-jar-repository lib ant jakarta-commons-httpclient jakarta-oro jsch 

# Build
ant /localivy /offline -Dtarget.ivy.bundle.version=%{version} -Dtarget.ivy.bundle.version.qualifier= -Dtarget.ivy.version=%{version} jar javadoc


%install
# Code
install -d $RPM_BUILD_ROOT%{_javadir}
install -p -m644 build/artifact/jars/ivy.jar $RPM_BUILD_ROOT%{_javadir}/ivy.jar

# Maven depmap
%add_maven_depmap org.apache.ivy:ivy:%{version} ivy.jar

# API Documentation
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/doc/reports/api/. $RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ivy" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%{_javadir}/*
%{_sysconfdir}/ant.d/%{name}
%doc RELEASE_NOTES CHANGES.txt LICENSE NOTICE README

%files javadoc
%{_javadocdir}/*
%doc LICENSE

%changelog
* Fri Nov  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Add Maven depmap

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Alexander Kurtakov <akurtako@redhat.com> 2.3.0-1
- Update to latest upstream.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-5
- Fix osgi metadata.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-2
- Fix ant integration.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to 2.2.0.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- Initial Fedora packaging
