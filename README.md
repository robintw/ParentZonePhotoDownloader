# ParentZonePhotoDownloader
Simple Python script to download photos from a ParentZone account.

Run the script with --help for command-line arguments, but by default it will prompt for
email address and password, and save into a folder called `output`.

Requires:
 - `selenium`
 - `click`
 - `requests`

You'll also need to set up [Chrome Driver](https://chromedriver.chromium.org/) for Selenium - or change the code to use another web driver.

For Windows instructions, see the [Windows README](README_for_Windows.md)
