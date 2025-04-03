from app import app, models

if __name__ == '__main__':
    #app.run(debug=True)


    # clear all tables in database
    from AISPIRE_demo import app, models

    with app.app_context():
        models.User.query.delete()
        models.EssayHistory.query.delete()
        models.db.session.commit()  

