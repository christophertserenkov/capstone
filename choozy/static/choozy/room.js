document.addEventListener('DOMContentLoaded', () => {
    // Get all used elements
    const bubbles = document.querySelector('#bubbles');
    const radios = document.querySelector('#radios');
    const backButton = document.querySelector('#backButton');
    const placeholder = document.querySelector('#placeholder');
    const nextButton = document.querySelector('#nextButton');
    const submitButton = document.querySelector('#submitButton');
    const cusineDiv = document.querySelector('#cusine');
    const typeDiv = document.querySelector('#type');
    const cusineSelector = document.querySelector('#selectCusine');
    const typeSelector = document.querySelector('#selectType');

    // Render or hide those elements
    bubbles.style.display = 'block'
    radios.style.display = 'none'
    nextButton.style.display = 'block'
    backButton.style.display = 'none';
    placeholder.style.display = 'block';
    submitButton.style.display = 'none'

    // Add event listeners to change between food bubble page and other questions page
    nextButton.addEventListener('click', displayRadios);
    backButton.addEventListener('click', displayBubbles);

    // Display cusine bubbles and hide type bubbles
    cusineDiv.style.display = 'flex';
    typeDiv.style.display = 'none';

    // Add event listeners to change between cusine and food type pages
    cusineSelector.addEventListener('click', displayCusine);
    typeSelector.addEventListener('click', displayType);

    // Allow mobile users to swipe to change pages
    if (window.innerWidth <= 768) {
        // Swipe detector by CS50 AI
        let startX;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });

        document.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const diffX = endX - startX;
        
            if (diffX > 50) {
                displayCusine()
            } else if (diffX < -50) {
                displayType()
            }
        });
    }

    // Get labels for checkboxes (bubbles)
    const checks =  document.querySelectorAll('label');

    // Add an event listener that adds a green ring to the bubble using daisyUI class if it is selected
    checks.forEach((check) => {
        const checkbox = check.querySelector('input[type="checkbox"]');
        const image = check.querySelector('img');

        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                image.className = 'foodimg ring-green-500 ring-offset-base-100 rounded-full ring ring-offset-2';
            } else {
                image.className = 'foodimg';
            }
        });
    });

    // Displays cusine bubbles
    function displayCusine() {
        cusineDiv.style.display = 'flex';
        typeDiv.style.display = 'none';
        cusineSelector.className = 'underline underline-offset-4 cursor-pointer';
        typeSelector.className = 'cursor-pointer';
    }
    
    // Displays type bubbles
    function displayType() {
        cusineDiv.style.display = 'none';
        typeDiv.style.display = 'flex';
        cusineSelector.className = 'cursor-pointer';
        typeSelector.className = 'underline underline-offset-4 cursor-pointer';
    }

    // Displays food selectors
    function displayBubbles() {
        bubbles.style.display = 'block'
        radios.style.display = 'none'

        nextButton.style.display = 'block'
        backButton.style.display = 'none';
        placeholder.style.display = 'block';
        submitButton.style.display = 'none'
    }

    // Displays other questions
    function displayRadios() {
        bubbles.style.display = 'none'
        radios.style.display = 'block'

        nextButton.style.display = 'none'
        backButton.style.display = 'block';
        placeholder.style.display = 'none';
        submitButton.style.display = 'block'
    }
});