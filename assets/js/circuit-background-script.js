var documentHeight=$(document).height();
var documentWidth=$(document).width();

// set number of paths based on document size
var count = documentHeight * documentWidth / 20000;

// set div height to document height
$("#circuit-background").css("height", documentHeight);

var lastX = Math.random() * documentWidth*1.5 - documentWidth/4
var lastY = Math.random() * documentHeight*1.5 - documentHeight/4;
var initialX = lastX;
var initialY = lastY;
var newPosition;
for (var i=0; i<count; i++) {
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
	var animationDuration = Math.random() * 3 + 3;
	if (y1 < y2) {
		$("#circuit-background").append('<div class="path vertical-path" style="top:'+y1+'px; left:'+x+'px; height:'+(y2-y1+4)+'px;"><span class="moving-down" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	} else {
		$("#circuit-background").append('<div class="path vertical-path" style="top:'+y2+'px; left:'+x+'px; height:'+(y1-y2+4)+'px;"><span class="moving-up" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	}
}

function addHorizontalPath(x1, x2, y) {
	var animationDuration = Math.random() * 3 + 3;
	if (x1 < x2) {
		$("#circuit-background").append('<div class="path horizontal-path" style="top:'+y+'px; left:'+x1+'px; width:'+(x2-x1+4)+'px;"><span class="moving-right" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	} else {
		$("#circuit-background").append('<div class="path horizontal-path" style="top:'+y+'px; left:'+x2+'px; width:'+(x1-x2+4)+'px;"><span class="moving-left" style="animation-duration:'+animationDuration+'s; -webkit-animation-duration:'+animationDuration+'s"></span></div>');	
	}
}
