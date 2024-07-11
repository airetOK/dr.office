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
    if (tooth_img.src.endsWith(tooth_num + 'g.png')) {
        tooth_img.src = '../static/images/' + tooth_num + '.png';
    } else {
        tooth_img.src = '../static/images/' + tooth_num + 'g.png';
    }
}

function saveTeeth() {
    let teethStr = '';
    for (let img of document.getElementsByTagName('img')) {
        if (img.src.endsWith(img.id + 'g.png')) {
            img.src = '../static/images/' + img.id + '.png';
            teethStr = teethStr + img.id + ' ';
        }
    }
    const input = document.querySelector('#teethInput');
    input.value += teethStr;
}

function expandRegisterForm() {
    if (document.querySelector('.register-form').style.display == 'none') {
        document.getElementById('chevron-icon').className = 'fa fa-chevron-up';
        document.querySelector('.register-form').style.display = 'block';
    } else {
        document.getElementById('chevron-icon').className = 'fa fa-chevron-down';
        document.querySelector('.register-form').style.display = 'none';
    }
}

function expandForgetPasswordForm() {
    if (document.querySelector('.forget-password-form').style.display == 'none') {
        document.getElementById('forget-chevron-icon').className = 'fa fa-chevron-up';
        document.querySelector('.forget-password-form').style.display = 'block';
    } else {
        document.getElementById('forget-chevron-icon').className = 'fa fa-chevron-down';
        document.querySelector('.forget-password-form').style.display = 'none';
    }
}