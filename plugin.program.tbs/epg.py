import sys
import os
import xbmc
import xbmcgui
import yt

sys.argv[1] = sys.argv[1].replace("'",'')
dialog  = xbmcgui.Dialog()
sfname  = sys.argv[1].upper()
sfname  = 'HOME_'+sfname
if os.path.exists(xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')):
    tvgskip = 1
else:
    tvgskip = 0
    
def foldercheck():
    directories = 0
    folderpath = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/',sfname))
    for dirs in os.walk(folderpath):
        directories += len(dirs[1])
    xbmc.log("### Dirs: "+str(directories))
    return directories

folders = foldercheck()

if sys.argv[1] == "live_tv" and folders == 0 and not tvgskip:
    choice = dialog.select(sys.argv[1].replace('_',' ').upper()+' Menu',['[COLOR=gold]Add[/COLOR] to Live TV','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Live TV Content'])
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv",return)')
    if choice == 1:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv_submenu",return)')
    if choice == 2:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
    if choice == 3:
         yt.PlayVideo('-taD-9lqjaw')

elif sys.argv[1] == "live_tv" and folders > 0 and not tvgskip:
    choice = dialog.select(sys.argv[1].replace('_',' ').upper()+' Menu',['[COLOR=gold]Add[/COLOR] to Live TV','[COLOR=gold]Remove[/COLOR] from Live TV','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','[COLOR=gold]Share[/COLOR] Live TV Item','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Live TV Content'])
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv",return)')
    if choice == 1:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=from_the_live_tv_menu",return)')
    if choice == 2:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=live_tv_submenu",return)')
    if choice == 3:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_LIVE_TV",return)')
    if choice == 4:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
    if choice == 5:
         yt.PlayVideo('-taD-9lqjaw')

elif sys.argv[1] == "mainmenu":
    choice = dialog.select('Main Menu Items',['Add Menus','Remove Menus'])
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=main_menu_install&url=add",return)')
        xbmc.executebuiltin('Container.Refresh')

    if choice == 1:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=main_menu_install&url=remove",return)')
        xbmc.executebuiltin('Container.Refresh')

elif sys.argv[1] != "mainmenu" and folders > 0:
# Clean up the name for display purposes only, just remove the 's' if the item ends in that
    cleanname = sys.argv[1].replace('_',' ')        
    choice = dialog.select('[COLOR=dodgerblue]------ SOCIAL SHARING ------[/COLOR]',['[COLOR=gold]Add[/COLOR] to main '+sys.argv[1].replace('_',' ')+' menu','[COLOR=gold]Remove[/COLOR] from main '+sys.argv[1].replace('_',' ')+' menu','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','[COLOR=gold]Share[/COLOR] a '+cleanname+' menu','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Main Menu Items','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Content','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Sharing Content'])
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'",return)')
    if choice == 1:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url=from_the_'+sys.argv[1]+'_menu",return)')
    if choice == 2:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'_submenu",return)')
    if choice == 3:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_'+sys.argv[1].replace(' ','_').upper()+'",return)')
    if choice == 4:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
    if choice == 5:
         yt.PlayVideo('eDK20XkyGXE')
    if choice == 6:
         yt.PlayVideo('IkRZJgup4gk')
    if choice == 7:
       yt.PlayVideo('FSOOED9v1RE')

elif sys.argv[1] != "mainmenu" and folders == 0:
    cleanname = sys.argv[1].replace('_',' ')        
    choice = dialog.select('[COLOR=dodgerblue]------ SOCIAL SHARING ------[/COLOR]',['[COLOR=gold]Add[/COLOR] to main '+sys.argv[1].replace('_',' ')+' menu','[COLOR=gold]Add / Remove[/COLOR] Sub-menus','','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Main Menu Items','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Add/Remove Content','[COLOR=lightsteelblue][TUTORIAL][/COLOR] Sharing Content'])
    if choice == 0:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'",return)')
    if choice == 1:
        xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.tbs/?description&mode=search_content_main&url='+sys.argv[1]+'_submenu",return)')
    if choice == 2:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/epg.py,'+sys.argv[1]+')')
    if choice == 3:
         yt.PlayVideo('eDK20XkyGXE')
    if choice == 4:
         yt.PlayVideo('IkRZJgup4gk')
    if choice == 5:
       yt.PlayVideo('FSOOED9v1RE')
