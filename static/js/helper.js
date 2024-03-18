function appendSelectedValueToInput(inputId, selectId) {
    const select = document.querySelector(selectId);
    if (select.selectedIndex != 0) {
        const selectedValue = select.options[select.selectedIndex].text;
        const input = document.querySelector(inputId);
        input.value += `${selectedValue} `;
    }
}

function chooseTooth(tooth_num) {
    const tooth_img = document.getElementById(tooth_num);
    if (tooth_img.style.opacity == 0.5) {
        tooth_img.style.opacity = 1;
    } else {
        tooth_img.style.opacity = 0.5;
    }
}

function saveTeeth() {
    let teethStr = '';
    for (let img of document.getElementsByTagName('img')) {
        if (img.style.opacity == 0.5) {
            img.style.opacity = 1;
            teethStr = teethStr + img.id + ' ';
        }
    }
    const input = document.querySelector('#teethInput');
    input.value += teethStr;
}