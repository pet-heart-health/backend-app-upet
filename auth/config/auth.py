from config.routes import prefix

# Auth service configuration
endpoint = "/auth"
tag = "Auth"
token_endpoint = endpoint + "/sign-in"
token_url = prefix + endpoint + "/sign-in"

# JWT configuration
SECRET_KEY = '197b2c371eas312ze#@1ssdsasd1123'
ALGORITHM = 'HS256'
