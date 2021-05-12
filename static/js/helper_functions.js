  function goBack(){
    history.back();
 }
  
  function loadVideo(){
    document.getElementById('video-container').innerHTML = '<img src="http://127.0.0.1:5000/live-stream" width="640" height="480">';
} 