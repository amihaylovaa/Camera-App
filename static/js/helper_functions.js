  function goBack(){
    history.back();
 }
  
  function loadVideo(fileName){
    let url = "http://127.0.0.1:5000"+ fileName;

    document.getElementById('video-container').innerHTML = '<img src="'+url+'" width="640" height="480">';
  }