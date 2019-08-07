$(document).ready(function() {
  $("#shoe-submit").click(function() {
    var shoe_brand = $("#shoe_brand").val()
    var shoe_price = $("#shoe_price").val()
    $.post("/post_new_shoe", {brand: shoe_brand, price: shoe_price}, function(data) {
      console.log(
        "This is what we get back after posting to the server:",
        data
      );
    });
  });
});
