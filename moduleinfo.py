from module import Module, MetaModule, ModuleSet

# gnome 2.0 support
head = ModuleSet()
head.add(Module(name='intltool'))
head.add(Module(name='gnome-common'))
head.add(Module(name='gtk-doc'))
head.add(Module(name='glib',
                dependencies=['gtk-doc']))
head.add(Module(name='pango', revision='pango-1-0', dependencies=['glib']))
head.add(Module(name='atk', dependencies=['glib']))
head.add(Module(name='gtk+',
                dependencies=['pango', 'atk']))
head.add(Module(name='gail',
                dependencies=['gtk+', 'atk', 'libgnomecanvas']))
head.add(Module(name='gtkhtml2', dependencies=['gtk+', 'gnome-xml', 'gail']))
head.add(Module(name='gnome-xml', checkoutdir='libxml2'))
head.add(Module(name='libxslt', dependencies=['gnome-xml']))
head.add(Module(name='linc', dependencies=['glib']))
head.add(Module(name='libIDL', dependencies=['glib']))
head.add(Module(name='ORBit2', dependencies=['linc', 'libIDL']))
head.add(Module(name='bonobo-activation',
         dependencies=['intltool', 'gnome-common','ORBit2','gnome-xml']))
head.add(Module(name='gconf', dependencies=['ORBit2','gnome-xml','gtk+']))
head.add(Module(name='libbonobo', dependencies=['ORBit2','bonobo-activation']))
head.add(Module(name='gnome-mime-data', dependencies=['gnome-common']))
head.add(Module(name='gnome-vfs',
                dependencies=['libbonobo','gconf', 'gnome-mime-data']))
head.add(Module(name='libart_lgpl'))
head.add(Module(name='libgnome',
                dependencies=['gnome-xml', 'libxslt', 'libbonobo',
                              'gnome-vfs', 'gconf']))
head.add(Module(name='libgnomecanvas', dependencies=['gtk+', 'libart_lgpl', 'libglade', 'gnome-common']))
head.add(Module(name='libbonoboui',
                dependencies=['libgnome', 'libbonobo', 'libgnomecanvas', 'libglade']))
head.add(Module(name='libgnomeui', dependencies=['libbonoboui', 'libglade']))

head.add(Module(name='libzvt', dependencies=['libart_lgpl', 'gtk+', 'gnome-common']))
head.add(Module(name='libglade',
                dependencies=['gtk+', 'gnome-xml']))
head.add(Module(name='gnome-python/pygtk',
                dependencies=['gtk+', 'libglade']))
head.add(Module(name='orbit-python',
                dependencies=['libIDL', 'ORBit2']))
head.add(Module(name='gnome-python/gnome-python',
         dependencies=['gnome-python/pygtk', 'libgnomecanvas', 'libgnomeui']))
head.add(Module(name='bug-buddy',
                dependencies=['libgnomeui']))
head.add(Module(name='libwnck',
                dependencies=['gtk+']))

head.add(Module(name='gnome-panel',
                dependencies=['libgnomeui','gnome-desktop']))
head.add(Module(name='gnome-desktop', dependencies=['libgnomeui', 'libwnck']))
head.add(Module(name='gnome-session', dependencies=['libgnomeui', 'libwnck']))

head.add(Module(name='gnome-applets',
         dependencies=['gnome-panel','libgtop']))
head.add(Module(name='gnome-games',
         dependencies=['libgnomeui']))
head.add(Module(name='eel',
         dependencies=['librsvg','libgnomeui']))
head.add(Module(name='librsvg',
         dependencies=['gnome-xml','gtk+', 'libart_lgpl', 'gnome-common']))
head.add(Module(name='nautilus',
         dependencies=['esound','eel','librsvg','libgnomeui','gnome-desktop']))
head.add(Module(name='nautilus-gtkhtml', dependencies=['nautilus', 'gtkhtml2']))
head.add(Module(name='metacity',
         dependencies=['gtk+','gconf']))
head.add(Module(name='metatheme',
         dependencies=['libgnomeui']))
head.add(Module(name='libgtop', revision='libgtop-GNOME-2-0-port',
                  dependencies=['glib']))
head.add(Module(name='procman',
         dependencies=['libgnomeui','libwnck','libgtop']))
head.add(Module(name='gnome-control-center',
         dependencies=['libgnomeui', 'esound', 'gnome-desktop']))
head.add(Module(name='yelp',
         dependencies=['libgnomeui', 'gtkhtml2', 'gnome-vfs']))
head.add(Module(name='gnome-utils',
         dependencies=['libgnomeui', 'gnome-panel']))
head.add(Module(name='gconf-editor',
                dependencies=['gconf']))
head.add(Module(name='esound'))
head.add(Module(name='gnome-media',
         dependencies=['libgnomeui', 'esound', 'gail']))
head.add(Module(name='gdm2',
                dependencies=['librsvg']))
head.add(Module(name='profterm',
                dependencies=['libglade', 'libgnomeui', 'libzvt']))
head.add(Module(name='gtk-engines',
                dependencies=['gtk+']))
head.add(Module(name='gedit',
                dependencies=['libgnomeui', 'libgnomeprintui']))
head.add(Module(name='libgnomeprintui',
                dependencies=['libgnomeprint']))
head.add(Module(name='libgnomeprint',
                dependencies=['libbonobo', 'libart_lgpl']))
head.add(Module(name='memprof',
                dependencies=['libgnomeui']))
head.add(Module(name='eog',
                dependencies=['libgnomeui']))
head.add(Module(name='gal', revision='gal-2',
                dependencies=['libgnomeui']))
head.add(Module(name='libole2',
                dependencies=['glib']))
head.add(Module(name='gnumeric',
                dependencies=['libole2', 'gal']))
head.add(Module(name='glade', revision='glade-gnome2-branch',
		dependencies=['gtk+', 'gnome-xml', 'libgnomeui', 'libgnomeprintui']))
head.add(Module(name='glade2c', dependencies=['gtk+', 'gnome-xml', 'libgnomeui']))
head.add(Module(name='gtkglarea', dependencies=['gtk+']))

head.add(Module(name='sawfish', revision='gnome-2', 
	 dependencies=['rep-gtk']))
head.add(Module(name='rep-gtk', dependencies=['librep', 'gtk+']))
head.add(Module(name='librep'))

# some simple tasks to make using jhbuild a bit easier
head.add(MetaModule(name='meta-gnome-devel-platform',
                    modules=['libgnome', 'libbonobo', 'libbonoboui',
                             'libgnomeui']))
head.add(MetaModule(name='meta-gnome-core',
                    modules=['gnome-desktop', 'gnome-panel', 'gnome-session',
                             'profterm']))
head.add(MetaModule(name='meta-nautilus',
                    modules=['nautilus', 'nautilus-gtkhtml']))
head.add(MetaModule(name='meta-gnome-desktop',
                    modules=['meta-gnome-core', 'gnome-control-center',
                             'meta-nautilus', 'yelp', 'bug-buddy',
                             'gtk-engines']))
head.add(MetaModule(name='meta-gnome-devel-tools',
                    modules=['glade', 'memprof', 'gconf-editor']))
head.add(MetaModule(name='meta-gnome-python',
                    modules=['gnome-python/pygtk', 'orbit-python',
                             'gnome-python/gnome-python']))

# gnome 1.x support
gnome1 = ModuleSet()
gnome1.add(Module(name='intltool'))
gnome1.add(Module(name='gnome-common'))
gnome1.add(Module(name='esound'))
gnome1.add(Module(name='gtk-doc'))
gnome1.add(Module(name='glib', revision='glib-1-2',
                  dependencies=['gtk-doc']))
gnome1.add(Module(name='gtk+', revision='gtk-1-2',
                  dependencies=['gtk-doc', 'glib']))
gnome1.add(Module(name='ORBit', revision='orbit-stable-0-5',
                  dependencies=['glib']))
gnome1.add(Module(name='gnome-xml', checkoutdir='libxml',
                  revision='LIB_XML_1_BRANCH'))
gnome1.add(Module(name='imlib',
                  dependencies=['gtk+']))
gnome1.add(Module(name='gnome-libs', revision='gnome-libs-1-0',
                  dependencies=['ORBit', 'imlib', 'esound']))
gnome1.add(Module(name='libglade', revision='libglade-1-0',
                  dependencies=['gtk+', 'gnome-libs', 'gnome-xml']))
gnome1.add(Module(name='gdk-pixbuf',
                  dependencies=['gtk+', 'gnome-libs']))
gnome1.add(Module(name='oaf',
                  dependencies=['intltool', 'ORBit', 'gnome-xml']))
gnome1.add(Module(name='gconf', revision='gconf-1-0',
                  dependencies=['ORBit', 'gnome-xml', 'gtk+']))
gnome1.add(Module(name='gnome-print', revision='gnome-1-4-branch',
                  dependencies=['gnome-libs', 'gnome-xml', 'gdk-pixbuf']))
gnome1.add(Module(name='gnome-mime-data', dependencies=['gnome-common']))
gnome1.add(Module(name='gnome-vfs', revision='gnome-vfs-1',
                  dependencies=['oaf', 'ORBit', 'gconf', 'gnome-xml', 'gnome-mime-data']))
gnome1.add(Module(name='bonobo',
                  dependencies=['gnome-libs', 'oaf', 'gnome-print']))
gnome1.add(Module(name='control-center', revision='control-center-1-0',
                  dependencies=['gnome-libs', 'gnome-vfs']))
gnome1.add(Module(name='gnome-core', revision='gnome-core-1-4',
                  dependencies=['gnome-libs', 'gdk-pixbuf', 'control-center',
                                'libglade']))
gnome1.add(Module(name='libgtop', revision='LIBGTOP_STABLE_1_0',
                  dependencies=['glib']))
gnome1.add(Module(name='gnome-http', checkoutdir='libghttp'))
gnome1.add(Module(name='gnome-applets', revision='gnome-applets-1-4',
                  dependencies=['gnome-core', 'libgtop', 'gnome-http']))
gnome1.add(Module(name='medusa',
                  dependencies=['gnome-vfs', 'gtk+']))
gnome1.add(Module(name='librsvg', revision='librsvg-1-0',
                  dependencies=['gtk+', 'gnome-xml', 'gdk-pixbuf']))
gnome1.add(Module(name='eel', revision='eel-1-0',
                  dependencies=['gnome-libs', 'librsvg', 'gnome-vfs']))
gnome1.add(Module(name='nautilus', revision='nautilus-gnome-1',
                  dependencies=['gnome-libs', 'eel', 'bonobo', 'control-center']))
