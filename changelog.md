
### a0.1

Initial release. Functions exactly like the old launcher.

### a0.2

Fixed a couple of crashes and bugs.

### a0.3

Prep for a0.4.  
~ Minor code rework in prep for 0.4.
~ Config.py layout changed.

### a0.4

~ Themes are now per instance.  
~ Install dir is now %appdata%/.PyMCL (or your OSes alternative to appdata)  
\+ Added instance selection.  
\+ Added a basic instance manager.  
\+ Added automated installing of modpacks from local filesystem.  
- Any text file containing `readme` or `included` will be opened.
- See the [Wiki](https://github.com/ModificationStation/PyMCL/wiki) for more info.

### a0.5

~ Per instance java settings.  
~ Better instance manager!  
~ Optimisation and crash fixes.  
~ Rewrite of some functions and general optimisation.  
~ Smaller file size! Down to 18mb!  
~ Fixed unix compile script!  
\- Can no longer display remote (internet) content.  
\+ The blog is now themable with a html4 file!  
\+ Commented code!  
\+ Discord rich presence.  

### a0.6-pre1
The beginning of something awesome.

~ Fixed a crash related to looking in the wrong folder on startup.  
~ Hopefully fixed random crashes after modpack installation.  
~ Partial rewrite of some functions to support threading. (pymcl is now multithreaded! woo!)  
~ Now uses "%appdata%/.PyMCL" on windows, "~/Library/Application Support/PyMCL" on OSX and "~/.PyMCL" on anything else.  
\+ PyMCL is now portable! Create a file named "stay.here" in the same folder pymcl.exe is located to set it to portable mode.  
\+ Online repository of modpacks that can be 1-click-installed. Only one modpack available at the moment.  
\+ Automatic creation of instances from partial jars. Will only initially support b1.7.3 though.  
\- Python library "appdirs" no longer used. Shaves about 10kb off the file size. /shrug  

### Upcoming a0.6-pre2
ETA unknown. Likely about 1-2 weeks after pre-1.

\+ Support for a1.2.6, b1.6.6.  
\+ Online repo of mods, texturepacks and themes that can be installed.  
\+ Automatic "dumb" mod installing. (just copies contents to mc.jar)  
\+ Revamped instance manager.  
\+ The launcher will have a working "export modpack" button in the instance manager.  
\+ A "create instance" button for creating vanilla instances.

### Upcoming a0.6
Woo!!!11 Automate EVERYTHING!  
  
\+ Online mod repository with tons of converted mods.  
\+ Automatic "semi-smart" mod installing. Most likely only gonna support optional classes and folders though.  
\+ Automatic launcher updates?  


### Upcoming a0.7+

~ Yet another rewrite. I have learned a lot about how pyqt5 works and I cant bear to look at my old code.  
~ Launching minecraft via [launchwrapper](https://github.com/Mojang/LegacyLauncher) to allow for mixins.  
~ Better theming system.  
\+ Custom compiler + qt modules? This is in the faaaar future though.
\+ Minecraft launches embedded in the launcher like the old minecraft launchers?