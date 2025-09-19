MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware ...
    'chats.middleware.OffensiveLanguageMiddleware',
]
