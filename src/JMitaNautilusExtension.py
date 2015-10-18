from gi.repository import Nautilus, GObject
import subprocess
import os
from pyjavaproperties import Properties

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    
    user=os.path.expanduser('~')+"/"
    jmita=user+".jmita2/"
    favoris=jmita+"favoris/"
    shJMita="/usr/bin/jmita2.sh"
   
    def __init__(self):
        pass

    def menu_activate_cb(self, menu, files):
        args=[self.shJMita]
        
        self.__addFilesToArgs(args, files)
            
        subprocess.Popen(args)
        
    def menu_activate_cb_favoris(self,menu,files,identifier):
        args=[self.shJMita]
        self.__addFilesToArgs(args, files)
        args.append("-d")
        args.append(identifier)
        subprocess.Popen(args)
        
    def __addFilesToArgs(self,args,files):
        for file in files:
            args.append("-f")
            args.append(file.get_location().get_path())
        
    def get_file_items(self, window, files):        
        #les variables sont ici pour le dynamisme du dossier
        #variables
        
        allFavoris=os.listdir(self.favoris)
        
        if len(files) <= 0:
            return
        
        
        listFile=[]
        for i in range(0,len(files)):
            if "video" in files[i].get_mime_type() :
                listFile.append(files[i])
            
        if len(listFile)<=0:
            return
        
        
        menu = Nautilus.Menu()

        mainItem=Nautilus.MenuItem(
            name="MenuExtension::JMita2_Menu",
            label="Lire sur ...",
            tip=""
        )
        
        mainItem.set_submenu(menu)
        
        itemJMita2 = Nautilus.MenuItem(
            name="MenuExtension::JMita2_Item",
            label="Rechercher un appareil...",
            tip=""
        )
        
        itemAbout= Nautilus.MenuItem(
            name="MenuExtencion::JMita2_About",
            label="about JMita 2",
            tip=""
        )
        
        menu.append_item(itemJMita2)
        
        
        itemJMita2.connect('activate', self.menu_activate_cb, listFile)
        count=1
        for file in allFavoris:
            p=Properties()
            p.load(open(self.favoris+file))
            
            item=Nautilus.MenuItem(
                name="MenuExtension::JMita2_Item_"+str(count),
                label=p["name"],
                tip=""
            )
            
            item.connect('activate',self.menu_activate_cb_favoris,listFile,p["identifier"])
            
            menu.append_item(item)
            count=count+1
            
        menu.append_item(itemAbout)
        
        return [mainItem]
        
