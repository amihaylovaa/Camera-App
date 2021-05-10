$(document).ready(function () {

   defineBehavior();

   $('#stop').click(function(){
      hideStopButton();
   });
   
   $("#video").click(function () {
      if(isStopButtonVisible()){
         hideStopButton();
       }

      $('#date').show();
      $('#send').show();

      return false;
   });

   $("#send").click(function () {
      hideDateInput();
      let date = $('#date').val();

      $.ajax({
         url: 'http://127.0.0.1:5000/video/'+date,
         type: 'GET',
         contentType: 'application/json',
         crossDomain: true,
       }).done(function (response) {
         response = '<input type="radio" id="" name="" value="">'
         $("#result").html('<img src="data:image/jpeg;base64,' +response+ '" />');         
        }).fail(function (jqXHR, textStatus, errorThrown) {
           
       }); 

      return false;
   });
   
   function defineBehavior() {
     hideStopButton();
     hideDateInput();
   }
   
   function hideDateInput(){
      $('#date').hide();
      $('#send').hide();
   }

  function hideStopButton(){
   $('#stop').hide();
   $('#picture').prop('disabled', false);
   $('#video').prop('disabled', false);
  }

  function isStopButtonVisible(){
     return $('#stop').is(':visible');
  }
});
