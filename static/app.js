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
      const form = postDiv.querySelector("form");
      if (!form) return;

      form.classList.toggle("hidden");
      const textarea = form.querySelector("textarea[name='comment']");
      if (!form.classList.contains("hidden") && textarea) textarea.focus();
    });
  });

  // ---------- Handle new comment submission ----------
  document.querySelectorAll(".post form").forEach(form => {
    form.addEventListener("submit", async e => {
      e.preventDefault();
      const textarea = form.querySelector("textarea[name='comment']");
      if (!textarea) return;

      const commentText = textarea.value.trim();
      if (!commentText) return;

      const postPk = form.dataset.postPk;

      try {
        const formData = new FormData();
        formData.append("comment", commentText);
        formData.append("post_fk", postPk);

        const res = await fetch(`/api-create-comment`, {
          method: "POST",
          body: formData,
          credentials: "same-origin"
        });

        const data = await res.json();
        if (data.success) {
          const commentsContainer = form.parentElement.querySelector(".comment-list");

          const commentEl = document.createElement("div");
          commentEl.className = "comment p-2 bg-gray-50 flex justify-between items-start border border-gray-100 shadow-sm mt-2";
          commentEl.dataset.commentPk = data.comment.comment_pk;
          commentEl.innerHTML = `
            <div class="comment-content flex-1">
              <strong>${data.user_first_name || "You"}</strong>: 
              <span class="comment-text">${commentText}</span>
            </div>
            <div class="comment-actions flex space-x-2 ml-2">
              <span class="time text-gray-400">${new Date().toLocaleString()}</span>
              <button class="edit-comment text-blue-500 hover:underline">Edit</button>
              <button class="delete-comment text-red-500 hover:underline">Delete</button>
            </div>
          `;

          commentsContainer.appendChild(commentEl);
          textarea.value = "";

          addInlineEditDelete(commentEl);
        }
      } catch (err) {
        console.error(err);
      }
    });
  });

  // ---------- Initialize existing comments ----------
  document.querySelectorAll(".comment").forEach(addInlineEditDelete);

  function addInlineEditDelete(commentEl) {
    const editBtn = commentEl.querySelector(".edit-comment");
    const deleteBtn = commentEl.querySelector(".delete-comment");
    const commentTextEl = commentEl.querySelector(".comment-text");

    let isEditing = false;

    // Inline edit toggle
    editBtn.addEventListener("click", async () => {
      if (!isEditing) {
        // Start editing
        commentTextEl.contentEditable = true;
        commentTextEl.focus();
        editBtn.textContent = "Save";
        isEditing = true;
      } else {
        // Save edited comment
        const updatedText = commentTextEl.textContent.trim();
        if (!updatedText) return;

        const commentPk = commentEl.dataset.commentPk;

        try {
          const formData = new FormData();
          formData.append("comment_pk", commentPk);
          formData.append("comment_message", updatedText);

          const res = await fetch(`/api-edit-comment`, {
            method: "POST",
            body: formData,
            credentials: "same-origin"
          });

          const data = await res.json();
          if (data.success) {
            commentTextEl.textContent = updatedText;
            commentTextEl.contentEditable = false;
            editBtn.textContent = "Edit";
            isEditing = false;
          }
        } catch (err) {
          console.error(err);
        }
      }
    });

    // Delete comment
    deleteBtn.addEventListener("click", async () => {
      const commentPk = commentEl.dataset.commentPk;
      if (!confirm("Delete this comment?")) return;

      try {
        const formData = new FormData();
        formData.append("comment_pk", commentPk);

        const res = await fetch(`/api-delete-comment`, {
          method: "POST",
          body: formData,
          credentials: "same-origin"
        });

        const data = await res.json();
        if (data.success) {
          commentEl.remove();
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

});


  // Trigger search on button click
const searchBtn = document.querySelector("#btn_search");
if (searchBtn) {
    searchBtn.addEventListener("click", function(e) {
        e.preventDefault();  // Prevent form submission if inside a form
        doSearch();           // Trigger the same search function
});
}

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
        commentEl.classList.add("comment", "p-2", "bg-gray-50", "flex", "justify-between", "items-start", "border", "border-gray-100", "shadow-sm", "mt-2");
        commentEl.dataset.commentPk = data.comment.comment_pk;
        commentEl.innerHTML = `
          <div class="comment-content flex-1">
            <strong>You:</strong> <span class="comment-text">${data.comment.comment_message}</span>
          </div>
          <div class="comment-actions flex space-x-2 ml-2">
            <button class="edit-comment text-blue-500 hover:underline">Edit</button>
            <button class="delete-comment text-red-500 hover:underline">Delete</button>
          </div>
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

    // EDIT COMMENT INLINE
    if (e.target.matches(".edit-comment")) {
      const editBtn = e.target;
      const commentTextEl = commentEl.querySelector(".comment-text");

      if (!commentTextEl.isContentEditable) {
        // Start editing
        commentTextEl.contentEditable = true;
        commentTextEl.focus();
        editBtn.textContent = "Save";
      } else {
        // Save edited comment
        const newText = commentTextEl.textContent.trim();
        if (!newText) return;

        try {
          const res = await fetch("/api-edit-comment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ comment_pk: commentPk, comment_message: newText })
          });
          const data = await res.json();
          if (data.success) {
            commentTextEl.contentEditable = false;
            editBtn.textContent = "Edit";
          } else {
            console.error(data.error || "Failed to edit comment");
          }
        } catch (err) {
          console.error(err);
        }
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
          console.error(data.error || "Failed to delete comment");
        }
      } catch (err) {
        console.error(err);
      }
    }
  });

});


// ############################
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("deleteModal");
  const openBtn = document.getElementById("deleteBtn");
  const cancelBtn = document.getElementById("cancelDeleteModal");

  // Open modal
  openBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
  });

  // Close modal
  cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  // Close if click outside modal content
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.add("hidden");
  });
});

// ########################
document.addEventListener("DOMContentLoaded", () => {
    const trendsContainer = document.querySelector("#trends-container");

    if (!trendsContainer) return;

    fetch("/api-trends")
        .then(res => res.json())
        .then(data => {
            if (!data.success) throw new Error(data.error || "Failed to load trends");

            trendsContainer.innerHTML = "";
            data.trends.forEach(trend => {
                const trendHTML = `
                    <div class="trend-card border-1 border-c-gray:+50 rounded-md pa-2 mb-2 d-flex flex-row items-center justify-between">
                        <div class="trend-content d-flex flex-row items-start gap-2">
                            ${trend.trend_image ? `<img src="/static/images/${trend.trend_image}" class="trend-img w-12 h-12 rounded-md object-cover" alt="${trend.trend_title}">` : ""}
                            <div class="trend-text">
                                <p class="text-c-gray:+20 text-90">${trend.trend_title}</p>
                                <p class="text-c-black text-80">${trend.trend_message} <button class="text-c-tealblue text-60">... more</button></p>
                            </div>
                        </div>
                        <span class="option cursor-pointer text-90">⋮</span>
                    </div>
                `;
                trendsContainer.innerHTML += trendHTML;
            });
        })
        .catch(err => console.error("Error loading trends:", err));
});

// ##############################
document.addEventListener("DOMContentLoaded", () => {
    const trends = Array.from(document.querySelectorAll(".trend-item"));
    const maxVisible = 6; // number of trends to show initially

    if (trends.length > maxVisible) {
        // Hide all trends beyond maxVisible
        trends.forEach((trend, i) => {
            if (i >= maxVisible) trend.classList.add("hidden");
        });

        // Create the "More news" button
        const moreBtn = document.createElement("button");
        moreBtn.textContent = "More news";
        moreBtn.className = "text-c-tealblue mt-2";
        trends[trends.length - 1].parentNode.appendChild(moreBtn);

        moreBtn.addEventListener("click", () => {
            trends.forEach(trend => trend.classList.remove("hidden"));
            moreBtn.remove(); // remove button after expanding
        });
    }

    // Optional: handle "... more" toggle for long messages
    document.querySelectorAll(".trend-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            const parent = btn.closest("p");
            const fullText = parent.querySelector(".trend-full");
            const shortText = parent.querySelector(".trend-short");

            if (fullText && shortText) {
                fullText.classList.toggle("hidden");
                shortText.classList.toggle("hidden");
                btn.textContent = fullText.classList.contains("hidden") ? "... more" : "show less";
            }
        });
    });
});


// ##############################
document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".follow-btn");
    if (!btn) return;

    const userPk = btn.dataset.user;
    const action = btn.dataset.action;

    // Optimistisk UI toggle
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

    try {
        const res = await fetch(`/api-${action}`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `following_pk=${encodeURIComponent(userPk)}`
        });
        const data = await res.json();
        if (!data.success) throw new Error(data.error);

    } catch (err) {
        console.error("Follow API error:", err);
        // Revert UI hvis API fejler
        if (action === "follow") {
            btn.textContent = "Follow";
            btn.classList.remove("bg-c-gray-500");
            btn.classList.add("bg-c-black");
            btn.dataset.action = "follow";
        } else {
            btn.textContent = "Unfollow";
            btn.classList.remove("bg-c-black");
            btn.classList.add("bg-c-gray-500");
            btn.dataset.action = "unfollow";
        }
    }
});




