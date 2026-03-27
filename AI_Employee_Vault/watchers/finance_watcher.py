#!/usr/bin/env python3
"""
Finance Watcher

Monitors bank transactions from CSV files or banking APIs.
Detects late fees, subscriptions, and unusual transactions.
Creates action files for review in the Needs_Action folder.

Usage:
    python finance_watcher.py <vault_path> [check_interval]
"""

import sys
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal

# Import base watcher
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher


class FinanceWatcher(BaseWatcher):
    """
    Watcher that monitors bank transactions and financial data.
    """

    def __init__(self, vault_path: str, check_interval: int = 300):
        """
        Initialize Finance Watcher.

        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 300 = 5 minutes)
        """
        super().__init__(vault_path, check_interval)

        # Transaction monitoring configuration
        self.transaction_folder = self.vault_path / 'Accounting'
        self.transaction_folder.mkdir(parents=True, exist_ok=True)

        # Track processed transaction hashes
        self.processed_transactions: set = set()

        # Alert thresholds
        self.large_transaction_threshold = Decimal('500.00')
        self.late_fee_keywords = ['late fee', 'overdraft', 'nsf', 'penalty', 'charge']
        self.subscription_patterns = {
            'netflix': 'Netflix Subscription',
            'spotify': 'Spotify Premium',
            'adobe': 'Adobe Creative Cloud',
            'notion': 'Notion',
            'slack': 'Slack',
            'aws': 'Amazon Web Services',
            'google cloud': 'Google Cloud',
            'microsoft': 'Microsoft 365',
            'github': 'GitHub',
            'zoom': 'Zoom',
        }

        # Load last processed state
        self._load_state()

        self.logger.info(f'Transaction folder: {self.transaction_folder}')
        self.logger.info(f'Large transaction threshold: ${self.large_transaction_threshold}')

    def _load_state(self) -> None:
        """Load last processed transaction state."""
        state_file = self.vault_path / 'Logs' / 'finance_watcher_state.json'
        if state_file.exists():
            try:
                import json
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_transactions = set(state.get('processed_ids', []))
                    self.logger.info(f'Loaded state: {len(self.processed_transactions)} transactions in history')
            except Exception as e:
                self.logger.warning(f'Could not load state: {e}')

    def _save_state(self) -> None:
        """Save current processed transaction state."""
        state_file = self.vault_path / 'Logs' / 'finance_watcher_state.json'
        try:
            import json
            # Keep only last 1000 transactions in memory
            processed_list = list(self.processed_transactions)[-1000:]
            with open(state_file, 'w') as f:
                json.dump({'processed_ids': processed_list}, f)
        except Exception as e:
            self.logger.error(f'Could not save state: {e}')

    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new bank transactions from CSV files.

        Returns:
            List of new transactions to process
        """
        new_transactions = []

        try:
            # Look for CSV files in Accounting folder
            csv_files = list(self.transaction_folder.glob('*.csv'))

            if not csv_files:
                self.logger.debug('No CSV files found in Accounting folder')
                return []

            for csv_file in csv_files:
                transactions = self._parse_csv(csv_file)

                for txn in transactions:
                    # Create unique transaction ID
                    txn_id = self._generate_transaction_id(txn)

                    if txn_id not in self.processed_transactions:
                        new_transactions.append(txn)
                        self.processed_transactions.add(txn_id)
                        self.logger.info(f'New transaction: {txn["description"]} - ${txn["amount"]}')

            # Save state after processing
            if new_transactions:
                self._save_state()

        except Exception as e:
            self.logger.error(f'Error checking transactions: {e}', exc_info=True)

        return new_transactions

    def _parse_csv(self, csv_file: Path) -> List[Dict[str, Any]]:
        """
        Parse bank CSV file.

        Expected format:
        Date,Description,Amount,Balance,Category

        Args:
            csv_file: Path to CSV file

        Returns:
            List of transaction dictionaries
        """
        transactions = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        # Normalize field names
                        txn = {
                            'date': row.get('Date', row.get('date', '')),
                            'description': row.get('Description', row.get('description', row.get('Narration', ''))),
                            'amount': Decimal(row.get('Amount', row.get('amount', '0'))),
                            'balance': Decimal(row.get('Balance', row.get('balance', '0'))),
                            'category': row.get('Category', row.get('category', 'Uncategorized')),
                            'source_file': csv_file.name,
                        }

                        # Analyze transaction
                        txn['analysis'] = self._analyze_transaction(txn)

                        transactions.append(txn)

                    except Exception as e:
                        self.logger.debug(f'Error parsing row: {e}')
                        continue

        except Exception as e:
            self.logger.error(f'Error reading CSV {csv_file}: {e}')

        return transactions

    def _analyze_transaction(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a transaction for alerts and categorization.

        Args:
            txn: Transaction dictionary

        Returns:
            Analysis results
        """
        analysis = {
            'is_large': False,
            'is_late_fee': False,
            'is_subscription': False,
            'subscription_name': None,
            'alert_type': None,
            'priority': 'normal',
        }

        description_lower = txn['description'].lower()
        amount = txn['amount']

        # Check for large transactions
        if abs(amount) >= self.large_transaction_threshold:
            analysis['is_large'] = True
            analysis['alert_type'] = 'large_transaction'
            analysis['priority'] = 'high'

        # Check for late fees
        for keyword in self.late_fee_keywords:
            if keyword in description_lower:
                analysis['is_late_fee'] = True
                analysis['alert_type'] = 'late_fee'
                analysis['priority'] = 'urgent'
                break

        # Check for subscriptions
        for pattern, name in self.subscription_patterns.items():
            if pattern in description_lower:
                analysis['is_subscription'] = True
                analysis['subscription_name'] = name
                analysis['alert_type'] = 'subscription'
                break

        return analysis

    def _generate_transaction_id(self, txn: Dict[str, Any]) -> str:
        """
        Generate unique ID for a transaction.

        Args:
            txn: Transaction dictionary

        Returns:
            Unique transaction ID hash
        """
        # Create unique string from transaction data
        unique_str = f"{txn['date']}|{txn['description']}|{txn['amount']}"
        return hashlib.md5(unique_str.encode()).hexdigest()

    def create_action_file(self, transaction: Dict[str, Any]) -> Optional[Path]:
        """
        Create an action file for a transaction.

        Args:
            transaction: Transaction dictionary

        Returns:
            Path to created action file
        """
        try:
            analysis = transaction['analysis']

            # Determine priority and action type
            priority = analysis['priority']
            action_type = analysis['alert_type']

            # Generate frontmatter
            frontmatter = self.generate_frontmatter(
                item_type='finance_transaction',
                description=transaction['description'],
                amount=str(transaction['amount']),
                date=transaction['date'],
                category=transaction['category'],
                priority=priority,
                alert_type=action_type or 'info'
            )

            # Create action file content based on transaction type
            if analysis['is_late_fee']:
                content = self._create_late_fee_action_file(transaction, frontmatter)
            elif analysis['is_large']:
                content = self._create_large_transaction_action_file(transaction, frontmatter)
            elif analysis['is_subscription']:
                content = self._create_subscription_action_file(transaction, frontmatter)
            else:
                content = self._create_standard_transaction_action_file(transaction, frontmatter)

            # Write action file
            safe_desc = transaction['description'][:30].replace(' ', '_').replace('/', '_')
            action_filepath = self.get_unique_filename(f'TXN_{safe_desc}')
            action_filepath.write_text(content, encoding='utf-8')

            self.logger.info(f'Finance action file created: {action_filepath.name}')
            return action_filepath

        except Exception as e:
            self.logger.error(f'Error creating finance action file: {e}', exc_info=True)
            return None

    def _create_late_fee_action_file(self, txn: Dict, frontmatter: str) -> str:
        """Create action file for late fee transaction."""
        return f'''{frontmatter}

# ⚠️ LATE FEE DETECTED

## Transaction Details
- **Date:** {txn['date']}
- **Description:** {txn['description']}
- **Amount:** ${txn['amount']}
- **Category:** {txn['category']}

## Alert
🚨 **Late fee or penalty charge detected!**

## Suggested Actions
- [ ] Review why this fee was charged
- [ ] Check if payment was missed
- [ ] Contact bank to dispute fee (if applicable)
- [ ] Set up automatic payment to prevent future fees
- [ ] Update cash flow projection
- [ ] Move to /Done when resolved

## Notes
Add investigation notes here:

---
*Detected by Finance Watcher - Late Fee Alert*
'''

    def _create_large_transaction_action_file(self, txn: Dict, frontmatter: str) -> str:
        """Create action file for large transaction."""
        return f'''{frontmatter}

# 💰 LARGE TRANSACTION DETECTED

## Transaction Details
- **Date:** {txn['date']}
- **Description:** {txn['description']}
- **Amount:** ${txn['amount']}
- **Category:** {txn['category']}
- **Balance After:** ${txn['balance']}

## Alert
💵 **Large transaction above ${self.large_transaction_threshold} threshold**

## Suggested Actions
- [ ] Verify this transaction is legitimate
- [ ] Check against budget/forecasts
- [ ] Update cash flow projections
- [ ] Review impact on monthly burn rate
- [ ] File/ categorize appropriately
- [ ] Move to /Done when reviewed

## Verification Notes
Add verification details here:

---
*Detected by Finance Watcher - Large Transaction Alert*
'''

    def _create_subscription_action_file(self, txn: Dict, frontmatter: str) -> str:
        """Create action file for subscription transaction."""
        sub_name = txn['analysis'].get('subscription_name', 'Unknown Subscription')
        return f'''{frontmatter}

# 🔄 SUBSCRIPTION PAYMENT

## Transaction Details
- **Date:** {txn['date']}
- **Description:** {txn['description']}
- **Amount:** ${txn['amount']}
- **Subscription:** {sub_name}
- **Category:** {txn['category']}

## Alert
📋 **Recurring subscription payment detected**

## Suggested Actions
- [ ] Verify subscription is still needed
- [ ] Check usage of this service
- [ ] Compare with budgeted amount
- [ ] Review for potential cancellation
- [ ] Update subscription tracking sheet
- [ ] Move to /Done when reviewed

## Usage Review
Is this subscription still valuable? ___

Last used: ___

---
*Detected by Finance Watcher - Subscription Tracking*
'''

    def _create_standard_transaction_action_file(self, txn: Dict, frontmatter: str) -> str:
        """Create action file for standard transaction."""
        return f'''{frontmatter}

# 📊 Financial Transaction

## Transaction Details
- **Date:** {txn['date']}
- **Description:** {txn['description']}
- **Amount:** ${txn['amount']}
- **Balance After:** ${txn['balance']}
- **Category:** {txn['category']}

## Suggested Actions
- [ ] Review transaction
- [ ] Categorize if needed
- [ ] Add to accounting records
- [ ] Move to /Done when processed

## Notes
Add notes here:

---
*Detected by Finance Watcher*
'''

    def run_continuous(self) -> None:
        """Run Finance Watcher continuously."""
        self.logger.info('Starting continuous Finance monitoring...')
        self.logger.info(f'Monitoring folder: {self.transaction_folder}')
        self.logger.info('Press Ctrl+C to stop')

        try:
            while True:
                transactions = self.check_for_updates()

                if transactions:
                    self.logger.info(f'Found {len(transactions)} new transaction(s)')
                    for txn in transactions:
                        self.create_action_file(txn)

                # Also update monthly summary
                self._update_monthly_summary()

                import time
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info('Finance Watcher stopped by user')
        finally:
            self._save_state()

    def _update_monthly_summary(self) -> None:
        """Update monthly financial summary."""
        try:
            current_month = datetime.now().strftime('%Y_%m')
            summary_file = self.transaction_folder / f'{current_month}_Summary.md'

            # Read all CSVs and calculate totals
            total_income = Decimal('0')
            total_expenses = Decimal('0')
            transaction_count = 0

            csv_files = list(self.transaction_folder.glob('*.csv'))
            for csv_file in csv_files:
                transactions = self._parse_csv(csv_file)
                for txn in transactions:
                    transaction_count += 1
                    if txn['amount'] > 0:
                        total_income += txn['amount']
                    else:
                        total_expenses += abs(txn['amount'])

            # Create/update summary
            content = f'''---
generated: {datetime.now().isoformat()}
month: {current_month}
---

# Monthly Financial Summary

## Overview
- **Month:** {current_month.replace('_', ' ')}
- **Total Income:** ${total_income}
- **Total Expenses:** ${total_expenses}
- **Net:** ${total_income - total_expenses}
- **Transactions:** {transaction_count}

## Alerts This Month
- Large transactions: Check /Needs_Action for TXN_* files
- Late fees: Check /Needs_Action for late fee alerts
- Subscriptions: Check /Needs_Action for subscription tracking

## Notes
Add monthly review notes here:

---
*Generated by Finance Watcher*
'''

            summary_file.write_text(content, encoding='utf-8')

        except Exception as e:
            self.logger.debug(f'Could not update summary: {e}')


def main():
    """Main entry point for Finance Watcher."""
    if len(sys.argv) < 2:
        print('Usage: python finance_watcher.py <vault_path> [check_interval]')
        print('')
        print('Arguments:')
        print('  vault_path       Path to the Obsidian vault root')
        print('  check_interval   Seconds between checks (default: 300)')
        print('')
        print('Example:')
        print('  python finance_watcher.py "./AI_Employee_Vault" 300')
        print('')
        print('Note: Place bank CSV files in the Accounting/ folder')
        print('      Expected format: Date,Description,Amount,Balance,Category')
        sys.exit(1)

    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)

    # Create watcher
    watcher = FinanceWatcher(vault_path, check_interval)

    print('=' * 60)
    print('Finance Watcher - Gold Tier')
    print('=' * 60)
    print(f'Vault: {vault_path}')
    print(f'Check Interval: {check_interval}s')
    print(f'Transaction Folder: {watcher.transaction_folder}')
    print(f'Large Transaction Threshold: ${watcher.large_transaction_threshold}')
    print('')
    print('Monitoring for:')
    print('  ✓ Large transactions')
    print('  ✓ Late fees')
    print('  ✓ Subscription payments')
    print('')
    print('Starting Finance monitoring...')
    print('Press Ctrl+C to stop')
    print('=' * 60)

    # Run watcher
    watcher.run_continuous()


if __name__ == '__main__':
    main()
