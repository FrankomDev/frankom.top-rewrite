function login() {
  let password = document.getElementById("password");
  if (password != "") {
    fetch("api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "password": password.value }),
      credentials: "include"
    }).then(response => {
      if (response.ok)
        window.location.href = "admin.html";
        // yes it is accessible but you won't be able to do anything without auth
      else
        password.value = "";
    });
  }
}


var href = window.location.href;
if (!href.endsWith("login") && !href.endsWith("login.html")) {
  if (!document.cookie.startsWith("admin"))
    window.location.href = "login.html";

  var nav = document.getElementById("nav");

  class Button {
      constructor(name, function_str) {
        this.name = name;
        this.function_str = function_str;
      }
  }

  var buttons = [
    new Button("blog posts", function() {posts_load("blog")}),
    new Button("projects", function() {posts_load("projects")}),
    new Button("guestbook entries", function() {guestbook_load()}),
    new Button("images", function() {images_load()})
  ]
  buttons.forEach((item) => {
    let btn = document.createElement("button");

    btn.type = "button";
    btn.innerText = item.name;
    btn.addEventListener("click", () => {
      item.function_str();
    });

    nav.appendChild(btn);
  })

} else {
  fetch("api/check-cookie", {
    method: "GET",
    credentials: "include"
  }).then(response => {
    if (response.ok)
      window.location.href = "admin.html";
  });
}

var block = document.getElementById("block");
var preview = document.getElementById("preview");

function posts_load(type) {
  clear_block();

  let new_post = document.createElement("button");
  new_post.textContent = `New (${type})`
  new_post.addEventListener("click", () => {
    load_editor(type);
  });

  fetch(`api/${type}`).then(response => response.json()).then(data => {
    data.forEach((item) => {
      let title = document.createElement("p");
      title.textContent = item['title'];
      let del_btn = document.createElement("button");
      del_btn.textContent = `delete ${item['id']}`;
      del_btn.addEventListener("click", () => {
        thing_delete(type, item['id']);
      });
      let edit_btn = document.createElement("button");
      edit_btn.addEventListener("click", () => {
        load_editor(type, item['id']);
      });
      edit_btn.textContent = `edit ${item['id']}`;

      block.appendChild(title);
      block.appendChild(edit_btn);
      block.appendChild(del_btn);
      block.appendChild(document.createElement("hr"));
    });
  });

  block.appendChild(new_post);
  block.appendChild(document.createElement("hr"));
  block.appendChild(document.createElement("br"));
  block.appendChild(document.createElement("br"));
}

function guestbook_load() {
  clear_block();
  fetch("api/guestbook").then(response => response.json()).then(data => {
    data.forEach((item) => {
      let message = document.createElement("p");
      message.textContent = item['message'];
      let username = document.createElement("p");
      username.textContent = item['username'];
      let btn = document.createElement("button");
      btn.textContent = `delete ${item['id']}`;
      btn.addEventListener("click", () => {
        thing_delete("guestbook", item['id']);
      });

      block.appendChild(username);
      block.appendChild(message);
      block.appendChild(btn);
      block.appendChild(document.createElement("hr"));
    });
  });
}

function images_load() {
  clear_block();

  let form = document.createElement("form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    fetch("api/images", {
      method: "POST",
      body: new FormData(form)
    }).then(response => {
      if (response.ok)
        images_load();
    });
  });

  let input = document.createElement("input");
  input.type = "file";
  input.name = "file";
  let button = document.createElement("button");
  button.type = "submit";
  button.textContent = "upload";

  form.appendChild(input);
  form.appendChild(document.createElement("br"));
  form.appendChild(document.createElement("br"));
  form.appendChild(button);
  block.appendChild(form);
  block.appendChild(document.createElement("hr"));
  block.appendChild(document.createElement("br"));
  block.appendChild(document.createElement("br"));

  fetch("api/images").then(response => response.json()).then(data => {
    data.forEach(item => {
      let div = document.createElement("div");
      div.classList.add("images");

      let div2 = document.createElement("div");

      let img = document.createElement("img");
      img.src = `api/images/${item}`;
      img.width = 150;
      img.height = 150;

      let h3 = document.createElement("h3");
      h3.textContent = `id: ${item}`;

      let btn = document.createElement("button");
      btn.textContent = "delete";
      btn.addEventListener("click", () => {
        thing_delete("images", item);
      });

      div.appendChild(img);
      div2.appendChild(h3);
      div2.appendChild(btn);
      div.appendChild(div2);
      block.appendChild(div);
      block.appendChild(document.createElement("hr"));
    });
  });
}

function thing_delete(type, id) {
  if (window.confirm("are u sure?")) {
    fetch(`api/${type}/${id}`, {
      method: "DELETE",
      credentials: "include"
    }).then(response => {
      if (response.ok) {
        clear_block();
        if (type == "guestbook")
          guestbook_load();
        else if (type == "images")
          images_load()
        else
          posts_load(type);
      }
    });
  }
}

function clear_block() {
  block.innerHTML = "";
  preview.style.display = "none";
  block.classList.remove("editor");
}

function load_editor(type, edit_id = -1) {
  clear_block();
  preview.style.display = "block";
  block.classList.add("editor");
  document.getElementById("title").textContent = "";
  document.getElementById("content").innerHTML = "";

  let title = document.createElement("input");
  title.placeholder = "title";
  let content = document.createElement("textarea");
  content.placeholder = "content";
  if (edit_id >= 0) {
    fetch(`api/${type}/${edit_id}`).then(response => response.json()).then(data => {
      title.value = data['title'];
      content.value = data['content'];
    });
  }

  block.appendChild(title);
  block.appendChild(document.createElement("br"));
  block.appendChild(document.createElement("br"));
  block.appendChild(content);

  let preview_btn = document.createElement("button");
  preview_btn.textContent = "preview";
  preview_btn.addEventListener("click", () => {
    document.getElementById("title").textContent = title.value;
    document.getElementById("content").innerHTML = content.value;
  });
  let publish_btn = document.createElement("button");
  publish_btn.textContent = "publish";
  publish_btn.addEventListener("click", () => {
    let url = `api/${type}`;
    if (edit_id >= 0)
      url += `/${edit_id}`;
    let method = (edit_id >= 0) ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "title": title.value, "content": content.value }),
      credentials: "include"
    }).then(response => {
      if (response.ok) {
        window.location.href = `${type}.html`;
      }
    });
  });

  block.appendChild(document.createElement("br"));
  block.appendChild(document.createElement("br"));
  block.appendChild(preview_btn);
  block.appendChild(publish_btn);
}
