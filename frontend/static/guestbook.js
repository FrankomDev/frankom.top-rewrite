var right = document.getElementById("right");
fetch("api/guestbook").then(response => response.json()).then(data => {
  data.forEach((item) => {
    console.log(item);
    let message = document.createElement("p");
    message.textContent = item['message'];
    let username = document.createElement("b");
    username.textContent = item['username'];

    right.appendChild(username);
    right.appendChild(message);
    right.appendChild(document.createElement("hr"));
  });
});

var form = document.getElementById("form");

//localStorage.clear();

form.addEventListener("submit", () => {
  if (localStorage.getItem("send") != null) {
    window.alert("Sorry, but you already posted before :/");
    return;
  }

  fetch("api/guestbook", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({"username": form['username'].value, "message": form['message'].value})
  }).then(response => {
    if (response.ok) {
      localStorage.setItem("send", 1);
    };
  });

});
