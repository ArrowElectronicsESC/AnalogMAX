# AnalogMAX
The AnalogMAX is multi-featured sensor fusion FPGA development platform targeting smart city and smart building applications. 
It is based on the MAX10 Intel FPGA, including the brand-new Smoke & Aerosol Detector ADPD188BI from Analog Devices. The ADPD188BI is a complete photometric system for smoke detection utilizing optical dual-wavelength technology. The chip integrates a highly efficient photometric front end, two LEDs, and a photodiode. The board also includes a fully calibrated single-chip temperature sensor (0.25°C, 16-Bit), MEMS accelerometer (3-axis), and compact 8-channel ADC/DAC/GPIO extender. A soft core NIOS II processor and sample HDL code provides the means by which the sensors are configured and read via Python code running within a Jupyter notebook .

# Installation

**Download Support files**

Add support files directly into Jupyter.
1.	Click on “Clone or Download” to download the files
2.	Unzip the folder into C:/Users/username

**Install Anaconda**

1.	Go to the following link http://docs.anaconda.com/anaconda/install/
2.	Click on the proper operating system (this guide is using Windows)
3.	Click “Download the Anaconda installer.”
4.	In the Python 3.7 version * box click on “64-Bit Graphical Installer “ under the download button 
5.	Run the installer
    a.	Do not change the Install Location
    b.	Leave the PATH variable unchecked
    c.	Skip Visual Studio

**Install pySerial**

The python serial port support library pySerial needs to be added. It provides backends for Python running on Windows, OSX, Linux, BSD (possibly any POSIX compliant system) and IronPython to access a serial port.
1.	 Open the Anaconda command prompt
    a.	Press the Windows key and type “Anaconda prompt”
2.	In the command prompt type “conda install -c anaconda pyserial”
3.	Type “y” to proceed with the install
    a.	“Executing transaction: done” means the install is complete
4.	Close the window

**Check the AnalogMAX connection**

1.	Plug in the AnalogMAX using a micro USB cable
2.	Open Device Manager
    a.	Press the Windows key and type “device manager”
3.	Check under Ports (COM & LPT) for “USB Serial Port (COMx)”
    a.	Remember the COM port number!
4.	Check under Universal Serial Bus controllers for “USB Serial Converter A” and “USB Serial Converter B”

**Open Jupyter**

1.	Open Anaconda Navigator
a.	Press the Windows key and type “Anaconda Navigator”
2.	Click “Launch” in the Jupyter notebook box 

