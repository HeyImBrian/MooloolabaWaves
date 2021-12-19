


var rows = getData();

//     Date/Time,Hs,Hmax,Tz,Tp,Peak Direction,SST
var months = [];
var days = [];
var years = [];
var hours = [];
var mins = [];



async function getData(){
    const response = await fetch('static/js/WaveData.csv');
    const data = await response.text();
    const rows = data.split('\r\n').slice(1);






    for (let i = 0; i < rows.length-1; i++){
        var dateTime = rows[i];
        var items = dateTime.split(',');

        var date = items[0];
        var splitDates = date.split('/');

        var hour = splitDates[2].slice(5, 7);
        var minute = splitDates[2].slice(8, 10);


        // Day Month Year
        if (i < 35039){
            days.push(splitDates[0]);
            months.push(splitDates[1]);
            years.push(splitDates[2].slice(0, 4));

        // Month Day Year
        } else if (i > 35039){
            months.push(splitDates[0]);
            days.push(splitDates[1]);
            years.push("2019");
        }

        // Hours
        hours.push(hour);

        // Minutes
        mins.push(minute);


    }


    console.log(hours);
    console.log(mins);



}

const labels = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
];

const chartData = {
  labels: labels,
  datasets: [{
    label: 'My First dataset',
    backgroundColor: 'rgb(255, 99, 132)',
    borderColor: 'rgb(255, 99, 132)',
    data: [0, 10, 5, 2, 20, 30, 45],
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