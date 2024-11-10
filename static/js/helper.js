function appendActionOptionsToInput() {
    const options = document.querySelectorAll('.list-group-item');
    const input = document.querySelector('#actionInput');
    for (let option of options) {
        if (option.getAttribute("data-chosen") === "1") {
            input.value += `| ${option.innerHTML} |`
        }
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

function appendOptionToSearchForm() {
    const searchParam = document.getElementById("searchParam");
    const value = searchParam.value;
    const searchInput = document.getElementById("searchInput");
    if (value === "date") {
        searchInput.placeholder = "день/місяць/рік";
    } else {
        searchInput.placeholder = "Введіть значення";
    }
    const searchForm = document.querySelector('.search-form');
    let arr = searchForm.action.split('/');
    arr[arr.length - 1] = value;
    searchForm.action = arr.join('/');
}

function showHidePassword(element, inputId) {
    const passwordInput = document.querySelector(`#${inputId}`);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        element.className = element.className.replace('fa-eye-slash', 'fa-eye');
    } else {
        passwordInput.type = "password";
        element.className = element.className.replace('fa-eye', 'fa-eye-slash');
    }
}

function appendPatientIdToHref(element) {
    document.querySelector('#deleteLinkPatient').href = '/delete/' + element.getAttribute('data-patient-id');
}

function chooseAction(element) {
    if (element.getAttribute("data-chosen") === "0") {
        element.setAttribute("data-chosen", "1");
        element.style.backgroundColor = "#cfcdca";
    } else {
        element.setAttribute("data-chosen", "0");
        element.style.backgroundColor = "";
    }
}
 