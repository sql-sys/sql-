"""
SQL语句验证工具
用于验证数据库模式创建和更新时的SQL语句
"""

import re
from typing import Tuple, List

class SQLValidator:
    """SQL语句验证器"""
    
    # 禁止的SQL关键词（修改、删除操作）
    FORBIDDEN_KEYWORDS = [
        'ALTER', 'DELETE', 'DROP', 'TRUNCATE', 'UPDATE', 'INSERT'
    ]
    
    # 允许的SQL关键词（建表相关）
    ALLOWED_KEYWORDS = [
        'CREATE', 'TABLE', 'INDEX', 'VIEW', 'SEQUENCE', 'FUNCTION', 
        'PROCEDURE', 'TRIGGER', 'CONSTRAINT', 'PRIMARY', 'FOREIGN',
        'KEY', 'REFERENCES', 'CHECK', 'UNIQUE', 'NOT', 'NULL',
        'DEFAULT', 'AUTO_INCREMENT', 'SERIAL', 'COMMENT'
    ]
    
    @classmethod
    def validate_create_table_sql(cls, sql_content: str) -> Tuple[bool, str]:
        """
        验证SQL内容是否只包含建表语句
        
        Args:
            sql_content: SQL语句内容
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        if not sql_content or not sql_content.strip():
            return False, "SQL内容不能为空"
        
        # 移除注释和多余空白
        cleaned_sql = cls._clean_sql(sql_content)
        
        # 检查是否包含禁止的关键词
        forbidden_found = cls._check_forbidden_keywords(cleaned_sql)
        if forbidden_found:
            return False, f"SQL语句包含禁止的操作关键词: {', '.join(forbidden_found)}。只允许使用建表语句（CREATE TABLE等）"
        
        # 检查是否包含CREATE TABLE语句
        if not cls._contains_create_table(cleaned_sql):
            return False, "SQL语句必须包含至少一个CREATE TABLE语句"
        
        return True, "SQL语句验证通过"
    
    @classmethod
    def _clean_sql(cls, sql_content: str) -> str:
        """清理SQL内容，移除注释和多余空白"""
        # 移除单行注释 (-- 注释)
        sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)
        
        # 移除多行注释 (/* 注释 */)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        # 移除多余的空白字符
        sql_content = re.sub(r'\s+', ' ', sql_content)
        
        return sql_content.strip().upper()
    
    @classmethod
    def _check_forbidden_keywords(cls, cleaned_sql: str) -> List[str]:
        """检查是否包含禁止的关键词"""
        found_keywords = []

        for keyword in cls.FORBIDDEN_KEYWORDS:
            # 使用单词边界确保精确匹配
            pattern = r'\b' + keyword + r'\b'
            matches = re.finditer(pattern, cleaned_sql)

            for match in matches:
                # 检查是否是允许的上下文
                if cls._is_allowed_context(cleaned_sql, match, keyword):
                    continue

                if keyword not in found_keywords:
                    found_keywords.append(keyword)

        return found_keywords

    @classmethod
    def _is_allowed_context(cls, sql: str, match, keyword: str) -> bool:
        """检查关键词是否在允许的上下文中"""
        start_pos = match.start()
        end_pos = match.end()

        # 获取关键词前后的上下文（前后各20个字符）
        context_start = max(0, start_pos - 20)
        context_end = min(len(sql), end_pos + 20)
        context = sql[context_start:context_end]

        # DELETE在外键约束中是允许的
        if keyword == 'DELETE':
            if 'ON DELETE' in context or 'ON UPDATE' in context:
                return True

        # UPDATE在外键约束中是允许的
        if keyword == 'UPDATE':
            if 'ON UPDATE' in context or 'ON DELETE' in context:
                return True

        return False
    
    @classmethod
    def _contains_create_table(cls, cleaned_sql: str) -> bool:
        """检查是否包含CREATE TABLE语句"""
        pattern = r'\bCREATE\s+TABLE\b'
        return bool(re.search(pattern, cleaned_sql))
    
    @classmethod
    def extract_table_names(cls, sql_content: str) -> List[str]:
        """提取SQL中的表名"""
        cleaned_sql = cls._clean_sql(sql_content)
        
        # 匹配 CREATE TABLE table_name 模式
        pattern = r'\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s\(]+)'
        matches = re.findall(pattern, cleaned_sql)
        
        # 清理表名（移除引号等）
        table_names = []
        for match in matches:
            table_name = match.strip('`"\'[]')
            if table_name:
                table_names.append(table_name)
        
        return table_names
    
    @classmethod
    def get_validation_message(cls) -> str:
        """获取验证规则说明"""
        return (
            "SQL语句验证规则：\n"
            "✅ 允许：CREATE TABLE、CREATE INDEX、CREATE VIEW等建表相关语句\n"
            "❌ 禁止：ALTER、DELETE、DROP、TRUNCATE、UPDATE、INSERT等修改删除语句\n"
            "📝 提示：请只使用建表语句来定义数据库结构"
        )
