#######################################################################
# Configuration file for Battray 1.6
# Please see battray(1) for more information.
#
# Note: This file is imported in Python, so any valid Python code goes.
#######################################################################

# You van override the data directory. Usually not needed.
#datadir = './'
#import os
#datadir = os.path.expanduser('~/.battray/')

# Check every n seconds.
pollinterval = 15

### Events
# Note: Icon and sound can be relative to datadir or an absolute path.

# Set icons
if charging():  icon = 'charging.png'
elif ac():      icon = 'connected.png'
elif not ac():  icon = 'battery.png'
else:           icon = 'error.png'

# Set the color for the status indicator.
if percent() <= 50: color = 'yellow'
if percent() <= 20: color = 'red'
if percent() >= 51: color = 'green'

# Blink the status indicator
if not ac() and lifetime() < 5:   blink = True
if not ac() and lifetime() >= 5:  blink = False
if ac():                          blink = False

# Play sounds if the battery is getting low
if not ac():
	if lifetime() < 15:    playonce('alert.wav', '1')
	elif lifetime() < 10:  playonce('alert.wav', '2')
	elif lifetime() < 5:   play('alert.wav')
else:
	reset_playonce('1')
	reset_playonce('2')

###
### A few more advanced examples below. These may not always be wanted or even
### work (Depends on notebook support/OS), so they're disabled by default
###
# Save some power by lowering brightness
# May not work on all notebooks...
#if switchedto() == 'battery': run('xbacklight -set 30')

# Put brightness back up when we are connected to AC
#if switchedto() == 'ac': run('xbacklight -set 60')

# Turn off screen after two minutes, saves some power.
# Should work on almost all notebooks ...
#if switchedto() == 'battery': run('xset dpms 120 120 120')

# Turn off screen after 10 mins, default is 40 mins orso
#if switchedto == 'ac': run('xset dpms 600 600 600')

# Shut down if battery status is below 5 minutes
# Normal users aren't typically allowed to execute shutdown, if you add
# something along the lines of:
#    <username> localhost=/sbin/shutdown NOPASSWD
# to your sudoers file then this will work ...
# Or you can also chmod +s /sbin/shutdown, but this is less secure ...
#if lifetime < 2: run('sudo shutdown -h +1 "Battery status very low, shutting down system!"')

# If suspend works on your notebook ...
#if not ac() and lifetime() < 2:
#	run('echo "== WARNING: Battery power low. Sleeping" | wall && sleep 10 && "zzz"')
