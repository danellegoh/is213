// Helper function to display error message
function showError(message) {
    // Display an error under the main container
    $('#main-container')
        .append("<label>" + message + "</label>");
}

// link to the submit buttons for each form 
var form1 = document.getElementById('submit1')
var form2 = document.getElementById('submit2')
var form4 = document.getElementById('submit4')

// ASYNC TO ADD REWARDS IN DB 
$(async() => {
    console.log('async1 working')

    // get the input from the forms 
    const rewardNameInput = document.getElementById('rewardName');
    const discountInput = document.getElementById('discount');
    const quantityInput = document.getElementById('quantity');
    const monthInput = document.getElementById('month');
    const specialInput = document.getElementById('special');

    form1.addEventListener('click', async(event) => {
        console.log('event listener 1 working')

        event.preventDefault();

        // store user input in variables
        const rewardName = rewardNameInput.value;
        const discount = discountInput.value / 100;
        const quantity = quantityInput.value;
        const month = monthInput.value;

        // create the data object 
        const data = {"rewardname": rewardName, "discount": discount, "quantity": quantity, "month": month, "special": 1};
        console.log(data);

        // // URL for routing
        // var bronzeURL = "http://localhost:5002/rewards/Bronze".concat("/", month);
        // var silverURL = "http://localhost:5002/rewards/Silver".concat("/", month);
        // var goldURL = "http://localhost:5002/rewards/Gold".concat("/", month);

        // docker URLs
        var bronzeURL = "http://127.0.0.1:5002/rewards/Bronze".concat("/", month);
        var silverURL = "http://127.0.0.1:5002/rewards/Silver".concat("/", month);
        var goldURL = "http://127.0.0.1:5002/rewards/Gold".concat("/", month);


        try {
            console.log("testing try");
            // bronze tier 
            const responseBronze =
                await fetch(
                    bronzeURL, { mode: 'cors', method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) }
            );

            const resultBronze = await responseBronze.json();
            console.log("bronze");
            console.log(resultBronze);

            if (responseBronze.status === 200) {
                // success case 
                console.log(resultBronze.message);
            } else if (responseBronze.status == 404) {
                // not found
                showError(resultBronze.message);
            } else {
                // unexpected outcome, throw the error
                throw responseBronze.status;
            }

            // silver tier 
            const responseSilver =
                await fetch(
                    silverURL, { mode: 'cors', method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) }
            );

            const resultSilver = await responseSilver.json();
            console.log("silver");
            console.log(resultSilver);

            if (responseSilver.status === 200) {
                // success case 
                console.log(resultSilver.message);
            } else if (responseSilver.status == 404) {
                // not found
                showError(resultSilver.message);
            } else {
                // unexpected outcome, throw the error
                throw responseSilver.status;
            }

            // gold tier 
            const responseGold =
                await fetch(
                    goldURL, { mode: 'cors', method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) }
            );

            const resultGold = await responseGold.json();
            console.log("gold");
            console.log(resultGold);

            if (responseGold.status === 200) {
                // success case 
                console.log(resultGold.message);
            } else if (responseGold.status == 404) {
                // not found
                showError(resultGold.message);
            } else {
                // unexpected outcome, throw the error
                throw responseGold.status;
            }
        } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        showError
            ('There is a problem adding the rewards, please try again later.<br />' + error);
        } // error
    })

});

// ASYNC TO SEND OUT EMAILS TO USERS
// anonymous async function - using await requires the function that calls it to be async
$(async () => {
    console.log('async2 working')

    // URL for routing
    var emailURL = "http://127.0.0.1:5009/sendEmail"; 

    // get the input from the forms 
    // const form = document.querySelector('#emailInput');
    const emailSubjectInput = document.getElementById('emailSubject');
    const emailBodyInput = document.getElementById('emailBody');

    form2.addEventListener('click', async(event) => {
        console.log('event listener 2 working')

        event.preventDefault();

        // store user input in variables
        const emailSubject = emailSubjectInput.value;
        const emailBody = emailBodyInput.value;

        // create the data object 
        const data = {"emailSubject": emailSubject, "emailBody": emailBody}; 
        console.log(data);

        try {
            const response =
                await fetch(
                    emailURL, { mode: 'cors', method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) }
            );

            // const clonedResponse = response.clone(); // clone the response object before consuming it 
            // const data = await clonedResponse.json(); // call json() on the cloned response object 

            const result = await response.json();
            console.log(result);

            if (response.status === 200) {
                // success case 
                console.log(result.message);
            } else if (response.status == 404) {
                // not found
                showError(result.message);
            } else {
                // unexpected outcome, throw the error
                throw response.status;
            }
        } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        showError
            ('There is a problem sending the email input, please try again later.<br />' + error);
        } // error

    })
});

// ASYNC TO SEND OUT TELEGRAM MESSAGE TO USERS IN CHANNEL
// anonymous async function - using await requires the function that calls it to be async
$(async () => {
    console.log('async4 working')

    // URL for routing
    var messageURL = "http://127.0.0.1:5007/sendEventMessage"; 

    // get the input from the forms 
    const messageBodyInput = document.getElementById('msgBody');

    form4.addEventListener('click', async(event) => {
        console.log('event listener 4 working')

        event.preventDefault();

        // store user input in variables 
        const messageBody = messageBodyInput.value;

        // create the data object 
        const data = {"message": messageBody}; 
        console.log(data);

        try {
            const response =
                await fetch(
                    messageURL, { mode: 'cors', method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) }
            );

            // const clonedResponse = response.clone(); // clone the response object before consuming it 
            // const data = await clonedResponse.json(); // call json() on the cloned response object 

            const result = await response.json();
            console.log(result);

            if (response.status === 200) {
                // success case 
                console.log(result.message);
            } else if (response.status == 404) {
                // not found
                showError(result.message);
            } else {
                // unexpected outcome, throw the error
                throw response.status;
            }
        } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        showError
            ('There is a problem sending the Telegram message input, please try again later.<br />' + error);
        } // error

    })
});


// SHERRY'S PORTION !!!!!!!!
var form3 = document.getElementById('submit3')

$(async() => {
    console.log('async 3 work')

    const titleInput = document.getElementById('eventTitle');
    console.log(titleInput)
    const descInput = document.getElementById('eventDesc');
    const dateInput = document.getElementById('eventDate');
    const startInput = document.getElementById('eventStart');
    const endInput = document.getElementById('eventEnd');
    const maxpaxInput = document.getElementById('eventMaxPax');

    form3.addEventListener('click', async(event) => {
        console.log('event listener 3 working')

        event.preventDefault();

        // create the data object 
        const title = titleInput.value;
        console.log(title)
        const desc = descInput.value;
        const date = dateInput.value;
        const start = startInput.value;
        const end = endInput.value;
        const maxpax = maxpaxInput.value;

        const data = {
            "eventtitle": title, 
            "eventdescription": desc, 
            "eventdate": date, 
            "starttime": start,
            "endtime": end, 
            "maxpax": maxpax
        };
        console.log(data);

        // URL for routing
        var createURL = "http://127.0.0.1:5007/create_event";

        try {
            console.log("testing try");
            const responseCreate =
                await fetch(
                    createURL, { 
                        mode: 'cors', 
                        method: 'POST', 
                        headers: {
                            'Content-Type': 'application/json'
                        }, 
                        body: JSON.stringify(data)
                    }
            );

            const resultCreate = await responseCreate.json();
            console.log("create works");
            console.log(resultCreate);

            if (responseCreate.status === 200) {
                // success case 
                console.log(responseCreate.message);
            } else if (responseCreate.status == 404) {
                // not found
                showError(responseCreate.message);
            } else {
                // unexpected outcome, throw the error
                throw responseCreate.status;
            }
        } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        showError
            ('There is a problem adding the event, please try again later.<br />' + error);
        } // error
    })

});



// display events
const url = 'http://127.0.0.1:3333/events';

async function displayEvents() {
    // console.log('is this even working')
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data)
      const events = data.data.events;
    //   console.log(events)

      const eventsContainer = document.getElementById('displayAllEvents');
      const table = document.createElement('table');
      table.style.borderCollapse = 'collapse';
      table.style.border = '1px solid black'; 
      const thStyle = 'border: 1px solid black; text-align: center; padding: 15px;';
      const tdStyle = 'border: 1px solid black; padding: 10px; text-align:center;';

      const headerRow = table.insertRow();

      const eventID = headerRow.insertCell();
      const nameTitle = headerRow.insertCell();
      const nameDesc = headerRow.insertCell();
      const dateHeader = headerRow.insertCell();
      const startTHeader = headerRow.insertCell();
      const endTHeader = headerRow.insertCell();
      const maxpaxHeader = headerRow.insertCell();
      const currentpaxTHeader = headerRow.insertCell();
    //   const viewParticipants = headerRow.insertCell();
      const deleteTheader = headerRow.insertCell();
      
      eventID.innerHTML = '<b>Event ID</b>';
      nameTitle.innerHTML = '<b>Event Name</b>';
      nameDesc.innerHTML = '<b>Event Description</b>';
      dateHeader.innerHTML = '<b>Event Date</b>';
      startTHeader.innerHTML = '<b>Event Start Time</b>';
      endTHeader.innerHTML = '<b>Event End Time</b>';
      maxpaxHeader.innerHTML = '<b> Maximum Capacity</b>';
      currentpaxTHeader.innerHTML = '<b>Current Capacity</b>';
    //   viewParticipants.innerHTML = '<b>View Sign ups</b>';
      deleteTheader.innerHTML = '<b>Cancel Event</b>';

      eventID.style = thStyle
      nameTitle.style = thStyle
      nameDesc.style = thStyle
      dateHeader.style = thStyle
      startTHeader.style = thStyle
      endTHeader.style = thStyle
      maxpaxHeader.style = thStyle
      currentpaxTHeader.style = thStyle
      deleteTheader.style = thStyle

      const today = new Date();
      const dateRegex = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;

      for (let i = 0; i < events.length; i++) {
        const match = events[i].eventdate.match(dateRegex);
        if (match) {
          const day = parseInt(match[1], 10);
          const month = parseInt(match[2], 10) - 1;
          const year = parseInt(match[3], 10);
          const eventDate = new Date(year, month, day);
          // console.log(eventDate)
          // console.log(today)
          
          if (eventDate > today) {
            const row = table.insertRow();
            const cell1 = row.insertCell();
            const cell2 = row.insertCell();
            const cell3 = row.insertCell();
            const cell4 = row.insertCell();
            const cell5 = row.insertCell();
            const cell6 = row.insertCell();
            const cell7 = row.insertCell();
            const cell8 = row.insertCell();
            const cell9 = row.insertCell();

            cell1.innerHTML = events[i].eventid;
            cell2.innerHTML = events[i].eventtitle;
            cell3.innerHTML = events[i].eventdescription;
            cell4.innerHTML = events[i].eventdate;
            cell5.innerHTML = events[i].starttime;
            cell6.innerHTML = events[i].endtime;
            cell7.innerHTML = events[i].maxpax;
            cell8.innerHTML = events[i].currentpax;

            cell1.style = tdStyle
            cell2.style = tdStyle
            cell3.style = tdStyle
            cell4.style = tdStyle
            cell5.style = tdStyle
            cell6.style = tdStyle
            cell7.style = tdStyle
            cell8.style = tdStyle
            cell9.style = tdStyle

            const deleteButton = document.createElement('button');
            deleteButton.setAttribute('id', `${events[i].eventtitle}`);
            deleteButton.innerText = 'Delete';

            deleteButton.addEventListener("click", function() {
              event.preventDefault();
              console.log("Delete button clicked");

              const eventTitle = deleteButton.getAttribute('id');
              console.log(eventTitle)
              console.log(typeof(eventTitle))

              eventURL = 'http://127.0.0.1:5007/delete_event';
            
              fetch(eventURL, {
                method: 'DELETE',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventTitle),
              })
                .then(response => response.json())
                .then(data => {
                  console.log('Delete event response:', data);
                  console.log(data.message)
                  alert('Event has been successfully removed');
                  location.reload();
                })
                .catch(error => {
                  console.error('Delete event error:', error);
                  alert('An error occurred while deleting the event.');
                });

            });
            cell9.appendChild(deleteButton);
          }
        }
      }
      eventsContainer.appendChild(table);
    } else {
      throw new Error('Error: ' + response.status);
    }

    } catch (error) {
      console.log(error);
    }
    // document.body.appendChild(eventsContainer);
  }

  displayEvents()