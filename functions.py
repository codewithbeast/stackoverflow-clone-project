def check(session):
    id = session.get("user_id")

    if id:
        return True
    
    else:
        return False