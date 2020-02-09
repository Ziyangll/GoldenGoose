/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 * 
 * For more information visit:
 * https://www.amcharts.com/
 * 
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */
function draw_graph(ticker) {
  // Themes begin
  am4core.useTheme(am4themes_dark);
  am4core.useTheme(am4themes_animated);
  // Themes end

  var chart = am4core.create("chartdiv", am4charts.XYChart);
  var date_amts=[-22,-21,-18,-17,-16,-15,-14,-10,-9,-8,-7,-4,-3,-2,-1,0,3,4,5,6,7];
  var values;

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "http://127.0.0.1:8080/graph/", true); // true for asynchronous 
  xmlHttp.send(JSON.stringify({"ticker":ticker}));
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == XMLHttpRequest.DONE) {

      values=xmlHttp.responseText.split("|");
      var data = [];
  for (var i in date_amts) {
    var date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date_amts[i]);

    data.push({
      date: date,
      value: parseFloat(values[i])
    });
  }

  chart.data = data;

  // Create axes
  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.minGridDistance = 60;

  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

  // Create series
  var series = chart.series.push(new am4charts.LineSeries());
  series.dataFields.valueY = "value";
  series.dataFields.dateX = "date";
  series.tooltipText = "{value}"

  series.tooltip.pointerOrientation = "vertical";

  chart.cursor = new am4charts.XYCursor();
  chart.cursor.snapToSeries = series;
  chart.cursor.xAxis = dateAxis;

  //chart.scrollbarY = new am4core.Scrollbar();
  chart.scrollbarX = new am4core.Scrollbar();
  chart.scrollbarX.parent = chart.bottomAxesContainer;
  chart.zoomOutButton.align = "right";
  chart.zoomOutButton.valign = "bottom";
    }
  }
  return false;
}

function buy_stock(ticker,amount) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "http://127.0.0.1:8080/buy/", true); // true for asynchronous 
  xmlHttp.send(JSON.stringify({"ticker":ticker,"quantity":amount}));
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == XMLHttpRequest.DONE) {

      alert(xmlHttp.responseText);
    }
}
}

function sell_stock(ticker,amount) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "http://127.0.0.1:8080/sell/", true); // true for asynchronous 
  xmlHttp.send(JSON.stringify({"ticker":ticker,"quantity":amount}));
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == XMLHttpRequest.DONE) {
      alert(xmlHttp.responseText);
    }
}
}