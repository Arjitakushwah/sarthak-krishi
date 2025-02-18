document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("weatherForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(this);

        fetch("/get_weather", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let resultDiv = document.getElementById("weatherResult");

            if (data.error) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <h4>Weather in ${document.getElementById("city").value}</h4>
                        <p><strong>Temperature:</strong> ${data.temperature} °C</p>
                        <p><strong>Humidity:</strong> ${data.humidity} %</p>
                        <p><strong>Condition:</strong> ${data.description}</p>
                        <p><strong>Wind Speed:</strong> ${data.wind_speed} m/s</p>
                    </div>
                `;
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
