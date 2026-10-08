console.log("SLSU EduQuest JavaScript loaded successfully.");


function comingSoon(itemName) {
    alert(
        itemName +
        " will be available in the next development step!"
    );
}


/* =================================
   GAME PROGRESS BAR
================================= */

document.addEventListener("DOMContentLoaded", function () {

    const progressBars = document.querySelectorAll(
        ".quiz-progress-bar"
    );

    progressBars.forEach(function (bar) {

        const progress = bar.getAttribute("data-progress");

        if (progress) {
            bar.style.width = progress + "%";
        }

    });

});