function copyActivityJson(event) {
    event.preventDefault();
    var el = document.getElementById("activity-json");
    var text = el.textContent;
    navigator.clipboard.writeText(text).then(function() {
        var link = event.target;
        var original = link.textContent;
        link.textContent = "Copied!";
        setTimeout(function() {
            link.textContent = original;
        }, 1500);
    });
}
