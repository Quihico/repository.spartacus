#
#      Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#



import xbmcaddon
import xbmc
import xbmcgui
import os

import dixie

try:
	openSettings = sys.argv[1]
except:
	openSettings = 'normal'

dixie.ADDON.openSettings()

if openSettings == 'normal':
	xbmcgui.Window(10000).setProperty('OTT_KODI', 'false')

	name   =  dixie.TITLE
	script =  os.path.join(dixie.HOME, 'launch.py')
	args   =  ''
	cmd    = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 0)

	xbmc.executebuiltin('CancelAlarm(%s,True)' % name)        
	xbmc.executebuiltin(cmd)

