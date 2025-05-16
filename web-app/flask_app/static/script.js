// static/js/piechart.js

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('diskPieChart').getContext('2d');

  const green = parseInt(document.getElementById("green-count").value);
  const blue = parseInt(document.getElementById("blue-count").value);

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Green', 'Blue'],
      datasets: [{
        label: 'Disk Color',
        data: [green, blue],
        backgroundColor: ['#00e676', '#2979ff'],
        borderColor: '#ffffff',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#525f7f',
            font: {
              size: 14,
              weight: '600'
            }
          }
        }
      }
    }
  });
});
