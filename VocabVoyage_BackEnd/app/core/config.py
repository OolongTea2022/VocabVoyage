from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"  # 指定环境变量文件
    env_file_encoding = "utf-8"

    # MySQL 配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DB: str = "vocab_voyage"

    @property
    def database_url(self) -> str:
        """
        动态生成数据库连接字符串
        """
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    # JWT 和 Cookie 配置
    COOKIE_SECRET = "memorize_the_word_tips"  # 安全密钥
    COOKIE_NAME = "session_id"
    COOKIE_EXPIRE_MINUTES = 30  # Cookie 有效期（分钟）

    # OSS 配置
    ENDPOINT: str
    ACCESS_KEY_ID: str
    ACCESS_KEY_SECRET: str
    BUCKET_NAME: str

    # OpenAI API 密钥
    OPENAI_API_KEY: str


# 实例化 settings
settings = Settings()

