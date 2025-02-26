function loadFolders() {
    fetch('/get_folders')  // נניח שיש נתיב בשרת שמחזיר את רשימת התיקיות
        .then(response => response.json())
        .then(data => {
            const folderList = document.getElementById('folder-list');
            data.folders.forEach(folder => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `/dashboard/${folder}`;  // הקישור לתוך תיקיה ספציפית
                link.innerText = folder;
                listItem.appendChild(link);
                folderList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error loading folders:', error));
}

// הרץ את הפונקציה כשעמוד נטען
document.addEventListener('DOMContentLoaded', function() {
    loadFolders();
});
