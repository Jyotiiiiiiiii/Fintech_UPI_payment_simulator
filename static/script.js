/* API Configuration */
const API_BASE_URL = 'http://localhost:8000/api';

/* Toast Notification Function */
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

/* Message Display Function */
function showMessage(elementId, message, type = 'success') {
    const msgElement = document.getElementById(elementId);
    msgElement.textContent = message;
    msgElement.className = `message ${type}`;
    setTimeout(() => {
        msgElement.className = 'message';
    }, 5000);
}

/* Tab Navigation */
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const tabName = e.target.dataset.tab;
        
        // Remove active from all
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active to clicked
        e.target.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

/* Register Form */
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('regName').value,
        email: document.getElementById('regEmail').value,
        upi_id: document.getElementById('regUPI').value,
        phone: document.getElementById('regPhone').value,
        initial_balance: parseFloat(document.getElementById('regBalance').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('registerMessage', `✓ User registered successfully! UPI ID: ${data.upi_id}`, 'success');
            showToast(`${data.name} registered with balance ₹${data.balance}`, 'success');
            document.getElementById('registerForm').reset();
            document.getElementById('regBalance').value = 1000;
        } else {
            showMessage('registerMessage', `✗ ${data.detail || 'Registration failed'}`, 'error');
        }
    } catch (error) {
        showMessage('registerMessage', `✗ Error: ${error.message}`, 'error');
    }
});

/* Payment Form */
document.getElementById('paymentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        sender_upi: document.getElementById('senderUPI').value,
        receiver_upi: document.getElementById('receiverUPI').value,
        amount: parseFloat(document.getElementById('amount').value),
        description: document.getElementById('description').value || null,
        pin: document.getElementById('pin').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/payments/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            showMessage('paymentMessage', `✓ Payment successful! Transaction ID: ${data.transaction_id}`, 'success');
            showToast(`₹${formData.amount} sent to ${formData.receiver_upi}`, 'success');
            document.getElementById('paymentForm').reset();
        } else {
            showMessage('paymentMessage', `✗ Payment failed: ${data.message}`, 'error');
            showToast(data.message, 'error');
        }
    } catch (error) {
        showMessage('paymentMessage', `✗ Error: ${error.message}`, 'error');
    }
});

/* Search User Function */
async function searchUser() {
    const upiId = document.getElementById('searchUPI').value.trim();
    
    if (!upiId) {
        showToast('Please enter a UPI ID', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users/${upiId}`);
        const data = await response.json();

        if (response.ok) {
            displayUserProfile(data);
        } else {
            showToast('User not found', 'error');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Display User Profile */
function displayUserProfile(user) {
    const dashboardResults = document.getElementById('dashboardResults');
    
    const html = `
        <div class="card user-profile-card">
            <div class="card">
                <h3>${user.name}</h3>
                <div class="user-info">
                    <div class="info-item">
                        <div class="info-label">UPI ID</div>
                        <div class="info-value">${user.upi_id}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Email</div>
                        <div class="info-value">${user.email}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Phone</div>
                        <div class="info-value">${user.phone}</div>
                    </div>
                    <div class="info-item balance-item">
                        <div class="info-label">Current Balance</div>
                        <div class="info-value">₹${user.balance.toFixed(2)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Account Created</div>
                        <div class="info-value">${new Date(user.created_at).toLocaleDateString()}</div>
                    </div>
                </div>
                <button class="btn-primary" style="width: 100%; margin-top: 20px;" onclick="loadUserTransactions('${user.upi_id}')">
                    View Transactions
                </button>
            </div>
        </div>
    `;
    
    dashboardResults.innerHTML = html;
}

/* Load User Transactions */
async function loadUserTransactions(upiId) {
    try {
        const response = await fetch(`${API_BASE_URL}/payments/transactions/${upiId}`);
        const transactions = await response.json();

        if (response.ok && transactions.length > 0) {
            displayTransactions(transactions);
            document.querySelector('[data-tab="transactions"]').click();
        } else {
            showToast('No transactions found', 'warning');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Load Transactions */
async function loadTransactions() {
    const upiId = document.getElementById('txnUPI').value.trim();
    
    if (!upiId) {
        showToast('Please enter a UPI ID', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/payments/transactions/${upiId}`);
        const data = await response.json();

        if (response.ok) {
            displayTransactions(data);
            showToast(`Loaded ${data.length} transactions`, 'success');
        } else {
            showToast('User not found or no transactions', 'error');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Load All Transactions */
async function loadAllTransactions() {
    try {
        const response = await fetch(`${API_BASE_URL}/payments/all-transactions`);
        const transactions = await response.json();

        if (response.ok) {
            displayTransactions(transactions);
            showToast(`Loaded ${transactions.length} total transactions`, 'success');
        } else {
            showToast('Failed to load transactions', 'error');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Display Transactions Table */
async function displayTransactions(transactions) {
    const tbody = document.getElementById('txnTableBody');
    
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No transactions found</td></tr>';
        return;
    }

    // Fetch user details for mapping
    const userMap = {};
    
    // Get unique user IDs
    const userIds = new Set();
    transactions.forEach(t => {
        userIds.add(t.sender_id);
        userIds.add(t.receiver_id);
    });

    // Fetch user details
    try {
        const response = await fetch(`${API_BASE_URL}/users/`);
        const users = await response.json();
        
        users.forEach(user => {
            userMap[user.id] = user.upi_id;
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }

    const rows = transactions.map(txn => {
        const senderUPI = userMap[txn.sender_id] || `User ${txn.sender_id}`;
        const receiverUPI = userMap[txn.receiver_id] || `User ${txn.receiver_id}`;
        const statusClass = txn.status === 'success' ? 'success' : txn.status === 'failed' ? 'failed' : 'pending';
        const datetime = new Date(txn.created_at).toLocaleString();
        
        return `
            <tr>
                <td>#${txn.id}</td>
                <td>${senderUPI}</td>
                <td>${receiverUPI}</td>
                <td>₹${txn.amount.toFixed(2)}</td>
                <td><span class="status ${statusClass}">${txn.status.toUpperCase()}</span></td>
                <td>${txn.description || '-'}</td>
                <td>${datetime}</td>
            </tr>
        `;
    }).join('');

    tbody.innerHTML = rows;
}

/* Load All Users */
async function loadAllUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/`);
        const users = await response.json();

        if (response.ok && users.length > 0) {
            displayUsers(users);
            showToast(`Loaded ${users.length} users`, 'success');
        } else {
            showToast('No users found', 'warning');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Display Users Grid */
function displayUsers(users) {
    const grid = document.getElementById('usersGrid');
    
    if (users.length === 0) {
        grid.innerHTML = '<p>No users registered yet.</p>';
        return;
    }

    const html = users.map(user => `
        <div class="user-card" onclick="showUserModal('${user.upi_id}')">
            <div class="user-card-header">
                <div class="user-card-title">${user.name}</div>
                <div class="user-card-badge">ID: ${user.id}</div>
            </div>
            <div class="user-card-info">
                <div class="user-card-item">
                    <span class="user-card-label">UPI ID:</span>
                    <span class="user-card-value">${user.upi_id}</span>
                </div>
                <div class="user-card-item">
                    <span class="user-card-label">Email:</span>
                    <span class="user-card-value">${user.email}</span>
                </div>
                <div class="user-card-item">
                    <span class="user-card-label">Phone:</span>
                    <span class="user-card-value">${user.phone}</span>
                </div>
                <div class="user-card-item">
                    <span class="user-card-label">Balance:</span>
                    <span class="user-card-balance">₹${user.balance.toFixed(2)}</span>
                </div>
            </div>
        </div>
    `).join('');

    grid.innerHTML = html;
}

/* Show User Modal */
async function showUserModal(upiId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${upiId}`);
        const user = await response.json();

        if (response.ok) {
            const modal = document.getElementById('userModal');
            const body = document.getElementById('userModalBody');
            
            const txnResponse = await fetch(`${API_BASE_URL}/payments/transactions/${upiId}`);
            const transactions = await txnResponse.json();

            const html = `
                <h2>${user.name}</h2>
                <div class="user-info" style="margin: 20px 0;">
                    <div class="info-item">
                        <div class="info-label">UPI ID</div>
                        <div class="info-value">${user.upi_id}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Email</div>
                        <div class="info-value">${user.email}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Phone</div>
                        <div class="info-value">${user.phone}</div>
                    </div>
                    <div class="info-item balance-item">
                        <div class="info-label">Current Balance</div>
                        <div class="info-value">₹${user.balance.toFixed(2)}</div>
                    </div>
                </div>
                <h3 style="margin-top: 25px;">Recent Transactions (${transactions.length})</h3>
                <div class="table-container" style="margin-top: 15px; max-height: 300px; overflow-y: auto;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${transactions.length > 0 ? transactions.slice(0, 5).map(t => `
                                <tr>
                                    <td>₹${t.amount.toFixed(2)}</td>
                                    <td><span class="status ${t.status}">${t.status.toUpperCase()}</span></td>
                                    <td>${new Date(t.created_at).toLocaleDateString()}</td>
                                </tr>
                            `).join('') : '<tr><td colspan="3" class="text-center">No transactions</td></tr>'}
                        </tbody>
                    </table>
                </div>
            `;
            
            body.innerHTML = html;
            modal.classList.add('show');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

/* Close Modal */
function closeModal() {
    document.getElementById('userModal').classList.remove('show');
}

/* Close modal when clicking outside */
window.addEventListener('click', (e) => {
    const modal = document.getElementById('userModal');
    if (e.target === modal) {
        modal.classList.remove('show');
    }
});
