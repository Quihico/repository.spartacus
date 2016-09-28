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
import dixie, shutil, extract
import threading
import requests

AddonID          =  'script.trtv'
ADDON            =  xbmcaddon.Addon(id=AddonID)
SFADDON          =  xbmcaddon.Addon(id='plugin.program.super.favourites')
USERDATA         =  xbmc.translatePath(os.path.join('special://profile'))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath('special://home/addons')
datapath         =  dixie.PROFILE
resources        =  dixie.RESOURCES
cookies          =  os.path.join(datapath,   'cookies')       
chanpath         =  os.path.join(datapath,   'channels')
extras           =  os.path.join(datapath,   'extras')
inprogress       =  os.path.join(datapath,   'xml_scan_in_progress')
logopack_none    =  os.path.join(extras,     'logos',   'None')
logopack_colour  =  os.path.join(extras,     'logos',   'Colour Logo Pack')
skin_path        =  os.path.join(extras,     'skins')
update_skin      =  os.path.join(skin_path,  'update_skin')
skin_zip         =  os.path.join(skin_path,  'skins.zip')
channel_xml      =  os.path.join(resources,  'chan.xml')
addremove_file   =  os.path.join(resources,  '-_ADD_OR_REMOVE_CHANNELS')
addremove        =  os.path.join(chanpath,   '-_ADD_OR_REMOVE_CHANNELS')
addremove_png    =  os.path.join(resources,  'add_remove.png')
addremove_dst    =  os.path.join(logopack_colour,   '-_ADD_OR_REMOVE_CHANNELS.png')
xmlmaster        =  os.path.join(resources,  'chan.xml')
catsmaster       =  os.path.join(resources,  'cats.xml')
chanxml          =  os.path.join(datapath,   'chan.xml')
catsxml          =  os.path.join(datapath,   'cats.xml')
updateicon       =  os.path.join(ADDONS,AddonID,'resources','update.png')
metalliq_ini_d   =  os.path.join(ADDONS,AddonID,'resources','metalliq.ini')
metalliq_ini_l   =  os.path.join(datapath,'ini','metalliq.ini')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()

showSFchannels   =  ADDON.getSetting('showSFchannels')
syncartwork      =  ADDON.getSetting('syncartwork')
sf_channels      =  ADDON.getSetting('SF_CHANNELS')
add_sf_items     =  ADDON.getSetting('add_sf_items')
sf_metalliq      =  ADDON.getSetting('SF_METALLIQ')
firstrun         =  ADDON.getSetting('FIRSTRUN')
sf_folder        =  SFADDON.getSetting('FOLDER')

cont             =  1
#--------------------------------------------------------------------
# Run the update command to make sure all files are downloaded
def Check_Updates():
    try:
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    except:
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
#--------------------------------------------------------------------
# Remove any channels that aren't in the SF folder
def Clean_SF_Chans():
    current_list = ['-_ADD_OR_REMOVE_CHANNELS']

# Grab a list of all valid SF folders
    for item in os.listdir(sf_channels):
        if os.path.exists(os.path.join(sf_channels,item,'favourites.xml')):
            current_list.append(item)
    
# Remove any channels from the channel path which aren't in the SF list
    for item in os.listdir(chanpath):
        if not item in current_list:
            try:
                os.remove(os.path.join(chanpath, item))
            except:
                dixie.log('### Failed to remove %s' % item)

# TODO - Pull details of all channels in the database and all then to the exceptions list
# Otherwise custom channel ordering will keep getting reset

#--------------------------------------------------------------------
# Grab all the channels and check for artwork
def Check_Artwork():
    channel_list = []

# Remove the country code from filename and add to list
    for item in os.listdir(chanpath):
        if item.endswith(')') and item[-4] == '(':
            country = item[-5:]
            item    = item.replace(country,'').replace('_PLUS1','')
        logo_path   = os.path.join(logopack_colour, item+'.png')
        if not os.path.exists(logo_path):
            channel_list.append(item+'.png')

    dixie.log('MISSING ART ARRAY: %s' % channel_list)

# If the logo doesn't exist locally check online to see if it exists there and download
    if len(channel_list) > 0:
        for_progress = []
        counter      = 0
        dp.create("GRABBING NEW ARTWORK","Scanning...",'', 'Please Wait')

        for item in channel_list:
     
# Update the dialog process with percentage bar
            counter += 1
            for_progress.append(counter)
            progress = len(for_progress) / float(len(channel_list)) * 100
            dixie.log('### Progress Percent: %s' % progress)
            dp.update(int(progress),"Checking",'[COLOR yellow]%s[/COLOR]'%item.replace('.png',''), 'Please Wait')

            ret = requests.head('http://tlbb.me/useful_links/logos/Colour Logo Pack/%s' % item)
            dixie.log('## Item: %s   Code: %s' % (item, ret.status_code))
            if ret.status_code == 200:
                response = requests.get('http://tlbb.me/useful_links/logos/Colour Logo Pack/%s' % item)
                with open(os.path.join(logopack_colour, item), 'wb') as f:
                    f.write(response.content)

        dp.close()
#--------------------------------------------------------------------
# Extract skin zip and write size to file
def Extract_Skins():
    extract.all(skin_zip, skin_path)
    skinsize  = os.path.getsize(skin_zip)
    writefile = open(update_skin, 'w')
    writefile.write(str(skinsize))
    writefile.close()
#-----------------------------------------------------------------------------
# Set a setting via json or one of the skin commands
def Set_Setting(setting, value = ''):
    try:
        setting = '"%s"' % setting
        value = '"%s"' % value
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
        response = xbmc.executeJSONRPC(query)
        if debug == 'true':
            xbmc.log(query)
        dixie.log('### Set [%s, %s]' % (setting, value))
        dixie.log('### RETURN %s' % response)

        if 'error' in str(response):
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
            response = xbmc.executeJSONRPC(query)
            if debug == 'true':
                dixie.log(query)
            dixie.log('### Set [%s, %s]' % (setting, value))
            dixie.log('### RETURN %s' % response)

    except:
        dixie.log('### Failed to set [%s, %s]' % (setting, value))
#--------------------------------------------------------------------
if not os.path.exists(os.path.join(ADDON_DATA,AddonID)):
    dixie.log("New addon_data folder created")
    os.makedirs(os.path.join(ADDON_DATA,AddonID))
else:
    dixie.log("addon_data already exists")

# Create the Colour logopack
if not os.path.exists(logopack_colour):
    os.makedirs(logopack_colour)

if not os.path.exists(chanpath):
    os.makedirs(chanpath)

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
if not os.path.exists(metalliq_path) and sf_metalliq == 'true':
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

if not os.path.exists(chanxml):
    dixie.log("Copying chan.xml to addon_data")
    shutil.copyfile(xmlmaster, chanxml)
else:
    dixie.log("Chan.xml file exists in addon_data")

sf_channels = xbmc.translatePath(default_path)
xbmc.log('SF CHANS PATH: %s' % sf_channels)

# If this is first run extract the skin zip
if os.path.exists(skin_zip):
    if not os.path.exists(update_skin):
        xbmc.log('### First run extraction of skins')
        Extract_Skins()
    else:
        skinsize     = os.path.getsize(skin_zip)
        readfile     = open(update_skin, 'r')
        current_size = readfile.read()
        readfile.close()
        if current_size != str(skinsize):
            xbmc.log('### New skin file, extracting')
            Extract_Skins()
else:
    dialog.ok('MISSING FILES', 'There are files missing on your system, click OK to check for updates then try opening Live TV again.')
    Check_Updates()
    cont = 0

if cont:
    if not os.path.exists(addremove):
        shutil.copyfile(addremove_file, addremove)

    if not os.path.exists(addremove_dst):
        shutil.copyfile(addremove_png, addremove_dst)

    if showSFchannels == 'true':
        Clean_SF_Chans()

    xbmc.executebuiltin("XBMC.Notification(PLEASE WAIT,Channels are currently updating,5000,%s)" % (updateicon))
    xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/createDB.py,normal)')
    xbmc.sleep(2000)
    xml_alive = os.path.exists(inprogress)

    while xml_alive:
       xbmc.sleep(500)
       xml_alive = os.path.exists(inprogress)

    if syncartwork == 'true':
        artwork_thread = threading.Thread(target = Check_Artwork)
        artwork_thread.start()
        artwork_alive  = artwork_thread.isAlive()

        while artwork_alive:
            xbmc.sleep(500)
            artwork_alive  = artwork_thread.isAlive()

    if sf_metalliq == 'true':
        if not os.path.exists(metalliq_ini_l):
            shutil.copyfile(metalliq_ini_d, metalliq_ini_l)
        xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/createFolders.py, silent)')
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/settings/players/tvportal)')
    else:
        try:
            os.remove(metalliq_ini_l)
        except:
            xbmc.log('### No metalliq ini file to remove')

    xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/launch.py)')

