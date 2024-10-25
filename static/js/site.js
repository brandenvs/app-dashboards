const checkbox = document.getElementById("checkbox")

checkbox.addEventListener("change", () => {
    toggleTheme();
});

const toastLiveExample = document.getElementById('errorToast');
const toast = new bootstrap.Toast(toastLiveExample, { autohide: true });


function getTheme() {
    selectedTheme = '';

    $.ajax({
        url: '/fetch-theme/',
        type: 'GET',
        success: function (response) {
            selectedTheme = response;
            document.body.classList.add(response);

            if (response == 'dark') {
                checkbox.checked = true;
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
    return selectedTheme;
}

function toggleTheme() {
    $.ajax({
        url: '/toggle-theme/',
        type: 'GET',

        success: function (response) {
            document.body.classList.remove('light', 'dark');

            selectedTheme = response;
            document.body.classList.add(response);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
    return selectedTheme;
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function deletePort(fullname) {
    const toastMessage = document.getElementById('toastNotification');
    const standaloneToast = new bootstrap.Toast(toastMessage, { autohide: true });
    $('#toastMsg').text('⌛ Loading ...');

    standaloneToast.show();

    // AJAX request to trigger backend operation
    $.ajax({
        url: '/hd-v00/delete-portfolio/',
        method: 'POST',
        data: {
            'fullname': fullname
        },
        headers: {
            'X-CSRFToken': getCSRFToken()  // Include CSRF token in headers
        },
        success: function (response) {
            $('#toastMessage').text('Removed student portfolio from tracker.');

            standaloneToast.show();

            $('#response').html('Successfully Finished Syncing!');
        },
        error: function (xhr, status, error) {
            $('#spinner').hide();
            $('#response').html('Error: ' + error);
        }
    });
}
