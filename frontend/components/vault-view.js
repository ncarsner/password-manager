import React from 'react';

const VaultView = ({ vaultName, passwords = [] }) => {
    return (
        <div>
            {vaultName && <h1>{vaultName}</h1>}
            {passwords.length === 0 ? (
                <p>No passwords available</p>
            ) : (
                <ul>
                    {passwords.map((password, index) => (
                        <li key={index}>{password}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default VaultView;
