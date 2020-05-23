from datetime import datetime, timedelta
import jwt


class CustomJWT:
    def __init__(self, duration="JWT_FORTY_FIVE_DAYS"):
        self.created_at = ""
        self.jwt = {
            "JWT_ONE_DAY": 1,
            "JWT_TWO_DAYS": 2,
            "JWT_ONE_WEEK": 7,
            "JWT_FORTY_FIVE_DAYS": 45,
            "JWT_ONE_YEAR": 365,
            "JWT_SECRET": '$3cR3t#K3y',
            "JWT_SECRET_SUBSCRIPTION": '$ubscr!pt!0n&Key#',
            "JWT_ALGO": 'HS256',
            "JWT_FIVE_MINUTES": 0.00347222,
            "JWT_ADMIN_SESSION": .125
        }
        self.expire = datetime.utcnow() + timedelta(days=self.jwt[duration])
        self.refresh_expire = datetime.utcnow() + timedelta(days=self.jwt[duration] * 2)

    @staticmethod
    def generate_token(payload, logger):
        token = jwt.encode(payload, '$3cR3t#K3y', 'HS256')
        return token

    @staticmethod
    def decode_token(token, logger):
        payload = jwt.decode(token, '$3cR3t#K3y', 'HS256')
        logger.info(payload)
        return payload
