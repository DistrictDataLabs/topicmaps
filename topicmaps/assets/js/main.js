/*
 * main.js
 * Main javascript function that should be run first thing in the TopicMaps App.
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Sun Aug 23 09:58:00 2015 -0500
 *
 * Dependencies:
 *  - jquery
 *  - underscore
 */

(function() {

  // Do the CSRf AJAX Modification
  var csrfToken   = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajaxSetup({headers: {"X-CSRFToken": csrfToken}});

  // Update the status and the version from the API.
  var statusURL = "/api/status/";
  $.get(statusURL)
    .success(function(data) {
      $("#footerVersion").text(data.version);
      if (data.status == "ok") {
        $("#footerStatus").addClass("text-success");
      } else {
        $("#footerStatus").addClass("text-warning");
      }
    })
    .fail(function() {
      $("#footerVersion").text("X.X");
      $("#footerStatus").addClass("text-danger");
    });

  console.log("Topic Maps App is started and ready");

})();
