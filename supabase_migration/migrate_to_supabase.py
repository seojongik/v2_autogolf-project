#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL/MariaDB → Supabase 마이그레이션 스크립트
- 백업된 스키마를 PostgreSQL 형식으로 변환하여 Supabase에 테이블 생성
- 백업된 데이터를 Supabase에 삽입
- 기존 테이블이 있으면 삭제 후 새로 생성
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

# Supabase 설정
SUPABASE_CONFIG = {
    'project_id': 'yejialakeivdhwntmagf',
    'host': 'db.yejialakeivdhwntmagf.supabase.co',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres.yejialakeivdhwntmagf',
    'password': None  # Supabase 비밀번호는 별도로 설정 필요
}

# 백업 디렉토리 설정
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'cafe24_backup')
SCHEMA_DIR = os.path.join(BACKUP_DIR, 'schemas')
DATA_DIR = os.path.join(BACKUP_DIR, 'data')

# 백업에서 제외할 테이블 목록 (backup_database.py와 동일)
EXCLUDED_TABLES = {
    'Board',
    'CHN_batch',
    'CHN_message',
    'Comment',
    'Event_log',
    'FMS_LS',
    'FMS_TS',
    'Junior',
    'Junior_relation',
    'LS_availability',
    'LS_availability_register',
    'LS_confirm',
    'LS_contracts',
    'LS_countings',
    'LS_feedback',
    'LS_history',
    'LS_orders',
    'LS_search_fail',
    'LS_total_history',
    'Locker_bill',
    'Locker_status',
    'Price_table',
    'Priced_FMS',
    'Revisit_discount',
    'Staff',
    'Staff_payment',
    'TS_usage',
    'Term_hold',
    'Term_member',
    'bills',
    'contract_history',
    'contract_history_view',
    'contracts',
    'member_pro_match',
    'members',
    'schedule_adjusted',
    'schedule_weekly_base',
    'staff_pro_mapping',
    'v2_LS_contracts',
    'v2_LS_countings',
    'v2_contract_history',
}


def load_supabase_password():
    """Supabase 비밀번호 로드 (환경 변수 또는 설정 파일에서)"""
    # 환경 변수에서 먼저 확인
    password = os.getenv('SUPABASE_DB_PASSWORD')
    if password:
        return password
    
    # 설정 파일에서 확인
    keys_file = os.path.join(os.path.dirname(__file__), 'supabase_keys.json')
    if os.path.exists(keys_file):
        with open(keys_file, 'r', encoding='utf-8') as f:
            keys = json.load(f)
            # Supabase 비밀번호는 별도로 저장되어야 함
            # 여기서는 사용자에게 입력받도록 함
            return keys.get('db_password')
    
    return None


def mysql_type_to_postgresql(mysql_type: str) -> str:
    """MySQL/MariaDB 타입을 PostgreSQL 타입으로 변환"""
    mysql_type = mysql_type.lower().strip()
    
    # int 타입 변환
    if mysql_type.startswith('int(') or mysql_type == 'int':
        return 'INTEGER'
    elif mysql_type.startswith('bigint(') or mysql_type == 'bigint':
        return 'BIGINT'
    elif mysql_type.startswith('smallint(') or mysql_type == 'smallint':
        return 'SMALLINT'
    elif mysql_type.startswith('tinyint(') or mysql_type == 'tinyint':
        # MySQL의 tinyint(1)은 보통 BOOLEAN으로 사용
        if '1' in mysql_type:
            return 'BOOLEAN'
        return 'SMALLINT'
    
    # varchar, char 타입
    if mysql_type.startswith('varchar('):
        match = re.search(r'varchar\((\d+)\)', mysql_type)
        if match:
            size = match.group(1)
            return f'VARCHAR({size})'
        return 'VARCHAR'
    elif mysql_type.startswith('char('):
        match = re.search(r'char\((\d+)\)', mysql_type)
        if match:
            size = match.group(1)
            return f'CHAR({size})'
        return 'CHAR'
    elif mysql_type == 'text':
        return 'TEXT'
    elif mysql_type == 'longtext':
        return 'TEXT'
    elif mysql_type == 'mediumtext':
        return 'TEXT'
    
    # 숫자 타입
    elif mysql_type.startswith('decimal(') or mysql_type.startswith('numeric('):
        return mysql_type.replace('decimal', 'NUMERIC').replace('numeric', 'NUMERIC')
    elif mysql_type.startswith('float(') or mysql_type == 'float':
        return 'REAL'
    elif mysql_type.startswith('double(') or mysql_type == 'double':
        return 'DOUBLE PRECISION'
    
    # 날짜/시간 타입
    elif mysql_type == 'date':
        return 'DATE'
    elif mysql_type == 'time':
        return 'TIME'
    elif mysql_type == 'datetime':
        return 'TIMESTAMP'
    elif mysql_type == 'timestamp':
        return 'TIMESTAMP'
    elif mysql_type.startswith('year(') or mysql_type == 'year':
        return 'INTEGER'
    
    # 기타
    elif mysql_type == 'blob':
        return 'BYTEA'
    elif mysql_type == 'longblob':
        return 'BYTEA'
    elif mysql_type == 'json':
        return 'JSONB'
    
    # 기본값: 그대로 반환 (이미 PostgreSQL 타입일 수 있음)
    return mysql_type.upper()


def convert_default_value(default: Optional[str], pg_type: str) -> Optional[str]:
    """MySQL 기본값을 PostgreSQL 기본값으로 변환"""
    if default is None:
        return None
    
    default = str(default).strip()
    
    # NULL 처리
    if default.upper() == 'NULL':
        return None
    
    # CURRENT_TIMESTAMP 변환
    if default.upper() in ('CURRENT_TIMESTAMP', 'NOW()'):
        return 'CURRENT_TIMESTAMP'
    
    # 문자열 타입인 경우 따옴표 추가
    if pg_type.upper().startswith(('VARCHAR', 'CHAR', 'TEXT')):
        if not (default.startswith("'") and default.endswith("'")):
            # 이스케이프 처리
            default = default.replace("'", "''")
            return f"'{default}'"
    
    # 숫자나 불린은 그대로
    return default


def generate_postgresql_create_table(schema: Dict[str, Any]) -> str:
    """백업된 스키마를 기반으로 PostgreSQL CREATE TABLE 문 생성"""
    table_name = schema['table_name']
    columns = schema['columns']
    
    # 테이블 이름을 소문자로 변환 (PostgreSQL 권장)
    pg_table_name = table_name.lower()
    
    column_definitions = []
    primary_keys = []
    
    for col in columns:
        field_name = col['Field'].lower()
        mysql_type = col['Type']
        is_nullable = col['Null'] == 'YES'
        is_primary = col['Key'] == 'PRI'
        default_val = col['Default']
        extra = col.get('Extra', '')
        
        # PostgreSQL 타입 변환
        pg_type = mysql_type_to_postgresql(mysql_type)
        
        # 컬럼 정의 생성
        col_def = f'  {field_name} {pg_type}'
        
        # NULL/NOT NULL
        if not is_nullable:
            col_def += ' NOT NULL'
        
        # AUTO_INCREMENT → SERIAL 또는 DEFAULT nextval()
        if 'auto_increment' in extra.lower():
            if pg_type == 'INTEGER':
                col_def = col_def.replace('INTEGER', 'SERIAL')
            elif pg_type == 'BIGINT':
                col_def = col_def.replace('BIGINT', 'BIGSERIAL')
            # SERIAL은 기본값이 자동으로 설정되므로 DEFAULT는 추가하지 않음
        elif default_val is not None:
            pg_default = convert_default_value(default_val, pg_type)
            if pg_default:
                col_def += f' DEFAULT {pg_default}'
        
        column_definitions.append(col_def)
        
        # PRIMARY KEY 수집
        if is_primary:
            primary_keys.append(field_name)
    
    # CREATE TABLE 문 생성
    create_sql = f'CREATE TABLE IF NOT EXISTS {pg_table_name} (\n'
    create_sql += ',\n'.join(column_definitions)
    
    # PRIMARY KEY 제약 조건 추가
    if primary_keys:
        create_sql += f',\n  PRIMARY KEY ({", ".join(primary_keys)})\n'
    
    create_sql += ');'
    
    return create_sql, pg_table_name


def get_backup_tables() -> List[str]:
    """백업된 테이블 목록 가져오기"""
    if not os.path.exists(SCHEMA_DIR):
        return []
    
    tables = []
    for filename in os.listdir(SCHEMA_DIR):
        if filename.endswith('_schema.json'):
            table_name = filename.replace('_schema.json', '')
            if table_name not in EXCLUDED_TABLES:
                tables.append(table_name)
    
    return sorted(tables)


def load_table_schema(table_name: str) -> Optional[Dict[str, Any]]:
    """테이블 스키마 로드"""
    schema_file = os.path.join(SCHEMA_DIR, f"{table_name}_schema.json")
    if not os.path.exists(schema_file):
        return None
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_table_data(table_name: str) -> Optional[List[Dict[str, Any]]]:
    """테이블 데이터 로드"""
    data_file = os.path.join(DATA_DIR, f"{table_name}_data.json")
    if not os.path.exists(data_file):
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('data', [])


def drop_table_if_exists(cursor, table_name: str):
    """테이블이 존재하면 삭제"""
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table_name} CASCADE;')
        print(f"  ✓ 기존 테이블 삭제: {table_name}")
    except Exception as e:
        print(f"  ⚠ 테이블 삭제 중 오류 (무시): {str(e)}")


def create_table(cursor, create_sql: str, table_name: str):
    """테이블 생성"""
    try:
        cursor.execute(create_sql)
        print(f"  ✓ 테이블 생성 완료: {table_name}")
        return True
    except Exception as e:
        print(f"  ✗ 테이블 생성 실패: {str(e)}")
        print(f"    SQL: {create_sql[:200]}...")
        return False


def insert_table_data(cursor, table_name: str, data: List[Dict[str, Any]]):
    """테이블 데이터 삽입 (psycopg2의 execute_values 사용)"""
    if not data:
        print(f"  ⚠ 데이터 없음: {table_name}")
        return
    
    try:
        # 컬럼 이름 추출 (소문자로 변환)
        columns = [key.lower() for key in data[0].keys()]
        
        # 데이터 값 추출 및 변환
        values_list = []
        for row in data:
            values = []
            for col in columns:
                # 대소문자 구분 없이 값 가져오기
                value = row.get(col.upper()) or row.get(col) or row.get(col.lower())
                
                # None 처리
                if value is None:
                    values.append(None)
                # 불린 처리
                elif isinstance(value, bool):
                    values.append(value)
                # 숫자 처리
                elif isinstance(value, (int, float)):
                    values.append(value)
                # 문자열 처리 (날짜/시간 포함)
                elif isinstance(value, str):
                    # ISO 형식의 datetime 문자열도 그대로 사용
                    # PostgreSQL이 자동으로 파싱함
                    values.append(value)
                else:
                    values.append(str(value))
            
            values_list.append(tuple(values))
        
        # psycopg2의 execute_values 사용 (SQL 인젝션 방지 및 성능 향상)
        # 테이블 이름과 컬럼 이름은 식별자로 안전하게 처리
        table_ident = sql.Identifier(table_name)
        cols_ident = [sql.Identifier(col) for col in columns]
        cols_str = sql.SQL(', ').join(cols_ident)
        
        insert_sql = sql.SQL('INSERT INTO {} ({}) VALUES %s').format(
            table_ident,
            cols_str
        )
        
        # 배치로 나누어 삽입 (메모리 효율)
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(values_list), batch_size):
            batch = values_list[i:i + batch_size]
            execute_values(cursor, insert_sql, batch, page_size=batch_size)
            total_inserted += len(batch)
        
        print(f"  ✓ 데이터 삽입 완료: {table_name} ({total_inserted}개 행)")
        
    except Exception as e:
        print(f"  ✗ 데이터 삽입 실패: {str(e)}")
        import traceback
        traceback.print_exc()


def migrate_table(cursor, table_name: str):
    """단일 테이블 마이그레이션"""
    print(f"\n테이블 마이그레이션: {table_name}")
    print("-" * 60)
    
    # 스키마 로드
    schema = load_table_schema(table_name)
    if not schema:
        print(f"  ✗ 스키마 파일을 찾을 수 없습니다: {table_name}")
        return False
    
    # PostgreSQL CREATE TABLE 문 생성
    create_sql, pg_table_name = generate_postgresql_create_table(schema)
    
    # 기존 테이블 삭제
    drop_table_if_exists(cursor, pg_table_name)
    
    # 테이블 생성
    if not create_table(cursor, create_sql, pg_table_name):
        return False
    
    # 데이터 로드 및 삽입
    data = load_table_data(table_name)
    if data:
        insert_table_data(cursor, pg_table_name, data)
    else:
        print(f"  ⚠ 데이터 파일을 찾을 수 없습니다: {table_name}")
    
    return True


def main():
    """메인 함수"""
    print("=" * 60)
    print("MySQL/MariaDB → Supabase 마이그레이션 시작")
    print("=" * 60)
    
    # Supabase 비밀번호 확인
    password = load_supabase_password()
    if not password:
        print("\n⚠ Supabase 데이터베이스 비밀번호가 필요합니다.")
        print("다음 중 하나의 방법으로 설정하세요:")
        print("1. 환경 변수: export SUPABASE_DB_PASSWORD='your_password'")
        print("2. supabase_keys.json 파일에 'db_password' 키 추가")
        print("\nSupabase 프로젝트 설정에서 데이터베이스 비밀번호를 확인하세요.")
        password = input("\nSupabase 데이터베이스 비밀번호를 입력하세요: ").strip()
        if not password:
            print("✗ 비밀번호가 입력되지 않았습니다.")
            return
    
    SUPABASE_CONFIG['password'] = password
    
    # 백업된 테이블 목록 가져오기
    print(f"\n백업 파일 확인 중...")
    tables = get_backup_tables()
    
    if not tables:
        print("✗ 백업된 테이블을 찾을 수 없습니다.")
        print(f"백업 디렉토리 확인: {SCHEMA_DIR}")
        return
    
    print(f"✓ {len(tables)}개의 테이블 발견")
    
    # Supabase 연결
    try:
        print(f"\nSupabase 연결 중...")
        print(f"호스트: {SUPABASE_CONFIG['host']}")
        print(f"데이터베이스: {SUPABASE_CONFIG['database']}")
        
        conn = psycopg2.connect(
            host=SUPABASE_CONFIG['host'],
            port=SUPABASE_CONFIG['port'],
            database=SUPABASE_CONFIG['database'],
            user=SUPABASE_CONFIG['user'],
            password=SUPABASE_CONFIG['password'],
            sslmode='require'
        )
        conn.autocommit = False
        cursor = conn.cursor()
        print(f"✓ Supabase 연결 성공")
        
    except Exception as e:
        print(f"✗ Supabase 연결 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        # 각 테이블 마이그레이션
        print(f"\n테이블 마이그레이션 시작...")
        print("=" * 60)
        
        success_count = 0
        fail_count = 0
        
        for i, table_name in enumerate(tables, 1):
            print(f"\n[{i}/{len(tables)}] {table_name}")
            
            try:
                if migrate_table(cursor, table_name):
                    conn.commit()
                    success_count += 1
                else:
                    conn.rollback()
                    fail_count += 1
            except Exception as e:
                print(f"  ✗ 마이그레이션 중 오류: {str(e)}")
                conn.rollback()
                fail_count += 1
                import traceback
                traceback.print_exc()
                continue
        
        # 결과 요약
        print(f"\n" + "=" * 60)
        print("마이그레이션 완료!")
        print(f"성공: {success_count}개 테이블")
        print(f"실패: {fail_count}개 테이블")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 마이그레이션 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    
    finally:
        # 연결 종료
        cursor.close()
        conn.close()
        print("\nSupabase 연결 종료")


if __name__ == '__main__':
    main()

