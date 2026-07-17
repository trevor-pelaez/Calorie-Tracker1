const searchBox = document.querySelector('#productSearch');
const productRows = document.querySelectorAll('#foodTable tbody tr');

if (searchBox) {
    searchBox.addEventListener('input', function () {
        const searchText = searchBox.value.toLowerCase();

        productRows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// What this means like you’re 5: