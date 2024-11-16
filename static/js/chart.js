async function fetchDataAndUpdate() {
    try {
        const response = await fetch("/data");
        const data = await response.json();

        // Update fuel efficiency
        document.getElementById("fuel-efficiency").textContent = data.fuelEfficiency || "Data not available";
        document.getElementById("fuel-efficiency-trend").textContent = data.fuelEfficiencyTrend || "Data not available";
        document.getElementById("health-issues").textContent = data.healthIssues || "Data not available";
        document.getElementById("overallDrivingBehaviour").innerHTML=(data.OverallDrivingBehaviour=="Aggressive" ? `<p style="color:red;">Aggressive</p>` : `<p>Normal</p>`) || "Data not avalable";

        // Update gear predictions
        const gearList = document.getElementById("gear-predictions");
        if (data.gearPredictions) {
            gearList.innerHTML = data.gearPredictions.map(gear => `<li>${gear}</li>`).join('');
        } else {
            gearList.innerHTML = '<li>No gear predictions available</li>';
        }

        // Update turn alerts
        const turnList = document.getElementById("turn-alerts");
        if (data.turnAlerts) {
            turnList.innerHTML = data.turnAlerts.map(alert => alert.sharp_turn ? `<li style="color:red;">Sharp Turn</li>` : `<li>Normal Turn</li>`).join('');
        } else {
            turnList.innerHTML = '<li>No turn alerts available</li>';
        }

        const drivingBehaviour = document.getElementById("driving-predictions");
        if (data.drivingBehaviourPredictions) {
            drivingBehaviour.innerHTML = data.drivingBehaviourPredictions.map(behaviour => behaviour==0 ? `<li style="color:red;">Aggressive</li>` : `<li>Normal</li>`).join('');
        } else {
            drivingBehaviour.innerHTML = '<li>No prediction behaviours available</li>';
        }

        // Prepare data for the driving patterns chart
        if (data.drivingPatterns && data.drivingPatterns.patterns) {
            const timestamps = data.drivingPatterns.patterns.map(item => item.timestamp);
            const speeds = data.drivingPatterns.patterns.map(item => item.gps_speed);

            // Render driving patterns chart
            const ctx = document.getElementById("driving-patterns-chart").getContext("2d");
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: 'GPS Speed (km/h)',
                        data: speeds,
                        backgroundColor: 'rgba(54, 162, 235, 0.9)', // Darker shade of blue
                        borderColor: 'rgba(54, 162, 235, 1)', // Border color for more definition
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: { display: true, text: 'Timestamp', color: 'black' }, // Darker label color
                            ticks: { color: '#333' } // Darker tick color
                        },
                        y: {
                            title: { display: true, text: 'Speed (km/h)', color: '#333' },
                            ticks: { color: 'black' }
                        }
                    }
                }
            });
        } else {
            console.warn("No driving patterns available to display.");
            document.getElementById("driving-patterns-chart").style.display = "none";
        }

    } catch (error) {
        console.error("Error loading data:", error);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    fetchDataAndUpdate(); // Initial fetch
    setInterval(fetchDataAndUpdate, 30000); // Repeat every 30 seconds
});
