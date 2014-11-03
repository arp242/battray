#
# See http://code.arp242.net/battray for docs
#


# Set icon
if charging:  set_icon('charging.png')
elif ac:      set_icon('connected.png')
elif not ac:  set_icon('battery.png')
else:         set_icon('error.png')

# Set the colour for the status indicator.
if ac:               set_color(None)
elif percent <= 50:  set_color('yellow')
elif percent <= 20:  set_color('red')
elif percent >= 51:  set_color('green')

# Play sounds if the battery is getting low
if not ac:
	if lifetime < 15:    play_once('alert.wav', '1')
	elif lifetime < 10:  play_once('alert.wav', '2')
	elif lifetime < 5:   play('alert.wav')
else:
	reset_play_once('1')
	reset_play_once('2')

# Send desktop notifications
if switched_to == 'battery':  notify('Switched to battery power', 'low')
if not ac:
	if lifetime < 30:   notify('30 minutes of battery time remaining', 'normal')
	elif lifetime < 15: notify('15 minutes of battery time remaining', 'normal')
	elif lifetime < 10: notify('10 minutes of battery time remaining', 'critical')
	elif lifetime < 5:  notify('5 minutes of battery time remaining', 'critical')


###
### A few more advanced examples below. These may not always be wanted or even
### work (Depends on notebook support/OS), so they're disabled by default
###

# Save some power by lowering brightness
#if switched_to == 'battery': run('xbacklight -set 30')

# Put brightness back up when we are connected to AC
#if switched_to == 'ac': run('xbacklight -set 60')

# Turn off screen after 2 minutes, saves some power.
#if switched_to == 'battery': run('xset dpms 120 120 120')

# Turn off screen after 10 mins
#if switched_to == 'ac': run('xset dpms 600 600 600')

# Shut down if battery status is below 5 minutes
# Normal users aren't typically allowed to execute shutdown, if you add
# something along the lines of:
#    <username> localhost=/sbin/shutdown NOPASSWD
# to your sudoers file then this will work ...
# Or you can also chmod +s /sbin/shutdown, but this is less secure ...
#if lifetime < 2: run('sudo shutdown -h +1 "Battery status very low, shutting down system!"')

# If suspend works on your notebook ...
#if not ac and lifetime < 2:
#	run('echo "== WARNING: Battery power low. Sleeping in 30 seconds" | wall && sleep 30 && "zzz"')
