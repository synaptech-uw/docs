# Muse + Python - detecting blinks

Using Muse headset to control the dinosaur game www.chromedino.com in chrome:
1. Download Anaconda and Python
2. Install muse-lsl by following instructions here: https://github.com/alexandrebarachant/muse-lsl
3. pip install muselsl
4. Muselsl list -b bgapi  ? to connect muse headset to the computer 
5. muselsl stream -b bgapi -a 00:55:DA:B3:81:73
6. Download blinks folder and extract it somewhere on the computer
	- blinks.py
	- utils.py
	- blinkFilter.py
8. In new anaconda prompt, navigate to the blinks folder
9. pip install pyautogui
10. python blinks.py     

Our muse address: 00:55:DA:B3:81:73

To record data, connect muse and then run
muselsl record --duration 60 


Project resources:
https://github.com/urish/eeg-explorer
                                                          
