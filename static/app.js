document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.remove("hidden-on-load");
});

const burger = document.querySelector(".burger");
const nav = document.querySelector("nav");

/// ########################
// CREATE POST
async function createPost(formId, postsContainerId) {
    const form = document.getElementById(formId);
    const container = document.getElementById(postsContainerId);
    const formData = new FormData(form);

    const res = await fetch("/api-create-post", {
        method: "POST",
        body: formData
    });

    const html = await res.text();
    container.insertAdjacentHTML("afterbegin", html);
    form.reset();
}

document.getElementById("post_container")?.addEventListener("submit", function(e){
    e.preventDefault();
    createPost("post_container", "posts");
});

// ########################
// EDIT / SAVE / CANCEL
function editPost(post_pk, currentText) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    if (!postDiv) return;

    const content = postDiv.querySelector(".post-content");
    const textEl = postDiv.querySelector(".text");

    // Hide original text
    if (textEl) textEl.style.display = "none";

    // Create textarea if not already created
    let textarea = postDiv.querySelector(".edit-textarea");
    if (!textarea) {
        textarea = document.createElement("textarea");
        textarea.className = "edit-textarea w-full border rounded p-2 mt-2";
        textarea.id = `edit_text_${post_pk}`;
        textarea.value = currentText || "";
        content.appendChild(textarea);
    }

    // Create Save + Cancel buttons if not already created
    let btnContainer = postDiv.querySelector(".edit-buttons");
    if (!btnContainer) {
        btnContainer = document.createElement("div");
        btnContainer.className = "edit-buttons flex gap-2 mt-2";

        btnContainer.innerHTML = `
            <button type="button" class="px-3 py-1 bg-blue-500 text-white rounded"
                onclick="savePost('${post_pk}')">Save</button>

            <button type="button" class="px-3 py-1 bg-gray-300 text-black rounded"
                onclick="cancelEdit('${post_pk}')">Cancel</button>
        `;

        content.appendChild(btnContainer);
    }
}

// ########################
// SAVE POST
async function savePost(post_pk) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    const textarea = postDiv.querySelector(".edit-textarea");
    if (!textarea) return;

    const formData = new FormData();
    formData.append("post_message", textarea.value);

    try {
        const res = await fetch(`/api-update-post/${post_pk}`, {
            method: "POST",
            body: formData,
            credentials: "same-origin"
        });
        const data = await res.json();

        if (data.success) {
            // Find existing text element
            let textEl = postDiv.querySelector(".text");

            // If no text element existed (image-only post), create one
            if (!textEl) {
                textEl = document.createElement("p");
                textEl.className = "text mt-2";

                // Insert it before the post actions
                const actions = postDiv.querySelector(".post-actions");
                postDiv.querySelector(".post-content").insertBefore(textEl, actions);
            }

            // Update text content and show it
            textEl.textContent = data.post_message;
            textEl.style.display = "block";

            // Cleanup edit UI
            textarea.remove();
            postDiv.querySelector(".edit-buttons")?.remove();
        } else {
            alert("Failed to save post: " + data.error);
        }
    } catch (err) {
        console.error("Save post error:", err);
    }
}

// ########################
// CANCEL EDIT
function cancelEdit(post_pk) {
    const postDiv = document.getElementById(`post_${post_pk}`);
    postDiv.querySelector(".edit-textarea")?.remove();
    postDiv.querySelector(".edit-buttons")?.remove();

    const textEl = postDiv.querySelector(".text");
    if (textEl) textEl.style.display = "block";
}

// ########################
// DELETE POST
function deletePost(post_pk) {
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

// #############################
 document.addEventListener("DOMContentLoaded", () => {

  // ---------- Toggle comment form and focus textarea ----------
  document.querySelectorAll(".post .fa-comment").forEach(icon => {
    icon.addEventListener("click", e => {
      const postDiv = e.target.closest(".post");
      const form = postDiv.querySelector("form"); // picks the form inside this post
      if (!form) return;

      // Toggle visibility (hidden class)
      form.classList.toggle("hidden");

      // Focus textarea if form is visible
      const textarea = form.querySelector("textarea[name='comment']");
      if (!form.classList.contains("hidden") && textarea) {
        textarea.focus();
      }
    });
  });

  // ---------- Handle comment submission ----------
  document.querySelectorAll(".post form").forEach(form => {
    form.addEventListener("submit", async e => {
      e.preventDefault();

      const textarea = form.querySelector("textarea[name='comment']");
      if (!textarea) return;

      const commentText = textarea.value.trim();

      // Validate input length
      if (!commentText || commentText.length > 1000) {
        alert("Comment must be 1-1000 characters.");
        return;
      }

      // Extract post_pk from form action URL
      const actionUrl = form.getAttribute("action"); // e.g., /api-create-comment/<post_pk>
      const postFk = actionUrl.split("/").pop();

      try {
        const formData = new FormData();
        formData.append("comment_text", commentText); // Flask expects this key

        const res = await fetch(`/api-create-comment/${postFk}`, {
          method: "POST",
          body: formData,
          credentials: "same-origin"
        });

        const data = await res.json();

        if (data.status === "ok") {
          // Clear textarea
          textarea.value = "";

          // Append new comment under the post
          const postDiv = form.closest(".post");
          const commentsContainer = postDiv.querySelector(".post-content");
          const commentEl = document.createElement("div");
          commentEl.className = "comment mt-2 p-2 bg-gray-100 rounded";
          commentEl.innerHTML = `<strong>${data.user_first_name || "You"} ${data.user_last_name || ""}</strong>: ${commentText}`;
          commentsContainer.appendChild(commentEl);

          // Optionally hide the form again
          form.classList.add("hidden");
        } else {
          alert(data.message || "Failed to post comment.");
        }

      } catch (err) {
        console.error("Create comment error:", err);
        alert("Could not post comment. Check console.");
      }
    });
  });

});

// ##############################
burger.addEventListener("click", () => {
    nav.classList.toggle("active");
    burger.classList.toggle("open");
});

// ------------------ Forgot Password Modal ------------------
const forgotLink = document.getElementById("forgotPasswordLink");
const forgotDialog = document.getElementById("forgotPasswordDialog");
const forgotClose = forgotDialog?.querySelector(".x-dialog__close");

forgotLink?.addEventListener("click", (e) => {
    e.preventDefault();
    forgotDialog.classList.remove("hidden");
});

forgotClose?.addEventListener("click", () => {
    forgotDialog.classList.add("hidden");
});

// Close modal on overlay click
forgotDialog?.querySelector(".x-dialog__overlay")?.addEventListener("click", () => {
    forgotDialog.classList.add("hidden");
});

// #############################
document.addEventListener("DOMContentLoaded", () => {

    // Toggle comment form for any post
    document.body.addEventListener("click", e => {
        const btn = e.target.closest(".comment-toggle");
        if (!btn) return;

        const postPk = btn.dataset.post;
        const container = document.getElementById("comments_" + postPk);
        if (!container) return;

        container.style.display = container.style.display === "none" ? "block" : "none";
    });

    // Handle MixHTML success
    document.body.addEventListener("mix:success", e => {
        const form = e.target;
        if (!form.classList.contains("comment-form")) return;

        const data = e.detail.data;
        if (data.success) {
            const postPk = form.querySelector("input[name='post_fk']").value;
            const list = document.querySelector(`#comments_${postPk} .comment-list`);

            const commentEl = document.createElement("div");
            commentEl.classList.add("comment");
            commentEl.innerHTML = `<strong>You:</strong> ${data.comment.comment_message} <span class="time">just now</span>`;
            list.appendChild(commentEl);
            form.querySelector("textarea[name='comment']").value = "";

            const toggleBtn = document.querySelector(`.comment-toggle[data-post='${postPk}']`);
            if (toggleBtn) {
                let currentCount = parseInt(toggleBtn.textContent.trim()) || 0;
                toggleBtn.innerHTML = `<i class="fa-regular fa-comment"></i> ${currentCount + 1}`;
            }

            commentEl.scrollIntoView({ behavior: "smooth" });
        } else {
            alert(data.error || "Failed to post comment");
        }
    });

});
