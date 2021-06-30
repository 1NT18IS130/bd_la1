from mongoengine import Document, ListField, StringField, URLField, errors
from bson import ObjectId

class Data(Document):
    discord_id = StringField(required=True, max_length=70, unique=True)
    artists = ListField(StringField(max_length=20))

class Database():

    def __init__(self, client):
        self.client = client
    
    def add_data(data):
        '''
        Save a new database entry or add a new data to existing record
        '''
        try:
            Data.objects.get(discord_id=data['discord_id'])
            Data.objects(discord_id=data['discord_id']).update(push_all__artists=data['artists'])
        except errors.DoesNotExist:   
            Data(discord_id = data['discord_id'],
                artists = data['artists']
            ).save()

    def del_data(data):
        try:
            dt = Data.objects(discord_id=data['discord_id'])
            dt.update(pull_all__artists=data['value'])
            return True
        except errors.DoesNotExist:
            return None

    def get_data(user: str):
        '''
        Fetch the artists for a particular user if it exists
        '''
        try:
            return Data.objects.get(discord_id=user)['artists']
        except Exception as e:
            print(e)
            print("No data found")
            return None

        
