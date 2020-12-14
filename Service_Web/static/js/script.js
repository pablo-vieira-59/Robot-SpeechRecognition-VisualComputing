var cam = document.getElementById("camera");
var cam_icon = document.getElementById("camera-icon");
var cam_feed = document.getElementById("cam-feed");

var sensor = document.getElementById("sensor");
var sensor_icon = document.getElementById("sensor-icon");
3
var speech = document.getElementById("microfone");
var speech_icon = document.getElementById("microfone-icon");
var speech_box = document.getElementById("speech-data");

var chatbot = document.getElementById("chatbot");
var chatbot_icon = document.getElementById("chatbot-icon");

var tts = document.getElementById("tts");
var tts_icon = document.getElementById("tts-icon");

function setOnline(div, icon){
    div.style.color = "green";
    icon.className = "fa fa-check-circle";
}

function setOffline(div, icon){
    div.style.color = "red";
    icon.className = "fa fa-times-circle";
}

function testSpeech(){
    var req = $.get("http://127.0.0.1:5003/speech_data");
    req.done(
        function (result){
            var txt = document.createTextNode(result.message);
            var spc = document.createElement("br");
            speech_box.append(txt);
            speech_box.append(spc);
        }
    )
}

function makeReq(){
    var req = $.get('/data');
    req.done( 
        function (result) {
            console.log(result);
            if(result.cam_status){
                setOnline(cam, cam_icon);
                cam_feed.src = "http://127.0.0.1:5001/video_feed";
            }
            else{
                setOffline(cam, cam_icon);
                cam_feed.src = "http://127.0.0.1/static/img/screen.gif";
            }

            if(result.sensor_status){
                setOnline(sensor, sensor_icon);
            }
            else{
                setOffline(sensor, sensor_icon);
            }

            if(result.speech_status){
                setOnline(speech, speech_icon);
            }
            else{
                setOffline(speech, speech_icon);
            }
            
            
            if(result.chatbot_status){
                setOnline(chatbot, chatbot_icon);
            }
            else{
                setOffline(chatbot, chatbot_icon);
            }

            if(result.tts_status){
                setOnline(tts, tts_icon);
            }
            else{
                setOffline(tts, tts_icon);
            }

        }
    );
    setTimeout(makeReq,1000);
}

makeReq();