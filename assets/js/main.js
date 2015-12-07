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
	clearSearch();
	resetFilters();
}

function clearSearch() {
	$("#recipe-input").val("")
}

function resetFilters() {
	$("input[type='radio']").prop('checked', false);
	$(".radio-button-default").prop('checked', 'checked');

	$("#ingredients input[type='text']").val("")

	$(".filter-on").attr("class", "filter-either")
	$(".filter-off").attr("class", "filter-either")
}

function changeRadioButton(elementId) {
	var index = elementId.lastIndexOf("-");
	if (index == -1) {
		return;
	}

	var spanId = "#" + elementId.substring(0, index+1) + "string";
	var newClass = "filter" + elementId.substring(index);
	$(spanId).attr("class", newClass)
}

$(document).ready(function() {
	$("#loading-search-results").hide();

	$("#ingredient-tabs a").click(function (e) {
		e.preventDefault()
		$(this).tab("show")
	})

	$("#recipe-labels input").click(function() {
		changeRadioButton($(this).attr('id'))
	});

	$("#ingredient-labels input").click(function() {
		changeRadioButton($(this).attr('id'))
	});
});
