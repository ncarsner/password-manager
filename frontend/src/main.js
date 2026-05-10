const apiBaseUrl = 'http://127.0.0.1:5000/api/v1';

let currentVaultId = null;

document.addEventListener('DOMContentLoaded', () => {
    const vaultForm = document.getElementById('vault-form');
    const vaultList = document.getElementById('vault-list');
    const passwordForm = document.getElementById('password-form');
    const backToVaults = document.getElementById('back-to-vaults');

    // Vault Form Submission
    vaultForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const vaultName = document.getElementById('vault-name').value;

        if (vaultName) {
            await createVault(vaultName);
            vaultForm.reset();
            loadVaults();
        }
    });

    // Password Form Submission
    passwordForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const domain = document.getElementById('new-domain').value.trim();
        const username = document.getElementById('new-username').value.trim();
        const password = document.getElementById('new-password').value;
        const notes = document.getElementById('new-notes').value.trim();

        if (password && currentVaultId) {
            await addPassword(currentVaultId, domain, username, password, notes);
            passwordForm.reset();
            loadPasswords(currentVaultId);
        }
    });

    // Back to Vaults
    backToVaults.addEventListener('click', () => {
        showVaults();
    });

    loadVaults();
});

async function createVault(name) {
    try {
        const response = await fetch(`${apiBaseUrl}/vaults`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name }),
        });
        if (!response.ok) throw new Error('Failed to create vault');
    } catch (error) {
        console.error(error);
        alert('Error creating vault');
    }
}

async function loadVaults() {
    try {
        const response = await fetch(`${apiBaseUrl}/vaults`);
        const vaults = await response.json();
        renderVaults(vaults);
    } catch (error) {
        console.error('Error loading vaults:', error);
    }
}

function renderVaults(vaults) {
    const vaultList = document.getElementById('vault-list');
    vaultList.innerHTML = '';
    vaults.forEach(vault => {
        const listItem = document.createElement('li');

        const nameSpan = document.createElement('span');
        nameSpan.textContent = vault.name;
        nameSpan.className = 'vault-name';
        nameSpan.onclick = () => openVault(vault.id, vault.name);

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            deleteVault(vault.id);
        };

        listItem.appendChild(nameSpan);
        listItem.appendChild(deleteBtn);
        vaultList.appendChild(listItem);
    });
}

async function deleteVault(id) {
    if (!confirm('Are you sure you want to delete this vault?')) return;
    try {
        await fetch(`${apiBaseUrl}/vaults/${id}`, { method: 'DELETE' });
        loadVaults();
    } catch (error) {
        console.error('Error deleting vault:', error);
    }
}

async function openVault(id, name) {
    currentVaultId = id;
    document.getElementById('current-vault-name').textContent = name;
    document.getElementById('vault-management').style.display = 'none';
    document.getElementById('password-management').style.display = 'block';
    loadPasswords(id);
}

function showVaults() {
    currentVaultId = null;
    document.getElementById('vault-management').style.display = 'block';
    document.getElementById('password-management').style.display = 'none';
    loadVaults();
}

async function loadPasswords(vaultId) {
    try {
        const response = await fetch(`${apiBaseUrl}/vaults/${vaultId}/passwords`);
        const passwords = await response.json();
        renderPasswords(passwords);
    } catch (error) {
        console.error('Error loading passwords:', error);
    }
}

function renderPasswords(credentials) {
    const container = document.getElementById('password-list');
    container.innerHTML = '';

    if (credentials.length === 0) {
        container.innerHTML = '<p class="empty-state">No credentials stored.</p>';
        return;
    }

    const table = document.createElement('table');
    table.className = 'credentials-table';

    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Domain</th><th>Username</th><th>Password</th><th>Notes</th><th></th></tr>';
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    credentials.forEach(p => {
        const row = document.createElement('tr');

        const domainCell = document.createElement('td');
        domainCell.className = 'col-domain';
        domainCell.textContent = p.domain || '—';
        row.appendChild(domainCell);

        const usernameCell = document.createElement('td');
        usernameCell.className = 'col-username';
        usernameCell.textContent = p.username || '—';
        row.appendChild(usernameCell);

        const passCell = document.createElement('td');
        passCell.className = 'col-password';

        const passContainer = document.createElement('div');
        passContainer.className = 'pass-container';

        if (p.password === null) {
            const errSpan = document.createElement('span');
            errSpan.className = 'pass-error';
            errSpan.textContent = 'Unrecoverable — delete and re-add';
            passContainer.appendChild(errSpan);
        } else {
            const passDisplay = document.createElement('span');
            passDisplay.className = 'pass-display';
            passDisplay.textContent = '••••••••';
            passDisplay.dataset.value = p.password;

            const toggleBtn = document.createElement('button');
            toggleBtn.textContent = 'Show';
            toggleBtn.className = 'toggle-btn toggle-show';
            toggleBtn.onclick = () => {
                const hidden = passDisplay.textContent === '••••••••';
                passDisplay.textContent = hidden ? passDisplay.dataset.value : '••••••••';
                toggleBtn.textContent = hidden ? 'Hide' : 'Show';
                toggleBtn.className = hidden ? 'toggle-btn toggle-hide' : 'toggle-btn toggle-show';
            };

            const copyBtn = document.createElement('button');
            copyBtn.textContent = 'Copy';
            copyBtn.className = 'copy-btn';
            copyBtn.onclick = async () => {
                try {
                    await navigator.clipboard.writeText(passDisplay.dataset.value);
                    copyBtn.textContent = 'Copied!';
                    copyBtn.classList.add('copy-success');
                    setTimeout(() => {
                        copyBtn.textContent = 'Copy';
                        copyBtn.classList.remove('copy-success');
                    }, 1500);
                } catch {
                    copyBtn.textContent = 'Error';
                    setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
                }
            };

            passContainer.appendChild(passDisplay);
            passContainer.appendChild(toggleBtn);
            passContainer.appendChild(copyBtn);
        }
        passCell.appendChild(passContainer);
        row.appendChild(passCell);

        const notesCell = document.createElement('td');
        notesCell.className = 'col-notes';
        notesCell.textContent = p.notes || '';
        row.appendChild(notesCell);

        const actionCell = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.className = 'delete';
        deleteBtn.onclick = () => deletePassword(p.id);
        actionCell.appendChild(deleteBtn);
        row.appendChild(actionCell);

        tbody.appendChild(row);
    });
    table.appendChild(tbody);
    container.appendChild(table);
}

async function addPassword(vaultId, domain, username, password, notes) {
    try {
        await fetch(`${apiBaseUrl}/vaults/${vaultId}/passwords`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain, username, password, notes }),
        });
    } catch (error) {
        console.error('Error adding credential:', error);
    }
}

async function deletePassword(passwordId) {
    if (!confirm('Delete this password?')) return;
    try {
        await fetch(`${apiBaseUrl}/passwords/${passwordId}`, { method: 'DELETE' });
        loadPasswords(currentVaultId);
    } catch (error) {
        console.error('Error deleting password:', error);
    }
}
