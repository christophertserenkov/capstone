document.addEventListener('DOMContentLoaded', (event) => {
    // Get all the neccecary elements
    const toggle = document.querySelector('#location-check');
    const pError = document.querySelector('#error');
    const countryInput = document.querySelector('#location-country');
    const cityInput = document.querySelector('#location-city');
    const submitInput = document.querySelector('#submit');

    // Set toggle to checked
    toggle.checked = false;
    toggle.disabled = true;
    const loadingDiv = document.querySelector('#loading');
    const loadingIndicator = createLoading(loadingDiv);

    // Hide the form
    countryInput.style.display = 'none';
    cityInput.style.display = 'none';

    // Check if browser supports geolocation
    if (navigator.geolocation) {
        // Try to get user's position
        navigator.geolocation.getCurrentPosition(successHandle, errorHandle);

        // If location retrieved
        function successHandle(position) {
            // Get coordinates
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Store the coordinates in the hidden inputs
            document.querySelector('#latitude').value = latitude;
            document.querySelector('#longitude').value = longitude;
            toggle.checked = true;
            toggle.disabled = false;
            loadingIndicator.remove();

            // If the toggle is toggled then display the form
            toggle.addEventListener('change', () => {
                console.log('Checkbox state changed');
                if (!toggle.checked) {
                    toggleUnCheck();
                } else {
                    toggleCheck();
                }
            });
        }

        // If location not retrieved
        function errorHandle() {
            locationError(
                'Could not retrieve location!<br/>Please enter location manually'
            );
        }
    } else {
        locationError(
            'Browser does not support location!<br/>Please enter location manually'
        );
    }

    // Handle toggle uncheck (display the form)
    function toggleUnCheck() {
        displayForm(countryInput, cityInput, submitInput);
        console.log('Untoggled');
    }

    // Handle toggle check (hide the form and enable the submit button)
    function toggleCheck() {
        countryInput.style.display = 'none';
        cityInput.style.display = 'none';

        countryInput.disabled = true;
        cityInput.disabled = true;
        submitInput.disabled = false;
        console.log('Toggled');
    }

    // Display error and render the location form
    function locationError(errormessage) {
        loadingIndicator.remove();
        pError.innerHTML = errormessage;
        toggle.checked = false;
        toggle.disabled = true;
        displayForm(countryInput, cityInput, submitInput);
    }
});

// Creates a loading element into a target div and returns loading object
function createLoading(targetdiv) {
    const loadingIndicator = document.createElement('span');
    loadingIndicator.id = 'loadingIndicator';
    loadingIndicator.className = 'loading loading-dots loading-lg';
    targetdiv.appendChild(loadingIndicator);
    return loadingIndicator;
}

// Function to display the location form
function displayForm(countryInput, cityInput, submitInput) {
    // Enable the country input and disable the city and submit inputs
    countryInput.disabled = false;
    cityInput.disabled = true;
    submitInput.disabled = true;

    // Set the default option for the select tags
    countryInput.innerHTML = '<option disabled selected>Country</option>';
    cityInput.innerHTML = '<option disabled selected>City</option>';

    // List of the locales supported by the Yelp API
    const supportedCountries = {
        'ar': 'Argentina',
        'au': 'Australia',
        'at': 'Austria',
        'be': 'Belgium',
        'br': 'Brazil',
        'ca': 'Canada',
        'cl': 'Chile',
        'cz': 'Czech Republic',
        'dk': 'Denmark',
        'fi': 'Finland',
        'fr': 'France',
        'de': 'Germany',
        'ie': 'Ireland',
        'it': 'Italy',
        'jp': 'Japan',
        'my': 'Malaysia',
        'mx': 'Mexico',
        'nl': 'Netherlands',
        'nz': 'New Zealand',
        'no': 'Norway',
        'ph': 'Philippines',
        'pl': 'Poland',
        'pt': 'Portugal',
        'sg': 'Singapore',
        'es': 'Spain',
        'se': 'Sweden',
        'ch': 'Switzerland',
        'tw': 'Taiwan',
        'tr': 'Turkey',
        'gb': 'United Kingdom',
        'us': 'United States'
    };

    // Add the supported countries as options in the country selector
    Object.keys(supportedCountries).forEach((country) => {
        const element = document.createElement('option');
        element.value = country;
        element.text = supportedCountries[country];
        countryInput.appendChild(element);
    });

    // Show the form elements
    countryInput.style.display = 'block';
    cityInput.style.display = 'block';

    // When the user chooses a country get the cities in thet country and add them as options
    countryInput.addEventListener('change', (event) => {
        // Clear existing options
        cityInput.innerHTML = '<option disabled selected>City</option>';

        // Get the selected country
        const country = supportedCountries[event.target.value];

        // Add a loading indicator (from daisyUI)
        const loadingDiv = document.querySelector('#loading');
        const loading = createLoading(loadingDiv);

        console.log(country)

        // Reference: Fetch request was generated by ChatGPT after I asked it to find acity retrieving API that doesn't require an API key
        // (The code in the .then(data) bracket is written by me)
        fetch('https://countriesnow.space/api/v0.1/countries/cities', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ country: country }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.data);
            // Add the city options to the city selector
            data.data.forEach((city) => {
                const element = document.createElement('option');
                element.value = city;
                element.text = city;
                cityInput.appendChild(element);
            });

            // Remove the loading indicator and enable the city selector
            loading.remove();
            cityInput.disabled = false;

            // Eneble the submit button if the user selects a city
            cityInput.addEventListener('change', (event) => {
                submitInput.disabled = false;
            });
        })
        .catch((error) => console.log(error));
    });
}
