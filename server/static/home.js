window.addEventListener('DOMContentLoaded', (event) => {
    first_time_load()
    setInterval(reload_page, 5000);
})

var profileValueChart;

function first_time_load() {
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
        userID: 2194
    }, function(data) {
        reload_graph(data);
        const values = data['values'];
        set_value_text(values)
    })
}

function set_value_text(values) {
    console.log(values)
    const lastValue = values.at(-1);
    const roundedValue = Math.round((lastValue + Number.EPSILON) * 100) / 100
    const valueText = document.getElementById("profileValue");
    if (lastValue > values.at(-2)) {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "green";
    } else if (lastValue < values.at(-2)) {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "red";
    } else {
        valueText.innerHTML = ("$" + roundedValue);
        valueText.style.color = "white";
    }
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