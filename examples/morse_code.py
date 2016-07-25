"""
Program for making the RedPitaya / Koheron laser development work as a morsecode emitter. 
Code is scanned from the command line by the program, and transmitted as short and long laser-pulses.
"""
import initExample # Necessary module, must be in the same
# program as the main file.
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from ldk.utilities import load_instrument
from ldk.drivers import Oscillo

# Enter board IP
host = os.getenv('HOST','10.42.0.53')
client = load_instrument(host, instrument='oscillo')
driver = Oscillo(client)

# Making a method for text input. Only small letters, commas, and punctuation marks allowed.
phrase = str(raw_input("Please type text to be translated, using only UTF-8 characters:"))

phrase = list(phrase) #Arranges all the leters in a list.

# Set laser current
current = float(raw_input("Please enter laser current (0ma - 40ma):"))  # mA

if current > 40:
	print('Current too high! Chose current in range 0ma - 40ma.')
	os._exit(0)


# Modulation on DAC
amp_mod = float(raw_input("Please enter modulation amplitude (0 - 1):"))

if amp_mod > 1:
	print('Modulation amplitude to high! Only range 0 - 1 is allowed.')	
	os._exit(0)

# Set modulaton frequency
freq_mod = float(raw_input("Please enter modulation frequency (0 - 62.50MHz):"))  #Scientific notation is alowed ex: 1e6 = 1,000,000 Hz

if freq_mod > 62.50e6:
	print('Frequency to high! Only frequencies in the range 0Hz - 62.5MHz are allowed.')
	os._exit(0)

# Function for creating a short signal - the dot.
def dot():
	print('.')
	#morsecode.append('.')
	# Enable laser
	driver.start_laser()
	driver.set_laser_current(current)
	driver.dac[1, :] = amp_mod*np.sin(2 * np.pi * freq_mod * driver.sampling.t)
	driver.set_dac()

	# Signal on ADC
	driver.get_adc()
	signal = driver.adc[0, :]
	
	time.sleep(.2)

	driver.stop_laser()
	driver.close()

	time.sleep(.25)

# Function for making a long signal - the dash.	
def dash():
	print('-')
	# Enable laser
	driver.start_laser()
	driver.set_laser_current(current)

	driver.dac[1, :] = amp_mod * np.sin(2 * np.pi * freq_mod * driver.sampling.t)
	driver.set_dac()

	# Signal on ADC
	driver.get_adc()
	signal = driver.adc[0, :]

	time.sleep(.4)
	driver.stop_laser()
	driver.close()
	time.sleep(.25)

# The letters arranged in a python dictionary. Each letter has assigned its
# Morse-code equivalent. All indices are saved as strings, and must be
# Converted to commands. E.g: 'dot()' must be changed to dot() without the ''
# In order for it to work.

letters = {'a': 'dot(), dash()', 'b' : 'dash(), dot(), dot(), dot()', \
'c' : 'dash(), dot(), dash(), dot()', 'd' : 'dash(), dot(), dot()', \
'e' : 'dot()', 'f' : 'dot(), dot(), dash(), dot()', 'g' : 'dash(), dash(), dot()', \
'h' : 'dot(), dot(), dot(), dot()', 'i' : 'dot(), dot()', \
'j' : 'dot(), dash(), dash(), dash()', 'k' : 'dash(), dot(), dash()', \
'l' : 'dot(), dash(), dot(), dot()', 'm' : 'dash(), dash()', \
'n' : 'dash(), dot()', 'o' : 'dash(), dash(), dash()', \
'p' : 'dot(), dash(), dash(), dot()', 'q' : 'dash(), dash(), dot(), dash()', \
'r' : 'dot(), dash(), dot()', 's' : 'dot(), dot(), dot()', 't' : 'dash()', \
'u' : 'dot(), dot(), dash()', 'v' : 'dot(), dot(), dot(), dash()', \
'w' : 'dot(), dash(), dash()', 'x' : 'dash(), dot(), dot(), dash()', \
'y' : 'dash(), dot(), dash(), dash()', 'z' : 'dash(), dash(), dot(), dot()', \
' ' : ' ', ',' : ','}

# Dictionary for turning capital letters into small letters.
capital = {'A' : 'a', 'B' : 'b', 'C' : 'c', 'D' : 'd', 'E' : 'e', 'F' : 'f', 'G' : 'g',\
'H' : 'h', 'I' : 'i', 'J' : 'j', 'K' : 'k', 'L' : 'l', 'M' : 'm', 'N' : 'n', 'O' : 'o',\
'P' : 'p', 'Q' : 'q', 'R' : 'r', 'S' : 's', 'T' : 't', 'U' : 'u', 'V' : 'v', 'W' : 'w',\
'X' : 'x', 'Y' : 'y', 'Z' : 'z'}

# This for-loop iteares over all the letters in the original
# Input text - list "phrase".
for letter in phrase:
	if letter in capital:
		letter = capital['%s'%(letter)] # Turns capital letters into small letters.
	if letter == ' ':	# prints a space, if a space is found in the text.
		print(' ')
		time.sleep(.5)
		
	if letter == '.':	# Prints "stop" when a punctuachion is found.
		print ' '
		eval(letters['s']), eval(letters['t'])
		eval(letters['o']), eval(letters['p'])
		print 'stop'
	if not (letter == ' ' or letter == '.' or letter == ','): # Only letters are evaluated.
		eval(letters['%s'%(letter)])
		print(letter)

# The last part of the for-loop, gathers the dictionary inputs, and uses the eval function and prints the corresponding letter from the text.


# Disable laser
driver.stop_laser()
driver.close()


"""
Written by Einar KNUDSEN. einarknudsen@yahoo.com
The code has been ported from a Raspberry PI project to work with the Koheron laser developement board. 
Awesome laser board, guys!
"""

