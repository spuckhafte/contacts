import mysql.connector as connector;

cnx = connector.connect(
    user='root', password='spuckjs@15.sql',
    database='mydb'
)
cursor = cnx.cursor();

class Db:
    def __init__(self, table):
        self.table = table;

    def get(self, fields, filter='', value=[]):
        cursor.execute(
            f'select {fields} from {self.table} {filter}',
            tuple(value) if len(value) > 0 else ()
        );
        return cursor.fetchall();

    def put(self, data):
        into = ", ".join(data.keys());
        total = len(data.keys());
        s = ('%s,' * total)[:-1];

        query = f"INSERT INTO {self.table} ({into}) VALUES ({s})";
        values = tuple(data.values());

        cursor.execute(query, values);
        cnx.commit();
        return 1;

    def remove(self, field, value):
        query = f'DELETE FROM {self.table} WHERE {field} = %s';
        cursor.execute(query, tuple(value));
        cnx.commit();
        return 1;

contacts = Db('contacts');

def createContact():
    name = input(' -name: ');
    phone = input(' -phone: ');
    email = input(' -email: ');

    contacts.put({
        'name': name,
        'phone': phone,
        'email': email
    });
    print('\n[CONTACT ADDED!]');

def deleteContact():
    name = input(' -name: ');
    contacts.remove('name', [name]);

    print(f'\n[{name} REMOVED SUCCESSFULLY]');

def viewAll():
    for user in contacts.get('*'):
        print(f'{user[0]}.{user[1]}: {user[2]}');
    input('\n...press enter to continue')

def viewOne():
    name = input(' -name: ');
    for user in contacts.get('*', f'where name = %s', [name]):
        print(f'\n{user[0]}: {user[1]}, {user[2]}, {user[3]}')
    input('\n...press enter to continue')

menu = '''
---MENU---
1: Create New
2: Delete One
3: View All
4: View One
----------'''

handler = {
    '1': createContact,
    '2': deleteContact,
    '3': viewAll,
    '4': viewOne
}

print('\nWELCOME TO THE CONTACT BOOK')
while True:
    print(menu);
    option = input('\n>> ');

    if (not option.isnumeric() or option not in handler.keys()):
        print('\n[INVALID OPTION]');
        continue;

    handler[option]();
