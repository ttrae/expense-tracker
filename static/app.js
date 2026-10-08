const API = "/api/expenses";
const form = document.getElementById("expenseForm");
const expenseIdField = document.getElementById("expenseId");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const expenseList = document.getElementById("expenseList");
const totalAmountEl = document.getElementById("totalAmount");
const totalCountEl = document.getElementById("totalCount");
const filterCategory = document.getElementById("filterCategory");

let allExpenses = [];

document.getElementById("date").valueAsDate = new Date();

form.addEventListener("submit", handleSubmit);
cancelBtn.addEventListener("click", resetForm);
filterCategory.addEventListener("change", renderExpenses);

async function fetchExpenses() {
  const res = await fetch(API);
  allExpenses = await res.json();
  renderExpenses();
}

function renderExpenses() {
  const filter = filterCategory.value;
  const expenses = filter
    ? allExpenses.filter((e) => e.category === filter)
    : allExpenses;

  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  totalAmountEl.textContent = "Rs" + total.toFixed(2);
  totalCountEl.textContent = expenses.length;

  if (expenses.length === 0) {
    expenseList.innerHTML =
      '<p class="empty-state">No expenses found.</p>';
    return;
  }

  expenseList.innerHTML = expenses
    .map(
      (e) => `
    <div class="expense-item">
      <div class="expense-info">
        <span class="expense-title">${escapeHtml(e.title)}</span>
        <span class="expense-meta">
          <span class="category-badge cat-${e.category}">${e.category}</span>
          &nbsp;${e.date}
        </span>
      </div>
      <div class="expense-right">
        <span class="expense-amount">Rs${e.amount.toFixed(2)}</span>
        <div class="expense-actions">
          <button onclick="editExpense(${e.id})" title="Edit">&#9998;</button>
          <button onclick="deleteExpense(${e.id})" title="Delete">&#10005;</button>
        </div>
      </div>
    </div>`
    )
    .join("");
}

async function handleSubmit(ev) {
  ev.preventDefault();
  const data = {
    title: document.getElementById("title").value.trim(),
    amount: parseFloat(document.getElementById("amount").value),
    category: document.getElementById("category").value,
    date: document.getElementById("date").value,
  };

  if (!data.title || !data.amount || !data.category || !data.date) return;

  const id = expenseIdField.value;
  if (id) {
    await fetch(`${API}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  } else {
    await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }

  resetForm();
  fetchExpenses();
}

function editExpense(id) {
  const expense = allExpenses.find((e) => e.id === id);
  if (!expense) return;
  expenseIdField.value = expense.id;
  document.getElementById("title").value = expense.title;
  document.getElementById("amount").value = expense.amount;
  document.getElementById("category").value = expense.category;
  document.getElementById("date").value = expense.date;
  formTitle.textContent = "Edit Expense";
  submitBtn.textContent = "Update Expense";
  cancelBtn.style.display = "inline-block";
}

async function deleteExpense(id) {
  if (!confirm("Delete this expense?")) return;
  await fetch(`${API}/${id}`, { method: "DELETE" });
  fetchExpenses();
}

function resetForm() {
  form.reset();
  document.getElementById("date").valueAsDate = new Date();
  expenseIdField.value = "";
  formTitle.textContent = "Add Expense";
  submitBtn.textContent = "Add Expense";
  cancelBtn.style.display = "none";
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

fetchExpenses();
