#Running on Windows

1. Download Cygwin installer from here: https://cygwin.com/install.html
2. Run it, choose default options until you get to select packages.
3. Click the dropdown next to "View" in the top left, change it from "Pending" to "Full"
4. Type "python38-pip" into the "Search" box, you should see a single package in the list below.
5. Click the dropdown in the "New" column, change it from "Skip" to "20.1.1-1"
6. Hit next to complete the installation.
7. Run Cygwin by going to C:\cygwin64\bin (assuming default install location) and doubleclicking on "mintty.exe" to open a terminal
8a. If you're comfortable with Git, clone the repo into the home directory. 
8b. If you don't know what that means, in the Windows File Manager, go to 
"C:\cygwin64\home\<your username here>" and right click on empty space, choose "New" and then Text Document. Copy and paste the contents of the file https://github.com/robintw/ParentZonePhotoDownloader/blob/master/download_parentzone_photos.py
into the text document. Save the document as "download_parentzone_photos.py"
9. Download ChromeDriver from here: https://chromedriver.chromium.org/downloads (choose the link matching the version of Chrome you have installed, and the file ending in "win32.zip")
10. Extract chromedriver.exe from the zip file, and copy it into "C:\cygwin64\home\<your username here>" in the Windows File Manager.
11. In the Cygwin terminal, run this command "export PATH=$^CTH:$(pwd)"
12. Then run this command "python3.8.exe download_parentzone_photos.py"
13. You will be prompted to enter your email / password, hit enter after each one.
14. Wait, you'll see a browser window open automatically. Eventually it will close.
15. Your photos should be in the "output" directory, i.e. "C:\cygwin64\home\<your username here>\output"