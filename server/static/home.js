window.addEventListener('DOMContentLoaded', (event) => {
    load_graph()
})

function load_graph() {
    const labels = [1, 2, 3, 4, 5, 6, 7];
        
        const data = {
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
            data: data,
            options: {}
        };
        
        var myChart = new Chart(
            document.getElementById('profileChart'),
            config
          );
}