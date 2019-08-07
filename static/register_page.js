$(document).ready(function() {
    $("#register").click(function() {
      var username = $("#username").val()
      var password = $("#password").val()
      $.post("/register", {username: username, password: password}, function(data) {
        console.log(
          "This is what we get back after posting to the server:",
          data
        );
      });
    });
  });