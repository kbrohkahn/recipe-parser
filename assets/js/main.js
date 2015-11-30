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

function clearIngredient(index) {
	$("#ingredient-" + index + "-string").val("")
}

function resetAll() {
	$("input[type='radio']").prop('checked', false);
	$(".radio-button-default").prop('checked', 'checked');

	$("#ingredients input[type='text']").val("")
}

$(document).ready(function() {
	$("#ingredient-tabs a").click(function (e) {
		e.preventDefault()
		$(this).tab("show")
	})
});
