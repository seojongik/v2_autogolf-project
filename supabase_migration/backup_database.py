#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL 데이터베이스 백업 스크립트
- 모든 테이블 구조를 JSON 파일로 저장
- 모든 테이블 데이터를 백업 파일로 저장
"""

import pymysql
import json
import os
from datetime import datetime
from typing import Dict, List, Any

# 데이터베이스 연결 정보
DB_CONFIG = {
    'host': '222.122.198.185',
    'port': 3306,
    'user': 'autofms',
    'password': 'a131150*',
    'db': 'autofms',
    'charset': 'utf8mb4'
}

# 백업 디렉토리 설정
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'cafe24_backup')
SCHEMA_DIR = os.path.join(BACKUP_DIR, 'schemas')
DATA_DIR = os.path.join(BACKUP_DIR, 'data')

# 백업에서 제외할 테이블 목록
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


def ensure_directories():
    """백업 디렉토리 생성"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(SCHEMA_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"백업 디렉토리 준비 완료: {BACKUP_DIR}")


def get_table_list(cursor) -> List[str]:
    """데이터베이스의 모든 테이블 목록 가져오기 (제외 테이블 필터링)"""
    cursor.execute("SHOW TABLES")
    all_tables = [table[0] for table in cursor.fetchall()]
    
    # 제외할 테이블 필터링
    tables = [table for table in all_tables if table not in EXCLUDED_TABLES]
    
    excluded_count = len(all_tables) - len(tables)
    if excluded_count > 0:
        excluded_list = [table for table in all_tables if table in EXCLUDED_TABLES]
        print(f"총 {len(all_tables)}개의 테이블 발견")
        print(f"제외된 테이블 ({excluded_count}개): {', '.join(excluded_list)}")
        print(f"백업 대상 테이블 ({len(tables)}개): {', '.join(tables)}")
    else:
        print(f"총 {len(tables)}개의 테이블 발견: {', '.join(tables)}")
    
    return tables


def get_table_structure(cursor, table_name: str) -> Dict[str, Any]:
    """테이블 구조 정보 가져오기"""
    # 컬럼 정보 가져오기
    cursor.execute(f"DESCRIBE `{table_name}`")
    columns = cursor.fetchall()
    
    # 컬럼 정보를 딕셔너리 리스트로 변환
    column_info = []
    for col in columns:
        column_info.append({
            'Field': col[0],
            'Type': col[1],
            'Null': col[2],
            'Key': col[3],
            'Default': str(col[4]) if col[4] is not None else None,
            'Extra': col[5]
        })
    
    # CREATE TABLE 문 가져오기
    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
    create_table_result = cursor.fetchone()
    create_statement = create_table_result[1] if create_table_result else None
    
    # 인덱스 정보 가져오기
    cursor.execute(f"SHOW INDEX FROM `{table_name}`")
    indexes = cursor.fetchall()
    
    index_info = []
    for idx in indexes:
        index_info.append({
            'Table': idx[0],
            'Non_unique': idx[1],
            'Key_name': idx[2],
            'Seq_in_index': idx[3],
            'Column_name': idx[4],
            'Collation': idx[5],
            'Cardinality': idx[6],
            'Sub_part': idx[7],
            'Packed': idx[8],
            'Null': idx[9],
            'Index_type': idx[10],
            'Comment': idx[11] if len(idx) > 11 else None
        })
    
    return {
        'table_name': table_name,
        'columns': column_info,
        'create_statement': create_statement,
        'indexes': index_info,
        'backup_timestamp': datetime.now().isoformat()
    }


def save_table_structure(table_name: str, structure: Dict[str, Any]):
    """테이블 구조를 JSON 파일로 저장"""
    filename = os.path.join(SCHEMA_DIR, f"{table_name}_schema.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 구조 저장: {filename}")


def backup_table_data(cursor, table_name: str):
    """테이블 데이터 백업"""
    try:
        # 데이터 가져오기
        cursor.execute(f"SELECT * FROM `{table_name}`")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        # 데이터를 딕셔너리 리스트로 변환
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # datetime, date 등의 객체를 문자열로 변환
                if isinstance(value, (datetime,)):
                    value = value.isoformat()
                elif hasattr(value, 'isoformat'):
                    value = value.isoformat()
                row_dict[col] = value
            data.append(row_dict)
        
        # JSON 파일로 저장
        json_filename = os.path.join(DATA_DIR, f"{table_name}_data.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'table_name': table_name,
                'row_count': len(data),
                'backup_timestamp': datetime.now().isoformat(),
                'data': data
            }, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"  ✓ 데이터 저장 (JSON): {json_filename} ({len(data)}개 행)")
        
        # SQL INSERT 문으로도 백업 (선택사항)
        if len(data) > 0:
            sql_filename = os.path.join(DATA_DIR, f"{table_name}_data.sql")
            with open(sql_filename, 'w', encoding='utf-8') as f:
                f.write(f"-- Table: {table_name}\n")
                f.write(f"-- Backup Date: {datetime.now().isoformat()}\n")
                f.write(f"-- Row Count: {len(data)}\n\n")
                f.write(f"SET FOREIGN_KEY_CHECKS=0;\n\n")
                f.write(f"TRUNCATE TABLE `{table_name}`;\n\n")
                
                # INSERT 문 생성
                for row in data:
                    cols = ', '.join([f"`{col}`" for col in columns])
                    values = []
                    for col in columns:
                        val = row[col]
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bool):
                            values.append('1' if val else '0')
                        else:
                            # 문자열 이스케이프 처리
                            val_str = str(val).replace('\\', '\\\\').replace("'", "\\'")
                            values.append(f"'{val_str}'")
                    
                    values_str = ', '.join(values)
                    f.write(f"INSERT INTO `{table_name}` ({cols}) VALUES ({values_str});\n")
                
                f.write(f"\nSET FOREIGN_KEY_CHECKS=1;\n")
            
            print(f"  ✓ 데이터 저장 (SQL): {sql_filename}")
        
    except Exception as e:
        print(f"  ✗ 데이터 백업 실패: {str(e)}")


def create_summary_file(tables: List[str], backup_timestamp: str):
    """백업 요약 파일 생성"""
    summary = {
        'database': DB_CONFIG['db'],
        'host': DB_CONFIG['host'],
        'backup_timestamp': backup_timestamp,
        'total_tables': len(tables),
        'tables': tables,
        'backup_locations': {
            'schemas': SCHEMA_DIR,
            'data_json': DATA_DIR,
            'data_sql': DATA_DIR
        }
    }
    
    summary_filename = os.path.join(BACKUP_DIR, 'backup_summary.json')
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n백업 요약 파일 생성: {summary_filename}")


def main():
    """메인 함수"""
    print("=" * 60)
    print("MySQL 데이터베이스 백업 시작")
    print("=" * 60)
    
    backup_timestamp = datetime.now().isoformat()
    
    # 디렉토리 준비
    ensure_directories()
    
    # 데이터베이스 연결
    try:
        print(f"\n데이터베이스 연결 중...")
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()
        print(f"✓ 데이터베이스 연결 성공: {DB_CONFIG['db']}")
    except Exception as e:
        print(f"✗ 데이터베이스 연결 실패: {str(e)}")
        return
    
    try:
        # 테이블 목록 가져오기
        print(f"\n테이블 목록 조회 중...")
        tables = get_table_list(cursor)
        
        if not tables:
            print("백업할 테이블이 없습니다.")
            return
        
        # 각 테이블 백업
        print(f"\n테이블 백업 시작...")
        print("-" * 60)
        
        for i, table_name in enumerate(tables, 1):
            print(f"\n[{i}/{len(tables)}] 테이블: {table_name}")
            
            try:
                # 테이블 구조 백업
                structure = get_table_structure(cursor, table_name)
                save_table_structure(table_name, structure)
                
                # 테이블 데이터 백업
                backup_table_data(cursor, table_name)
                
            except Exception as e:
                print(f"  ✗ 테이블 백업 중 오류 발생: {str(e)}")
                continue
        
        # 백업 요약 파일 생성
        print(f"\n" + "-" * 60)
        create_summary_file(tables, backup_timestamp)
        
        print(f"\n" + "=" * 60)
        print("백업 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 백업 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 연결 종료
        cursor.close()
        db.close()
        print("\n데이터베이스 연결 종료")


if __name__ == '__main__':
    import sys
    
    # 통합 마이그레이션 스크립트가 있으면 그것을 사용하도록 안내
    full_migration_path = os.path.join(os.path.dirname(__file__), 'full_migration.py')
    if os.path.exists(full_migration_path):
        print("=" * 60)
        print("통합 마이그레이션 스크립트를 사용하는 것을 권장합니다.")
        print("백업 + Supabase 마이그레이션을 한 번에 수행하려면:")
        print(f"  python3 {full_migration_path}")
        print("=" * 60)
        print()
        
        response = input("통합 스크립트를 실행하시겠습니까? (y/n, 기본값: n): ").strip().lower()
        if response == 'y':
            import subprocess
            subprocess.run([sys.executable, full_migration_path])
            sys.exit(0)
    
    # 기존 백업만 수행
    main()

