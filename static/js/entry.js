$(document).ready(function () {

   hideDateInput();
   
   $("#picture").click(function () {

      location.href = "http://127.0.0.1:5000/picture";
      return false;
   });
   
   $("#stream").click(function () {

      location.href = "http://127.0.0.1:5000/stream";
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
      location.href = "http://127.0.0.1:5000/video/"+date;

      return false;
   });
   
   function hideDateInput(){
      $('#date').hide();
      $('#send').hide();
   }
});
