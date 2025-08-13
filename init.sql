-- 使用MySQL 8.0的默认caching_sha2_password认证插件
CREATE USER 'athena_user'@'%' IDENTIFIED BY '052756';

GRANT ALL PRIVILEGES ON athena_eye_db.* TO 'athena_user'@'%';

FLUSH PRIVILEGES;