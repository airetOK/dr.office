function appendSelectedValueToInput(inputId, selectId) {
    const select = document.querySelector(selectId);
    if (select.selectedIndex != 0) {
        const selectedValue = select.options[select.selectedIndex].text;
        const input = document.querySelector(inputId);
        input.value += `${selectedValue} `;
    }
}