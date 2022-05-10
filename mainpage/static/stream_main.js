'use strict';

/* globals MediaRecorder */

let mediaRecorder;
let recordedBlobs;

//const codecPreferences = 'video/webm;codecs=vp9,opus';
const codecPreferences ='video/webm;codecs=h264'
const errorMsgElement = document.querySelector('span#errorMsg');
const recordButton = document.querySelector('button#record');

// ajax token 
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

// record start + end
recordButton.addEventListener('click', async () => {
  if (recordButton.textContent === 'Start Recording') {
    const constraints = {
      audio: false,
      video: {facingMode : {exact : 'environment'}}
     // video : true
  };
    console.log('Using media constraints:', constraints);
    await init(constraints);

    startRecording();
  } else {
    stopRecording();
    recordButton.textContent = 'Start Recording';
  }
  
});


function handleDataAvailable(event) {
  console.log('handleDataAvailable', event);
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}


function startRecording() {
  recordedBlobs = [];
  const mimeType = codecPreferences;
  const options = {mimeType};

  try {
    mediaRecorder = new MediaRecorder(window.stream, options);
  } catch (e) {
    console.error('Exception while creating MediaRecorder:', e);
    errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
    return;
  }

  console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
  recordButton.textContent = 'Stop Recording';

  mediaRecorder.onstop = (event) => {
    console.log('Recorder stopped: ', event);
    console.log('Recorded Blobs: ', recordedBlobs);

    var fd = new FormData();
    const blob = new Blob(recordedBlobs, {type: 'video/webm'});
    const file = new File([blob], "JH_Test.webm");

    fd.append('data', file);
    $.ajax({
      url: '/stream/',
      type: "POST",
      data: fd,
      contentType: false,
      processData: false,
      headers: { "X-CSRFToken": csrftoken },
      success : function (data) {
        console.log("전송 성공");
        // console.log(data);
      },
      // error: function (xhr, textStatus, thrownError) {
      //   alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
      // }
    });
  };
  mediaRecorder.ondataavailable = handleDataAvailable;
  mediaRecorder.start();
  console.log('MediaRecorder started', mediaRecorder);

}

function stopRecording() {
  mediaRecorder.stop();
}

function handleSuccess(stream) {
  // recordButton.disabled = false;
  console.log('getUserMedia() got stream:', stream);
  window.stream = stream;
  console.log('되고있음...............................');
  const gumVideo = document.querySelector('video#gum');
  gumVideo.srcObject = stream;

  // codecPreferences.disabled = false;
}

async function init(constraints) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    errorMsgElement.innerHTML = 'navigator.getUserMedia error:${e.toString()}';
  }
}
