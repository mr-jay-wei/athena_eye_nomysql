# athena_eye_project/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger

try:
    # 1. 创建数据库引擎 (Engine)
    # 根据数据库类型使用不同的连接参数
    if settings.DATABASE_URL.startswith("sqlite"):
        # SQLite 配置
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False}  # SQLite 特有参数
        )
    else:
        # MySQL 配置
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10}
        )

    # 2. 创建一个 SessionLocal 类
    # 这个类本身不是一个数据库会话，而是一个会话的“工厂”。
    # 当我们实例化 SessionLocal() 时，才会创建一个新的会话。
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 3. 创建一个 Base 类
    # 这是所有ORM模型的基类。我们之后创建的所有数据表模型，
    # 都需要继承自这个Base类，SQLAlchemy才能发现并管理它们。
    Base = declarative_base()

    logger.info("数据库连接引擎和会话工厂已成功初始化。")

except Exception as e:
    logger.critical(f"数据库初始化失败，无法创建引擎: {e}. 请检查.env中的数据库配置和网络连接。")
    # 这是一个致命错误，直接抛出异常以阻止应用启动。
    raise

def get_db():
    """
    FastAPI 依赖注入函数 (Dependency Injection)。

    它的作用是为每个API请求，都生成一个独立的数据库会话，
    并在请求处理完成后，无论成功或失败，都确保会话被关闭。
    这是一种非常健壮和高效的会话管理模式。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    初始化数据库函数。

    它会连接到数据库，并根据所有继承自 Base 的模型，
    创建出所有对应的表。
    关键点：它不会重复创建已经存在的表，所以可以安全地在每次应用启动时调用。
    """
    try:
        logger.info("正在检查并同步数据库表结构...")
        # Base.metadata.create_all() 是SQLAlchemy的魔法所在，
        # 它会遍历所有子类模型，并生成 'CREATE TABLE IF NOT EXISTS ...' 类似的语句。
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表结构同步完成。")
    except Exception as e:
        logger.error(f"创建数据库表时发生严重错误: {e}")
        # 表创建失败也是一个致命错误。
        raise