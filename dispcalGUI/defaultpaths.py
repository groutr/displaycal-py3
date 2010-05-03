#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if sys.platform == "win32":
	try:
		from win32com.shell.shell import SHGetSpecialFolderPath
		from win32com.shell.shellcon import (CSIDL_APPDATA, 
											 CSIDL_COMMON_APPDATA, 
											 CSIDL_COMMON_STARTUP, 
											 CSIDL_PROGRAM_FILES_COMMON, 
											 CSIDL_STARTUP, CSIDL_SYSTEM)
	except ImportError:
		(CSIDL_APPDATA, CSIDL_COMMON_APPDATA, CSIDL_COMMON_STARTUP, 
		 CSIDL_PROGRAM_FILES_COMMON, CSIDL_STARTUP, CSIDL_SYSTEM) = (26, 35, 
																	 24, 43, 
																	 7, 37)
		def SHGetSpecialFolderPath(hwndOwner, nFolder):
			return {
				CSIDL_APPDATA: getenvu("APPDATA"),
				CSIDL_COMMON_APPDATA: None,
				CSIDL_COMMON_STARTUP: None,
				CSIDL_PROGRAM_FILES_COMMON: getenvu("CommonProgramFiles"),
				CSIDL_STARTUP: None,
				CSIDL_SYSTEM: getenvu("SystemRoot")
			}.get(nFolder)

from util_os import expanduseru, expandvarsu, getenvu

if sys.platform == "win32":
	appdata = SHGetSpecialFolderPath(0, CSIDL_APPDATA)
	commonappdata = SHGetSpecialFolderPath(0, CSIDL_COMMON_APPDATA)
	commonprogramfiles = SHGetSpecialFolderPath(0, CSIDL_PROGRAM_FILES_COMMON)
	try:
		autostart = SHGetSpecialFolderPath(0, CSIDL_COMMON_STARTUP)
		# Can fail under Vista and later if directory doesn't exist
	except Exception, exception:
		autostart = None
	try:
		autostart_home = SHGetSpecialFolderPath(0, CSIDL_STARTUP)
		# Can fail under Vista and later if directory doesn't exist
	except Exception, exception:
		autostart_home = None
	iccprofiles = [os.path.join(SHGetSpecialFolderPath(0, CSIDL_SYSTEM), 
								"spool", "drivers", "color")]
	iccprofiles_home = iccprofiles
elif sys.platform == "darwin":
	prefs = os.path.join(os.path.sep, "Library", "Preferences")
	prefs_home = os.path.join(expanduseru("~"), "Library", "Preferences")
	appsupport = os.path.join(os.path.sep, "Library", "Application Support")
	appsupport_home = os.path.join(expanduseru("~"), "Library", 
								   "Application Support")
	autostart = autostart_home = None
	iccprofiles = [os.path.join(os.path.sep, "Library", "ColorSync", 
								"Profiles"),
				   os.path.join(os.path.sep, "System", "Library", "ColorSync", 
								"Profiles")]
	iccprofiles_home = [os.path.join(expanduseru("~"), "Library", "ColorSync", 
									 "Profiles")]
else:
	xdg_config_home = getenvu("XDG_CONFIG_HOME",
								  os.path.join(expanduseru("~"), ".config"))
	xdg_config_dir_default = "/etc/xdg"
	xdg_config_dirs = getenvu("XDG_CONFIG_DIRS", 
							  xdg_config_dir_default).split(os.pathsep)
	if not xdg_config_dir_default in xdg_config_dirs:
		xdg_config_dirs += [xdg_config_dir_default]
	xdg_data_home_default = expandvarsu("$HOME/.local/share")
	xdg_data_home = getenvu("XDG_DATA_HOME", xdg_data_home_default)
	xdg_data_dirs_default = "/usr/local/share:/usr/share"
	xdg_data_dirs = getenvu("XDG_DATA_DIRS", 
							xdg_data_dirs_default).split(os.pathsep)
	for dir_ in xdg_data_dirs_default.split(os.pathsep):
		if not dir_ in xdg_data_dirs:
			xdg_data_dirs += [dir_]
	autostart = None
	for dir_ in xdg_config_dirs:
		if os.path.exists(dir_):
			autostart = os.path.join(dir_, "autostart")
			break
	autostart_home = os.path.join(xdg_config_home, "autostart")
	iccprofiles = []
	for dir_ in xdg_data_dirs:
		if os.path.exists(dir_):
			iccprofiles += [os.path.join(dir_, "color", "icc")]
	del dir_
	iccprofiles_home = [os.path.join(xdg_data_home, "color", "icc")]
	iccprofiles_display = os.path.join(iccprofiles[0], "devices", "display")
	iccprofiles_display_home = os.path.join(iccprofiles_home[0], "devices", 
											"display")
