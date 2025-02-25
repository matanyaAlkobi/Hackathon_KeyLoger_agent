let activeIndex = null;

function toggleDetails(index) {
    let details = document.querySelectorAll(".to_row1 div");

    if (activeIndex !== null && activeIndex !== index) {
        details[activeIndex].style.display = "none";
    }

    if (activeIndex === index) {
        details[index].style.display = "none";
        activeIndex = null;
    } else {
        details[index].style.display = "block";
        activeIndex = index;
    }
}
