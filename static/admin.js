const container = document.getElementById("container");
const preview = document.getElementById("preview_box");

function clear_view() {
  container.innerHTML = "";
  preview.style.display = "none";
}

function blog() {
  clear_view();
  new_btn = document.createElement("button");
  new_btn.textContent = "new blog post";
  new_btn.onclick = function(){ display_editor("/blog") };
  container.appendChild(new_btn);
  container.appendChild(document.createElement("br"));
  container.appendChild(document.createElement("br"));
  edit_btn = document.createElement("button")
  edit_btn.textContent = "edit posts";
  edit_btn.onclick = function(){ display_edit_entries("/blog") };
  container.appendChild(edit_btn);
}

function display_editor(action, to_edit=false, id=-1) {
    clear_view();

    form = document.createElement("form");
    form.method = "POST";
    form.action = action;

    title = document.createElement("input");
    title.placeholder = "title";
    title.id = "title";
    title.name = "title";
    form.appendChild(title);
    form.appendChild(document.createElement("br"));

    content = document.createElement("textarea");
    content.placeholder = "content";
    content.id = "content";
    content.name = "content";
    form.appendChild(content);
    form.appendChild(document.createElement("br"));

    submit = document.createElement("button");
    submit.textContent = "post";
    submit.type = "submit";
    form.appendChild(submit);

    preview_btn = document.createElement("button");
    preview_btn.textContent = "preview";
    preview_btn.onclick = function() {
      prev_t = document.getElementById("prev_title");
      prev_c = document.getElementById("prev_content");

      prev_t.textContent = title.value;
      prev_c.innerHTML = content.value;
    };

    container.appendChild(form);
    container.appendChild(preview_btn);
    preview.style.display = "block";

    if (to_edit){
      fetch(`${action}?api=1`)
        .then((response) => response.json())
        .then((data) => {
          title.value = data[0]
          content.value = data[1]
        })

    }
}

function projects() {
  clear_view();
  new_btn = document.createElement("button");
  new_btn.textContent = "new project";
  new_btn.onclick = function(){ display_editor("/projects") };
  container.appendChild(new_btn);
  container.appendChild(document.createElement("br"));
  container.appendChild(document.createElement("br"));
  edit_btn = document.createElement("button")
  edit_btn.textContent = "edit projects";
  edit_btn.onclick = function(){ display_edit_entries("/projects") };
  container.appendChild(edit_btn);
}

function display_edit_entries(url){
  clear_view();
  fetch(`${url}?api=1`)
    .then((response) => response.json())
    .then((data) => {
      for (i in data) {
        p = document.createElement("p");
        p.textContent = data[i][0];
        container.appendChild(p);
        del = document.createElement("button");
        edit = document.createElement("button");
        const id = data[i][1];
        del.textContent = `del ${id}`;
        del.onclick = function(){ del_thing(url, id) };
        edit.textContent = `edit ${id}`;
        edit.onclick = function(){ display_editor(`${url}/${id}`, true, id) };
        container.appendChild(edit);
        container.appendChild(document.createElement("br"));
        container.appendChild(del);
        container.appendChild(document.createElement("hr"));
      }
    })
}

function guestbook() {
  clear_view();
  fetch("/guestbook?api=1")
    .then((response) => response.json())
    .then((data) => {
      for (i in data) {
        for (x = 0; x < 2; x++) {
          p = document.createElement("p");
          p.textContent = data[i][x];
          container.appendChild(p);
        }
        del = document.createElement("button");
        const id = data[i][2];
        del.textContent = `del ${id}`;
        del.onclick = function(){ del_thing("/guestbook", id) };
        container.appendChild(del);
        container.appendChild(document.createElement("hr"));
      }
    });
}

function del_thing(thing, id){
  if (window.confirm("u sure?")){
    fetch(`${thing}/${id}`, {method:"DELETE"})
    .then((response) => {
      if (response.status == 200){
        location.reload();
      }
    });
  }
}