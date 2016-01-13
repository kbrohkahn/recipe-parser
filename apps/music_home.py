#!/usr/bin/env python
with open("../templates/header.html", "r") as header:
	print header.read()
with open("../templates/navbar.html", "r") as navbar:
	print navbar.read()

print("""
<div class="subheader">Never be forced to power your screen on again</div>
<div class="badge-container">

	<a target="blank" class="apple-badge" href="https://itunes.apple.com/us/developer/kevin-broh-kahn/id1047274120#">
		<img alt="Find in App Store" src="/assets/img/Download_on_the_App_Store_Badge_US-UK_135x40.svg">
	</a>
	<a target="blank" href="https://play.google.com/store/apps/details?id=com.acrilogic.musichome">
		<img alt="Get it on Google Play" src="/assets/img/en_generic_rgb_wo_45.png" />
	</a>
</div>
<h2>Description</h2>
<p class="indented">Music Home is an app that allows you to easily and quickly control music from a variety of players. Through Music Home's lightweight screen saver and efficient home screen, your music will always be just a tap away. Hate having to unlock your phone to choose the next song? Don't want to fiddle for the power button to turn your screen on? Then Music Home is the perfect app for you!</p>
<p class="indented">The prime feature of Music Home is its screen saver. The screen saver is a highly efficient page that displays only the current artist and track title with a black background. By preventing the screen from turning off and the device from locking, the application allows for quick wakeups from the screen saver with a simple tap on the screen. In case you're worried about screen burn, fear not: the "Now Playing" info on the screen saver continuously moves about the screen, preventing a portion of the device display from being on and fully colored for an extended period of time. The screen saver will automatically start before the the device's screen timeout setting, or you can manually start the screen saver via the "Sleep" button</p>
<p class="indented">Music Home is designed to control one music application at a time. To select which application to control on Android, press the settings icon at the top right of the "Now Playing" pane, then press "Select music app". Since iOS only allows control of the system music application, Music Home on iPhones and iPads will only control the iTunes app.</p>
<h2>Features</h2>
<ul>
	<li>Control iTunes music app (iOS only)</li>
	<li>Control any of the following music apps (Android only)
		<ul>
			<li>Google Play Music</li>
			<li>Spotify</li>
			<li>Amazon Prime Music</li>
			<li>Poweramp</li>
			<li>Samsung Music Player</li>
			<li>Any music app! <em>(<a href="mailto:support@acrilogic.com">contact us</a> to make a request)</em></li>
		</ul>
	</li>
	<li>Screen saver that keeps screen on in low power setting without locking device</li>
	<li>Control media volume level</li>
	<li>Pressing now playing pane opens current media app (Android only)</li>
	<li>Choose light or dark theme, or select a schedule for light and dark themes</li>
	<li>Automatically change theme based on device brightness. Useful when using auto brightness for device (iOS only)</li>
</ul>

<h2>Screenshots</h2>

<ul class="nav nav-tabs" role="tablist">
	<li role="presentation" class="active">
		<a href="#droid_maxx_screenshots" aria-controls="droid_maxx_screenshots" role="tab" data-toggle="tab">Droid Maxx</a>
	</li>
	<li role="presentation">
		<a href="#galaxy_tab_2_7_screenshots" aria-controls="galaxy_tab_2_7_screenshots" role="tab" data-toggle="tab">Galaxy Tab 2 7.0</a>
	</li>
	<li role="presentation">
		<a href="#galaxy_tab_s_10_screenshots" aria-controls="galaxy_tab_s_10_screenshots" role="tab" data-toggle="tab">Galaxy Tab S 10.1</a>
	</li>
	<li role="presentation">
		<a href="#iphone_6s_screenshots" aria-controls="iphone_6s_screenshots" role="tab" data-toggle="tab">iPhone 6s</a>
	</li>
	<li role="presentation">
		<a href="#iphone_6s_plus_screenshots" aria-controls="iphone_6s_plus_screenshots" role="tab" data-toggle="tab">iPhone 6s Plus</a>
	</li>
	<li role="presentation">
		<a href="#ipad_air_2_screenshots" aria-controls="ipad_air_2_screenshots" role="tab" data-toggle="tab">iPad Air 2</a>
	</li>
</ul>
<div class="tab-content clearfix">
	<div role="tabpanel" class="tab-pane active" id="droid_maxx_screenshots" style="display: block;">
		<div class="screenshot">
			<img src="/assets/img/music_home/droid_maxx/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/droid_maxx/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/droid_maxx/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/droid_maxx/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/droid_maxx/home_landscape.png" alt="Home screen landscape">
			<div>
				<em>Home screen, landscape orientation</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/droid_maxx/home_dark_theme_landscape.png" alt="Home screen dark landscape">
			<div>
				<em>Home screen with dark theme, landscape orientation</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="galaxy_tab_2_7_screenshots">
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/home_landscape.png" alt="Home screen landscape">
			<div>
				<em>Home screen, landscape orientation</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_2_7.0/home_dark_theme_landscape.png" alt="Home screen dark landscape">
			<div>
				<em>Home screen with dark theme, landscape orientation</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="galaxy_tab_s_10_screenshots">
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/home_portrait.png" alt="Home screen portrait">
			<div>
				<em>Home screen, portrait orientation</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/galaxy_tab_s_10.1/home_dark_theme_portrait.png" alt="Home screen dark portrait">
			<div>
				<em>Home screen with dark theme, portrait orientation</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="iphone_6s_screenshots">
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/iphone_6s/home_landscape.png" alt="Home screen landscape">
			<div>
				<em>Home screen, landscape orientation</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/iphone_6s/home_dark_theme_landscape.png" alt="Home screen dark landscape">
			<div>
				<em>Home screen with dark theme, landscape orientation</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="iphone_6s_plus_screenshots">
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s_plus/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s_plus/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s_plus/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/iphone_6s_plus/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/iphone_6s_plus/home_landscape.png" alt="Home screen landscape">
			<div>
				<em>Home screen, landscape orientation</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/iphone_6s_plus/home_dark_theme_landscape.png" alt="Home screen dark landscape">
			<div>
				<em>Home screen with dark theme, landscape orientation</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="ipad_air_2_screenshots">
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/ipad_air_2/home.png" alt="Home screen">
			<div>
				<em>Home screen</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/ipad_air_2/screensaver.png" alt="Screen saver">
			<div>
				<em>Screensaver</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/ipad_air_2/home_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Home screen with dark theme</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/music_home/ipad_air_2/screensaver_dark_theme.png" alt="Home screen dark">
			<div>
				<em>Screensaver with dark theme</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/ipad_air_2/home_portrait.png" alt="Home screen portrait">
			<div>
				<em>Home screen, portrait orientation</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/music_home/ipad_air_2/home_dark_theme_portrait.png" alt="Home screen dark portrait">
			<div>
				<em>Home screen with dark theme, portrait orientation</em>
			</div>
		</div>
	</div>
</div>

<h2>Button descriptions</h2>
<div class="button-description">
	<img src="/assets/img/music_home/toggle_pause_button.png" alt="Toggle pause icon">
	<div>
		<h4>Toggle pause</h4>
		<p>If music is currently playing, pauses it. Otherwise, playback will resume in the current player.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/play_button.png" alt="Play icon">
	<div>
		<h4>Play</h4>
		<p>Resumes playback in the current player.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/pause_button.png" alt="Pause icon">
	<div>
		<h4>Pause</h4>
		<p>Pauses playback in the current player.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/previous_button.png" alt="Previous icon">
	<div>
		<h4>Previous Track</h4>
		<p>Timing varies with each player. If playback of current song is within first few seconds, skips to the previous track in the queue. Otherwise, skips to the beginning of the current track.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/next_button.png" alt="Next icon">
	<div>
		<h4>Next Track</h4>
		<p>Skips to the next track in the queue.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/volume_down.png" alt="Volume down icon">
	<div>
		<h4>Volume Down</h4>
		<p>Decreases media volume level by 1.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/volume_up.png" alt="Volume up icon">
	<div>
		<h4>Volume Up</h4>
		<p>Increases media volume level by 1.</p>
	</div>
</div>
<div class="button-description">
	<img src="/assets/img/music_home/sleep_button.png" alt="Sleep icon">
	<div>
		<h4>Sleep</h4>
		<p>Turns on the screen saver.</p>
	</div>
</div>

<h2>Purchase full version</h2>
<div class="badge-container">
	<a target="blank" class="apple-badge" href="https://itunes.apple.com/us/developer/kevin-broh-kahn/id1047274120#">
		<img alt="Find in App Store" src="/assets/img/Download_on_the_App_Store_Badge_US-UK_135x40.svg">
	</a>
	<a target="blank" href="https://play.google.com/store/apps/details?id=com.acrilogic.musichome">
		<img alt="Get it on Google Play" src="/assets/img/en_generic_rgb_wo_45.png" />
	</a>
</div>

<h2>Download 2 week trial</h2>
<div class="badge-container">
	<a target="blank" class="apple-badge" href="https://itunes.apple.com/us/developer/kevin-broh-kahn/id1047274120#">
		<img alt="Find in App Store" src="/assets/img/Download_on_the_App_Store_Badge_US-UK_135x40.svg">
	</a>
	<a target="blank" href="https://play.google.com/store/apps/details?id=com.acrilogic.musichometrial">
		<img alt="Get it on Google Play" src="/assets/img/en_generic_rgb_wo_45.png" />
	</a>
</div>
""")

with open("../templates/footer.html", "r") as footer:
	print footer.read()
