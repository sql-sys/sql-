"""
全局异常处理中间件
将所有异常信息记录到日志文件中
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback
from datetime import datetime

class GlobalExceptionHandler(BaseHTTPMiddleware):
    """全局异常处理中间件"""
    
    def __init__(self, app):
        super().__init__(app)
        self.error_logger = logging.getLogger('error')
        self.app_logger = logging.getLogger('app')
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            # HTTP异常记录到应用日志
            self.app_logger.warning(
                f"HTTP异常 - {request.method} {request.url} - "
                f"状态码: {e.status_code} - 详情: {e.detail}"
            )
            raise e
        except Exception as e:
            # 系统异常记录到错误日志
            error_id = datetime.now().strftime("%Y%m%d%H%M%S")
            self.error_logger.error(
                f"系统异常 [ID: {error_id}] - {request.method} {request.url} - "
                f"异常类型: {type(e).__name__} - 异常信息: {str(e)} - "
                f"堆栈跟踪: {traceback.format_exc()}"
            )
            
            # 返回通用错误响应
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "message": "服务器内部错误",
                    "error_id": error_id
                }
            )
