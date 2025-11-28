document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.remove("hidden-on-load");
});

const burger = document.querySelector(".burger");
const nav = document.querySelector("nav");

// ########################
async function createPost(formId, postsContainerId) {
    const form = document.getElementById(formId);
    const container = document.getElementById(postsContainerId);
    const formData = new FormData(form);

    fetch("/api-create-post", {
        method: "POST",
        body: formData,
        credentials: "same-origin"
    })
    .then(res => res.text()) // now returning HTML snippet
    .then(html => {
        // Insert returned post into DOM
        container.insertAdjacentHTML("afterbegin", html);
        form.reset();
        console.log("Post created successfully!");
    })
    .catch(err => {
        console.error("Create post error:", err);
        alert("Could not create post. Check console.");
    });
}

document.getElementById("post_container").addEventListener("submit", function(e){
    e.preventDefault();
    createPost("post_container", "posts");
});

// ##############################
function editPost(post_pk, currentText) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    postDiv.innerHTML = `
        <textarea id="edit_text_${post_pk}">${currentText}</textarea>
        <button onclick="savePost('${post_pk}')">Save</button>
        <button onclick="cancelEdit('${post_pk}', '${currentText.replace(/'/g,"\\'")}')">Cancel</button>
    `;
async function server(url, method, data_source_selector, function_after_fetch) {
  let conn = null;
  if (method.toUpperCase() == "POST") {
    const data_source = document.querySelector(data_source_selector);
    conn = await fetch(url, {
      method: method,
      body: new FormData(data_source),
    });
  }
  const data_from_server = await conn.text();
  if (!conn) {
    console.log("error connecting to the server");
  }
  window[function_after_fetch](data_from_server);
}

// ##############################
function savePost(post_pk) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    const newText = document.getElementById(`edit_text_${post_pk}`).value;

    const formData = new FormData();
    formData.append("post_message", newText);

    fetch(`/api-update-post/${post_pk}`, {
        method: "POST",
        body: formData,
        credentials: "same-origin"  // <--- IMPORTANT: sends cookies for session
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            postDiv.innerHTML = `
                <p class="text">${data.post_message}</p>
                <button onclick="editPost('${post_pk}', \`${data.post_message}\`)">Edit</button>
                <button onclick="deletePost('${post_pk}')">Delete</button>
            `;
        } else {
            alert("Failed to save post: " + data.error);
        }
    })
    .catch(err => console.error("Save post error:", err));
}

// ##############################
function cancelEdit(post_pk, originalText) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    if (postDiv) {
        postDiv.innerHTML = `
            <p class="text">${originalText}</p>
            <button onclick="editPost('${post_pk}', \`${originalText}\`)">Edit</button>
            <button onclick="deletePost('${post_pk}')">Delete</button>
        `;
    }
}

function get_search_results(
  url,
  method,
  data_source_selector,
  function_after_fetch
) {
  const txt_search_for = document.querySelector("#txt_search_for");
  if (txt_search_for.value == "") {
    console.log("empty search");
    document.querySelector("#search_results").innerHTML = "";
    document.querySelector("#search_results").classList.add("d-none");
    return false;
  }
  server(url, method, data_source_selector, function_after_fetch);
}

// ##############################
function deletePost(post_pk) {
    console.log("Delete clicked", post_pk);
    if (!confirm("Are you sure you want to delete this post?")) return;

    fetch(`/api-delete-post/${post_pk}`, {
        method: "POST",
        credentials: "same-origin"
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const postDiv = document.getElementById(`post_${post_pk}`);
            if (postDiv) postDiv.remove();
        } else {
            alert("Failed to delete post: " + data.error);
        }
    })
    .catch(err => console.error("Delete post error:", err));
}

// ##############################
async function server(url, method, data_source_selector, function_after_fetch) {
    let conn = null;
    if (method.toUpperCase() === "POST") {
        const data_source = document.querySelector(data_source_selector);
        conn = await fetch(url, {
            method: method,
            body: new FormData(data_source)
        });
    }
    if (!conn) return console.log("error connecting to the server");
    const data_from_server = await conn.text();
    window[function_after_fetch](data_from_server);
}

// ##############################
function get_search_results(url, method, data_source_selector, function_after_fetch) {
    const txt_search_for = document.querySelector("#txt_search_for");
    if (txt_search_for.value === "") {
        console.log("empty search");
        document.querySelector("#search_results").innerHTML = "";
        document.querySelector("#search_results").classList.add("d-none");
        return false;
    }
    server(url, method, data_source_selector, function_after_fetch);
}

// ##############################
document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", async (e) => {
        const button = e.target.closest(".follow-btn");
        if (!button) return;

        const user_pk = button.dataset.user;
        // Use data-action attribute instead of textContent
        let action = button.dataset.action || (button.textContent.trim().toLowerCase() === "follow" ? "follow" : "unfollow");

        const formData = new FormData();
        formData.append("following_pk", user_pk);

        try {
            const res = await fetch(`/api-${action}`, {
                method: "POST",
                body: formData,
                credentials: "same-origin",
            });

            const data = await res.json();

            if (data.success) {
                if (action === "follow") {
                    button.textContent = "Unfollow";
                    button.dataset.action = "unfollow"; // update for next click
                    button.classList.remove("bg-c-black");
                    button.classList.add("bg-c-gray-500");
                } else {
                    button.textContent = "Follow";
                    button.dataset.action = "follow"; // update for next click
                    button.classList.remove("bg-c-gray-500");
                    button.classList.add("bg-c-black");
                }
                console.log(`Button toggled: ${action} -> ${button.textContent}`);
            } else {
                console.error("Server error:", data.error);
                alert("Error: " + data.error);
            }
        } catch (err) {
            console.error("Fetch error:", err);
            alert("Could not toggle follow. Check console.");
        }
    });
});


// ##############################
burger.addEventListener("click", () => {
    nav.classList.toggle("active");
    burger.classList.toggle("open");
});

}

