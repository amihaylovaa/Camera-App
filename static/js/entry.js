$(document).ready(function () {

   const host = "http://127.0.0.1:5000"
   hideDateInput();
   
   $("#picture").click(function () {
      let url = host + "/picture"

      location.href = url;
      return false;
   });
   
   $("#stream").click(function () {
      let url = host + "/stream"

      location.href = url;
      return false;
   });

   $("#video").click(function () {

      $('#date').show();
      $('#send').show();

      return false;
   });

   $("#send").click(function () {
      hideDateInput();
      let date = $('#date').val();
      let url = host + "/videos/" + date

      location.href = url;

      return false;
   });
   
   function hideDateInput(){
      $('#date').hide();
      $('#send').hide();
   }
});
