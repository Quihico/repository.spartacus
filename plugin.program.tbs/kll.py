import re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys
scriptfolder     =  xbmc.translatePath(os.path.join('special://home','userdata','addon_data','plugin.program.tbs','scripts'))

def KLL():
    if not os.path.exists(scriptfolder):
        os.makedirs(scriptfolder)
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if xbmc.getCondVisibility('system.platform.windows'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'win_xbmc.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im XBMC.exe /f\ntskill XBMC.exe\nXBMC.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_xbmc.bat'))
            except:
                print"### Failed to run win_xbmc.bat"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'win_kodi.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im Kodi.exe /f\ntskill Kodi.exe\nKodi.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_kodi.bat'))
            except:
                print"### Failed to run win_kodi.bat"
    elif xbmc.getCondVisibility('system.platform.osx'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_xbmc.sh'), 'w+')
                writefile.write('killall -9 XBMC\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                print"### Failed to run osx_xbmc.sh"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_kodi.sh'), 'w+')
                writefile.write('killall -9 Kodi\nKodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                print"### Failed to run osx_kodi.sh"
#    else:
    elif xbmc.getCondVisibility('system.platform.android'):
        if os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
            dialog.ok('Attempting to force close','On the following screen please press the big button at the top which says "KILL selected apps". Kodi will restart, please be patient while your system updates the necessary files and your skin will automatically switch once fully updated.')
            try:
                xbmc.executebuiltin('StartAndroidActivity(com.rechild.advancedtaskkiller)')
            except:
                print"### Failed to run Advanced Task Killer. Make sure you have it installed, you can download from https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk"
        else:
            dialog.ok('Advanced Task Killer Not Found',"The Advanced Task Killer app cannot be found on this system. Please make sure you actually installed it after downloading. We can't do everything for you - on Android you do have to physically click on the download to install an app.")
        try:
            os.system('adb shell am force-stop org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc());')
        except:
            pass
    elif xbmc.getCondVisibility('system.platform.linux'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_xbmc'), 'w+')
                writefile.write('killall XBMC\nkillall -9 xbmc.bin\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_xbmc'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_xbmc'))
            except:
                print "### Failed to run: linux_xbmc"
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_kodi'), 'w+')
                writefile.write('killall Kodi\nkillall -9 kodi.bin\nkodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_kodi'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_kodi'))
            except:
                print "### Failed to run: linux_kodi"
    else: #ATV and OSMC
        try:
            os.system('killall AppleTV')
        except:
            pass
        try:
            os.system('sudo initctl stop kodi')
        except:
            pass
        try:
            os.system('sudo initctl stop xbmc')
        except:
            pass
