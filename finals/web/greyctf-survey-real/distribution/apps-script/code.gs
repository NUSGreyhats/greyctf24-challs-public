// This function runs when the form is submitted.
function onSubmit(event) {

  // The event is a FormResponse object:
  // https://developers.google.com/apps-script/reference/forms/form-response
  var formResponse = event.response;

  // Gets all ItemResponses contained in the form response
  // https://developers.google.com/apps-script/reference/forms/form-response#getItemResponses()
  var itemResponses = formResponse.getItemResponses();

  // Gets the actual response strings from the array of ItemResponses
  var responses = itemResponses.map(function getResponse(e) { return e.getResponse(); });

  const [teamname, best_chal, difficulty] = responses;


  // This token is different on the real challenge service
  const token = "477367dac5740dad0657c1f38fd455f7";
  const file_id = "1xMEAwxHhYahxkJaSBpF472QS0ExZdgD2";

  var options = {
    'method' : 'post',
    'payload' : {
      token,
      difficulty,
      best_chal
    }
  };

  console.log(options);
  UrlFetchApp.fetch(`http://challs.nusgreyhats.org:33340/form_response?teamname=${teamname}&challenge_file_id=${file_id}`, options);
}