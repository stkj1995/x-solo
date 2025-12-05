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
// Trigger search on Enter key
const searchInput = document.querySelector("#txt_search_for");
if (searchInput) {
    searchInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();  // Prevent form submission / reload
            doSearch();          // Trigger search
        }
    });
}

// Validate input and trigger search
function doSearch() {
    const input = document.querySelector("#txt_search_for");
    const query = input.value.trim();
    const results = document.querySelector("#search_results");

    if (!query) {
        results.innerHTML = "";
        results.classList.add("d-none");
        return;
    }

    fetch("/api-search-json", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ search_for: query })
    })
    .then(res => res.json())
    .then(data => displayResults(data))
    .catch(err => console.error("Search error:", err));
}

// Render search results dynamically
function displayResults(data) {
    const container = document.querySelector("#search_results");
    if (!container) return;

    container.innerHTML = "";

    let hasResults = false;

    // ---------------- Users ----------------
    if (data.users && data.users.length > 0) {
        hasResults = true;
        const usersHeader = document.createElement("div");
        usersHeader.className = "font-bold mb-1";
        usersHeader.textContent = "Users:";
        container.appendChild(usersHeader);

        data.users.forEach(user => {
            const div = document.createElement("div");
            div.className = "d-flex a-items-center mb-2";
            div.innerHTML = `
                <img src="/static/images/${user.user_avatar_path || 'unknown.jpg'}" class="w-8 h-8 rounded-full" alt="Profile">
                <div class="w-full ml-2">
                    <p>${user.user_first_name} ${user.user_last_name} 
                        <span class="text-c-gray:+20 text-70">@${user.user_username}</span>
                    </p>
                </div>
                <button class="px-4 py-1 text-c-white bg-c-black rounded-lg">Follow</button>
            `;
            container.appendChild(div);
        });
    }

    // ---------------- Posts ----------------
    if (data.posts && data.posts.length > 0) {
        hasResults = true;
        const postsHeader = document.createElement("div");
        postsHeader.className = "font-bold mt-2 mb-1";
        postsHeader.textContent = "Posts:";
        container.appendChild(postsHeader);

        data.posts.forEach(post => {
            const div = document.createElement("div");
            div.className = "border-t border-c-gray:+20 mt-1 pt-1";
            div.textContent = post.post_message;
            container.appendChild(div);
        });
    }

    // ---------------- Trends ----------------
    if (data.trends && data.trends.length > 0) {
        hasResults = true;
        const trendsHeader = document.createElement("div");
        trendsHeader.className = "font-bold mt-2 mb-1";
        trendsHeader.textContent = "Trends:";
        container.appendChild(trendsHeader);

        const trendDiv = document.createElement("div");
        trendDiv.className = "flex flex-wrap gap-2";
        data.trends.forEach(t => {
            const span = document.createElement("span");
            span.className = "px-2 py-1 bg-c-gray:+10 rounded-md text-sm";
            span.textContent = t.trend_title || t;
            trendDiv.appendChild(span);
        });
        container.appendChild(trendDiv);
    }

    // ---------------- No results ----------------
    if (!hasResults) {
        container.innerHTML = "<p class='text-c-gray:+50'>No results found</p>";
    }

    container.classList.remove("d-none");
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

  // ----------------------------
  // COMMENT SUBMIT HANDLER
  // ----------------------------
  document.body.addEventListener("submit", async (e) => {
    const form = e.target;
    if (!form.classList.contains("comment-form")) return;

    e.preventDefault(); // prevent full page reload

    const postPk = form.querySelector("input[name='post_fk']").value;
    const commentMessage = form.querySelector("textarea[name='comment']").value.trim();
    if (!commentMessage) return;

    try {
      const formData = new FormData();
      formData.append("post_fk", postPk);
      formData.append("comment", commentMessage);

      const res = await fetch("/api-create-comment", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (data.success) {
        // Append comment locally with Edit/Delete buttons
        const list = document.querySelector(`#comments_${postPk} .comment-list`);
        const commentEl = document.createElement("div");
        commentEl.classList.add("comment");
        commentEl.dataset.commentPk = data.comment.comment_pk;
        commentEl.innerHTML = `
          <strong>You:</strong> ${data.comment.comment_message}
          <button class="edit-comment">Edit</button>
          <button class="delete-comment">Delete</button>
        `;
        list.appendChild(commentEl);

        // Clear textarea
        form.querySelector("textarea[name='comment']").value = "";

        // Update comment count in header
        const toggleBtn = document.querySelector(`.comment-toggle[data-post='${postPk}']`);
        if (toggleBtn) {
          let currentCount = parseInt(toggleBtn.textContent.trim()) || 0;
          toggleBtn.innerHTML = `<i class="fa-regular fa-comment"></i> ${currentCount + 1}`;
        }

        // REMOVE scrollIntoView so page doesn't jump
        // commentEl.scrollIntoView({ behavior: "smooth" });

      } else {
        alert(data.error || "Failed to post comment");
      }

    } catch (err) {
      console.error(err);
      alert("Something went wrong posting the comment.");
    }
  });

  // ----------------------------
  // COMMENT EDIT / DELETE HANDLER
  // ----------------------------
  document.body.addEventListener("click", async (e) => {
    const commentEl = e.target.closest(".comment");
    if (!commentEl) return;

    const commentPk = commentEl.dataset.commentPk;
    const postContainer = commentEl.closest(".post");
    const postPk = postContainer?.id.replace("post_", "");

    // EDIT COMMENT
    if (e.target.matches(".edit-comment")) {
      const currentText = commentEl.querySelector("strong")?.nextSibling?.textContent?.trim() || "";
      const newText = prompt("Edit your comment:", currentText);
      if (!newText || newText.trim() === "" || newText === currentText) return;

      try {
        const res = await fetch("/api-edit-comment", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ comment_pk: commentPk, comment_message: newText })
        });
        const data = await res.json();
        if (data.success) {
          // Replace comment text in place without reloading
          commentEl.querySelector("strong").nextSibling.textContent = ` ${newText} `;
        } else {
          alert(data.error || "Failed to edit comment");
        }
      } catch (err) {
        console.error(err);
        alert("Error editing comment");
      }
    }

    // DELETE COMMENT
    if (e.target.matches(".delete-comment")) {
      if (!confirm("Delete this comment?")) return;

      try {
        const res = await fetch("/api-delete-comment", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ comment_pk: commentPk })
        });
        const data = await res.json();
        if (data.success) {
          commentEl.remove();

          // Update comment count in header
          const toggleBtn = document.querySelector(`.comment-toggle[data-post='${postPk}']`);
          if (toggleBtn) {
            let currentCount = parseInt(toggleBtn.textContent.trim()) || 1;
            toggleBtn.innerHTML = `<i class="fa-regular fa-comment"></i> ${currentCount - 1}`;
          }
        } else {
          alert(data.error || "Failed to delete comment");
        }
      } catch (err) {
        console.error(err);
        alert("Error deleting comment");
      }
    }
  });

// ############################
document.addEventListener("DOMContentLoaded", () => {
    console.log("🔥 app.js loaded");

    document.addEventListener("click", async function (event) {
        const btn = event.target.closest(".follow-btn");
        if (!btn) return;

        const userPk = btn.dataset.user;
        const action = btn.dataset.action;

        const endpoint = action === "follow" ? "/api-follow" : "/api-unfollow";

        const formData = new FormData();
        formData.append("following_pk", userPk);

        try {
            const res = await fetch(endpoint, {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            if (!data.success) {
                console.error(data.error);
                return;
            }

            // Update button UI
            if (action === "follow") {
                btn.textContent = "Unfollow";
                btn.classList.remove("bg-c-black");
                btn.classList.add("bg-c-gray-500");
                btn.dataset.action = "unfollow";
            } else {
                btn.textContent = "Follow";
                btn.classList.remove("bg-c-gray-500");
                btn.classList.add("bg-c-black");
                btn.dataset.action = "follow";
            }

        } catch (err) {
            console.error("Follow error:", err);
        }
    });
});



});
