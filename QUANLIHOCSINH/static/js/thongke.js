document.addEventListener("DOMContentLoaded", function () {
    function getDataFromTable(tableId) {
        const table = document.getElementById(tableId);
        const labels = [];
        const siSo = [];
        const soLuongDat = [];
        const tyLe = [];

        const rows = table.querySelectorAll("tbody tr");
        rows.forEach(row => {
            const cells = row.querySelectorAll("td, th");
            labels.push(cells[1].innerText.trim()); // Lớp
            siSo.push(parseInt(cells[2].innerText.trim()) || 0); // Sĩ số
            soLuongDat.push(parseInt(cells[3].innerText.trim()) || 0); // Số lượng đạt
            tyLe.push(parseFloat(cells[4].innerText.trim().replace('%', '')) || 0); // Tỷ lệ
        });

        return { labels, siSo, soLuongDat, tyLe };
    }

    const { labels, siSo, soLuongDat, tyLe } = getDataFromTable("dataTable");

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Sĩ số',
                    data: siSo,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Số lượng đạt',
                    data: soLuongDat,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Tỷ lệ (%)',
                    data: tyLe,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    type: 'line'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const ctxPie = document.getElementById('myPieChart').getContext('2d');
    const myPieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tỷ lệ (%)',
                data: tyLe,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return `${tooltipItem.label}: ${tooltipItem.raw}%`;
                        }
                    }
                }
            }
        }
    });
});