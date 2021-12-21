


var rows = [];

//     Date/Time,Hs,Hmax,Tz,Tp,Peak Direction,SST
var months = [];
var days = [];
var years = [];
var hours = [];
var mins = [];

var dateTimes = [];
var hs = [];
var hMax = [];
var tz = [];
var tp = [];
var peakDirection = [];
var temperature = [];


var highestTemps2017 = []; // Contains an extra value at the beginning of the array
var highestTemps2018 = [];







async function getData(){
    const response = await fetch('./static/js/wavedata.csv');
    const data = await response.text();
    const rows = await data.split('\r\n').slice(1);

    console.log(data.slice(0, 50));
    console.log(rows[5]);

    var currHighest = 0;
    var currMonth = 1;

    for (let i = 0; i < rows.length-1; i++){
        var dateTime = rows[i];
        var items = dateTime.split(',');
        dateTimes.push(items[0]);

        var date = items[0];
        var splitDates = date.split('/');

        var hour = splitDates[2].slice(5, 7);
        var minute = splitDates[2].slice(8, 10);




        // Fixing the -99.9 values
        for (let j = 0; j < items.length; j++){
            if (items[j] == "-99.9"){

                currAddIndex = 0;
                while (parseFloat(items[j]) < 0){
                    items[j] = (((items[j - (7 * currAddIndex)]) + (items[j + (7 * currAddIndex)])) / 2);
                    currAddIndex += 1;
                }

            }
        }



        // This is required because the days and months swap at a certain point in the data.
        // Day Month Year
        if (i < 35039){
            months.push(parseInt(splitDates[0]));
            days.push(parseInt(splitDates[1]));
            years.push(parseInt(splitDates[2].slice(0, 4)));

        // Month Day Year
        } else if (i > 35039){
            days.push(parseInt(splitDates[0]));
            months.push(parseInt(splitDates[1]));
            years.push("2019");
        }



        // Gathering the highest temps
        var temp = items[6];
        if (i < 17509){ // 2017
            if (temp > currHighest){
                currHighest = temp;
            }

            // Increase month index
            if (i % 1440 == 0){
                currMonth += 1;
                highestTemps2017.push(currHighest);
                currHighest = 0;

                if (currMonth == 13){
                    currMonth = 1;
                }
            }
        } else if (i < 35040){ // 2018
            if (temp > currHighest){
                currHighest = temp;
            }

            // Increase month index
            if (i % 1440 == 0){
                currMonth += 1;
                highestTemps2018.push(currHighest);
                currHighest = 0;

                if (currMonth == 13){
                    currMonth = 1;
                }
            }
        }





        // Hours
        hours.push(hour);

        // Minutes
        mins.push(minute);


        // Hs,Hmax,Tz,Tp,Peak Direction,SST
        hs.push(items[1]);
        hMax.push(items[2]);
        tz.push(items[3]);
        tp.push(items[4]);
        peakDirection.push(items[5]);
        temperature.push(items[6]);
    }
}



// Get the predicted temperature from the HTML
var tempText = document.getElementById("predictedText").innerHTML;
var predictedTemp = parseInt(tempText.slice(49, 51));
var tempAsWords = document.getElementById("tempAsWords");
var cToF = ((predictedTemp * (9/5)) + 32);

tempAsWords.innerHTML = "(" + Math.round(cToF * 10)/10 + " degrees Fahrenheit)<br>";

// Add text to make the temperature more relatable
if (predictedTemp > 37){
    tempAsWords.innerHTML += "This is hot tub temperature.";
} else if (predictedTemp > 32){
    tempAsWords.innerHTML += "This is great for warm water relaxation.";
} else if (predictedTemp > 28){
    tempAsWords.innerHTML += "This is about the temperature used at hotels.";
} else if (predictedTemp > 22){
    tempAsWords.innerHTML += "This temperature is comfortable for most people.";
} else if (predictedTemp > 16){
    tempAsWords.innerHTML += "This temperature is considered chilly.";
}






async function createChart1(){
    rows = await getData();

    var tempLabels = dateTimes.slice(0, 47);
    var tempData = temperature.slice(0, 47);


    const chartData = {
      labels: tempLabels,
      datasets: [{
        label: 'Relationship Between Time of Day and Temperature',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: tempData,
      }]
    };

    const config = {
      type: 'line',
      data: chartData,
      options: {}
    };

    const myChart = new Chart(
        document.getElementById('firstChart'),
        config
    );
}


createChart2();
async function createChart2(){
    await createChart1();
    createChart3();
    createChart4();

    var tempDT = months;
    var tempData = temperature;



    const chartData = {
      labels: tempDT,
      datasets: [{
        label: 'Relationship Between Month and Temperature',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: tempData,
      }]
    };

    const config = {
      type: 'scatter',
      data: chartData,
      options: {}
    };

    const myChart = new Chart(
        document.getElementById('secondChart'),
        config
    );
}


function createChart3() {
  var myTableDiv = document.getElementById("thirdChart");

  var table = document.createElement('TABLE');
  table.border = '1';

  var tableBody = document.createElement('TBODY');
  table.appendChild(tableBody);



  // Set the headers
    var tr = document.createElement('TR');
    tableBody.appendChild(tr);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Date Time"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Significant Wave Height"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Maximum Wave Height"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Zero Upcrossing"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Peak Wave Energy"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Peak Direction"));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode("Temperature"));
    tr.appendChild(td);


  // Fill table rows with data
  for (var i = 0; i < 30; i++) {
    var tr = document.createElement('TR');
    tableBody.appendChild(tr);


    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(dateTimes[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(hs[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(hMax[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(tz[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(tp[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(peakDirection[i]));
    tr.appendChild(td);

    var td = document.createElement('TD');
    td.width = '200';
    td.appendChild(document.createTextNode(temperature[i]));
    tr.appendChild(td);

  }
  myTableDiv.appendChild(table);
}











function createChart4(){
    highestTemps2017.shift();

    const data = {
      labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      datasets: [
        {
          label: '2017',
          data: highestTemps2017,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgb(255, 99, 132)',
          fill: false
        },
        {
          label: '2018',
          data: highestTemps2018,
          borderColor: 'rgb(99, 255, 132)',
          backgroundColor: 'rgb(99, 255, 132)',
          fill: false
        }
      ]
    };






    const chartData = {
      labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      datasets: [{
        label: 'Relationship Between Month and Temperature',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: data,
      }]
    };

    const config = {
      type: 'radar',
      data: data,
      options: {
        plugins: {
          filler: {
            propagate: false
          },
          'samples-filler-analyser': {
            target: 'chart-analyser'
          }
        },
        interaction: {
          intersect: true
        }
      }
    };


    const myChart = new Chart(
        document.getElementById('fourthChart'),
        config
    );



}