# XISMuS
#### X-Ray fluorescence Imaging Software for Multiple Samples

This software is distributed with a MIT license. Further details can be found [here](../master/LICENSE)<br>
XISMuS is a dedicated imaging software for X-Ray Fluorescence data (MA-XRF) for Windows OS. The software has been tested on Windows 7 (Ultimate 32-Bit and 64-Bit and Home Premium 64-Bit) and Windows 10. Windows XP is not supported. Be sure to have the latest Visual C++ Redistributable Package when running on *Windows 7*. It can be downloaded directly from Microsoft webpage [here](https://www.microsoft.com/en-us/download/details.aspx?id=40784)<br>
<br>
XISMuS most recent distribution packages can be found here [32-Bit][x86] and here [64-Bit][x64].<br>
A comprehensive guide is provided in the Wiki section. And a User Guide PDF is provided in [this link][UserGuide].
<br>
## Installation
To install XISMuS through any of the installers distribution provided above, simply double-click the executable *XISMuS-1.0.0-x86.exe* or *XISMuS-1.0.0-x64.exe* (depending on your system), carefully read the license agreement and follow the instructions on screen. If you chose to, XISMuS will launch after the setup is finished.<br>
<br>
If you rather run it from the source, straight inside your local Python environment interpreter, simply fork or clone the repository as 
no package form distribution is yet available to use with Python.<br>
<br>
`git clone https://github.com/linssab/XISMuS`<br>
<br>
Be sure to have all the required Python modules installed! They are listed below:<br>

## Dependencies
XISMuS uses xraylib version 3.3.0 but it is optional. You can download it for free [here][xraylib]. Be sure to download the corresponding version to your system architecture. <ins>Note: It is strongly recommended that you install the xraylib package.</ins><br>
If xraylib is not installed, the program will still run, but chemical mapping will be limited to few elements.<br>
Xraylib is used to ensure more precise experimental X-rays data are used. Its absence will cause XISMuS to use its internal database, which may be outdated and may be missing information for low-Z or high-Z elements.
<br>
To run it within a Python interpreter, we recommend you have Python 3.7 installed and the following packages:<br>
The packages whose versions are mentioned are the stable versions working with XISMuS. Numba, for example, has some issues with opencv and may cause JIT funtions to malfunction.<br>
* numpy _v 1.18.1_<br>
* numba _v 0.45.1_<br>
* llvmlite _v 0.31_<br>
* opencv-python<br>
* psutil<br>
* matplotlib<br>

[xraylib]: http://lvserver.ugent.be/xraylib/xraylib-3.3.0-win64.exe
[x64]: https://mega.nz/#!oTJVXYIY!jAJ3u8dL8_ItcH-8jYYzgkcLBibLeWosSU7msBzSZK0
[x86]: https://mega.nz/#!MbY1WKzA!AKqHqlcAQQzaLGkF1BPhasG85U9dA67baJV7gOICo14
[UserGuide]: https://www.google.com
