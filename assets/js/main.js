function selectType(value) {
	$("#" + value + "Select").show().siblings().hide();
}

function changeSelectedRecipe(value) {
	$("#recipeInput").val(value);
}

$(document).ready(function() {
	selectType($("#recipeInput").val());
});