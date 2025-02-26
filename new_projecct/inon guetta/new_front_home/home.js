let count = 1;

function addRow() {
    const table = document.getElementById("dataTable").getElementsByTagName('tbody')[0];
    const row = table.insertRow();

    row.insertCell(0).innerText = count++;
    row.insertCell(1).innerText = "Device " + (Math.floor(Math.random() * 100));
    row.insertCell(2).innerText = new Date().toLocaleString();
    row.insertCell(3).innerText = "file_" + Math.floor(Math.random() * 100) + ".txt";
    row.insertCell(4).innerText = "Event logged";

    const selectCell = row.insertCell(5);
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.onclick = function() {
        row.classList.toggle("selected", checkbox.checked);
    };
    selectCell.appendChild(checkbox);
}

function selectAll() {
    document.querySelectorAll("#dataTable tbody tr").forEach(row => {
        row.classList.add("selected");
        row.cells[5].querySelector("input").checked = true;
    });
}

function deselectAll() {
    document.querySelectorAll("#dataTable tbody tr").forEach(row => {
        row.classList.remove("selected");
        row.cells[5].querySelector("input").checked = false;
    });
}

function showPopup() {
    document.getElementById("popup").style.display = "block";
}

function hidePopup() {
    document.getElementById("popup").style.display = "none";
}

function confirmDelete() {
    document.querySelectorAll("#dataTable tbody tr.selected").forEach(row => {
        row.remove();
    });
    hidePopup();
}
