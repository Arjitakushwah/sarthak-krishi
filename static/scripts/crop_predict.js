document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cropForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form reload

        let formData = new FormData(this);

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let recommendationDiv = document.getElementById("recommendationResult");
            recommendationDiv.innerHTML = `<div class="alert alert-success text-center">
                <h4>Your recommended crop is: <span class="text-success">${data.recommendation}</span></h4>
            </div>`;
        })
        .catch(error => console.error("Error:", error));
    });
});
