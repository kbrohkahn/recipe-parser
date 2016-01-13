#!/usr/bin/env python
with open("../templates/header.html", "r") as header:
	print header.read()
with open("../templates/navbar.html", "r") as navbar:
	print navbar.read()

print("""
<h1>Ratfink</h1>
<div class="subheader">A combination of poker and bridge that's easy to learn and fun to play</div>
<div class="badge-container">
	<a target="blank" href="https://play.google.com/store/apps/details?id=com.play2think.ratfink">
		<img alt="Get it on Google Play" src="/assets/img/en_generic_rgb_wo_45.png" />
	</a>
</div>
<h2>Description</h2>
<p class="indented">Ratfink is a trick taking card game and a fun and easy way learn the basics of the bridge card game!</p>
<p class="indented">Do you enjoy strategy, card games, or math? Do you want to learn card statistics or the basics of bridge such as bidding and trick taking? Even if you just want to play an enjoyable thought-oriented game, you should try Ratfink! Take our tutorial and you will know everything you need to know about Ratfink in less than 5 minutes!</p>
<h2>Features</h2>
<ul>
	<li>Play games with hands from as little as 1 card to as many as 13</li>
	<li>Play against 1, 2, or 3 robot opponents</li>
	<li>Select your game's difficulty</li>
	<li>Take a tutorial to learn the basics of bidding and trick taking in Ratfink</li>
	<li>Arrange the way the suits are ordered in your hand</li>
	<li>Customize the game to your liking</li>
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
		<a href="#galaxy_tab_s_10_screenshots" aria-controls="galaxy_tab_s_10_screenshots" role="tab" data-toggle="tab">Galaxy Tab S 10.5</a>
	</li>
</ul>
<div class="tab-content clearfix">
	<div role="tabpanel" class="tab-pane active" id="droid_maxx_screenshots">
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/playing.png" alt="Playing">
			<div>
				<em>Playing a trick</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/bidding.png" alt="Bidding">
			<div>
				<em>Bidding a round</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/playing_theme_a.png" alt="Playing">
			<div>
				<em>Playing a trick</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/trick.png" alt="Trick">
			<div>
				<em>Trick summary</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/score.png" alt="Score">
			<div>
				<em>Round score summary</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/droid_maxx/playing_theme_c_3p.png" alt="Playing, 3 players">
			<div>
				<em>Playing a trick with 3 players</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/droid_maxx/playing_theme_b_2p_land.png" alt="Playing, 2 players">
			<div>
				<em>Playing a trick with 2 players in landscape</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="galaxy_tab_2_7_screenshots">
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/playing.png" alt="Playing">
			<div>
				<em>Playing a trick</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/bidding.png" alt="Bidding">
			<div>
				<em>Bidding a round</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/playing_theme_a.png" alt="Playing">
			<div>
				<em>Playing a trick</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/trick.png" alt="Trick">
			<div>
				<em>Trick summary</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/score.png" alt="Score">
			<div>
				<em>Round score summary</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/playing_theme_b_3p.png" alt="Playing, 3 players">
			<div>
				<em>Playing a trick with 3 players</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_2_7.0/playing_theme_c_2p_land.png" alt="Playing, 2 players">
			<div>
				<em>Playing a trick with 2 players in landscape</em>
			</div>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="galaxy_tab_s_10_screenshots">
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/playing.png" alt="Playing">
			<div>
				<em>Playing a trick</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/bidding.png" alt="Bidding">
			<div>
				<em>Bidding a round</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/playing_theme_a_3p.png" alt="Playing, 3 players">
			<div>
				<em>Playing a trick with 3 players</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/trick.png" alt="Trick">
			<div>
				<em>Trick summary</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/score.png" alt="Score">
			<div>
				<em>Round score summary</em>
			</div>
		</div>
		<div class="screenshot landscape">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/playing_theme_b_2p.png" alt="Playing, 2 players">
			<div>
				<em>Playing a trick with 2 players</em>
			</div>
		</div>
		<div class="screenshot">
			<img src="/assets/img/ratfink/galaxy_tab_s_10.0/playing_theme_c_port.png" alt="Playing">
			<div>
				<em>Playing a trick in landscape</em>
			</div>
		</div>
	</div>
</div>

<h2>Download Ratfink for free</h2>
<div class="badge-container">
	<a target="blank" href="https://play.google.com/store/apps/details?id=com.play2think.ratfink">
		<img alt="Get it on Google Play" src="/assets/img/en_generic_rgb_wo_45.png" />
	</a>
</div>
""")

with open("../templates/footer.html", "r") as footer:
	print footer.read()
