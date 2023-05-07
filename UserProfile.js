var transactionIDInput = "";
var transactionAmtInput = "";
var confirmEmailInput = "";

let imptEmail;


// form + qr code display 
const form = document.querySelector('#form');
var formContainer = document.getElementById('transactionDetails');

let qrContent = document.getElementById("confirmEmail").value;

document.addEventListener('DOMContentLoaded', function() {
form.addEventListener('submit', function(event) {

    // blocks the page from refreshing 
    event.preventDefault();

    var transactionIDInput = document.getElementById('transactionID');
    var transactionAmtInput = document.getElementById('transactionAmt');
    var confirmEmailInput = document.getElementById("confirmEmail");

    $(async() => {
      var url = 'http://127.0.0.1:5100/update_point';
      imptEmail = confirmEmailInput.value;
  
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            transaction_id: transactionIDInput.value,
            transaction_value: transactionAmtInput.value,
            userEmail: imptEmail
          })
        });
        
        const clonedResponse = response.clone(); // clone the response object before consuming it
        const data = await clonedResponse.json(); // call json() on the cloned response object

        const result = data;
        console.log(result)
  
        if (response.status === 200 && result.reward) {
          // intro block + name
          var greeting = document.getElementById('greeting')
          greeting.innerHTML = 'WELCOME BACK,'

          var name = result.reward.name;
          var nameContainer = document.getElementById('name')
          nameContainer.innerHTML = name

          // TRANSACTION (OVERALL)
          const initialPaymentDiv = document.getElementById('initialPayment')
          const finalPaymentDiv = document.getElementById('finalPayment')
          const actualFinal = document.getElementById('actualFinal')
          let initialPayment = Number(transactionAmtInput.value)
          initialPayment = initialPayment.toFixed(2)

          initialPaymentDiv.innerHTML = '<b>Transaction Amount:</b> $' + initialPayment;
          finalPaymentDiv.style.display = 'inline';
          actualFinal.innerHTML = initialPayment;
          actualFinal.style.display = 'inline';
  
          //  your current tier image 
          var tier = result.reward.tier;
          var tierContainer = document.getElementById('tierImg')
          if (tier == 'Bronze') {
            tierContainer.src = "assets/bronze.png";
          } else if (tier == 'Silver') {
            tierContainer.src = "assets/silver.png";
          } else {
            tierContainer.src = "assets/gold.png";
          }
  
          // your current progress 
          var currentPoints = result.reward.total_points
          console.log(currentPoints)
  
          if (tier == 'Bronze') {
            var minValue = 0;
            var maxValue = 300;
          } else if (tier == 'Silver') {
            var minValue = 301;
            var maxValue = 600;
          } else {
            var minValue = 601;
            var maxValue = currentPoints;
          }
  
          // console.log(typeof(currentPoints))
          // console.log(currentPoints)
  
          // setting main progress bar
          const progress = document.querySelector('.progress');
          const progressBar = document.querySelector('.progress-bar');
  
          progress.setAttribute('aria-valuemin', minValue);
          progress.setAttribute('aria-valuemax', maxValue);
          progress.setAttribute('aria-valuenow', currentPoints);
          progressBar.setAttribute("style", "width: " + currentPoints + ";");
  
          // setting labels for progress bar 
          const minLabel = document.querySelector('.min-label');
          const maxLabel = document.querySelector('.max-label');
          minLabel.innerHTML = minValue
          maxLabel.innerHTML = maxValue
  
  
          // current progress
          var more = 0
          if (tier == 'Bronze' || tier == 'Silver') {
            more = maxValue - currentPoints
          } else {
            more = 'Well done! Keep saving to maintain your status as a Gold Pal <3'
          }
  
          var morePoints = document.getElementById('morePoints1')
          var moreTxt = document.getElementById('morePoints2')
  
          if (tier == 'Gold') {
            morePoints.innerHTML = ''
            moreTxt.innerHTML = more
          } else {
            morePoints.innerHTML = more
          }

          // rewards -- rachel
          // console.log("This is tier", tier)

          var bronzebuttonContainer = document.getElementById('bronzebutton')
          var silverbuttonContainer = document.getElementById('silverbutton')
          var goldbuttonContainer = document.getElementById('goldbutton')

          if (tier == 'Bronze') {
            bronzebuttonContainer = document.getElementById('bronzebutton')
            silverbuttonContainer = document.getElementById('silverbutton').disabled = true;
            goldbuttonContainer = document.getElementById('goldbutton').disabled = true;
          } else if (tier == 'Silver') {
            bronzebuttonContainer = document.getElementById('bronzebutton')
            silverbuttonContainer = document.getElementById('silverbutton')
            goldbuttonContainer = document.getElementById('goldbutton').disabled = true;
          } else if (tier == 'Gold') {
            bronzebuttonContainer = document.getElementById('bronzebutton')
            silverbuttonContainer = document.getElementById('silverbutton')
            goldbuttonContainer = document.getElementById('goldbutton')
          }

        } else {
          throw response.status;
        } 
      } catch (error) {
        console.log(error)
        // showError('error !!!!!!! <br>' + error);
      }
    })

    var formFields = formContainer.querySelectorAll('input, select');

    // disable all input fields
    formFields.forEach(field => {
      field.disabled = true;
    });

    const qrDiv = document.getElementById('qr');
    const tierDiv = document.getElementById('tier')
    const progressTierDiv = document.getElementById('progressTier')
    const eventsDiv = document.getElementById('events')
    const morePoints1 = document.getElementById('morePoints1')
    const morePoints2 = document.getElementById('morePoints2')
    const rewardsContainer = document.getElementById('container')
    const paymentContainer = document.getElementById('payment')

    // qrDiv.style.display = 'block';
    tierDiv.style.display = 'block';
    progressTierDiv.style.display = 'block';
    eventsDiv.style.display = 'block';
    morePoints1.style.display = 'inline';
    morePoints2.style.display = 'inline';
    rewardsContainer.style.display = 'block';
    paymentContainer.style.display = 'block';
    console.log('block is working')
  })
});



// EVENTS
const eventURL = 'http://127.0.0.1:3333/events';

async function displayEvents() {
  try {
    console.log('is this even working???')
    const response = await fetch(eventURL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data)
      const events = data.data.events;

      const eventsContainer = document.getElementById('availableEvents');
      const table = document.createElement('table');
      table.style.borderCollapse = 'collapse';
      table.style.border = '1px solid black'; 
      const thStyle = 'border: 1px solid black; text-align: center';
      const tdStyle = 'border: 1px solid black;';

      const headerRow = table.insertRow();
      const nameTitle = headerRow.insertCell();
      const nameDesc = headerRow.insertCell();
      const dateHeader = headerRow.insertCell();
      const startTHeader = headerRow.insertCell();
      const endTHeader = headerRow.insertCell();
      const join = headerRow.insertCell();
      
      nameTitle.innerHTML = '<b>Event Name</b>';
      nameDesc.innerHTML = '<b>Event Description</b>';
      dateHeader.innerHTML = '<b>Event Date</b>';
      startTHeader.innerHTML = '<b>Event Start Time</b>';
      endTHeader.innerHTML = '<b>Event End Time</b>';
      join.innerHTML = '<b>Sign Up</b>';

      nameTitle.style = thStyle
      nameDesc.style = thStyle
      dateHeader.style = thStyle
      startTHeader.style = thStyle
      endTHeader.style = thStyle
      join.style = thStyle

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
            console.log('yes')
            const row = table.insertRow();
            const cell1 = row.insertCell();
            const cell2 = row.insertCell();
            const cell3 = row.insertCell();
            const cell4 = row.insertCell();
            const cell5 = row.insertCell();
            const cell6 = row.insertCell();

            cell1.innerHTML = events[i].eventtitle;
            cell2.innerHTML = events[i].eventdescription;
            cell3.innerHTML = events[i].eventdate;
            cell4.innerHTML = events[i].starttime;
            cell5.innerHTML = events[i].endtime;

            cell1.style = tdStyle
            cell2.style = tdStyle
            cell3.style = tdStyle
            cell4.style = tdStyle
            cell5.style = tdStyle
            cell6.style = tdStyle
            
            const joinButton = document.createElement('button');
            joinButton.setAttribute('id', `${events[i].eventid}+${events[i].eventtitle}`);
            joinButton.innerText = 'Join';

            joinButton.addEventListener("click", function() {
              console.log("Join button clicked");

              const idTitle = joinButton.getAttribute('id');
              const [eventId, eventTitle] = idTitle.split('+');

              console.log(imptEmail)

              const participantAndEvent = {
                userEmail: imptEmail,
                eventid: eventId,
                eventtitle: eventTitle
              };
            
              fetch('http://127.0.0.1:5008/join_event', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(participantAndEvent),
              })
                .then(response => response.json())
                .then(data => {
                  // console.log('Join event response:', data);
                  console.log(data.message)
                  if (data.message == undefined) {
                    var message = 'You have successfully joined the event! \nRemember to join our telegram channel for the latest updates <3'
                    alert(message)
                  } else {
                    alert(data.message);
                  }
                })
                .catch(error => {
                  console.error('Join event error:', error);
                  alert('An error occurred while joining the event.');
                });

            });

            cell6.appendChild(joinButton);
          }
        } else {
          console.error(`Invalid date format for event ${events[i].eventtitle}`);
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
  // .catch(error => {
  //   console.log(error);
  // });

  displayEvents()

// REWARDS?? (hope it works)

// bronze rewards
  $(async() => {
    const now = new Date();
    const currentMonth = now.getMonth() + 1;

    var bronzeURL = "http://127.0.0.1:5002/rewards/".concat(currentMonth + '/Bronze' + '/0')

    // console.log('async working')
    // console.log("this is bronzeurl", bronzeURL)

    try {
        const response = await fetch(bronzeURL,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const clonedResponse = response.clone(); // clone the response object before consuming it
        const data = await clonedResponse.json(); // call json() on the cloned response object

        // bronze data
        const bronzeresult = data;
        console.log("this is bronzeresult", bronzeresult)

        // check bronze reward name / information
        var bronzeinfo = bronzeresult.reward.rewardname;
        var bronzeinfoContainer = document.getElementById('brewardinfo')
        bronzeinfoContainer.innerHTML = bronzeinfo

        // check if bronze reward is available
        var bronzeQuantity = bronzeresult.reward.quantity
        // console.log(bronzeQuantity)

        // generate bronze qr code
        let bronzeQRContent = bronzeresult.reward.rewardid
        let bronzeQrCode

        console.log("this is", bronzeQRContent)

        function generatebronzeQR(bronzeQRContent) {
          return new QRCode("bronzeQR", {
            text: bronzeQRContent,
            width: 128,
            height: 128,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H,
          });
          }
        
        if (bronzeQrCode == null) {
          // Generate code initially
          bronzeQrCode = generatebronzeQR(bronzeQRContent);
          console.log("qr code generated", bronzeQrCode)
        } else {
          // If code already generated then make
          // again using same object
          bronzeQrCode.makeCode(bronzeQRContent);
        }

        // bronze disabled button works when qty=0! huat!!!!!
        if (bronzeQuantity=0) {
            var bronzebuttonContainer = document.getElementById('bronzebutton').disabled = true;
        }

        // TRANSACTION (BRONZE)
        const discountDiv = document.getElementById('discountPayment')
        const actualDiscount = document.getElementById('actualDiscount')

        bronzeButton = document.getElementById('bronzebutton')
        console.log(bronzeQRContent)

        bronzeButton.addEventListener('click', function() {

          // THIS PART !!!!!!! REDUCING THE QUANTITY
          bronzeLastURL = 'http://127.0.0.1:5002/rewards/' + bronzeQRContent
          console.log(bronzeLastURL)
          fetch(bronzeLastURL, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                }
              })
          
          .then(response => response.json())
          .then(data => {
            console.log(data.message)
          })
          .catch(error => {
            console.error('Bronze Reward Reduce error:', error);
          });

          discountDiv.style.display = 'block';

          initialPayment = Number(document.getElementById('transactionAmt').value)
          let bronzeDiscount = bronzeresult.reward.discount
          let calculatedDisc = bronzeDiscount * initialPayment;
          calculatedDisc = calculatedDisc.toFixed(2)
          console.log(bronzeDiscount)
          console.log(calculatedDisc)
          actualDiscount.innerHTML = '<b>Discount Applied:</b> $' + calculatedDisc;

          const actualFinal = document.getElementById('actualFinal')
          let reallyLast = initialPayment - calculatedDisc
          reallyLast = reallyLast.toFixed(2)
          console.log(reallyLast)
          actualFinal.innerHTML = reallyLast;

          document.getElementById('bronzebutton').disabled = true;
          document.getElementById('silverbutton').disabled = true;
          document.getElementById('goldbutton').disabled = true;
          document.getElementById('spbutton').disabled = true;
        })

    // CODE ABOVE THIS LINE
        }  // Try Ends
    catch(error){
        // console.log(error)
    }     
})


// silver rewards
$(async() => {
    const now = new Date();
    const currentMonth = now.getMonth() + 1;

    var silverURL = "http://127.0.0.1:5002/rewards/".concat(currentMonth + '/Silver' + '/0')

    // console.log('async working')
    // console.log("this is silverurl", silverURL)

    try {
        const response = await fetch(silverURL,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const clonedResponse = response.clone(); // clone the response object before consuming it
        const data = await clonedResponse.json(); // call json() on the cloned response object

        // silver data
        const silverresult = data;
        // console.log(silverresult)

        // check silver reward name / information
        var silverinfo = silverresult.reward.rewardname;
        var silverinfoContainer = document.getElementById('srewardinfo')
        silverinfoContainer.innerHTML = silverinfo

        // check if silver reward is available
        var silverQuantity = silverresult.reward.quantity
        // console.log(silverQuantity)

        // generate silver rewards qr code
        let silverQRContent = silverresult.reward.rewardid
        let silverQrCode

        console.log("this is silverQRContent", silverQRContent)

        function generatesilverQR(silverQRContent) {
          return new QRCode("silverQR", {
            text: silverQRContent,
            width: 128,
            height: 128,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H,
          });
          }
        
        if (silverQrCode == null) {
          // Generate code initially
          silverQrCode = generatesilverQR(silverQRContent);
          console.log("qr code generated", silverQrCode)
        } else {
          // If code already generated then make
          // again using same object
          silverQRCode.makeCode(silverQRContent);
        }

        // silver disabled button works when qty=0! huat!!!!!
        if (silverQuantity=0) {
            var silverbuttonContainer = document.getElementById('silverbutton').disabled = true;
        }

        // TRANSACTION (SILVER)
        const discountDiv = document.getElementById('discountPayment')
        const actualDiscount = document.getElementById('actualDiscount')

        silverButton = document.getElementById('silverbutton')
        silverButton.addEventListener('click', function() {
          silverLastURL = 'http://127.0.0.1:5002/rewards/' + silverQRContent
          console.log(silverLastURL)
          fetch(silverLastURL, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                }
              })
          
          .then(response => response.json())
          .then(data => {
            console.log(data.message)
          })
          .catch(error => {
            console.error('Silver Reward Reduce error:', error);
          });
            
          discountDiv.style.display = 'block';

          initialPayment = Number(document.getElementById('transactionAmt').value)
          let silverDiscount = silverresult.reward.discount
          let calculatedDisc = silverDiscount * initialPayment;
          calculatedDisc = calculatedDisc.toFixed(2)
          console.log(silverDiscount)
          console.log(calculatedDisc)
          actualDiscount.innerHTML = '<b>Discount Applied:</b> $' + calculatedDisc;

          const actualFinal = document.getElementById('actualFinal')
          let reallyLast = initialPayment - calculatedDisc
          reallyLast = reallyLast.toFixed(2)
          console.log(reallyLast)
          actualFinal.innerHTML = reallyLast;

          document.getElementById('bronzebutton').disabled = true;
          document.getElementById('silverbutton').disabled = true;
          document.getElementById('goldbutton').disabled = true;
          document.getElementById('spbutton').disabled = true;
        });
    
    // CODE ABOVE THIS LINE
        }  // Try Ends

    catch(error){
        // console.log(error)
    }     
})

// gold rewards
$(async() => {
    const now = new Date();
    const currentMonth = now.getMonth() + 1;

    var goldURL = "http://127.0.0.1:5002/rewards/".concat(currentMonth + '/Gold' + '/0')   

    // console.log('async working')
    // console.log("this is goldurl", goldURL)

    try {
        const response = await fetch(goldURL,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const clonedResponse = response.clone(); // clone the response object before consuming it
        const data = await clonedResponse.json(); // call json() on the cloned response object

        // gold data
        const goldresult = data;
        // console.log(goldresult)

        // check gold reward name / information
        var goldinfo = goldresult.reward.rewardname;
        var goldinfoContainer = document.getElementById('grewardinfo')
        goldinfoContainer.innerHTML = goldinfo

        // check if gold reward is available
        var goldQuantity = goldresult.reward.quantity
        // console.log(goldQuantity)

        // generate gold rewards qr code
        let goldQRContent = goldresult.reward.rewardid
        let goldQrCode

        console.log("this is goldQRContent", goldQRContent)

        function generategoldQR(goldQRContent) {
          return new QRCode("goldQR", {
            text: goldQRContent,
            width: 128,
            height: 128,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H,
          });
          }
        
        if (goldQrCode == null) {
          // Generate code initially
          goldQrCode = generategoldQR(goldQRContent);
          console.log("qr code generated", goldQrCode)
        } else {
          // If code already generated then make
          // again using same object
          goldQRCode.makeCode(goldQRContent);
        }

        // gold disabled button works when qty=0! huat!!!!!
        if (goldQuantity=0) {
            var goldbuttonContainer = document.getElementById('goldbutton').disabled = true;
        }

        // TRANSACTION (GOLD)
        const discountDiv = document.getElementById('discountPayment')
        const actualDiscount = document.getElementById('actualDiscount')

        goldButton = document.getElementById('goldbutton')
        goldButton.addEventListener('click', function() {
          goldLastURL = 'http://127.0.0.1:5002/rewards/' + goldQRContent
          console.log(goldLastURL)
          fetch(goldLastURL, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                }
              })
          
          .then(response => response.json())
          .then(data => {
            console.log(data.message)
          })
          .catch(error => {
            console.error('Gold Reward Reduce error:', error);
          });

          discountDiv.style.display = 'block';

          initialPayment = Number(document.getElementById('transactionAmt').value)
          let goldDiscount = goldresult.reward.discount
          let calculatedDisc = goldDiscount * initialPayment;
          calculatedDisc = calculatedDisc.toFixed(2)
          console.log(goldDiscount)
          console.log(calculatedDisc)
          actualDiscount.innerHTML = '<b>Discount Applied:</b> $' + calculatedDisc;

          const actualFinal = document.getElementById('actualFinal')
          let reallyLast = initialPayment - calculatedDisc
          reallyLast = reallyLast.toFixed(2)
          console.log(reallyLast)
          actualFinal.innerHTML = reallyLast;

          document.getElementById('bronzebutton').disabled = true;
          document.getElementById('silverbutton').disabled = true;
          document.getElementById('goldbutton').disabled = true;
          document.getElementById('spbutton').disabled = true;
        });
    
    // CODE ABOVE THIS LINE
        }  // Try Ends

    catch(error){
        // console.log(error)
    }     
})

// sp rewards
$(async() => {
  const now = new Date();
  const currentMonth = now.getMonth() + 1;

  var spURL = "http://127.0.0.1:5002/rewards/".concat(currentMonth + '/Bronze' + '/1')   

  // console.log('async working')
  console.log("this is ", spURL)

  try {
      const response = await fetch(spURL,{
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      })
      const clonedResponse = response.clone(); // clone the response object before consuming it
      const data = await clonedResponse.json(); // call json() on the cloned response object

      // sp data
      const spresult = data;
      console.log(spresult)

      // check sp reward name / information
      var spinfo = spresult.reward.rewardname;
      var spinfoContainer = document.getElementById('sprewardinfo')
      spinfoContainer.innerHTML = spinfo

      // check if sp reward is available
      var spQuantity = spresult.reward.quantity
      console.log(spQuantity)

      // generate sp rewards qr code
      let spQRContent = spresult.reward.rewardid
      let spQrCode

      console.log("this is spQRContent", spQRContent)

      function generatespQR(spQRContent) {
        return new QRCode("spQR", {
          text: spQRContent,
          width: 128,
          height: 128,
          colorDark: "#000000",
          colorLight: "#ffffff",
          correctLevel: QRCode.CorrectLevel.H,
        });
        }
      
      if (spQrCode == null) {
        // Generate code initially
        spQrCode = generatespQR(spQRContent);
        console.log("qr code generated", spQrCode)
      } else {
        // If code already generated then make
        // again using same object
        spQrCode.makeCode(spQRContent);
      }

      // gold disabled button works when qty=0! huat!!!!!
      if (spQuantity=0) {
          var spbuttonContainer = document.getElementById('spbutton').disabled = true;
      }

      // TRANSACTION (SPECIAL)
      const discountDiv = document.getElementById('discountPayment')
      const actualDiscount = document.getElementById('actualDiscount')

      spButton = document.getElementById('spbutton')
      spButton.addEventListener('click', function() {
        spLastURL = 'http://127.0.0.1:5002/rewards/' + spQRContent
          console.log(spLastURL)
          fetch(spLastURL, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                }
              })
          
          .then(response => response.json())
          .then(data => {
            console.log(data.message)
          })
          .catch(error => {
            console.error('Special Reward Reduce error:', error);
          });

        discountDiv.style.display = 'block';

        initialPayment = Number(document.getElementById('transactionAmt').value)
        let spDiscount = spresult.reward.discount
        let calculatedDisc = spDiscount * initialPayment;
        calculatedDisc = calculatedDisc.toFixed(2)
        console.log(spDiscount)
        console.log(calculatedDisc)
        actualDiscount.innerHTML = '<b>Discount Applied:</b> $' + calculatedDisc;

        const actualFinal = document.getElementById('actualFinal')
        let reallyLast = initialPayment - calculatedDisc
        reallyLast = reallyLast.toFixed(2)
        console.log(reallyLast)
        actualFinal.innerHTML = reallyLast;

        document.getElementById('bronzebutton').disabled = true;
        document.getElementById('silverbutton').disabled = true;
        document.getElementById('goldbutton').disabled = true;
        document.getElementById('spbutton').disabled = true;
      });
  
  // CODE ABOVE THIS LINE
      }  // Try Ends

  catch(error){
      // console.log(error)
  }     
})