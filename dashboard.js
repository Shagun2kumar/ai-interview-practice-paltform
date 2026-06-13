async function load(){
    let res = await fetch("/dashboard");
    let data = await res.json();

    if(data.length === 0){
        alert("No data yet. Submit answers first.");
        return;
    }

    let labels = data.map((x, i) => "Attempt " + (i+1));
    let scores = data.map(x => x[1]);

    // total attempts
    document.getElementById("total").innerText = data.length;

    // average score
    let avg = scores.reduce((a,b)=>a+b,0) / scores.length;
    document.getElementById("avg").innerText = avg.toFixed(2);

    // chart
    new Chart(document.getElementById("c"), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "Performance Trend",
                data: scores,
                fill: true,
                tension: 0.3
            }]
        }
    });
}

load();





