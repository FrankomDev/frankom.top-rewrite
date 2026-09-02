// load header
class Button {
    constructor(name, url) {
      this.name = name;
      this.url = url;
    }
}
var buttons = [
  new Button("main", "."),
  new Button("hardware", "hardware.html"),
  new Button("shit in my mind", "blog.html"),
  new Button("projectz", "projects.html"),
  new Button("linkz", "links.html"),
  new Button("guestbook", "guestbook.html")
]

var nav = document.createElement("nav");
nav.className = "block";

buttons.forEach((item) => {
  var a = document.createElement("a");
  var btn = document.createElement("button");

  btn.type = "button";
  btn.innerText = item.name;
  a.href = item.url;

  a.append(btn);
  nav.appendChild(a);
})

var logo = document.createElement("img");
logo.src = "static/img/logo.png";
logo.alt = "logo";
document.getElementById("nav").appendChild(logo);

document.getElementById("nav").appendChild(nav);




// load footer
buttons = [];
var footer = document.createElement("footer");
footer.className = "block";

var h3 = document.createElement("h3");
h3.textContent = "© 2026 frankom";
footer.appendChild(h3);

var div = document.createElement("div");
buttons = [
  new Button("powered by debian", "static/img/buttons/debian.gif"),
  new Button("archlinux", "static/img/buttons/archlinux.gif"),
  new Button("best viewed with eyes", "static/img/buttons/besteyes.gif"),
  new Button("Jesus now", "static/img/buttons/jesus_now.gif"),
  new Button("vim", "static/img/buttons/vim.gif")
];
buttons.forEach((item) => {
  var img = document.createElement("img");

  img.src = item.url;
  img.alt = item.name;

  div.appendChild(img);
})
footer.appendChild(div);

document.getElementById("footer").appendChild(footer);




// age thing on main page
var item = document.getElementById("age");
if (item) {
  var birthdate = new Date("12/05/2009");
  function display_age() {
      let num = (new Date() - birthdate) / (1000*3600*24*365.25);
      num = num.toFixed(10)
      item.innerText = "age: " + num;
      requestAnimationFrame(display_age);
  }
  display_age();

}
