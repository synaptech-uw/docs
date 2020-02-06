# Muse + Python - detecting blinks

Using Muse headset to control the [dinosaur game](www.chromedino.com) in chrome:
1. Download [Anaconda](https://www.anaconda.com/distribution/#download-section) and Python. Python may come installed with Anaconda, but double check. 
2. Install [muse-lsl](https://github.com/alexandrebarachant/muse-lsl) using the anaconda prompt
	2.1 ```pip install muselsl```
3. (optional) Install [BlueMuse](https://github.com/kowalej/BlueMuse/tree/master/Dist)<br />
	3.1 Unzip folder<br />
	3.2 Right click on InstallBlueMuse.ps1 and choose "Run with Powershell"<br />
	3.3 Powershell will lead you through prompts. You will need to turn on developer mode (maybe turn that off after you're done here. Or not). <br />
4. In anaconda prompt: ```Muselsl list -b bgapi``` to connect muse headset to the computer 
5. ```muselsl stream -b bgapi -a 00:55:DA:B3:81:73```
	(without BlueMuse you will need a BLED112 dongle)
6. Download blinks folder and extract it somewhere on the computer. You should have these three files:
	- blinks.py
	- utils.py
	- blinkFilter.py<br />
	6.1 (optional) If you want to look at the files, Anaconda should have also installed Jupyter notebook. To open jupyter, launch anaconda navigator, then launch jupyter. From there you can navigate to where you downloaded blinks. Look at the code!
8. In new anaconda prompt, navigate to the blinks folder
9. Still in the anaconda prompt: ```pip install pyautogui```
10. ```python blinks.py```
	Now it should work! Navigate to [www.chromedino.com](www.chromedino.com) and play! You may have to adjust the threshold inside of blinks.py if it's not working well. 

## Helpful notes
Our muse 1 address: 00:55:DA:B3:81:73

To record data, connect muse and then run
```muselsl record --duration 60```                  
