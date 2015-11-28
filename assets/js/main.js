
function viewRecipe(recipeName) {
	$("#recipe-selection").val(recipeName)
	$("#recipe-search-form").submit()
}

function viewAndTransformRecipe(recipeName) {
	// get transformation value
	var transformationSelect = document.getElementById("transformation-select");
	var transformation = transformationSelect.options[transformationSelect.selectedIndex].value;

	$("#transformation").val(transformation)
	$("#recipe-selection").val(recipeName)
	$("#recipe-search-form").submit()
}

function clearIngredientToInclude(index) {
	$("#include-" + index).val("")
}

function clearIngredientToEnclude(index) {
	$("#exclude-" + index).val("")
}
