# Source the default configuration file; this way you can append the default
# configuration file with your own commands, rather than completely overwrite
# it.
#source_default()

# Set icon
if charging:  set_icon('charging')
elif ac:      set_icon('connected')
elif not ac:  set_icon('battery')
else:         set_icon('error')

# Set the colour for the status indicator.
#if ac and not charging:  set_color(None)
if percent <= 20:        set_color('red')
elif percent <= 50:      set_color('orange')
else:                    set_color('green')

# Play sounds if the battery is getting low
if not ac:
	if lifetime < 15:    play_once('alert', 1)
	elif lifetime < 10:  play_once('alert', 2)
	elif lifetime < 5:   play('alert')
else:
	reset_play_once(1)
	reset_play_once(2)

# Send desktop notifications
if switched_to == 'battery': notify('Switched to battery power', 'low')
if not ac:
	if lifetime <= 30:    notify_once('30 minutes of battery time remaining', 'normal', 30)
	elif lifetime <= 15:  notify_once('15 minutes of battery time remaining', 'normal', 15)
	elif lifetime <= 10:  notify('10 minutes of battery time remaining', 'critical', 10)
	elif lifetime <= 5:   notify('5 minutes of battery time remaining', 'critical', 5)

if lifetime > 30:  reset_notify_once(30)
if lifetime > 15:  reset_notify_once(15)
if lifetime > 10:  reset_notify_once(10)
if lifetime > 5:   reset_notify_once(5)


###
### A few more advanced examples below. These may not always be wanted or even
### work (Depends on notebook support/OS), so they're disabled by default.
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
#	run('echo "== WARNING: Battery power low. Sleeping in 30 seconds" | wall && sleep 30 && zzz')
