from models import Role

def add_roles(database):
    """Utility function to avoid creating roles manually."""

    roles = [
        {
            'name': 'Administrator',
            'description': 'Has access to delete users.'
        },
        {
            'name': 'Client',
            'description': None
        }
    ]

    for r in roles:
        new_role = Role(
            name=r['name'],
            description=r['description']
        )
        database.session.add(new_role)

    database.session.commit()

    return


if __name__ == '__main__':
    from app import db
    add_roles(db)
