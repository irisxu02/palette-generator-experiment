document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Form submitted!");

    const formData = new FormData();
    formData.append('image', e.target.image.files[0]);
    formData.append('method', e.target.method.value);

    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    // Display newly uploaded image
    const imageContainer = document.getElementById('image-container');
    const img = new Image();
    img.src = `/static/uploads/${data.filename}`;
    imageContainer.innerHTML = '';
    imageContainer.appendChild(img);

/*     const paletteDiv = document.getElementById('palette');
    paletteDiv.innerHTML = '';
    data.palette.forEach(color => {
        const colorDiv = document.createElement('div');
        colorDiv.style.backgroundColor = color;
        paletteDiv.appendChild(colorDiv);
    }); */
});
