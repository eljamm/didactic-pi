function analyzeText(raspi_id, raspi_name) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var requestBody = JSON.stringify({
        raspi_id: raspi_id,
        raspi_name: raspi_name
    });

    const myModal = new bootstrap.Modal('#deleteModal', {
        keyboard: false
    })

    const modalToggle = document.getElementById('deleteModal'); myModal.show(modalToggle)

    document.querySelector('#deletePi').onclick = function (e) {
        const request = new Request(
            '/remove-pi/',
            {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin', // Do not send CSRF token to another domain.
                body: requestBody
            }
        )
        console.log(request);

        fetch(request).then(function (response) {
            window.location.href = "/remove-pi/"
        });
    };
}