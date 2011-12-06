%global tarball xf86-input-evdev
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global policydir %{_datadir}/hal/fdi/policy/10osvendor

Summary:    Xorg X11 evdev input driver
Name:       xorg-x11-drv-evdev
Version:    2.3.2
Release:    8%{?dist}
URL:        http://www.x.org
License:    MIT
Group:      User Interface/X Hardware Support
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   10-x11-lid.fdi

# 562687 - Option "ReopenAttempts" with a value of 0 leads to infinite
# reopen attempts
Patch001:   evdev-2.3.2-reopen-infinity.patch
# 583878 - evdev sends motion events for wheel events
Patch002:   evdev-2.3.2-wheel-motion-events.patch
# 584234 - evdev leaks memory
Patch003:   evdev-2.3.2-memory-leaks.patch
# 609333 - out-of-bounds memory access for valuators > MAX_VALUATORS
Patch004:   evdev-2.3.2-max-valuators-oob.patch
# 618845 - Laptop monitor is activated when notebook lid is closed
Patch005:   evdev-2.3.2-lid.patch

ExcludeArch: s390 s390x

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-sdk >= 1.5.99.1
BuildRequires:  xorg-x11-util-macros >= 1.3.0

Requires:  xorg-x11-server-Xorg >= 1.5.99.1
Requires:  xkeyboard-config >= 1.4-1

%description 
X.Org X11 evdev input driver.

%prep
%setup -q -n %{tarball}-%{version}

%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch004 -p1
%patch005 -p1

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{policydir}
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{policydir}

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/evdev_drv.so
%{_mandir}/man4/evdev.4*
%{policydir}/10-x11-lid.fdi


%package devel
Summary:    Xorg X11 evdev input driver development package.
Group:	    Development/Libraries
%description devel
X.Org X11 evdev input driver development files.

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/xorg-evdev.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/evdev-properties.h


%changelog
* Fri Jul 30 2010 Adam Jackson <ajax@redhat.com> 2.3.2-8
- 10-x11-lid.fdi: Add so switch devices appear to have an X driver in hal.
- evdev-2.3.2-lid.patch: Scan for lid switch devices, translate events on
  them into RANDR rescans so the desktop will pick them up. (#618845)

* Wed Jun 30 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-7
- evdev-2.3.2-max-valuators-oob.patch: avoid OOB access when a device has
  more than MAX_VALUATORS axes (#609333)

* Wed Apr 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-6
- evdev-2.3.3-memory-leaks.patch: free up memory after using options.
  (#584234)

* Tue Apr 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-5
- evdev-2.3.2-wheel-motion-events.patch: don't send motion events for wheel
  events (#583878)

* Mon Feb 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-4
- evdev-2.3.2-reopen-infinity.patch: Don't reopen into infinity if
  ReopenAttempts is 0. (#562687)

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-3
- Use global instead of define as per Packaging Guidelines
- Remove tab/spaces mixup.

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-2
- remove references to git builds and matching sources aux files.
- remove libxkbfile-devel BuildRequires
- actually disable autoreconf this time.

* Fri Dec 11 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.2-1
- evdev 2.3.2
- disable autoreconf, we're not building from git anymore.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.1-2
- 0001-Fix-drag-lock-property-handler-for-multiple-draglock.patch
  drop, merged upstream.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.1-1
- evdev 2.3.1

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-4
- BuildRequires macros, not Requires.

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-3
- Require xorg-x11-util-macros 1.3.0

* Mon Nov 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-2
- 0001-Fix-drag-lock-property-handler-for-multiple-draglock.patch
  Fix property handler indexing for multiple draglock buttons
  (#524428).

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.3.0-1
- evdev 2.3.0

* Thu Oct 08 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99.2-1
- evdev 2.2.99.2

* Wed Sep 23 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-8.20090923
- Update to today's git master (fixes wheel emulation)

* Wed Sep 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-7.20090909
- Update to today's git master

* Fri Aug 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-6.20090814
- Update to today's git master

* Thu Jul 30 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-5.20090730
- Update to today's git master

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.99-4.20090629.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 2.2.99-3.20090629.1
- ABI bump

* Thu Jul 09 2009 Adam Jackson <ajax@redhat.com> 2.2.99-3.20090629
- Fix EVR inversion, 1.20090629 < 2.20090619

* Mon Jun 29 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090629
- Update to today's git master
- Add commitid file with git's sha1.

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-2.20090619
- rebuild for server ABI 7

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090619
- Update to today's git master

* Thu May 21 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.99-1.20090521
- Update to today's git master

* Thu May 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.2-1
- evdev 2.2.2

* Mon Apr 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-2
- evdev-2.2.1-read-deadlock.patch: handle read errors on len <= 0 (#494245)

* Tue Mar 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.1-1
- evdev 2.2.1 

* Mon Mar 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.2.0-1
- evdev 2.2.0

* Mon Mar 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.1-1
- evdev 2.2 snapshot 1

* Thu Feb 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99.2.20090226
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.99-1.20090219
- Update to today's git master.

* Thu Feb 19 2009 Peter Hutterer <peter.hutterer@redhat.com>
- purge obsolete patches.

* Tue Feb 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.3-1
- evdev 2.1.3

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.2-1
- evdev 2.1.2

* Tue Jan 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.1.1-1
- evdev 2.1.1
- update Requires to 1.5.99.1 to make sure the ABI is right.

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 2.1.0-3
- Rebuild again - latest tag wasn't in buildroot

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-2
- Rebuild for server 1.6.

* Wed Nov 19 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-1
- evdev 2.1.0

* Tue Nov 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.3-1
- evdev 2.0.99.3 (evdev 2.1 RC 3)

* Fri Oct 24 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.2-1
- evdev 2.0.99.2 (evdev 2.1 RC 2)

* Fri Oct 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99.1-1
- evdev 2.0.99.1 (evdev 2.1 RC 1)
- Upstream change now requires libxkbfile-devel to build.

* Mon Oct 13 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.99-1
- Today's git snapshot.
- Require xkeyboard-config 1.4 and higher for evdev ruleset.
- Provide devel subpackage for evdev header files.

* Fri Oct 3 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.6-1
- update to 2.0.6
- remove patches merged upstream.

* Fri Sep 12 2008 Adam Jackson <ajax@redhat.com> 2.0.4-3
- evdev-2.0.4-reopen-device.patch: When arming the reopen timer, stash it in
  the driver private, and explicitly cancel it if the server decides to
  close the device for real.
- evdev-2.0.4-cache-info.patch: Rebase to account for same.

* Thu Aug 28 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-2
- evdev-2.0.4-reopen-device.patch: try to reopen devices if a read error
  occurs on the fd.
- evdev-2.0.4-cache-info.patch: cache device info to ensure reopened device
  isn't different to previous one.

* Mon Aug 25 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.4-1
- evdev 2.0.4

* Fri Aug 1 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.3-1
- evdev 2.0.3

* Mon Jul 21 2008 Peter Hutterer <peter.hutterer@redhat.com> 2.0.2-1
- evdev 2.0.2

* Fri Mar 14 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.5
- Today's snapshot.  Maps REL_DIAL to REL_HWHEEL.

* Wed Mar 12 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.4
- Today's snapshot.  Fixes mouse button repeat bug, and therefore Apple
  Mighty Mice are usable.  Props to jkeating for the hardware.

* Tue Mar 11 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.3
- Today's snapshot.  Fixes right/middle button swap hilarity.

* Mon Mar 10 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.2
- Updated snapshot, minor bug fixes.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 1.99.1-0.1
- evdev 2.0 git snapshot

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.0-2
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Adam Jackson <ajax@redhat.com> 1.2.0-1
- xf86-input-evdev 1.2.0

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.2-5
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.2-4
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.2-3
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-2
- Build on ppc64

* Mon Jun 05 2006 Adam Jackson <ajackson@redhat.com> 1.1.2-1
- Update to 1.1.2 + CVS fixes.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-3
- Work around header pollution on ia64, re-add to arch list.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2
- Disable on ia64 until build issues are sorted.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-evdev to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-evdev to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-evdev to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-evdev to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for evdev input driver generated automatically
  by my xorg-driverspecgen script.
