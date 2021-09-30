window.addEventListener('DOMContentLoaded', (event) => {
    first_time_load()
    setInterval(reload_page, 5000);
    setInterval(update_balances, 10000);
})

function set_user_id(id) {
    userID = id;
}

var profileValueChart;
var lastTotal = 0;
var userID = 0;

function first_time_load() {
    update_balances()
    $.getJSON('/account_value_data', {
        userID: 2194
    }, function(data) {
        const values = data['values'];
        const dates = data['dates'];

        set_value_text(values)

        const graphData = {
            labels: dates,
            datasets: [{
                label: 'Account Value',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: values
            }]
            };
            
            const config = {
                type: 'line',
                data: graphData,
                options: {
                    elements: {
                        point: {
                            radius: 0
                        }
                    },
                    animation: {
                        duration: 0
                    }
                }
            };
                
            profileValueChart = new Chart(
                document.getElementById('profileValueChart'),
                config
                );
    })
}

function reload_page() {
    $.getJSON('/account_value_data', {
        userID: userID
        }, function(data) {
            reload_graph(data);
            const values = data['values'];
            set_value_text(values);
    })
}

function update_balances() {
    $.getJSON('/account_holdings', {
        userID: userID
    }, function(data) {
        var table = document.getElementById("holdingTable");
        for(var i = table.rows.length - 1; i > 0; i--) {
            table.deleteRow(i);
        }
        data.sort(function(first, second) {return second.value - first.value;});
        data.forEach(function(holding) {
            var row = table.insertRow(-1);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            cell1.innerHTML = holding['asset']
            cell2.innerHTML = holding['balance']
            cell3.innerHTML = holding['value']
        })
    })
}

function set_value_text(values) {
    const roundedValue = Math.round((values.at(-1) + Number.EPSILON) * 100) / 100
    const valueText = document.getElementById("profileValue");
    if (roundedValue > lastTotal) {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "green";
    } else if (roundedValue < lastTotal) {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "red";
    } else {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "white";
    }
    lastTotal = roundedValue;  
}

function reload_graph(data) {
    const values = data['values'];
    const dates = data['dates'];

    const lastValue = values.at(-1);
    const valueText = document.getElementById("profileValue");
    if (lastValue > values.at(-2)) {
        valueText.innerHTML = ("$" + lastValue);
        valueText.style.color = "green";
    } else if (lastValue < values.at(-2)) {
        valueText.innerHTML = ("$" + lastValue);
        valueText.style.color = "red";
    }

    const graphData = {
        labels: dates,
        datasets: [{
            label: 'Account Value',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: values
        }]
        };
        
    profileValueChart.data = graphData;
    profileValueChart.options.animation = false;
    profileValueChart.update()
}