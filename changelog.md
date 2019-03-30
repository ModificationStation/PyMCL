key:  
- \#\<key\> Website change.
- \+ New feature.
- \- Removed feature.
- ~ Modified feature.
- \* Bugfix

Version format: \<prefix\>major.minor.bugfix
- Prefix: Annotates if a version is alpha, beta or release. (a, b, r)
- Major: Full rewrite/ui change or something drastic like that.
- Minor: Normal updates. e.g added/remove/modified individual features.
- Bugfix: If a version is just buxfixes, it will instead have the bugfix number. e.g a0.6.1 for bugfix 1.
- Exceptions:
- - Pre: pre release versions will have pre-number appended to it. These versions should NOT be used if you have instances you care about.


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
\- Any text file containing `readme` or `included` will be opened.
\- See the [Wiki](https://github.com/ModificationStation/PyMCL/wiki) for more info.

### a0.5

~ Per instance java settings.  
~ Better instance manager!  
~ Rewrite of some functions and general optimisation.  
~ Smaller file size! Down to 18mb!  
\- Can no longer display remote (internet) content.  
\+ The blog is now themable with a html4 file!  
\+ Commented code!  
\+ Discord rich presence.  
\* Fixed unix compile script!  
\* Optimisation and crash fixes.  

### a0.6-pre1
The beginning of something awesome.

~ Fixed a crash related to looking in the wrong folder on startup.  
~ Hopefully fixed random crashes after modpack installation.  
~ Partial rewrite of some functions to support threading. (pymcl is now multithreaded! woo!)  
~ Now uses "%appdata%/.PyMCL" on windows, "\~/Library/Application Support/PyMCL" on OSX and "\~/.PyMCL" on anything else.  
\#\+\+ Online repository of modpacks that can be 1-click-installed. 
\+ PyMCL is now portable! Create a file named "stay.here" in the same folder pymcl.exe is located to set it to portable mode.  Only one modpack available at the moment.  
\+ Automatic creation of instances from partial jars. Will only initially support b1.7.3 though.  
\- Python library "appdirs" no longer used. Shaves about 10kb off the file size. /shrug  

### a0.6-pre2
ETA unknown. Likely about 1-2 weeks after pre-1.

\#\+ A proper wiki. (WIP)  
\#\+\+ Online repo of mods, texturepacks and themes that can be installed.  
\+ Command line arguments! Allows exporting of instances and overriding of install directory along with some more options coming in the future! Use -h to get started.  
\+ There is now an instance setting to use a proxy to fix skins, sounds and capes!
\* Fixed instance settings not loading or saving correctly.  

### a0.6-pre2.1

~ Made it so that more things log to console.  
\+ EasyMineLauncher is now used to launch minecraft. This uses LaunchWrapper, which allows modders to use mixins.  
\- Removed some commented out legacy code.  
\* Techically a modification, but minecraft now launches via MinecraftApplet.  
\* Username not being set on minecraft a1.2.6 and below should be fixed.  
\* Fixed a crash when logon failes.  
\* Fixed a crash when installing local modpacks.  
\* Fixed a crash when installing a partial modpack that didnt have a bin folder.  
\* Fixed the skin and cape fix proxy not working on really old versions of minecraft.  

### Upcoming a0.6-pre3
What pre2 was meant to be.

\+ Automatic resource downloads when installing instances/modpacks. Will only download missing files. It will not replace modified files.  
\+ Support for a1.2.6, b1.6.6.  
\+ Automatic "dumb" mod installing. (just copies contents to mc.jar)    
\+ The launcher will have a working modpack exporter window.  
\+ A "create instance" button for creating vanilla instances.  

### Upcoming a0.6
Woo!!!11 Automate EVERYTHING!  

\#\+\+ Online mod repository with tons of converted mods.  
\+ Revamped instance manager.  
\+ Automatic "semi-smart" mod installing. Most likely only gonna support optional classes and folders though.  
\+ Automatic launcher updates?  


### Upcoming b1.0+

~ UI overhaul. Some of the UI isnt fit for purpose anymore.  
~ Yet another rewrite. I have learned a lot about how pyqt5 works and I cant bear to look at some of my old code.  
~ Better theming system.  
\+ Custom compiler + qt modules? This is in the faaaar future though.  
\+ Minecraft launches embedded in the launcher like the old minecraft launchers?