import json

class SessionManager:

    sessions = {}

    @classmethod
    def create_session(cls, accesscode, engine):

        if accesscode in cls.sessions:

            old_engine = cls.sessions[accesscode]

            # Save holdings before destroying
            with open(f"{accesscode}_holdings.json", "w") as f:
                json.dump(old_engine.holdings, f)

            del cls.sessions[accesscode]

        cls.sessions[accesscode] = engine


    @classmethod
    def get_engine(cls, accesscode):

        return cls.sessions.get(accesscode)


    @classmethod
    def load_holdings(cls, accesscode):

        try:
            with open(f"{accesscode}_holdings.json") as f:
                return json.load(f)
        except:
            return {}