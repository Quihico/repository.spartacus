#
#       Copyright (C) 2016 whufclee (Lee Randall)
#
#  This software is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License
#  You can find a copy of the license in the add-on folder

import binascii
import datetime
import hashlib
import os
import re
import shutil
import sys
import threading
import time
import urllib
import urllib2
import xbmcplugin
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import yt
import zipfile

from functions import Get_Params, Encrypt, Open_URL, Get_Mac, Create_Paths, Log_Check, Text_File, My_Mac

try:
    import json as simplejson 
except:
    import simplejson

ADDONID                    = 'script.openwindow'
ADDON                      = xbmcaddon.Addon(ADDONID)
ADDONID2                   = 'plugin.program.tbs'
try:
    ADDON2                 = xbmcaddon.Addon(ADDONID2)
    debug                  = ADDON2.getSetting('debug')
except:
    ADDON2                 = xbmcaddon.Addon(ADDONID)
    debug                  = 'false'
HOME                       = xbmc.translatePath('special://home')
PROFILE                    = xbmc.translatePath('special://profile')
CACHE                      = xbmc.translatePath('special://temp')
ADDONS                     = os.path.join(HOME,'addons')
PACKAGES                   = os.path.join(ADDONS,'packages')
ADDON_DATA                 = xbmc.translatePath('special://profile/addon_data')
ADDON_PATH                 = xbmcaddon.Addon(ADDONID).getAddonInfo("path")
LANGUAGE_PATH              = os.path.join(ADDON_PATH,'resources','language')
RUN_WIZARD                 = os.path.join(PACKAGES,'RUN_WIZARD')
INSTALL_COMPLETE           = os.path.join(PACKAGES,'INSTALL_COMPLETE')
PRE_WIZARD                 = os.path.join(PACKAGES,'PRE_WIZARD')
SPARTACUS                  = os.path.join(ADDONS,'repository.spartacus')
OPENWINDOW_DATA            = os.path.join(ADDON_DATA,ADDONID)
NON_REGISTERED             = os.path.join(OPENWINDOW_DATA,'unregistered')
INSTALL_FILE               = os.path.join(ADDONS,ADDONID,'default.py')
THUMBNAILS                 = os.path.join(HOME,'userdata','THUMBNAILS')
TARGET_ZIP                 = os.path.join(PACKAGES,'target.zip')
KEYWORD_ZIP                = os.path.join(PACKAGES,'keyword.zip')
TEMP_DL_TIME               = os.path.join(PACKAGES,'dltime')
XBMC_VERSION               = xbmc.getInfoLabel("System.BuildVersion")[:2]
YAHOO_WEATHER              = os.path.join(ADDONS,'weather.yahoo')
OPEN_WEATHER               = os.path.join(ADDONS,'weather.openweathermap.extended')
IP_ADDRESS                 = xbmc.getIPAddress()
DIALOG                     = xbmcgui.Dialog()
dp                         = xbmcgui.DialogProgress()
CURRENT_SKIN               = xbmc.getSkinDir()
REGISTRATION_FILE          = os.path.join(OPENWINDOW_DATA,'DO_NOT_DELETE')
OEM_ID                     = os.path.join(OPENWINDOW_DATA,'id')
KEYWORD_FILE               = os.path.join(OPENWINDOW_DATA,'keyword')

branding                   = xbmc.translatePath('special://home/media/branding/branding.png')
if not os.path.exists(branding):
    branding = os.path.join(ADDONS,ADDONID,'resources','images','branding.png')

STOP_COOKIE_CHECK          = 0
ACTION_HOME                = 7
ACTION_PREVIOUS_MENU       = 10
ACTION_SELECT_ITEM         = 7
runamount                  = 0
download_thread            = ''
extract_thread             = ''
updatescreen_thread        = ''
update_thread_full         = ''
skin_settings_thread       = ''
main_order                 = []

MENU_FILE                  = os.path.join(OPENWINDOW_DATA,'menus')
if not os.path.exists(MENU_FILE):
    MENU_FILE              = os.path.join(ADDONS,ADDONID,'resources','menus')
# Check the menu order set by admin panel
with open(MENU_FILE) as f:
    content = f.read().splitlines()

for line in content:
    order, function = line.split('|')
    main_order.append([order,function])

main_order.sort()
debug = 'true'
#-----------------------------------------------------------------------------
##############################################################################
######################## MAIN SKINNING/IMAGE CODE ############################
##############################################################################
#-----------------------------------------------------------------------------
class DialogDisclaimer( xbmcgui.WindowXMLDialog ):
    def onInit(self):
        self.ACTION = 0
            
    def onClick( self, controlID ):         
        if controlID==11:
            self.ACTION = 1
            self.close()
        elif controlID==10:
            self.ACTION = 0
            self.close()
        elif controlID==12:
            self.close()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.close()
#-----------------------------------------------------------------------------
def show(xmlfile,exec_file):
    if not os.path.exists(OEM_ID):
        ACTION = 0
        d = DialogDisclaimer(xmlfile,ADDON_PATH)
        d.doModal()    
        ACTION = d.ACTION    
        del d
        
        if ACTION:
            params = Get_Params()
            xbmc.log('params: %s' % params)
            url_return = Open_URL('http://tlbb.me/boxer/my_details.php?x=%s&y=%s' % (params, ACTION)).replace('\r','').replace('\n','').replace('\t','')
            xbmc.log('### mydetails orig: %s' % url_return)
            xbmc.log('### mydetails new: %s' % Encrypt('d', url_return))
            url_return = Encrypt('d', url_return)
            exec(url_return)            

        # xbmc.executebuiltin('RunScript(%s,%s)' % (exec_file,ACTION))
#-----------------------------------------------------------------------------
# Show the keyword install menu
def Select_Audio_Android():
    backpage    = Pages('back','Select_Audio_Android()')
    nextpage    = Pages('next','Select_Audio_Android()')
    mydisplay = MainMenu(
        header=30136,
        background='audio1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30137,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('StartAndroidActivity(,\"android.settings.SOUND_SETTINGS\")')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30138,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the keyword install menu
def Select_Keyword():
    backpage    = Pages('back','Select_Keyword()')
    nextpage    = Pages('next','Select_Keyword()')
    mydisplay = MainMenu(
        header=30023,
        background='keywords1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30024,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Keyword_Check()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30025,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the local content selection menu
def Select_Local_Content():
    backpage    = Pages('back','Select_Local_Content()')
    nextpage    = Pages('next','Select_Local_Content()')
    mydisplay = MainMenuThreeItems(
        header=30026,
        background='localcontent1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        optionbutton1=30027,
        optionbutton2=30028,
        optionbutton3=30029,
        option1function="Add_Music()",
        option2function="Add_Photos()",
        option3function="Add_Videos()",
        maintext=30030,
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the language selection screen
def Select_Language(status = False):
    global registered
    registered = status
    xbmc.log('Registered status: %s' % registered)
    try:
        nextpage    = Pages('next','Select_Language()')
        registered = status
        current    = xbmc.getInfoLabel('System.ProfileName')
        mydisplay  = MainMenu(
            header=30003,
            background='language1.png',
            backbutton='',
            nextbutton=30002,      
            backbuttonfunction='',
            nextbuttonfunction='self.close();'+nextpage,
            selectbutton=30004,
            toggleup='',
            toggledown='',
            selectbuttonfunction="Set_Language();self.close();xbmc.executebuiltin('LoadProfile(current)');xbmc.sleep(2000);xbmc.executebuiltin('StopScript(script.openwindow)');xbmc.executebuiltin('RunScript(script.openwindow)')",
            toggleupfunction='',
            toggledownfunction='',
            maintext=30005,
            noconnectionbutton='',
            noconnectionfunction=""
            )        
        mydisplay.doModal()
        del mydisplay
    except:
        xbmc.log('#### Set Language disabled by admin, loading: %s' % Pages('start'))
        exec(Pages('start'))
#-----------------------------------------------------------------------------
# Show the region select screen
def Select_Region():
    backpage    = Pages('back','Select_Region()')
    nextpage    = Pages('next','Select_Region()')
    mydisplay = MainMenuThreeItems(
        header=30006,
        background='region1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        optionbutton1=30008,
        optionbutton2=30007,
        optionbutton3=30009,
        option1function="Set_Timezone_Country()",
        option2function="Set_Region()",
        option3function="Set_Timezone()",
        maintext=30010,
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the resolution select screen
def Select_Resolution():
    backpage    = Pages('back','Select_Resolution()')
    nextpage    = Pages('next','Select_Resolution()')
    mydisplay = MainMenu(
        header=30011,
        background='resolution1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30011,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Resolution()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30012,
        noconnectionbutton='',
        noconnectionfunction=""
        )
    mydisplay .doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the skin selection screen
def Select_Skin():
    backpage    = Pages('back','Select_Skin()')
    nextpage    = Pages('next','Select_Skin()')
    speedtest=0
    mydisplay = MainMenu(
        header=30020,
        background='skins1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30021,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Set_Skin()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30022,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the third party enable/disable menu
def Select_Third_Party():
    backpage    = Pages('back','Select_Third_Party()')
    nextpage    = Pages('next','Select_Third_Party()')
    mydisplay = MainMenu(
        header=30091,   
        background='thirdparty.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30089,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Third_Party_Check()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30087,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the third party enable/disable menu
def Select_Timezone_Android():
    backpage    = Pages('back','Select_Timezone_Android()')
    nextpage    = Pages('next','Select_Timezone_Android()')
    mydisplay = MainMenu(
        header=30006,   
        background='region1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30009,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('StartAndroidActivity(,\"android.settings.DATE_SETTINGS\")')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30010,
        noconnectionbutton=30019,
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the weather selection menu
def Select_Weather():
    backpage    = Pages('back','Select_Weather()')
    nextpage    = Pages('next','Select_Weather()')
    mydisplay = MainMenu(
        header=30016,
        background='weather1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30017,
        toggleup='',
        toggledown='',
        selectbuttonfunction="Weather_Info()",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30018,
        noconnectionbutton=30019,
        noconnectionfunction="xbmc.executebuiltin('ActivateWindow(home)');xbmc.executebuiltin('RunAddon(service.openelec.settings)');xbmc.executebuiltin('RunAddon(script.openwindow)')"
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the screen calibration menu
def Select_Zoom():
    backpage    = Pages('back','Select_Zoom()')
    nextpage    = Pages('next','Select_Zoom()')
    mydisplay = MainMenu(
        header=30013,
        background='zoom1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        selectbutton=30014,
        toggleup='',
        toggledown='',
        selectbuttonfunction="xbmc.executebuiltin('ActivateWindow(screencalibration)')",
        toggleupfunction='',
        toggledownfunction='',
        maintext=30015,
        noconnectionbutton='',
        noconnectionfunction=""
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Show the region select screen
def Select_Zoom_Android():
    backpage    = Pages('back','Select_Zoom_Android()')
    nextpage    = Pages('next','Select_Zoom_Android()')
    mydisplay = MainMenuThreeItems(
        header=30013,
        background='zoom1.png',
        backbutton=30001,
        nextbutton=30002,
        backbuttonfunction='self.close();'+backpage,
        nextbuttonfunction='self.close();'+nextpage,
        optionbutton1=30011,
        optionbutton2=30134,
        optionbutton3=30135,
        option1function="os.system('am start --user 0 -n com.giec.settings/.ScreenSettings')",
        option2function="os.system('am start --user 0 -n com.giec.settings/.ScreenScaleSettings')",
        option3function="xbmc.executebuiltin('ActivateWindow(screencalibration)')",
        maintext=30139,
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
# Not on system, get user to register at www.totalrevolution.tv
def Enter_Licence():
    DIALOG.ok('NOT REGISTERED', 'No valid licence has been found on this unit for the TotalRevolution software you\'re attempting to run.', '', 'Please contact the vendor for further support.')
#-----------------------------------------------------------------------------
##############################################################################
######################## MAIN SKINNING/IMAGE CODE ############################
##############################################################################
#-----------------------------------------------------------------------------
# Main update screen
class Image_Screen(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=kwargs['header']
    self.background=kwargs['background']
    self.icon=kwargs['icon']
    self.maintext=kwargs['maintext']

    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images','whitebg.jpg')))
    self.updateimage = xbmcgui.ControlImage(200,230,250,250, os.path.join(ADDON_PATH,'resources','images',self.icon))
    self.addControl(self.updateimage)   
    self.updateimage.setAnimations([('conditional','effect=rotate start=0 end=360 center=auto time=3000 loop=true condition=true',)])


## Attemted to get the download progress working but can't get it to update on screen. The property in win 10000 IS updating, just not showing on screen
#    self.strDownloading = xbmcgui.ControlTextBox(270, 330, 200, 200, 'font14','0xFF000000')
#    self.strPercentage = xbmcgui.ControlTextBox(320, 270, 200, 200, 'font14','0xFF000000')
#    self.addControl(self.strPercentage)
#    self.addControl(self.strDownloading)
#    self.percent = xbmcgui.Window(10000).getProperty('percent')
#    self.strDownloading.setText('Downloaded')
#    self.strPercentage.setText(self.percent)

# Add description text
    self.strDescription = xbmcgui.ControlTextBox(570, 250, 600, 300, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU or action == ACTION_HOME:
      xbmc.log("ESC and HOME Disabled")
#-----------------------------------------------------------------------------
# Main menu GUI page        
class MainMenu(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=ADDON.getLocalizedString(kwargs['header'])
    self.background=kwargs['background']
    
    if kwargs['backbutton'] != '':
        self.backbutton = ADDON.getLocalizedString(kwargs['backbutton'])
    else:
        self.backbutton = ''
    if kwargs['nextbutton'] != '':
        self.nextbutton = ADDON.getLocalizedString(kwargs['nextbutton'])
    else:
        self.nextbutton = ''

    self.backbuttonfunction = kwargs['backbuttonfunction']
    self.nextbuttonfunction = kwargs['nextbuttonfunction']

    if self.backbuttonfunction.endswith('none'):
        self.backbutton = ''

    if kwargs['selectbutton'] != '':
        self.selectbutton=ADDON.getLocalizedString(kwargs['selectbutton'])
    else:
        self.selectbutton = ''
    self.toggleup = kwargs['toggleup']
    self.toggledown = kwargs['toggledown']
    self.selectbuttonfunction = kwargs['selectbuttonfunction']
    self.toggleupfunction = kwargs['toggleupfunction']
    self.toggledownfunction = kwargs['toggledownfunction']
    self.maintext = ADDON.getLocalizedString(kwargs['maintext'])

    if kwargs['noconnectionbutton'] != '':
        self.noconnectionbutton = ADDON.getLocalizedString(kwargs['noconnectionbutton'])
    else:
        self.noconnectionbutton = ''

    self.noconnectionfunction = kwargs['noconnectionfunction']
# Add background images
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images','smoke_background.jpg')))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH,'resources','images',self.background)))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding))

# Add next button
    self.button1 = xbmcgui.ControlButton(910, 600, 225, 35, self.nextbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH,'resources','images','button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.addControl(self.button1)

# Add back button
    if self.backbutton != '':
        self.button2 = xbmcgui.ControlButton(400, 600, 225, 35, self.backbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button2)

# Add buttons - if toggle buttons blank then just use one button
    if self.toggleup == '':
        if self.noconnectionbutton == '':
            self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        else:
            if IP_ADDRESS != '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.selectbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
            elif IP_ADDRESS == '0':
                self.button0 = xbmcgui.ControlButton(910, 480, 225, 35, self.noconnectionbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button0)
        self.button0.controlDown(self.button1)
        self.button0.controlRight(self.button1)
        self.button0.controlUp(self.button1)
        if self.backbutton != '':
            self.button0.controlLeft(self.button2)
    else:
        self.toggleupbutton = xbmcgui.ControlButton(1000, 480, 35, 35, '', focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.toggledownbutton = xbmcgui.ControlButton(1000, 500, 35, 35, '', focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.toggleupbutton)
        self.addControl(self.toggledownbutton)
        self.strToggleUp = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font13','0xFFFFFFFF')
        self.strToggleDown = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font13','0xFFFFFFFF')
        self.addControl(self.strToggleUp)
        self.addControl(self.strToggleDown)
        self.strToggleUp.setLabel(self.toggleup)
        self.strToggleDown.setLabel(self.toggledown)
        self.toggleupbutton.controlDown(self.toggledownbutton)
        if self.backbutton != '':
            self.toggleupbutton.controlLeft(self.button2)
            self.toggledownbutton.controlLeft(self.button2)
        self.toggledownbutton.controlUp(self.toggleupbutton)
        self.toggledownbutton.controlDown(self.button1)
        
    if self.toggleup=='':
        self.setFocus(self.button1)
    else:
        self.setFocus(self.toggleupbutton)

    if self.backbutton != '':
        self.button1.controlLeft(self.button2)
        self.button1.controlRight(self.button2)
        self.button2.controlRight(self.button1)
        self.button2.controlLeft(self.button1)
    if self.toggleup=='':
        self.button1.controlUp(self.button0)
        if self.backbutton != '':
            self.button2.controlUp(self.button0)
    else:
        self.button1.controlUp(self.toggledownbutton)
        if self.backbutton != '':
            self.button2.controlUp(self.toggledownbutton)        

# Add header text
    self.strHeader = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font14','0xFFFFFFFF')
    self.addControl(self.strHeader)
    self.strHeader.setLabel(self.header)
# Add internet warning text (only visible if not connected)
    if IP_ADDRESS == '0':
        self.strWarning = xbmcgui.ControlTextBox(830, 300, 300, 200, 'font13','0xFFFF0000')
        self.addControl(self.strWarning)
        self.strWarning.setText('No internet connection.[CR]To be able to get the most out of this device and set options like this you must be connected to the web. Please insert your ethernet cable or setup your Wi-Fi.')
# Add description text
    self.strDescription = xbmcgui.ControlTextBox(830, 130, 300, 350, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)

    xbmc.log(self.header)
    xbmc.log(self.nextbutton)
    xbmc.log(self.nextbuttonfunction)
    xbmc.log(self.backbutton)
    xbmc.log(self.backbuttonfunction)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU and self.selectbutton == 'Register':
      self.close()
 
  def onControl(self, control):
    if control == self.button0:
        if IP_ADDRESS != '0' or self.noconnectionbutton=='':
            exec self.selectbuttonfunction
        else:
            exec self.noconnectionfunction
    if control == self.button1:
      exec self.nextbuttonfunction
    if not self.backbuttonfunction.endswith('none') and not self.backbutton == '':
        if control == self.button2:
          exec self.backbuttonfunction

  def message(self, message):
    DIALOG.ok(" My message title", message) 
#-----------------------------------------------------------------------------
class MainMenuThreeItems(xbmcgui.Window):
  def __init__(self,*args,**kwargs):
    self.header=ADDON.getLocalizedString(kwargs['header'])
    self.background=kwargs['background']
    
    if kwargs['backbutton']!='':
        self.backbutton=ADDON.getLocalizedString(kwargs['backbutton'])
    else:
        self.backbutton=''
    if kwargs['nextbutton']!='':
        self.nextbutton=ADDON.getLocalizedString(kwargs['nextbutton'])
    else:
        self.nextbutton=''
    
    self.backbuttonfunction=kwargs['backbuttonfunction']
    self.nextbuttonfunction=kwargs['nextbuttonfunction']

    if self.backbuttonfunction.endswith('none'):
        self.backbutton = ''

    if kwargs['optionbutton1']!='':
        self.optionbutton1=ADDON.getLocalizedString(kwargs['optionbutton1'])
    else:
        self.optionbutton1=''
    if kwargs['optionbutton2']!='':
        self.optionbutton2=ADDON.getLocalizedString(kwargs['optionbutton2'])
    else:
        self.optionbutton2=''
    if kwargs['optionbutton3']!='':
       self.optionbutton3=ADDON.getLocalizedString(kwargs['optionbutton3'])
    else:
        self.optionbutton3=''

    self.maintext=ADDON.getLocalizedString(kwargs['maintext'])
    self.option1function=kwargs['option1function']
    self.option2function=kwargs['option2function']
    self.option3function=kwargs['option3function']
# Add background images
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH, 'resources', 'images', 'smoke_background.jpg')))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, os.path.join(ADDON_PATH, 'resources', 'images', self.background)))
    self.addControl(xbmcgui.ControlImage(0,0,1280,720, branding))
    if self.nextbutton != '':
        self.button1 = xbmcgui.ControlButton(910, 600, 225, 35, self.nextbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button1)
    if self.backbutton != '':
        self.button2 = xbmcgui.ControlButton(400, 600, 225, 35, self.backbutton,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
        self.addControl(self.button2)

    self.button0 = xbmcgui.ControlButton(910, 400, 225, 35, self.optionbutton1,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.button3 = xbmcgui.ControlButton(910, 440, 225, 35, self.optionbutton2,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.button4 = xbmcgui.ControlButton(910, 480, 225, 35, self.optionbutton3,font='font13',alignment=2,focusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'button-focus.png'), noFocusTexture = os.path.join(ADDON_PATH, 'resources', 'images', 'non-focus.jpg'))
    self.addControl(self.button0)
    self.addControl(self.button3)
    self.addControl(self.button4)
    self.button0.controlDown(self.button3)
    self.button3.controlDown(self.button4)
    self.setFocus(self.button1)
    self.button3.controlUp(self.button0)
    self.button4.controlUp(self.button3)
    if self.nextbutton != '':
        self.button0.controlUp(self.button1)
        self.button3.controlRight(self.button1)
        self.button4.controlDown(self.button1)
        self.button0.controlRight(self.button1)
        self.button4.controlRight(self.button1)
        self.button1.controlLeft(self.button2)
        self.button1.controlRight(self.button2)
        self.button1.controlDown(self.button0)
        self.button1.controlUp(self.button4)
    if self.backbutton != '':
        self.button0.controlLeft(self.button2)
        self.button3.controlLeft(self.button2)
        self.button2.controlRight(self.button1)
        self.button2.controlLeft(self.button1)
        self.button2.controlUp(self.button4)
        self.button4.controlLeft(self.button2)

# Add header text
    self.strHeader = xbmcgui.ControlLabel(380, 50, 250, 20, '', 'font14','0xFFFFFFFF')
    self.addControl(self.strHeader)
    self.strHeader.setLabel(self.header)
# Add description text
    self.strDescription = xbmcgui.ControlTextBox(830, 130, 300, 300, 'font14','0xFF000000')
    self.addControl(self.strDescription)
    self.strDescription.setText(self.maintext)
    
  def onAction(self, action):
    if action == ACTION_PREVIOUS_MENU and 'Register' in self.header:
      self.close()

  def onControl(self, control):
    if control == self.button0:
      exec self.option1function
    if control == self.button1:
      exec self.nextbuttonfunction
    if not self.backbuttonfunction.endswith('none') and not self.backbutton == '':
        if control == self.button2:
          exec self.backbuttonfunction
    if control == self.button3:
      exec self.option2function
    if control == self.button4:
      exec self.option3function
#-----------------------------------------------------------------------------
##############################################################################
########################### ALL OTHER FUNCTIONS ##############################
##############################################################################
#-----------------------------------------------------------------------------
def Add_Music():
    xbmc.executebuiltin('ActivateWindow(Music,Files,return)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
def Add_Photos():
    xbmc.executebuiltin('ActivateWindow(Pictures,Files,return)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
def Add_Videos():
    xbmc.executebuiltin('ActivateWindow(Videos,sources://video/)')
    xbmc.executebuiltin('Action(PageDown)')
    xbmc.executebuiltin('Action(Select)')
#-----------------------------------------------------------------------------
# Check to see if it's time to re-check activation
def Check_Cookie():
    global runamount
    checkurl = 0

    Update_Cookie(Get_Mac('eth'))

# If the tbs addon isn't installed we can assume this unit hasn't been setup so they need to register
    if not os.path.exists(os.path.join(ADDONS, ADDONID2)):
        dolog('### TBS NOT INSTALLED')
        Check_Status('1')
    
# Otherwise check if the cookie exists
    elif os.path.exists(REGISTRATION_FILE):
        dolog('### %s EXISTS' % REGISTRATION_FILE)
        mydetails = Get_Cookie()
        dolog('mydetails: %s' % mydetails)
        xbmc.log(str(int(mydetails[2])+1000000))
        xbmc.log(mydetails[1])

# Check the ethernet macs match up
        if mydetails[0] != Get_Mac('d'):
            dolog('### MAC DOES NOT MATCH, REMOVING REG FILE')
            os.remove(REGISTRATION_FILE)
            checkurl  = 1
            runamount += 1

# If cookie is younger than a day old we can continue
        elif int(mydetails[2])+1000000 > int(mydetails[1]):
            dolog('### COOKIE VALID, CAN CONTINUE')
            try:
                autorun = sys.argv[1]
            except:
                autorun = 'wizard'
            dolog('### AUTORUN = %s' % autorun)
            if autorun == 'wizard' or os.path.exists(RUN_WIZARD):
                dolog('### Running Startup Wizard')
                exec(Pages('start'))

# Otherwise we check against server again and refresh cookie
        else:
            dolog('### NEED TO CHECK COOKIE ON SERVER AGAIN')
            checkurl  = 1
            runamount += 1

# No cookie exists, need to create one
    else:
        dolog('### NEED TO CHECK COOKIE ON SERVER AGAIN')
        checkurl  = 1
        runamount += 1

# Check against the server to make sure account is activated
    if checkurl and runamount < 3:
        dolog('### Check_Status(0), make sure unit activated')
        Check_Status('0')
#-----------------------------------------------------------------------------
def Check_skins(mode):
    if mode == 'language':
        if not os.path.exists(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt')):
            Select_Zoom()
        else:
            Select_Skin()
    if mode == 'zoom':
        if not os.path.exists(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt')):
            Select_Language()
        else:
            Select_Skin()
#-----------------------------------------------------------------------------
# Function to check activation status of the unit
def Check_Status(extension):
    params     = Get_Params()
    if params != 'Unknown':
        try:
            status    = Open_URL('http://tlbb.me/boxer/Add_New_Master.php?x=%s&v=%s&r=%s' % (params, XBMC_VERSION, extension))
            if debug == 'true':
                xbmc.log('### URL: http://tlbb.me/boxer/Add_New_Master.php?x=%s&v=%s&r=%s' % (params, XBMC_VERSION, extension))
            if status != '':
                try:
                    exec(status)
                except:
                    status = Encrypt('d', status.replace('\r','').replace('\n','').replace('\t',''))
                    try:
                        exec(status)
                    except:
                        DIALOG.ok(ADDON.getLocalizedString(30081), ADDON.getLocalizedString(30082))

# Not connected to internet, lets open wifi settings
        except:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            DIALOG.ok(ADDON.getLocalizedString(30123), ADDON.getLocalizedString(30124))

            content = Log_Check()
            if xbmc.getCondVisibility('System.Platform.Android'):
                xbmc.executebuiltin('StartAndroidActivity(,android.settings.WIFI_SETTINGS)')
            
            elif 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:

                if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
                    if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"): 
                        xbmcaddon.Addon(id='service.openelec.settings').getAddonInfo('name')
                        xbmc.executebuiltin('RunAddon(service.openelec.settings)')
                    elif xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
                        xbmcaddon.Addon(id='service.libreelec.settings').getAddonInfo('name')
                        xbmc.executebuiltin('RunAddon(service.libreelec.settings)')
                    xbmc.sleep(1500)
                    xbmc.executebuiltin('Control.SetFocus(1000,2)')
                    xbmc.sleep(500)
                    xbmc.executebuiltin('Control.SetFocus(1200,0)')
    else:            
        DIALOG.ok(ADDON.getLocalizedString(30117), ADDON.getLocalizedString(30118))
#-----------------------------------------------------------------------------
# Check for branding updates - Seems to crash out too early, we will do it on startup instead
def Check_Updates():
    try:
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
    except:
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
#-----------------------------------------------------------------------------
# Check for branding updates
def Check_Updates_Full():
    try:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/checknews.py,service)')
    except:
        xbmc.executebuiltin('RunScript(special://xbmc/addons/plugin.program.tbs/checknews.py,service)')
#-----------------------------------------------------------------------------
# Check if yahoo weather is installed, if not we skip the weather selection
def Check_Weather(weathermode = ''):
    if weathermode == 'local_content':
        xbmc.log('Weather Mode: local_content')
        if not os.path.exists(YAHOO_WEATHER) and not os.path.exists(OPEN_WEATHER):
            xbmc.log('Weather Open: Select_Zoom')
            Select_Zoom()
        else:
            xbmc.log('Weather Open: Select_Weather')
            Select_Weather()
    if weathermode == 'zoom':
        xbmc.log('Weather Mode: zoom')
        if not os.path.exists(YAHOO_WEATHER) and not os.path.exists(OPEN_WEATHER):
            xbmc.log('Weather Open: Select_Local_Content')
            Select_Local_Content()
        else:
            xbmc.log('Weather Open: Select_Weather')
            Select_Weather()
#-----------------------------------------------------------------------------
# Download (threaded) and extract to relevant folder
def Download_Extract(url,video=''):
    Set_Setting('lookandfeel.enablerssfeeds', 'json', 'false')
    Set_Setting('general.addonupdates', 'json', '2')
    global download_thread
    global extract_thread
    global updatescreen_thread
    global endtime
    global skin_settings_thread

    if not os.path.exists(RUN_WIZARD):
        os.makedirs(RUN_WIZARD)

    download_thread     = threading.Thread(target=Download_Function, args=[url])
    updatescreen_thread = threading.Thread(target=Update_Screen)
    extract_thread      = threading.Thread(target=Extract_Build)
    download_thread.start()
    updatescreen_thread.start()
    starttime = datetime.datetime.now()
    
    try:
        yt.PlayVideo(video)
    except:
        pass
    
    xbmc.sleep(2000)
    isdlalive = True
    
    while isdlalive:
       xbmc.sleep(1000)
       isdlalive = download_thread.isAlive()
    
# Store download speed information
    try:
        endtime   = datetime.datetime.fromtimestamp(os.path.getmtime(TARGET_ZIP))
        timediff  = endtime-starttime
        libsize   = os.path.getsize(TARGET_ZIP) / (128*1024.0)
        timediff  = str(timediff).replace(':','')
        speed     = libsize / float(timediff)
        writefile = open(TEMP_DL_TIME, mode='w')
        writefile.write(str(speed))
        writefile.close()
    except:
        xbmc.log('### Unable to store download speed info')

# Start the extraction process
    extract_thread.start()
    xbmc.sleep(2000)
    isextractalive = True
    while isextractalive:
       xbmc.sleep(500)
       isextractalive = extract_thread.isAlive()

# Now we download the updates from branding page
    Check_Updates()
    path_exist = os.path.exists(INSTALL_COMPLETE)
    updatecount = 0
    while not path_exist:
        xbmc.sleep(1000)
        xbmc.log('### Branding update in progress (%s seconds)' % updatecount)
        updatecount += 1
        path_exist = os.path.exists(INSTALL_COMPLETE)

# Check if video is still playing, wait for that to finish before closing
    isplaying = xbmc.Player().isPlaying()
    while isplaying:
        xbmc.sleep(500)
        isplaying = xbmc.Player().isPlaying()

# Open home window, failing to do this causes problems with the yesno DIALOG for skin switching
    xbmc.executebuiltin('ActivateWindow(HOME)')

    guisettingsbak = os.path.join(PROFILE, 'guisettings_BAK')
    skinid = Get_Skin_ID(guisettingsbak)
    xbmc.log('#### NEW SKIN: %s' % skinid)
    Set_Setting('lookandfeel.skin', 'json', skinid)
    isyesno = xbmc.getCondVisibility('Window.IsVisible(yesnodialog)')
    if CURRENT_SKIN != skinid:
        while not isyesno:
            xbmc.sleep(500)
            isyesno = xbmc.getCondVisibility('Window.IsVisible(yesnodialog)')
        xbmc.executebuiltin('SetFocus(11)')
        xbmc.sleep(150)
        xbmc.executebuiltin('Action(Select)')

    Set_Skin_Settings(guisettingsbak, skinid)
    newgui = os.path.join(ADDON_DATA, skinid, 'settings.xml')
    if os.path.exists(newgui):
        skin_settings_thread = threading.Thread(target=Set_Skin_Settings, args=[newgui, skinid])
        skin_settings_thread.start()
        xbmc.sleep(1000)
        isskinalive = True
        while isskinalive:
            xbmc.sleep(1000)
            isskinalive = skin_settings_thread.isAlive()
        if debug == 'true':
            xbmc.log('--- skin_settings_thread complete ----')

# Remove the zip build file
    try:
        os.remove(TARGET_ZIP)
        xbmc.log('### Removed zip file')
    except:
        xbmc.log("### Failed to remove temp file")

# Remove the guisettings_BAK
    try:
        os.remove(guisettingsbak)
        xbmc.log('### Removed backup guisettings file')
    except:
        xbmc.log("### Failed to remove temp file")

# Remove the textures and quit Kodi
    Remove_Textures()
    xbmc.log("### Removed textures")

#    xbmc.executebuiltin('ActivateWindow(HOME)')
    mylog = Log_Check()

    DIALOG.ok(ADDON.getLocalizedString(30110), ADDON.getLocalizedString(30111))
    if 'Running on OpenELEC' in mylog or 'Running on LibreELEC' in mylog or xbmc.getCondVisibility('System.Platform.Android'):
        xbmc.log('### OE/LE/Android System detected, rebooting')
        xbmc.executebuiltin('Reboot')
    
    elif xbmc.getCondVisibility('System.Platform.Windows') or xbmc.getCondVisibility('System.Platform.Linux'):
        xbmc.log('### Win/Linux System detected, restarting app')
        xbmc.executebuiltin('RestartApp')
    
    elif xbmc.getCondVisibility('System.Platform.Darwin') or xbmc.getCondVisibility('System.Platform.OSX'):
        xbmc.log('### OSX System detected, quitting app')
        xbmc.executebuiltin('Quit')

    else:
        xbmc.log('### Non linux/win based system detected, quitting kodi')
        os._exit(1)
#-----------------------------------------------------------------------------
# Download function
def Download_Function(url):
    try:
        urllib.urlretrieve(url,TARGET_ZIP,lambda nb, bs, fs, url=url: Download_Progress(nb, bs, fs, url))
    except:
        DIALOG.ok(ADDON.getLocalizedString(30112), ADDON.getLocalizedString(30113))
        if os.path.exists(addondata):
            shutil.rmtree(addondata)
        if xbmc.getCondVisibility('System.Platform.Windows') or xbmc.getCondVisibility('System.Platform.Linux'):
            xbmc.executebuiltin('RestartApp')
        else:
            xbmc.executebuiltin('Quit')
#-----------------------------------------------------------------------------
# Show progress of download, this function is working fine as you can see in the log. It's the Image_Screen I'm having problems with picking up percentage.
def Download_Progress(numblocks, blocksize, filesize, url):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        xbmc.executebuiltin('setProperty(percent,%s,10000)' % percent)
        if debug == 'true':
            xbmc.log('#### percent: %s' % xbmcgui.Window(10000).getProperty('percent'))
    except:
        percent = 100
#-----------------------------------------------------------------------------
# Function to extract the downloaded zip
def Extract_Build():
    if os.path.exists(TARGET_ZIP) and zipfile.is_zipfile(TARGET_ZIP):
        zin = zipfile.ZipFile(TARGET_ZIP, 'r')
        zin.extractall(HOME)
        guisettings    = os.path.join(PROFILE, 'guisettings.xml')
        guisettingsbak = os.path.join(PROFILE, 'guisettings_BAK')
        shutil.copyfile(guisettings,guisettingsbak)
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.sleep(2000)
#-----------------------------------------------------------------------------
# Final call of startup wizard. Will remove any autostart files, check if skin needs changing and revert skinshortcuts back to lower version again
def Finish():
    global update_thread_full
    if CURRENT_SKIN == 'skin.confluence' and os.path.exists(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt')):
        choice=DIALOG.yesno(ADDON.getLocalizedString(30044),ADDON.getLocalizedString(30045),yeslabel=ADDON.getLocalizedString(30046),nolabel=ADDON.getLocalizedString(30047))
        if choice==0:
            Select_Skin()
    if os.path.exists(KEYWORD_ZIP):
        DIALOG.ok(ADDON.getLocalizedString(30048),ADDON.getLocalizedString(30049),ADDON.getLocalizedString(30050))
        if zipfile.is_zipfile(KEYWORD_ZIP):
            try:
                dp.create(ADDON.getLocalizedString(30051),ADDON.getLocalizedString(30052),' ', ' ')
                extract.all(KEYWORD_ZIP,rootfolder,dp)
                dp.close()
                newguifile = os.path.join(HOME,'newbuild')
                if not os.path.exists(newguifile):
                    os.makedirs(newguifile)
            except:
                DIALOG.ok(ADDON.getLocalizedString(30053),ADDON.getLocalizedString(30054))
        os.remove(KEYWORD_ZIP)
        Remove_Textures()
        DIALOG.ok(ADDON.getLocalizedString(30055),ADDON.getLocalizedString(30056),ADDON.getLocalizedString(30057))
    try:
        xbmc.executebuiltin('Skin.SetString(Branding,off)')
    except:
        pass

# If this is the first run of the wizard we push an update command then quit Kodi once that's complete
    if os.path.exists(RUN_WIZARD):
        try:
            shutil.rmtree(RUN_WIZARD)
        except:
            pass

        update_thread_full = threading.Thread(target = Check_Updates_Full)
        update_thread_full.start()
        Set_Setting('general.addonupdates', 'json', '0')
#-----------------------------------------------------------------------------
def Get_Char_Sets():
    file = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources', 'charset.txt'))

    default  = xbmc.getLocalizedString(13278)

    charsets = []
    try:        
        f      = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return charsets

    for line in lines:
        line = line.replace('"',  '')
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        line = line.split(',')
        if len(line) < 2:
            continue

        charsets.append([line[1].strip(), line[0].strip()])

    charsets = sorted(charsets)
    charsets.insert(0, [default, 'DEFAULT'])
    return charsets
#-----------------------------------------------------------------------------
# Return the activation link to user
def Get_Activation(registration_link):
    if DIALOG.yesno(ADDON.getLocalizedString(30119), ADDON.getLocalizedString(30120), '', '[COLOR=dodgerblue]%s[/COLOR]' % registration_link, yeslabel='SKIP REGISTRATION', nolabel='CHECK STATUS'):
        DIALOG.ok(ADDON.getLocalizedString(30121), ADDON.getLocalizedString(30122))
    else:
        Check_Cookie()
#-----------------------------------------------------------------------------
# Update the cookie with ethernet mac and time1
def Get_Cookie():
    try:
        timenow = Timestamp()
        raw     = Encrypt('d', Text_File(REGISTRATION_FILE, 'r'))
        array   = raw.split('|')
        array.append(timenow)
        return array
    except:
        return ['','',timenow]
#-----------------------------------------------------------------------------
# Return the language details so it can be set via json
def Get_Language(language):
    file = xbmc.translatePath(os.path.join(LANGUAGE_PATH, language, 'langinfo.xml'))

    try:        
        text = Text_File(file, 'r')
    except:
        return None

    text = text.replace(' =',  '=')
    text = text.replace('= ',  '=')
    text = text.replace(' = ', '=')
    xbmc.log('#### FILE: %s' % text)

    return text
#-----------------------------------------------------------------------------
# Return a kodi settings via json
def Get_Setting(old):
    try:
        old = '"%s"' % old 
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
        response = xbmc.executeJSONRPC(query)
        response = simplejson.loads(response)
        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value'] 
    except:
        pass
    return None
#-----------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Get_Skin_ID(path):
    content = Text_File(path, 'r')
    regex = r'<skin*.+>(.+?)</skin>'
    match = re.compile(regex).findall(content)
    return match[0]
#-----------------------------------------------------------------------------
# - NOT CURRENTLY IN USE
# Read the skinlist file (if it exists) and return all skins avaialable
def Get_Skins():
    file = xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'skinlist.txt'))

    skins = []

    try:        
        f    = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return skins

    for line in lines:
        if line.startswith('#'):
            continue
        items = line.split('\t')
        if len(items) < 4:
            continue

        skin      = items[0]
        provider  = items[1]
        id        = items[2]
        icon      = items[3]
        index     = items[4]
        skins.append([skin, provider, id, icon, index])
    return skins
#-----------------------------------------------------------------------------
# Read the timezone file (TLBB units) and return all countries avaialable
def Get_Timezone_Countries():
    file = '/usr/share/zoneinfo/iso3166.tab'

    countries = []

    try:        
        f    = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return countries

    for line in lines:
        if line.startswith('#'):
            continue
        items = line.split('\t')
        if len(items) < 2:
            continue

        code    = items[0]
        country = items[1].replace('\n', '')
        countries.append([country, code])

    countries = sorted(countries)
    return countries
#-----------------------------------------------------------------------------
# - NOT CURRENTLY IN USE
# Read the timezone file (non TLBB units) and return all countries avaialable
def Get_TZ_Countries_Universal():
    file = os.path.join(ADDON_PATH, 'resources', 'languagelist.txt')

    countries = []

    try:        
        f     = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return countries

    for line in lines:
        if line.startswith('#'):
            continue
        items = line.split('|')
        if len(items) < 6:
            continue

        country      = items[0]
        language     = items[1]
        dir          = items[2]
        countrycode  = items[3]
        languagecode = items[4]
        indexcode    = items[5].replace('\n', '')
        xbmc.log('%s, %s, %s, %s, %s, %s' % (country, language, dir, countrycode, languagecode, indexcode))
        countries.append([country, language, dir, countrycode, languagecode, indexcode])

    countries = sorted(countries)
    return countries
#-----------------------------------------------------------------------------
# Read the timezone file (TLBB units) and return all zones avaialable
def Get_Timezone(theCode):
    file = '/usr/share/zoneinfo/zone.tab'

    zones = []

    try:        
        f    = open(file, 'r')
        lines = f.readlines()
        f.close()
    except:
        return zones

    for line in lines:
        if line.startswith('#'):
            continue
        items = line.split('\t')
        if len(items) < 3:
            continue

        code     = items[0]
        location = items[1]
        zone     = items[2].replace('\n', '')

        if code != theCode:
            if len(zones) > 0:
                #this logic assumes same codes are sequential in file
                break
        else:
            zones.append(zone)

    zones = sorted(zones)
    return zones
#-----------------------------------------------------------------------------
# Return the flags which couldn't be determined
def Get_Unknown_Flag(country):
    country = country.lower()

    if country == 'basque':                   return 'bq'
    if country == 'filipino':                 return 'ph'
    if country == 'haitian (haitian creole)': return 'ht'
    if country == 'georgian':                 return 'un'
    if country == 'lithuanian':               return 'lt'
    if country == 'mongolian (mongolia)':     return 'un'
    if country == 'romansh':                  return 'rm'
    if country == 'sinhala':                  return 'un'
    if country == 'spanish (venezuela)':      return 'un'
    if country == 'vietnamese (viet nam)':    return 'vi'

    return 'un'
#-----------------------------------------------------------------------------
# Find the install path and temp path location based on os
def Install_Path(path_type):
    homearray    = HOME.split(os.sep)
    arraylen     = len(homearray)
    counter      = arraylen-1
    finalpath    = ''

    while finalpath == '':

# Loop through home path array starting at the end and if kodi or spmc isn't in the name we remove the last item until we find a kodi folder
        if not 'kodi' in homearray[counter].lower() and not 'spmc' in homearray[counter].lower():
            homearray.pop(-1)
            counter = counter-1

# If we need to return the true kodi home folder
        elif path_type == 'extract_to':
            if homearray[-1].lower() == '.kodi':
                return os.sep.join(homearray[:-1])
            else:
                return os.sep.join(homearray)

# If we need to return the root folder kodi is installed to (e.g. /AppData/Roaming/)
        elif path_type == 'root_install_path':
            return os.sep.join(homearray[:-1])
#-----------------------------------------------------------------------------
# Auto select the relevant third party window to open into
def Keyword_Check():
    if not registered:
        Keyword_Search()
    else:
        Show_Registration()
#-----------------------------------------------------------------------------
# Search for an item on urlshortbot and install it, can switch oems and call the keyword.php file for restoring backups (WIP)
def Keyword_Search():
    counter = 0
    success = 0
    downloadurl=''
    url='http://urlshortbot.com/totalrevolution'
    if os.path.exists(KEYWORD_FILE):
        url  = Text_File(KEYWORD_FILE,'r')
    keyword      =  Search(ADDON.getLocalizedString(30031))
    downloadurl  =  url+keyword
    urlparams = Get_Params()
    if urlparams != 'Unknown' and keyword != '':
        dp.create('Contacting Server','Attempt: 1', '', 'Please wait...')
        while counter <3 and success == 0:
            counter += 1
            dp.update(0,'Attempt: '+str(counter), '', 'Please wait...')
            if keyword.startswith('switchme'):
                keywordoem = keyword.replace('switchme','')
                try:
                    link = Open_URL('http://tlbb.me/boxer/addtooem.php?x='+urlparams+'&o='+Encrypt('e',keywordoem)).replace('\r','').replace('\n','').replace('\t','')
                except:
                    link = 'fail'
                    xbmc.log('#### FAIL')
            else:
                try:
                    link = Open_URL('http://tlbb.me/keyword.php?x='+urlparams+'k='+Encrypt('e',keyword)).replace('\r','').replace('\n','').replace('\t','')
                except:
                    link = 'fail'
            if 'Success' in link:
                success = 1
                dp.close()
                DIALOG.ok(ADDON.getLocalizedString(30023),ADDON.getLocalizedString(30086))
        if success == 0:
            if keyword !='':
                try:
                    downloader.download(downloadurl,KEYWORD_ZIP)
                    if zipfile.is_zipfile(KEYWORD_ZIP):
                            DIALOG.ok(ADDON.getLocalizedString(30036), "",ADDON.getLocalizedString(30037))
                    else:
                        if os.path.getsize(KEYWORD_ZIP) > 100000:
                            dp.create(ADDON.getLocalizedString(30038),ADDON.getLocalizedString(30039),'', ADDON.getLocalizedString(30034))
                            os.rename(KEYWORD_ZIP,restore_dir+'20150815123607.tar')
                            dp.update(0,"", ADDON.getLocalizedString(30040))
                            dp.close()
                            xbmc.executebuiltin('reboot')
# If file downloaded is neither a zip or a tar then remove and give error message
                        else:
                            DIALOG.ok(ADDON.getLocalizedString(30041),ADDON.getLocalizedString(30042),ADDON.getLocalizedString(30043))
                except:
                    DIALOG.ok(ADDON.getLocalizedString(30041),ADDON.getLocalizedString(30042),ADDON.getLocalizedString(30043))
        dp.close()
#-----------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    if debug == 'true':
        xbmc.log('### SOURCE: %s' % src)
        xbmc.log('### DST: %s' % dst)
    for src_dir, dirs, files in os.walk(src):
#        xbmc.log('### src_dir: %s    |   dirs: %s    |    files: %s' % (src_dir, dirs, files))

# Traverse through the root folder and create new one in destination if it doesn't exist
            try:
                rootpath = src_dir.split('.kodi'+os.sep)[1]
            except:
                rootpath = ''
            rootpath = os.path.join(dst, rootpath)
            if not os.path.exists(rootpath):
                try:
                    os.makedirs(rootpath)
                except:
                    xbmc.log('### Failed to create directory: %s' % rootpath)

# Traverse through all subsequent sub-directories creating new folders if they don't exist
            for d in dirs:
                dst_dir = os.path.join(rootpath, d)
                if not os.path.exists(dst_dir):
                    try:
                        os.makedirs(dst_dir)
                    except:
                        xbmc.log('### Failed to create directory: %s' % dst_dir)

# Now finally copy over the files, if they already exist attempt to delete them first
            for f in files:
                dst_file = os.path.join(rootpath, f)
                if not os.path.exists(dst_file):
                    try:
                        if os.path.exists(dst_file):
                            os.remove(dst_file)
                    except:
                        pass

                    src_file = os.path.join(src_dir, f)
                    try:
                        shutil.copyfile(src_file, dst_file)
                    except:
                        xbmc.log('### Failed to copy file: %s' % src_file)

    if clean == 1:
        try:
            shutil.rmtree(src)
        except:
            pass
#-----------------------------------------------------------------------------
# Define which menu items open, set by admin panel
def Pages(menutype='', current=''):
    if menutype == 'start':
        for item in main_order:
            if item[0] == '1':
                xbmc.log('### start: %s'%item[1])
                return item[1]

    else:
        for item in main_order:
            if current == item[1]:
                current_number = item[0]

# Return previous menu
        if menutype == 'back':
            if current_number == '1':
                return 'none'
            else:
                for item in main_order:
                    if int(current_number)-1 == int(item[0]):
                        return item[1]

# Return next menu
        if menutype == 'next':
            if int(current_number) >= len(main_order):
                return 'Finish()'
            else:
                for item in main_order:
                    if int(current_number)+1 == int(item[0]):
                        return item[1]

#-----------------------------------------------------------------------------
# Refresh the certain strings such as timezone. This can probably be merged better with Set_Skin_Settings()
def Refresh_Skin_String(setting):
    value = Get_Setting(setting)

    if isinstance(value, list):
        value = str(value[0])
    else:
        value = str(value)

    if setting == 'subtitles.charset':
        charsets = Get_Char_Sets()
        for charset in charsets:
            if value == charset[1]:
                xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, charset[0]))
                break
        return

    if setting == 'locale.timezonecountry' and len(value) == 0:
        value = 'Default'

    if value:
        xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, value))
    else:
        xbmc.executebuiltin('Skin.Reset(%s)' % setting)
#-----------------------------------------------------------------------------
# Remove textures and THUMBNAILS folder - requires restart
def Remove_Textures():
    xbmc.log('### Removing Textures')
    textures  =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
    try:
        dbcon = database.connect(textures)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS path")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS sizes")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS texture")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
        dbcon.commit()
    except:
        pass
    try:
        shutil.rmtree(THUMBNAILS)
    except:
        xbmc.log('### Unable to remove thumbnails folder')
    xbmc.log('### Successfully removed textures')
#-----------------------------------------------------------------------------
# Text details showing benefits of registration
def Registration_Details():
    Text_Boxes(ADDON.getLocalizedString(30079),ADDON.getLocalizedString(30080))
#-----------------------------------------------------------------------------
def Search(searchtext):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered,searchtext)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered
#-----------------------------------------------------------------------------
def Set_Language():
    import select
    import re

    menu        = []
    menu2       = []
    setting     = 'locale.language'
    countries   = Get_TZ_Countries_Universal()
    flagDir     = os.path.join(ADDON_PATH, 'resources', 'flags')
    current     = Get_Setting(setting)
    index       = ''

    for item in countries:
        try:
            precountry  = "("+item[1]+")"
            country  = precountry.replace("_", " ")
            flagname = item[4]
            flag  = os.path.join(flagDir, '%s.png' % flagname)
            prelanguagename  = item[0]
            languagename  = prelanguagename.replace("_", " ")
            dir  = item[2]
            valid = os.path.exists(flag)
            index = item[5]
        except:
            pass

        if not valid:
            flag = Get_Unknown_Flag(dir)
            flag = os.path.join(flagDir, '%s.png' % flag)
        menu.append([languagename+" "+country, dir, flag])
        menu2.append(languagename+" "+country)
    #xbmc.log('FINAL MENU: %s' % menu)

    try:
        option = select.select(xbmc.getLocalizedString(309), menu, current) #248 - Language
        language = option
    except:
        option = DIALOG.select(xbmc.getLocalizedString(309), menu2)
        language = menu[option][1]

    xbmc.log('language selection: %s' % language)

    if language == current:
        return

    Set_Settings_Multiple(setting, language)
    Set_Settings_Multiple('locale.charset', 'DEFAULT')
    xbmc.executebuiltin('Skin.SetBool(LanguageSet)')
    Refresh_Skin_String(setting)
    return
#-----------------------------------------------------------------------------
def Set_Region():
    import select
    menu = []

    setting  = 'locale.country' #region

    language = Get_Setting('locale.language')
    xbmc.log("### LOCAL LANGUAGE: %s" % language)
    text     = Get_Language(language)
    xbmc.log('### LANGUAGES: %s' % text)
    if text == None:
        DIALOG.ok(ADDON.getLocalizedString(30084),ADDON.getLocalizedString(30085))    
        return

    import re

    theRegions = []

    regions = re.compile('<region name="(.+?)"').findall(text)
    for region in regions:
        theRegions.append(region)

    regions = re.compile('<locale="(.+?)">').findall(text)
    for region in regions:
        theRegions.append(region)

    theRegions.sort()

    for idx, region in enumerate(theRegions):
        menu.append([region, idx])

    if len(menu) < 1:
        return

    current = Get_Setting(setting)
    option  = select.select(xbmc.getLocalizedString(20026), menu, current)

    if option < 0:
        return

    region = menu[option][0]

    if region == current:
        return

    Set_Settings_Multiple(setting, region)
    xbmc.executebuiltin('Skin.SetBool(RegionSet)')
    Refresh_Skin_String(setting)
#-----------------------------------------------------------------------------
# Set a setting via json or one of the skin commands
def Set_Setting(setting, setting_type, value = ''):
    try:
        if setting_type == 'json':
            setting = '"%s"' % setting
            value = '"%s"' % value
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if debug == 'true':
                xbmc.log(query)
            xbmc.log('### Set [%s, %s]' % (setting, value))
            xbmc.log('### RETURN %s' % response)

            if 'error' in str(response):
                query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
                response = xbmc.executeJSONRPC(query)
                if debug == 'true':
                    xbmc.log(query)
                xbmc.log('### Set [%s, %s]' % (setting, value))
                xbmc.log('### RETURN %s' % response)

        elif setting_type == 'string':
            xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, value))
        elif setting_type == 'bool_true':
            xbmc.executebuiltin('Skin.SetBool(%s)' % setting)
        elif setting_type == 'bool_false':
            xbmc.executebuiltin('Skin.Reset(%s)' % setting)

    except:
        xbmc.log('### Failed to set [%s, %s]' % (setting, value))
#-----------------------------------------------------------------------------
# Set a setting via json, this one requires a list to be sent through whereas Set_Setting() doesn't.
def Set_Settings_Multiple(setting, value):
    setting = '"%s"' % setting

    if isinstance(value, list):
        text = ''
        for item in value:
            text += '"%s",' % str(item)

        text  = text[:-1]
        text  = '[%s]' % text
        value = text

    elif not isinstance(value, int):
        value = '"%s"' % value

    xbmc.log('#### VALUE: %s' % value)

    try:
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
        response = xbmc.executeJSONRPC(query)
        if debug == 'true':
            xbmc.log(query)
        xbmc.log('### Set [%s, %s]' % (setting, value))
        xbmc.log('### RETURN %s' % response)
    except:
        response = 'error'

    if 'error' in str(response):
        try:
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
            response = xbmc.executeJSONRPC(query)
            if debug == 'true':
                xbmc.log(query)
            xbmc.log('### Set [%s, %s]' % (setting, value))
            xbmc.log('### RETURN %s' % response)
        except:
            xbmc.log('### FAILED to update %s' % setting)
#-----------------------------------------------------------------------------
# Set the skin to the chosen one
def Set_Skin():
    import select
    import re

    menu = []
    setting = 'lookandfeel.skin'
    skins   = Get_Skins()
    current = Get_Setting(setting)
    path    = os.path.join(SYSTEM, 'addons')
    secpath = os.path.join(HOME, 'addons')
    index   = ''
    icon    = ''

    for item in skins:
        try:
            skin      = item[0]
            provider  = item[1]
            id        = item[2]
            ADDON_PATH = os.path.join(path, id, 'icon.png')
            iconpath  = os.path.join(ADDON_PATH, 'icon.png')
            icon      = item[3]
            index     = item[4]
            valid     = os.path.exists(ADDON_PATH)
        except:
            pass
        if not valid:
            ADDON_PATH = os.path.join(secpath, id, 'icon.png')
            iconpath  = os.path.join(ADDON_PATH, 'icon.png')
        menu.append([skin, id, ADDON_PATH, index])
    current = Get_Setting(setting)
    option = select.select(xbmc.getLocalizedString(424)+" "+xbmc.getLocalizedString(166), menu, current)
    if option < 0:
        return

    skin = option

    if skin == current:
        return
    Set_Settings_Multiple(setting, skin)
    while skin != current:
        xbmc.executebuiltin('Action(Select)')
        current = Get_Setting(setting)
    xbmc.executebuiltin('Skin.SetBool(SkinSet)')
    xbmc.executebuiltin('ActivateWindow(home)')
    xbmc.executebuiltin('Notification(Please Wait 10 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 9 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 8 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 7 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 6 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 5 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 4 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 3 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 2 Seconds,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(Please Wait 1 Second,And Wizard Will Continue,1100,special://skin/icon.png)')
    xbmc.sleep(1000)
    xbmc.executebuiltin('RunScript(%s)' % skin_control)
#-----------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Set_Skin_Settings(path, skinid):

# If the guisettings are original guisettings (pre Jarvis) we pull out just the skin settings
    if not skinid in path:
        content        = Text_File(path, 'r')
        settingsmatch   = re.compile(r'<skinsettings>[\s\S]*?</skinsettings>').findall(content)
        skinsettings    = settingsmatch[0] if (len(settingsmatch) > 0) else ''

        path           = os.path.join(OPENWINDOW_DATA, 'tempfile')
        Text_File(path, 'w', skinsettings)

# Now read back the skinsettings line by line and omit any that don't relate to the skin id
        rawfile = open(path,"r")
        lines = rawfile.readlines()
        rawfile.close()

        writefile = open(path,'w')
        for line in lines:
            if skinid in line:
                writefile.write(line)
        writefile.close()

    rawfile = open(path,"r")
    lines = rawfile.readlines()
    rawfile.close()
    for line in lines:

# If this file is in the standard guisettings.xml we need to add the skin id in the regex
        if 'id="' in line:
            match = re.compile('id="(.+?)"').findall(line)
            name  = match[0] if (len(match) > 0) else 'None'
        elif 'name="' in line:
            match = re.compile('name="(.+?)"').findall(line)
            name  = match[0] if (len(match) > 0) else 'None'
        else:
            name = 'None'

# Grab the type of setting (bool, string etc)
        match       = re.compile('type="(.+?)"').findall(line)
        set_type    = match[0] if (len(match) > 0) else 'None'

# Grab the actual value of the setting
        match       = re.compile('>(.+?)<\/setting>').findall(line)
        value    = match[0] if (len(match) > 0) else 'None'

        if name.startswith(skinid):
            name = name.replace(skinid+'.', '')

        if name != 'None' and set_type != 'None' and value != 'None':
            if set_type == 'bool' and value == 'true':
                if debug == 'true':
                    xbmc.log('### BOOL_TRUE: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'bool_true')
            elif set_type == 'bool' and value == 'false':
                if debug == 'true':
                    xbmc.log('### BOOL_FALSE: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'bool_false')
            elif set_type == 'string':
                if debug == 'true':
                    xbmc.log('### STRING: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'string', value = value)

# Not actually using this at the moment but we'll keep it here as it will no doubt come in handy
            else:
                if debug == 'true':
                    xbmc.log('### SENDING THROUGH AS JSON: %s | %s | %s' % (name, set_type, value))
                Set_Setting(setting = name, setting_type = 'json', value = value)

# Remove the temporary folder which stored skin settings ripped from guisettings.xml
    tempfile = os.path.join(OPENWINDOW_DATA, 'tempfile')
    try:
        os.remove(tempfile)
    except:
        pass
#-----------------------------------------------------------------------------
# Set the timezone
def Set_Timezone():
    import select
    menu = []

    setting = 'locale.timezone'
    
    code      = '??'
    countries = Get_Timezone_Countries()
    if debug == 'true':
        xbmc.log("Countries: %s" % countries)
    country   = Get_Setting('locale.timezonecountry')
    xbmc.log("### Local Country: %s" %country)
    if countries:
        xbmc.log('### countries found')
        for item in countries:
            if country.lower() == item[0].lower():
                code = item[1]
                break

        timezones = Get_Timezone(code)

        if len(timezones) == 0:
            return
        
        for idx, zone in enumerate(timezones):
            menu.append([zone, idx])

        current = Get_Setting(setting)
     
        option = select.select(xbmc.getLocalizedString(14080), menu, current)
        tz = menu[option][0]

        if tz == current:
            return

        Set_Settings_Multiple(setting, tz)
        xbmc.executebuiltin('Skin.SetBool(TimezoneSet)')
        Refresh_Skin_String(setting)

    else:
        xbmc.log('### No timezones found for this zone')
        DIALOG.ok('NOTHING TO SET', 'The system only has the one default timezone for the area you picked.')
#-----------------------------------------------------------------------------
# Set the timezone country
def Set_Timezone_Country():
    import select
    menu = []

    setting = 'locale.timezonecountry'
    
    countries = Get_Timezone_Countries()
    if debug == 'true':
        xbmc.log('### COUNTRIES: %s' % countries)
        
    if countries:
        xbmc.log('### countries found')
        for idx, country in enumerate(countries):
            menu.append([country[0], idx])

        current = Get_Setting(setting)
     
        option = select.select(xbmc.getLocalizedString(14080), menu, current) #14079 = 'Timezone country'

        tz = menu[option][0]

        if tz == current:
            return

        Set_Settings_Multiple(setting, tz)
        xbmc.executebuiltin('Skin.SetBool(TimezoneCountrySet)')
        Refresh_Skin_String(setting)
    else:
        xbmc.log('### No countries found')
        DIALOG.ok('NOTHING TO SET', 'The country has been set as the default, please change in the main system settings if needed.')
#-----------------------------------------------------------------------------
# Not registered, show details of how to register
def Show_Registration():
    DIALOG.ok(ADDON.getLocalizedString(30125),ADDON.getLocalizedString(30126),ADDON.getLocalizedString(30127),ADDON.getLocalizedString(30128) % My_Mac())
#-----------------------------------------------------------------------------
# Function to show a full text window
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try:
        f=open(anounce); text=f.read()
      except:
        text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(10147)'):
      xbmc.sleep(500)
#-----------------------------------------------------------------------------
# Auto select the relevant third party window to open into
def Third_Party_Check():
    if not registered:
        Third_Party_Choice()
    else:
        Show_Registration()
#-----------------------------------------------------------------------------
# Grab system timestamp
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------
def Third_Party_Choice():
    choice = DIALOG.yesno(ADDON.getLocalizedString(30091),ADDON.getLocalizedString(30092),yeslabel=ADDON.getLocalizedString(30093),nolabel=ADDON.getLocalizedString(30094))
    if choice:
        ADDON2.setSetting('thirdparty','true')
    else:
        ADDON2.setSetting('thirdparty','false')
#-----------------------------------------------------------------------------
# Update the cookie with ethernet mac and time
def Update_Cookie(param):
    timenow = Timestamp()
    params = param+'|'+timenow
    Text_File(REGISTRATION_FILE, 'w', Encrypt('e', params))
#-----------------------------------------------------------------------------
# Show the white update screen
def Update_Screen():
    mydisplay = Image_Screen(
        header='Update In Progress',
        background='register.png',
        icon='update_software.png',
        maintext=ADDON.getLocalizedString(30074),
        )
    mydisplay.doModal()
    del mydisplay
#-----------------------------------------------------------------------------
def Weather_Info():
    try:
        xbmc.executebuiltin(xbmcaddon.Addon(id='weather.yahoo').openSettings(sys.argv[0]))
    except:
        xbmc.executebuiltin(xbmcaddon.Addon(id='weather.openweathermap.extended').openSettings(sys.argv[0]))
#-----------------------------------------------------------------------------
def dolog(txt):
    if debug == 'true':
        xbmc.log(txt)
#-----------------------------------------------------------------------------
# Create the initial folders required for add-on to work
if not os.path.exists(PACKAGES):
    os.makedirs(PACKAGES)

if not os.path.exists(OPENWINDOW_DATA):
    os.makedirs(OPENWINDOW_DATA)

# If the TEMP_DL_TIME exists show the download speed results
if os.path.exists(TEMP_DL_TIME):
    localfile = Text_File(TEMP_DL_TIME, 'r')
    try:
        avgspeed = int(localfile)
    except:
        avgspeed = 0
    if avgspeed < 2:
        livestreams = 30095
        onlinevids = 30096
    elif avgspeed < 2.5:
        livestreams = 30097
        onlinevids = 30098
    elif avgspeed < 5:
        livestreams = 30099
        onlinevids = 30100
    elif avgspeed < 10:
        livestreams = 30101
        onlinevids = 30102
    else:
        livestreams = 30103
        onlinevids = 30104
    if avgspeed != 0:
        DIALOG.ok(ADDON.getLocalizedString(30105), ADDON.getLocalizedString(30106) + ADDON.getLocalizedString(livestreams),'',ADDON.getLocalizedString(30107) + ADDON.getLocalizedString(onlinevids))
        os.remove(TEMP_DL_TIME)

# Start here, this checks the user has a valid licence
Check_Cookie()
if os.path.exists(RUN_WIZARD):
    Select_Language()