import csv


def transactions_data_collecting(csv_file_name: str) -> dict:
    """
    The function receives csv file name that contains contract(card) transactions info, reads this file and collects
    necessary info in dictionary fot further adding to database.
    :return: dictionary with contract(card) transactions
    """

    # Contract and card numbers, as well as all types of transactions are collected in dictionary
    data_for_db = {}

    def table_collecting(csvfile_iterator) -> list:
        """
        The function collects rows of table with transaction data from csv file
        :param csvfile_iterator: iterator returned by csv.reader
        :return: list of table rows (first row in returned list is table header)
        """
        transactions = []
        for table_row in csvfile_iterator:
            if not table_row[0].startswith('Всего') and table_row[0] != '':
                transactions.append(table_row[:-1])
            else:
                return transactions
        return transactions

    with open(csv_file_name) as file:
        reader = csv.reader(file, delimiter=';')

        for row in reader:

            # Searching for file header main info (Contract number and Card number)
            if row and row[0] == 'Номер контракта:':
                contract_number = row[1].split(' ')[0][-4:]  # last 4 digits
                data_for_db['Contract number'] = contract_number
            elif row and row[0] == 'Карта:':
                card_number = row[1].split(' ')[0][-4:]  # last 4 digits
                data_for_db['Card number'] = card_number

            # Searching for table with valid Contract transactions and adding table to the dictionary
            elif row and row[0].startswith('Операции по') and row[0][-4:] == contract_number:
                data_for_db['Contract transactions'] = table_collecting(reader)

            # Searching for table with valid Card transactions and adding table to the dictionary
            elif row and row[0].startswith('Операции по') and row[0][-4:] == card_number:
                data_for_db['Card transactions'] = table_collecting(reader)

            # Searching for table with blocked Contract transactions and adding table to the dictionary
            elif row and row[0].startswith('Заблокированные суммы по') and row[0][-4:] == contract_number:
                data_for_db['Blocked contract transactions'] = table_collecting(reader)

            # Searching for table with blocked Card transactions and adding table to the dictionary
            elif row and row[0].startswith('Заблокированные суммы по') and row[0][-4:] == card_number:
                data_for_db['Blocked card transactions'] = table_collecting(reader)

    return data_for_db


if __name__ == '__main__':
    import sys

    result = transactions_data_collecting(sys.argv[1])
    for elem in result:
        if isinstance(result[elem], list):
            print(elem)
            for index, row in enumerate(result[elem]):
                print(index, row)
            print()
        elif isinstance(result[elem], str):
            print(elem, result[elem])
        else:
            print(f'Unexpected type ({type(result[elem])}) is found among dictionary values')
