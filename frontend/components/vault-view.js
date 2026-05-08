import React, { useEffect, useState } from 'react';

const VaultView = () => {
    const [vaults, setVaults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchVaults = async () => {
            try {
                const response = await fetch('/api/v1/vaults');
                const data = await response.json();
                setVaults(data);
            } catch (error) {
                console.error('Error fetching vaults:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchVaults();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Your Vaults</h1>
            <ul>
                {vaults.map(vault => (
                    <li key={vault.id}>
                        <h2>{vault.name}</h2>
                        <p>Passwords: {vault.passwords.length}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default VaultView;