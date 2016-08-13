# TotalRevolution TV EPG Launcher
# Copyright (C) 2016 Lee Randall (whufclee)
#

#  I M P O R T A N T :

#  You are free to use this code under the rules set out in the license below.
#  Should you wish to re-use this code please credit whufclee for the original work.
#  However under NO circumstances should you remove this license!

#  GPL:
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
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import xbmc, xbmcaddon, xbmcgui, os
import dixie, shutil
import threading

AddonID          =  'script.trtv'
ADDON            =  xbmcaddon.Addon(id=AddonID)
SFADDON          =  xbmcaddon.Addon(id='plugin.program.super.favourites')
USERDATA         =  xbmc.translatePath(os.path.join('special://profile'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath('special://home/addons')
showSFchannels   =  ADDON.getSetting('showSFchannels')
usenanchan       =  ADDON.getSetting('usenanchan')
usenancats       =  ADDON.getSetting('usenancats')
sf_channels      =  ADDON.getSetting('SF_CHANNELS')
showSFchannels   =  ADDON.getSetting('showSFchannels')
add_sf_items     =  ADDON.getSetting('add_sf_items')
sf_metalliq      =  ADDON.getSetting('SF_METALLIQ')
firstrun         =  ADDON.getSetting('FIRSTRUN')
sf_folder        =  SFADDON.getSetting('FOLDER')
updateicon   	 =  os.path.join(ADDONS,AddonID,'resources','update.png')
resources        =  dixie.RESOURCES
cookies          =  os.path.join(ADDON_DATA,AddonID,'cookies')       
datapath         =  dixie.PROFILE
extras           =  os.path.join(datapath,   'extras')
logopack_none    =  os.path.join(extras,'logos','None')
logopack_colour  =  os.path.join(extras,'logos','Colour Logo Pack')
channel_xml      =  os.path.join(resources,  'chan.xml')
xmlmaster        =  os.path.join(resources,  'chan.xml')
catsmaster       =  os.path.join(resources,  'cats.xml')
chanxml          =  os.path.join(datapath,   'chan.xml')
catsxml          =  os.path.join(datapath,   'cats.xml')
dialog           =  xbmcgui.Dialog()
cont             =  0
#########################################################################################
if not os.path.exists(os.path.join(ADDON_DATA,AddonID)):
    dixie.log("New addon_data folder created")
    os.makedirs(os.path.join(ADDON_DATA,AddonID))
else:
    dixie.log("addon_data already exists")

if not os.path.exists(logopack_none):
    os.makedirs(logopack_none)

if not os.path.exists(logopack_colour):
    os.makedirs(logopack_colour)

if not os.path.exists(chanxml) and usenanchan == 'true':
    dixie.log("Copying chan.xml to addon_data")
    shutil.copyfile(xmlmaster, chanxml)
else:
    dixie.log("Chan.xml file already exists in addon_data")

if firstrun == 'false':
 
 # If the settings in SF haven't been setup we do so now
    sf_folder = xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites')
    SFADDON.setSetting('FOLDER',sf_folder)
    SFADDON.setSetting('SHOWUNAVAIL','true')
    SFADDON.setSetting('SHOWNEW','false')
    SFADDON.setSetting('SHOWXBMC','false')
    SFADDON.setSetting('SHOWSEP','false')
    SFADDON.setSetting('ALPHA_SORT','true')
    root_SF_path = os.path.join(sf_folder,'Super Favourites')

    try:
        os.makedirs(sf_folder)
    except:
        pass

    try:
        os.makedirs(root_SF_path)
    except:
        pass

    default_path = os.path.join(root_SF_path, 'HOME_LIVE_TV')
    if not os.path.exists(default_path):
        try:
            os.makedirs(default_path)
        except:
            xbmc.log('### TRTV: Error creating SF folders')

    metalliq_path = os.path.join(default_path, '-metalliq')
    if not os.path.exists(metalliq_path):
        try:
            os.makedirs(metalliq_path)
        except:
            xbmc.log('### TRTV: Error creating MetalliQ folder')

    ADDON.setSetting('SF_CHANNELS', default_path)

if not os.path.exists(catsxml):
    dixie.log("Copying cats.xml to addon_data")
    shutil.copyfile(catsmaster, catsxml)
else:
    dixie.log("Cats.xml file exists in addon_data")


xbmc.executebuiltin("XBMC.Notification(PLEASE WAIT,Channels are currently updating,5000,%s)" % (updateicon))

update_thread = threading.Thread(target = xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)'))
xml_thread    = threading.Thread(target = xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/createDB.py,normal)'))

update_thread.start()
update_alive = update_thread.isAlive()

while update_alive:
   xbmc.sleep(500)
   update_alive = update_thread.isAlive()

xml_thread.start()
xml_alive = update_thread.isAlive()

while xml_alive:
   xbmc.sleep(500)
   xml_alive = xml_thread.isAlive()

xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/createFolders.py)')
xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/launch.py)')
xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/settings/players/tvportal)')
