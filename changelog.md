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

[Latest release](#a06-pre4)  
[Latest in-progress version](#upcoming-website-changes)


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
Some nice things ive been working on.

\#\+ A proper wiki. (WIP)  
\#\+\+ Online repo of modpacks that can be installed.  
\+ Command line arguments! Allows exporting of instances and overriding of install directory along with some more options coming in the future! Use -h to get started.  
\+ There is now an instance setting to use a proxy to fix skins, sounds and capes!
\* Fixed instance settings not loading or saving correctly.  

### a0.6-pre2.1
So many bugs. SO MANY MIXINS.

~ Made it so that more things log to console.  
\+ EasyMineLauncher is now used to launch minecraft. This uses LaunchWrapper, which allows modders to use mixins.  
\- Removed some commented out legacy code.  
\* Techically a modification, but minecraft now launches via MinecraftApplet.  
\* Username not being set on minecraft a1.2.6 and below should be fixed.  
\* Fixed a crash when logon fails.  
\* Fixed a crash when installing local modpacks.  
\* Fixed a crash when installing a partial modpack that didnt have a bin folder.  
\* Fixed the skin and cape fix proxy not working on really old versions of minecraft.  

### a0.6-pre3
What pre2 was meant to be.

\+ Links in the blog section are now clickable. They will open in your default browser.
\+ Automatic resource downloads when installing instances/modpacks. Will only download missing files. It will not replace modified files.  
\+ A working modpack exporter window. Launch PyMCL with `--export` OR `-e`.  
\+ MultiMC instance support. This is extremely experimental and may not work with some modpacks.  
\* Fixed PyMCL not deleting META-INF when needed.  
\* Fixed random crashes when closing the instance manager for good.  

### a0.6-pre3.1
Bugfix  

\* Fixed not launching minecraft on unix systems because I was using the wrong syntax for a command.  

### a0.6-pre3.2
Never let me QA test.  

\* Fixed resources not being downloaded into the right folder.  
\* Fixed the unix compile script not uncluding mitmproxy resources.  
\* Fixed the unit start script not working because I was referencing a non-existent file.  

### a0.6-pre4
Woo!!!11 Automate EVERYTHING!  
Estimated release date: mid June - early July  

~ Removed b1.8 from the blog.html.  
~ Added support for more "modern" versions of minecraft into the proxy.  
\+ Automated blank instance creation.   
\+ Added the ability to cache sounds, LWJGL and MC versions. No more 200mb downloads every time you make an instance!  
\+ Revamped options window.  
\+ Automatic "dumb" mod installing. (just copies contents of zip to mc.jar)   
\* Fixed the instance manager not blocking input to the main window.  
\* Fixed a temp folder issue which could cause garbled instances, slow startup and crashes. (woops!)  

### a0.6-pre4.1
Woops. Again.  

\* Fixed a temp folder issue which caused crashes because of folders not being generated properly.  

### Upcoming website changes
Lets start to change how we install mods!  
Ordered in chronological order of release.  
Accounts should be made reflecting your in game name, or certain features wont work.  
Estimated release date: late June - late July as features roll out.  

\#\+ Closed beta of the account system with a group of people to try and break the website.  
\#\+ A public account system for modpacks and mods and the ability to create and edit modpack and mod pages.  
\#\+ A public modpack and mod uploading system!  
\#\+ A report button to flag a mod/modpack to me and any web admins.  
\#\+ Online mod repository with tons of old converted mods.  
\#\+ A custom cape system for people to upload a cape of thier choice.  
\#\+ A public API to allow the use of custom clients for certain actions.  

### Upcoming a0.6
Its about time I stopped doing prereleases.  
Estimated release date: mid July  

\+ Automatic launcher updates?  
\+ Automatic "semi-smart" mod installing. Most likely only gonna support optional classes and folders though.  

### Upcoming website changes
Power to the user!  
Estimated release date: gradual roll-out over late July to potentially late August  

\#\+ Slightly prettier font page that explains the launcher better.  
\#\+ Proper API documentation.  
\#\+ A filled out wiki.  
\#\+ Unification of website design.  
\#\+ The ability to use uploaded pymcl launcher themes on the website?  

### PyMCS
What could this be?  
This could be very interesting for hosts.  
Keep your eyes on pymcl.net once the new website changes are done.  

### Upcoming b1.0
Lets make things look pretty!  
Estimated release date: when it's ready.  

\+ A fully fleshed out mod installer which can spot conflicting mods and suggest solutions, lets the user pick optional config options and have a pretty mod image display on the modlist in a given modpack.  
\+ A rudimentary modlist system. More documentation on this closer to release.  
\+ Custom compile script to reduce likelyhood of incorrect python versions being used.  
~ UI overhaul. Some of the UI isnt fit for purpose anymore.  
~ Yet another global refactor. I have learned a lot about how pyqt5 works and some of my old code is terrible.  
~ Better theming system.  


### Upcoming b1.1+

\+ A real exporting system including the ability to create ".pymclcl" files. More documentation on how these might work after b1.0.  
\+ Minecraft launches embedded in the launcher like the old minecraft launchers?  

### Release+

\+ Custom compiler + qt modules? This is in the faaaar future though.  