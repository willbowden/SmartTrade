window.addEventListener('DOMContentLoaded', (event) => {
    first_time_load()
    setInterval(reload_graph, 5000);
})

var profileValueChart;

function first_time_load() {
    $.getJSON('/account_value_data', {
        userID: 2194
    }, function(data) {
        const values = data['values'];
        const dates = data['dates'];

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

function reload_graph() {
    $.getJSON('/account_value_data', {
        userID: 2194
    }, function(data) {
        const values = data['values'];
        const dates = data['dates'];

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
    })
}