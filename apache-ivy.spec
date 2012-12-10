Name:           apache-ivy
Version:        2.1.0
Release:        4
Summary:        Java-based dependency manager

Group:          Development/Java
License:        ASL 2.0
URL:            http://ant.apache.org/ivy/
Source0:        http://www.apache.org/dist/ant/ivy/2.1.0/%{name}-%{version}-src.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

Provides:       ivy = %{version}-%{release}

BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  commons-httpclient
BuildRequires:  jsch
BuildRequires:  oro
BuildRequires:  java-devel >= 1.5
BuildRequires:  jpackage-utils
Requires:       jpackage-utils

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.


%package javadoc
Summary:        API Documentation for ivy
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

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
build-jar-repository lib ant ant/ant-nodeps commons-httpclient oro jsch

# Build
ant /localivy /offline jar javadoc


%install
rm -rf $RPM_BUILD_ROOT

# Code
install -d $RPM_BUILD_ROOT%{_javadir}
install -p -m644 build/artifact/jars/ivy.jar $RPM_BUILD_ROOT%{_javadir}/ivy-%{version}.jar
ln -sf ivy-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ivy.jar

# API Documentation
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp build/doc/reports/api/. $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc RELEASE_NOTES CHANGES.txt LICENSE NOTICE README


%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*




%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 2.1.0-4
+ Revision: 733821
- rebuild
- imported package apache-ivy

