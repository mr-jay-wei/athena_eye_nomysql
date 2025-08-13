# athena_eye_project/notifications/email_sender.py (最终优化版)
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from athena_eye_project.config import settings
from athena_eye_project.utils.logger import logger

class EmailSender:
    def send_email(self, subject: str, body: str) -> bool:
        """
        发送邮件通知 (使用STARTTLS方式，并健壮地处理连接关闭)

        Args:
            subject (str): 邮件主题
            body (str): 邮件正文 (支持HTML)

        Returns:
            bool: 如果发送成功返回True，否则返回False
        """
        if not all([settings.SENDER_EMAIL, settings.EMAIL_APP_PASSWORD, settings.RECIPIENT_EMAIL]):
            logger.error("邮件配置不完整，无法发送邮件。")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.SENDER_EMAIL
        message["To"] = settings.RECIPIENT_EMAIL
        message.attach(MIMEText(body, "html"))
        
        server = None
        try:
            context = ssl.create_default_context()
            logger.info(f"正在连接邮件服务器 {settings.SMTP_SERVER}:{settings.SMTP_PORT}...")
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
            server.starttls(context=context)
            logger.info("TLS加密已启动，正在登录...")
            server.login(settings.SENDER_EMAIL, settings.EMAIL_APP_PASSWORD)
            logger.info("登录成功，正在发送邮件...")
            server.sendmail(settings.SENDER_EMAIL, settings.RECIPIENT_EMAIL, message.as_string())
            
            # 只要sendmail不抛出异常，我们就认为发送成功
            logger.info(f"邮件已成功递交至SMTP服务器，目标邮箱: {settings.RECIPIENT_EMAIL}！")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("邮件发送失败：SMTP认证错误。请检查发件箱地址和邮箱授权码。")
            return False
        except Exception as e:
            logger.error(f"发送邮件时发生错误: {e}")
            return False
        finally:
            # 无论成功失败，都尝试关闭连接
            if server:
                try:
                    server.quit()
                    logger.info("SMTP服务器连接已成功关闭。")
                except Exception as e:
                    # 这个错误是可接受的，只记录警告即可
                    logger.warning(f"关闭SMTP连接时发生非关键性问题: {e}")

# 创建一个单例
email_client = EmailSender()