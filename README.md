# Minecraft Playtime
Gets your total playtime of the game by reading game logs.

There is no accurate way to determine the total playtime for all cases, such as cases when the client is open, but a world isn't, or if tick warping is used and the world statistics become messed up, or worlds are deleted and statistics become inaccessible. However by reading game logs you can get the total playtime from the moment the client is started to when it is closed, similar to how game launchers such as Steam count your playtime.

Simply run the script from a terminal (or your favourite IDE) and it should work automatically. If not, it may be because your Minecraft directory is not installed in the default location, which means you will have to change it on line 7 (I'm too lazy to add GUI yet so DIY).

Things to add:
- Multiple MC directory support
- GUI for selecting directories
- More statistics
