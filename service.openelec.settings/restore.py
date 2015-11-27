import sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
restore_dir  = '/storage/.restore'
backup_dir   = '/storage/backup/'

def RESTORE():
    if not os.path.exists(restore_dir):
        os.makedirs(restore_dir)
    restorechoice = dialog.yesno('Where do you want to restore from?','Would you like to restore a file from your default backup', 'folder or would you prefer to browse your system','for another location (such as USB/SD)', nolabel='Backup Folder',yeslabel='Browse')
    if restorechoice == 0:
        filename = xbmcgui.Dialog().browse(1, 'Select the .tar file you want to restore', 'files', '.tar', False, False, backup_dir)
    else:
        filename = xbmcgui.Dialog().browse(1, 'Select the .tar file you want to restore', 'files', '.tar', False, False)
    if filename !='':
        dp.create("Restoring Backup","Copying Files...",'', 'Please Wait')
        shutil.copyfile(filename,restore_dir)
        dp.update(0,"", "Kodi will now reboot")
        xbmc.executebuiltin('reboot')
       
if __name__ == '__main__':
    RESTORE()