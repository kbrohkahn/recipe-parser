var documentHeight=$(document).height();
var documentWidth=$(document).width();

var count = documentHeight * documentWidth / 20000;
console.log(count);

$("#circuit-background").css("height", documentHeight);

var initialX;
var initialY;
var lastX;
var lastY;
var newPosition;
var animationDuration;
for (var i=0; i<count; i++) {
	animationDuration = Math.random() * 3 + 3;

	if (i==0) {
		lastX = Math.random() * documentWidth*1.5 - documentWidth/4;
		lastY = Math.random() * documentHeight*1.5 - documentHeight/4;

		initialX = lastX;
		initialY = lastY;
	}
	
	if (i % 2 == 0) {
		// vertical
		newPosition = Math.random() * documentHeight*1.5-documentHeight/4;
		addVerticalPath(lastX, lastY, newPosition);
		lastY = newPosition;
	} else {
		// horizontal
		newPosition = Math.random() * documentWidth*1.5-documentWidth/4;
		addHorizontalPath(lastX, newPosition, lastY);
		lastX = newPosition;
	}
}

addVerticalPath(lastX, initialY, lastY)
addHorizontalPath(lastX, initialX, lastY);

function addVerticalPath(x, y1, y2) {
	if (y1 < y2) {
		y2 = y2-4;
		$("#circuit-background").append('<div class="path vertical-path" style="top:'+y1+'px; left:'+x+'px; height:'+(y2-y1)+'px; bottom:'+y2+'px"><span class="moving-up" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	} else {
		y1 = y1-4;
		$("#circuit-background").append('<div class="path vertical-path" style="top:'+y2+'px; left:'+x+'px; height:'+(y1-y2)+'px; bottom:'+y1+'px"><span class="moving-down" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	}
}

function addHorizontalPath(x1, x2, y) {
	if (x1 < x2) {
		x2 = x2-4;
		$("#circuit-background").append('<div class="path horizontal-path" style="top:'+y+'px; left:'+x1+'px; width:'+(x2-x1)+'px; right:'+x2+'px"><span class="moving-left" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	} else {
		x1 = x1-4;
		$("#circuit-background").append('<div class="path horizontal-path" style="top:'+y+'px; left:'+x2+'px; width:'+(x1-x2)+'px; right:'+x1+'px"><span class="moving-right" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	}
}
