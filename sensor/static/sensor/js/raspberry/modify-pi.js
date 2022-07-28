function analyzeText(raspi_id, raspi_name, raspi_address) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const name = document.querySelector('#id_name');
    const address = document.querySelector('#id_address');

    name.value = raspi_name
    address.value = raspi_address

    const myModal = new bootstrap.Modal('#modifyModal', {
        keyboard: false
    })

    const modalToggle = document.getElementById('modifyModal'); myModal.show(modalToggle)

    document.querySelector('#modifyPi').onclick = function (e) {
        const newName = name.value
        const newAddress = address.value

        var requestBody = JSON.stringify({
            raspi_id: raspi_id,
            raspi_name: newName,
            raspi_address: newAddress
        });

        const request = new Request(
            '/modify-pi/',
            {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin', // Do not send CSRF token to another domain.
                body: requestBody,
                credentials: 'include'
            }
        )

        fetch(request).then(function (response) {
            window.location.href = "/modify-pi/"
        });
    };
}