import { render, screen } from '@testing-library/react';
import VaultView from '../components/vault-view';

describe('VaultView Component', () => {
    test('renders vault name', () => {
        const vaultName = 'My Vault';
        render(<VaultView vaultName={vaultName} />);
        const vaultElement = screen.getByText(/My Vault/i);
        expect(vaultElement).toBeInTheDocument();
    });

    test('renders password list', () => {
        const passwords = ['password1', 'password2'];
        render(<VaultView passwords={passwords} />);
        passwords.forEach(password => {
            const passwordElement = screen.getByText(password);
            expect(passwordElement).toBeInTheDocument();
        });
    });

    test('renders empty state when no passwords', () => {
        render(<VaultView passwords={[]} />);
        const emptyStateElement = screen.getByText(/No passwords available/i);
        expect(emptyStateElement).toBeInTheDocument();
    });
});
