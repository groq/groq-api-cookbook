import json
from bitcoinlib import keys, wallets, mnemonic
from bitcoinlib.wallets import WalletError
from bitcoinlib.encoding import to_hexstring

class CryptoWallet:
    def __init__(self, wallet_name, network='bitcoin', seed_phrase=None):
        self.wallet_name = wallet_name
        self.network = network
        self.seed_phrase = seed_phrase

        # Validate wallet name
        if not wallet_name or not isinstance(wallet_name, str):
            raise ValueError("Invalid wallet name")

        # Validate network
        supported_networks = ['bitcoin', 'testnet', 'litecoin']
        if network not in supported_networks:
            raise ValueError(f"Unsupported network: {network}")

        # Check if a wallet with the same name already exists
        try:
            self.wallet = wallets.Wallet(self.wallet_name)
            print(f"Wallet '{self.wallet_name}' already exists. Using the existing wallet.")
        except wallets.WalletError:
            # Create a new HDKey object from the seed phrase or generate a new one
            if seed_phrase:
                if not mnemonic.Mnemonic().check(seed_phrase):
                    raise ValueError("Invalid seed phrase")
                self.hd_key = keys.HDKey.from_passphrase(seed_phrase)
            else:
                self.seed_phrase = mnemonic.Mnemonic().generate()
                self.hd_key = keys.HDKey.from_passphrase(self.seed_phrase)

            # Create a new Wallet object
            self.wallet = wallets.Wallet.create(self.wallet_name, keys=self.hd_key, network=self.network)
            print(f"New wallet '{self.wallet_name}' created.")

    def get_wallet_info(self):
        # Get wallet information
        address = self.wallet.keys()[0].address
        balance = self.wallet.balance()
        transactions = self.wallet.transactions()

        wallet_info = {
            'address': address,
            'balance': balance,
            'transactions': [tx.as_dict() for tx in transactions]
        }
        return wallet_info

    def send_transaction(self, destination_address, amount, fee=None):
        try:
            # Validate the destination address
            if not keys.Address.is_valid(destination_address, network=self.network):
                raise ValueError("Invalid destination address")

            # Validate the amount
            if not isinstance(amount, int) or amount <= 0:
                raise ValueError("Invalid amount. Must be a positive integer.")

            # Create and send the transaction
            transaction = self.wallet.send_to(destination_address, amount, fee=fee)
            return {
                'txid': to_hexstring(transaction.txid),
                'status': 'success'
            }

        except (ValueError, WalletError) as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_transaction_history(self, limit=10, offset=0):
        # Retrieve transaction history
        transactions = self.wallet.transactions(limit=limit, offset=offset)
        return [tx.as_dict() for tx in transactions]

    def backup_wallet(self, backup_file):
        # Backup wallet data to a file
        wallet_data = {
            'seed_phrase': self.seed_phrase,
            'xpub': self.wallet.public_master().wif(),
            'addresses': [key.address for key in self.wallet.keys()],
            'balance': self.wallet.balance()
        }
        with open(backup_file, 'w') as f:
            json.dump(wallet_data, f)

    def restore_wallet(self, backup_file):
        # Restore wallet from a backup file
        with open(backup_file, 'r') as f:
            wallet_data = json.load(f)
        self.seed_phrase = wallet_data['seed_phrase']
        self.hd_key = keys.HDKey.from_passphrase(self.seed_phrase)
        self.wallet = wallets.Wallet.create(self.wallet_name, keys=self.hd_key, network=self.network)
        print(f"Wallet '{self.wallet_name}' restored from backup.")

    def generate_new_address(self):
        # Generate a new address
        new_address = self.wallet.get_key().address
        return new_address

    def __str__(self):
        return f"CryptoWallet(name='{self.wallet_name}', network='{self.network}')"