$(document).ready(function () {
    
    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 840,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.10",
        autostart: true
      });

      $('.siri-message').textillate({
        loop: false,
        sync: true,
        in:{
            effect: "fadeInUp",
            sync: true,
        },
        out:{
            effect: "fadeOutUp",
            sync: true,
        },
    });

    $("#MicBtn").click(function (e) { 
        eel.playAssistantSound()()
        $("#oval").attr("hidden", true);
        $("#siriWave").attr("hidden", false);
        eel.allCommands()()
    });
    
    
    $("#SettingsBtn").click(function (e) { 
        eel.playAssistantSound()();
        $("#oval").attr("hidden", true);
        $("#siriWave").attr("hidden", true); 
        $("#settings").attr("hidden", false);
    });

    $("#SettingsBtn1").click(function (e) { 
        eel.playAssistantSound()();
        $("#oval").attr("hidden", false);
        $("#siriWave").attr("hidden", true); 
        $("#settings").attr("hidden", true);
    });

    $("#SwitchVoiceBtn").click(function (e) {
        eel.switch_voice()();
    });

    $("#IncreaseRateBtn").click(function (e) {
        eel.change_rate(10)(); // Increase rate by 10
    });

    $("#DecreaseRateBtn").click(function (e) {
        eel.change_rate(-10)(); // Decrease rate by 10
    });
    

    function doc_keyUp(e) {
        
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#oval").attr("hidden", true);
            $("#siriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {

            $("#oval").attr("hidden", true);
            $("#siriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

    // In your JavaScript file
    eel.expose(message);
    function message(text) {
        console.log(text); // You can change this to update the UI
        document.getElementById('message_display').innerText = text; // Assuming you have an element with this ID
    }


});