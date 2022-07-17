function analyzeText(pi_name) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var requestBody = JSON.stringify({
        pi_name: pi_name
    });
    const request = new Request(
        '/remove-pi/',
        {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            mode: 'same-origin', // Do not send CSRF token to another domain.
            body: requestBody
        }
    )
    fetch(request).then(function (response) {
        // console.log(response);
        window.location.href = "/"
    });
    // console.log(request);
}