import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# --- 测试环境设置 ---
TEST_DATABASE_FILE = "test_athena_eye.db"
TEST_DATABASE_URL = f"sqlite:///./{TEST_DATABASE_FILE}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from athena_eye_project.config import settings
settings.DATABASE_URL = TEST_DATABASE_URL

from athena_eye_project.db.database import Base, get_db
from athena_eye_project.main_api import app
from athena_eye_project.db.models import Alert
from athena_eye_project.archiving.archiver import decision_archiver, ALERT_HISTORY_LIMIT

# --- Pytest Fixture ---
@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    为每个测试函数创建一个独立的、干净的文件数据库。
    并在测试结束后自动清理。
    """
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)
        
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 【核心修正】在删除文件前，彻底关闭引擎的所有连接
        engine.dispose()
        if os.path.exists(TEST_DATABASE_FILE):
            os.remove(TEST_DATABASE_FILE)

# --- FastAPI 测试客户端设置 ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- 测试用例 ---

def test_archive_and_cleanup_logic(db_session: Session):
    """
    核心测试：验证存档和自动清理功能。
    """
    print(f"开始测试存档与清理逻辑，记录上限为 {ALERT_HISTORY_LIMIT}...")
    total_to_create = ALERT_HISTORY_LIMIT + 10
    mock_alert_details = {
        "ticker": "TEST", "alert_type": "Test Alert", "reason": "Testing cleanup",
        "price_details": {}, "volume_details": {}, "sentiment_details": {}
    }

    for i in range(total_to_create):
        current_alert_details = mock_alert_details.copy()
        current_alert_details['reason'] = f"Testing cleanup {i+1}"
        decision_archiver.archive_decision_to_db(db_session, current_alert_details, [])

    final_count = db_session.query(Alert).count()
    print(f"存档 {total_to_create} 条记录后，数据库中剩余 {final_count} 条。")
    assert final_count == ALERT_HISTORY_LIMIT

    oldest_remaining_alert = db_session.query(Alert).order_by(Alert.id.asc()).first()
    assert oldest_remaining_alert is not None
    assert "11" in oldest_remaining_alert.reason
    print("验证通过：最旧的10条记录已被正确删除。")


def test_archive_api_endpoints(db_session: Session):
    """
    API集成测试：验证/api/archive端点能否在共享数据库上正常工作。
    """
    print("开始测试API端点...")
    
    alert1 = Alert(ticker="API_T1", alert_type="Type A", reason="Reason A")
    alert2 = Alert(ticker="API_T2", alert_type="Type B", reason="Reason B")
    db_session.add_all([alert1, alert2])
    db_session.commit()
    
    response = client.get("/api/archive")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['ticker'] == "API_T2"
    print("验证通过：/api/archive 端点工作正常。")