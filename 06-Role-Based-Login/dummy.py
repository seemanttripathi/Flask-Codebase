from app import Role, User, db

# NOTE: You need to call the below functions only once

def create_roles():
    admin = Role(id=1, name='Admin')
    teacher = Role(id=2, name='Teacher')
    staff = Role(id=3, name='Staff')
    student = Role(id=4, name='Student')

    db.session.add(admin)
    db.session.add(teacher)
    db.session.add(staff)
    db.session.add(student)

    db.session.commit()
    print("Roles created successfully!")

def create_users():
    admin = Role.query.filter_by(id=1).first()
    teacher = Role.query.filter_by(id=2).first()
    staff = Role.query.filter_by(id=3).first()
    student = Role.query.filter_by(id=4).first()

    user1 = User(email='a1@gmail.com', active=1, password='a1')
    user2 = User(email='a2@gmail.com', active=1, password='a2')
    user3 = User(email='t1@gmail.com', active=1, password='t1')
    user4 = User(email='t2@gmail.com', active=1, password='t2')
    user5 = User(email='st1@gmail.com', active=1, password='st1')
    user6 = User(email='st2@gmail.com', active=1, password='st2')
    user7 = User(email='s1@gmail.com', active=1, password='s1')
    user8 = User(email='s2@gmail.com', active=1, password='s2')

    user1.roles.append(admin)
    user2.roles.append(admin)
    user3.roles.append(teacher)
    user4.roles.append(teacher)
    user5.roles.append(staff)
    user6.roles.append(staff)
    user7.roles.append(student)
    user8.roles.append(student)

    for item in [user1, user2, user3, user4, user5, user6, user7, user8]:
        db.session.add(item)
    db.session.commit()
    print("User created successfully!")

