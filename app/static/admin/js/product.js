function filterSubcategories(categoryId) {
  console.log("Function called 1");
  var subcategoryField = $('#id_subcategory');
  subcategoryField.html('<option value="">---------</option>');

  if (categoryId) {
      $.ajax({
        url: '/subcategories/',
        data: { category: categoryId },
        dataType: 'json',
        success: function(subcategories) {
          console.log(subcategories)
          subcategory_select.empty();
          var subcategory_select = $('#id_subcategory');
          subcategory_select.append($('<option>', {
            value: '',
            text: '---------'
        }));
                $.each(subcategories, function(index, subcategory) {
                    subcategory_select.append('<option value="' + subcategory.id + '">' + subcategory.name + '</option>');
                });
        },
        error: function(xhr, status, error) {
          console.log('Request failed. Returned status of ' + xhr.status);
        }
      });
  }
}

