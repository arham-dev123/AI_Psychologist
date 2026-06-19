document.addEventListener('DOMContentLoaded', function () {
  // Function to scroll the chat container to the bottom
  function scrollChatToBottom() {
      var messagesContainer = document.getElementById('messages');
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Scroll the chat container to the bottom when the page loads
  scrollChatToBottom();

  // Function to focus on the input field
  function focusInputField() {
      var messageInput = document.getElementById('messageInput');
      messageInput.focus();
  }

  function resizeMessageInput() {
      var messageInput = document.getElementById('messageInput');
      if (!messageInput) {
          return;
      }

      messageInput.style.height = 'auto';
      messageInput.style.height = Math.min(messageInput.scrollHeight, 150) + 'px';
  }

  // Focus on the input field when the page loads
  focusInputField();
  resizeMessageInput();

  var messageInput = document.getElementById('messageInput');
  if (messageInput) {
      messageInput.addEventListener('input', resizeMessageInput);
      messageInput.addEventListener('keydown', function (event) {
          if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault();
              sendMessage();
          }
      });
  }

})

// Function to simulate click on the send button
function sendMessage() {
  document.getElementById("sendButton").click(); // Trigger click event on send button
}

function speechToTextConversion() {
  var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
  var diagnostic = document.getElementById('messageInput');
  var i = 0; // Declare i here

  recognition.continuous = true;
  recognition.lang = 'en-IN';
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;

  document.getElementById("micButton").onclick = function () {
      var micButtonIcon = document.querySelector("#micButton .material-symbols-outlined");
      if (i == 0) {
          if (micButtonIcon) {
              micButtonIcon.textContent = "graphic_eq";
          }
          recognition.start();
          i = 1;
      }
      else {
          if (micButtonIcon) {
              micButtonIcon.textContent = "mic";
          }
          recognition.stop();
          i = 0;
          sendMessage();
      }
  };

  recognition.onresult = function (event) {
      var last = event.results.length - 1;
      var convertedText = event.results[last][0].transcript;
      diagnostic.value = convertedText;
      diagnostic.dispatchEvent(new Event('input'));
      console.log('Confidence: ' + event.results[0][0].confidence);
  };

  recognition.onnomatch = function (event) {
      diagnostic.value = 'I didnt recognise that.';
  };

  recognition.onerror = function (event) {
      diagnostic.value = 'Error occurred in recognition: ' + event.error;
  };
}

document.addEventListener('DOMContentLoaded', function () {
  speechToTextConversion(); // Call the function when the DOM is loaded
});
