var list = document.getElementById("list");

var href = window.location.href;

var type;
if (href.endsWith("blog") || href.endsWith("blog.html"))
  type = "blog";
else
  type = "projects";

if (list) {
  fetch(`api/${type}`).then(response => response.json()).then(data => {
    data.forEach((item) => {
      let a = document.createElement("a");
      a.href = `post.html?id=${item['id']}&type=${type}`;

      let li = document.createElement("li");
      li.textContent = item['title'];

      a.appendChild(li);
      list.appendChild(a);
    });
  });
} else {
  var title = document.getElementById("title");
  var content = document.getElementById("content");
  var params = new URLSearchParams(window.location.search);

  if (params.get("id") && params.get("type")) {
    let id = params.get("id");
    let type = params.get("type");
    fetch(`api/${type}/${id}`).then(response => response.json().then(data => {
      if (response.ok) {
        title.textContent = data['title'];
        content.innerHTML = data['content'];
      } else
          title.textContent = "Not found :O";
    }));
  } else {
    window.location.href = ".";
  }
}
