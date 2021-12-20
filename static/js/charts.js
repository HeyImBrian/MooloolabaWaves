


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


async function getData(){
    const response = await fetch('static/js/WaveData.csv');
    const data = await response.text();
    const rows = data.split('\r\n').slice(1);


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



        // Day Month Year
        if (i < 35039){
            months.push(splitDates[0]);
            days.push(splitDates[1]);
            years.push(splitDates[2].slice(0, 4));

        // Month Day Year
        } else if (i > 35039){
            days.push(splitDates[0]);
            months.push(splitDates[1]);
            years.push("2019");
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





//createChart1();
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


function createChart3(){
    createChart1();
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