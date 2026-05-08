const apiBaseUrl = 'http://localhost:5000/api/v1';

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
        const password = document.getElementById('new-password').value;

        if (password && currentVaultId) {
            await addPassword(currentVaultId, password);
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

function renderPasswords(passwords) {
    const passwordList = document.getElementById('password-list');
    passwordList.innerHTML = '';
    passwords.forEach(p => {
        const listItem = document.createElement('li');
        
        const passSpan = document.createElement('span');
        passSpan.textContent = p.password;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = () => deletePassword(p.id);
        
        listItem.appendChild(passSpan);
        listItem.appendChild(deleteBtn);
        passwordList.appendChild(listItem);
    });
}

async function addPassword(vaultId, password) {
    try {
        await fetch(`${apiBaseUrl}/vaults/${vaultId}/passwords`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password }),
        });
    } catch (error) {
        console.error('Error adding password:', error);
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
