$(document).ready(function() {
  $.get("/all_shoes", function(data) {
    data = JSON.parse(data);
    for (var i = 0; i < data.length; i++) {
      $("#all-shoes").append(`
        <p>
            ${data[i][1]}
            ${data[i][2]}
        </p>
      `);
    }
  });
  $(document.body).on("click", ".delete", function(e) {
    var id = e.target.id;
    $.post("/delete_shoe", { id: id }, function(data) {
      location.reload();
    });
  });
});
