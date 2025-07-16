"""
日志配置模块
控制台只输出在线人数和时间，其他信息记录到日志文件
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# 创建日志目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

class ConsoleOnlineStatusHandler(logging.Handler):
    """自定义控制台处理器，只显示在线状态信息"""
    
    def __init__(self):
        super().__init__()
        self.last_online_count = 0
        self.last_update_time = None
    
    def emit(self, record):
        """只处理在线状态相关的日志"""
        if hasattr(record, 'online_count') and hasattr(record, 'total_visits'):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 只有在线人数变化或每分钟更新一次时才输出
            if (record.online_count != self.last_online_count or 
                self.last_update_time is None or 
                (datetime.now() - self.last_update_time).seconds >= 60):
                
                print(f"\r[{current_time}] 在线人数: {record.online_count} | 累计访问: {record.total_visits}", end="", flush=True)
                self.last_online_count = record.online_count
                self.last_update_time = datetime.now()

def setup_logging():
    """设置日志配置"""
    
    # 创建根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 1. 控制台处理器 - 只显示在线状态
    console_handler = ConsoleOnlineStatusHandler()
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # 2. 访问日志文件处理器
    access_log_file = LOG_DIR / f"access_{datetime.now().strftime('%Y%m%d')}.log"
    access_handler = logging.handlers.RotatingFileHandler(
        access_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=30,
        encoding='utf-8'
    )
    access_handler.setLevel(logging.INFO)
    access_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    access_handler.setFormatter(access_formatter)
    
    # 3. 错误日志文件处理器
    error_log_file = LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=30,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    error_handler.setFormatter(error_formatter)
    
    # 4. 应用日志文件处理器
    app_log_file = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    app_handler = logging.handlers.RotatingFileHandler(
        app_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=30,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app_handler.setFormatter(app_formatter)
    
    # 创建专门的日志器
    access_logger = logging.getLogger('access')
    access_logger.handlers.clear()  # 清除现有处理器
    access_logger.addHandler(access_handler)
    access_logger.propagate = False

    error_logger = logging.getLogger('error')
    error_logger.handlers.clear()  # 清除现有处理器
    error_logger.addHandler(error_handler)
    error_logger.propagate = False

    app_logger = logging.getLogger('app')
    app_logger.handlers.clear()  # 清除现有处理器
    app_logger.addHandler(app_handler)
    app_logger.propagate = False
    
    # 配置uvicorn日志
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = [access_handler]
    uvicorn_access_logger.propagate = False
    
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers = [error_handler]
    uvicorn_error_logger.propagate = False
    
    # 配置FastAPI日志
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.handlers = [app_handler]
    fastapi_logger.propagate = False
    
    return {
        'access': access_logger,
        'error': error_logger,
        'app': app_logger,
        'console': root_logger
    }

def get_logger(name: str = 'app'):
    """获取指定名称的日志器"""
    return logging.getLogger(name)

def log_online_status(online_count: int, total_visits: int):
    """记录在线状态到控制台"""
    logger = logging.getLogger()
    record = logging.LogRecord(
        name='monitor',
        level=logging.INFO,
        pathname='',
        lineno=0,
        msg='',
        args=(),
        exc_info=None
    )
    record.online_count = online_count
    record.total_visits = total_visits
    logger.handle(record)

# 初始化日志配置
loggers = setup_logging()
