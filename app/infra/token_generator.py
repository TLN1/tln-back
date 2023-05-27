class TokenGenerator:
    _i = 0

    @classmethod
    def generate_token(cls) -> str:
        cls._i += 1
        return f"token_{cls._i}"
