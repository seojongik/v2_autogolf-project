#!/usr/bin/env python3
"""
Supabase Query Tool - MCP 대용 만능 DB 조회 도구
개발 시 필요한 모든 DB 정보를 조회할 수 있습니다.

=== 기본 사용법 ===

    # 테이블 목록 (행 수 포함)
    python supabase_query.py --list-tables

    # 테이블 스키마 (컬럼, 타입, 제약조건)
    python supabase_query.py --schema v2_staff_manager

    # 데이터 조회
    python supabase_query.py -t v2_staff_manager -l 5

=== 고급 스키마 정보 ===

    # 기본키, 외래키, 인덱스 전체 보기
    python supabase_query.py --full-schema v2_staff_manager

    # 외래키 관계만 보기
    python supabase_query.py --fk v2_staff_manager

    # 인덱스 보기
    python supabase_query.py --indexes v2_staff_manager

    # 제약조건 보기
    python supabase_query.py --constraints v2_staff_manager

    # 테이블 간 관계도 (ERD 텍스트)
    python supabase_query.py --relations v2_staff_manager

    # 모든 테이블 관계 요약
    python supabase_query.py --all-relations

=== 데이터 분석 ===

    # 컬럼별 데이터 샘플 및 통계
    python supabase_query.py --analyze v2_staff_manager

    # 특정 컬럼의 고유값 목록
    python supabase_query.py --distinct v2_staff_manager.staff_status

    # 컬럼별 NULL 비율
    python supabase_query.py --null-check v2_staff_manager

=== 데이터 조회 ===

    # 기본 조회
    python supabase_query.py -t v2_staff_manager

    # 조건 검색
    python supabase_query.py -t v2_staff_manager -w "branch_id=test"

    # 복합 조건
    python supabase_query.py -t v2_staff_manager -w "branch_id=test" -w "staff_status=재직"

    # LIKE 검색
    python supabase_query.py -t v2_staff_manager --like "manager_name=%혜%"

    # 정렬
    python supabase_query.py -t v2_staff_manager -o "updated_at DESC" -l 5

    # 특정 필드만
    python supabase_query.py -t v2_staff_manager -f manager_id,manager_name

    # JSON 출력
    python supabase_query.py -t v2_staff_manager -l 3 --json

=== SQL 직접 실행 ===

    python supabase_query.py --sql "SELECT COUNT(*) FROM v2_staff_manager"

=== CUD 작업 ===

    # INSERT
    python supabase_query.py -t v2_test --insert '{"name": "test"}'

    # UPDATE (where 필수)
    python supabase_query.py -t v2_test --update '{"value": 456}' -w "name=test"

    # DELETE (where 필수)
    python supabase_query.py -t v2_test --delete -w "name=test"
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("psycopg2 패키지가 필요합니다. 설치: pip install psycopg2-binary")
    sys.exit(1)

# 키 파일 경로
KEYS_FILE = Path(__file__).parent / "supabase_keys.json"


def load_keys():
    """Supabase 키 파일 로드"""
    if not KEYS_FILE.exists():
        print(f"❌ 키 파일을 찾을 수 없습니다: {KEYS_FILE}")
        sys.exit(1)

    with open(KEYS_FILE, 'r') as f:
        return json.load(f)


def get_connection():
    """Supabase PostgreSQL 연결"""
    keys = load_keys()
    conn_string = keys.get('connection_string')

    try:
        conn = psycopg2.connect(conn_string)
        return conn
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
        sys.exit(1)


def json_serial(obj):
    """JSON 직렬화 헬퍼"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


# ============================================
# 테이블 목록 및 기본 정보
# ============================================

def list_tables(conn, verbose=False):
    """모든 테이블 목록 및 행 수 조회"""
    query = """
        SELECT
            t.table_name,
            pg_stat_user_tables.n_live_tup as row_count,
            pg_size_pretty(pg_total_relation_size(quote_ident(t.table_name))) as size
        FROM information_schema.tables t
        LEFT JOIN pg_stat_user_tables ON t.table_name = pg_stat_user_tables.relname
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name
    """
    with conn.cursor() as cur:
        cur.execute(query)
        tables = cur.fetchall()

    print(f"\n📋 테이블 목록 ({len(tables)}개)")
    print("-" * 60)
    print(f"{'테이블명':<40} {'행 수':>10} {'크기':>10}")
    print("-" * 60)

    for table_name, row_count, size in tables:
        row_str = str(row_count) if row_count else '?'
        size_str = size if size else '?'
        print(f"{table_name:<40} {row_str:>10} {size_str:>10}")
    print()


def list_views(conn):
    """뷰 목록 조회"""
    query = """
        SELECT table_name, view_definition
        FROM information_schema.views
        WHERE table_schema = 'public'
        ORDER BY table_name
    """
    with conn.cursor() as cur:
        cur.execute(query)
        views = cur.fetchall()

    if not views:
        print("\n📋 뷰 없음")
        return

    print(f"\n📋 뷰 목록 ({len(views)}개)")
    print("-" * 60)
    for name, definition in views:
        print(f"\n• {name}")
        if definition:
            # 첫 100자만 표시
            short_def = definition[:200] + "..." if len(definition) > 200 else definition
            print(f"  {short_def}")


# ============================================
# 스키마 정보
# ============================================

def get_schema(conn, table_name):
    """테이블 기본 스키마 조회"""
    query = """
        SELECT
            c.column_name,
            c.data_type,
            c.character_maximum_length,
            c.numeric_precision,
            c.is_nullable,
            c.column_default,
            col_description(
                (SELECT oid FROM pg_class WHERE relname = c.table_name),
                c.ordinal_position
            ) as column_comment
        FROM information_schema.columns c
        WHERE c.table_schema = 'public' AND c.table_name = %s
        ORDER BY c.ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        columns = cur.fetchall()

    if not columns:
        print(f"❌ 테이블 '{table_name}'을 찾을 수 없습니다.")
        return None

    print(f"\n📊 테이블 스키마: {table_name}")
    print("=" * 90)
    print(f"{'Column':<30} {'Type':<20} {'Null':<6} {'Default':<20} {'Comment'}")
    print("-" * 90)

    for col in columns:
        name, dtype, char_len, num_prec, nullable, default, comment = col

        # 타입 포맷팅
        type_str = dtype
        if char_len:
            type_str = f"{dtype}({char_len})"
        elif num_prec:
            type_str = f"{dtype}({num_prec})"

        null_str = "YES" if nullable == 'YES' else "NO"
        default_str = str(default)[:18] + '..' if default and len(str(default)) > 20 else (default or '')
        comment_str = comment or ''

        print(f"{name:<30} {type_str:<20} {null_str:<6} {default_str:<20} {comment_str}")

    print()
    return columns


def get_primary_key(conn, table_name):
    """기본키 조회"""
    query = """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_schema = 'public'
            AND tc.table_name = %s
            AND tc.constraint_type = 'PRIMARY KEY'
        ORDER BY kcu.ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        pks = [row[0] for row in cur.fetchall()]
    return pks


def get_foreign_keys(conn, table_name):
    """외래키 조회"""
    query = """
        SELECT
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column,
            tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.table_schema = 'public'
            AND tc.table_name = %s
            AND tc.constraint_type = 'FOREIGN KEY'
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        fks = cur.fetchall()
    return fks


def get_indexes(conn, table_name):
    """인덱스 조회"""
    query = """
        SELECT
            i.relname as index_name,
            a.attname as column_name,
            ix.indisunique as is_unique,
            ix.indisprimary as is_primary
        FROM pg_class t
        JOIN pg_index ix ON t.oid = ix.indrelid
        JOIN pg_class i ON i.oid = ix.indexrelid
        JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
        WHERE t.relname = %s AND t.relkind = 'r'
        ORDER BY i.relname, a.attnum
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        indexes = cur.fetchall()
    return indexes


def get_constraints(conn, table_name):
    """제약조건 조회"""
    query = """
        SELECT
            tc.constraint_name,
            tc.constraint_type,
            kcu.column_name,
            cc.check_clause
        FROM information_schema.table_constraints tc
        LEFT JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        LEFT JOIN information_schema.check_constraints cc
            ON tc.constraint_name = cc.constraint_name
        WHERE tc.table_schema = 'public' AND tc.table_name = %s
        ORDER BY tc.constraint_type, tc.constraint_name
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        constraints = cur.fetchall()
    return constraints


def show_full_schema(conn, table_name):
    """전체 스키마 정보 (컬럼 + PK + FK + 인덱스 + 제약조건)"""
    # 기본 스키마
    get_schema(conn, table_name)

    # 기본키
    pks = get_primary_key(conn, table_name)
    if pks:
        print(f"🔑 기본키: {', '.join(pks)}")

    # 외래키
    fks = get_foreign_keys(conn, table_name)
    if fks:
        print(f"\n🔗 외래키:")
        for col, ftable, fcol, cname in fks:
            print(f"   {col} → {ftable}.{fcol}")

    # 인덱스
    indexes = get_indexes(conn, table_name)
    if indexes:
        print(f"\n📇 인덱스:")
        current_idx = None
        for idx_name, col_name, is_unique, is_primary in indexes:
            if is_primary:
                continue  # PK는 이미 표시함
            if idx_name != current_idx:
                unique_str = " (UNIQUE)" if is_unique else ""
                print(f"   • {idx_name}{unique_str}: ", end="")
                current_idx = idx_name
            print(f"{col_name} ", end="")
        print()

    # 제약조건
    constraints = get_constraints(conn, table_name)
    check_constraints = [c for c in constraints if c[1] == 'CHECK']
    unique_constraints = [c for c in constraints if c[1] == 'UNIQUE']

    if unique_constraints:
        print(f"\n✓ UNIQUE 제약:")
        for cname, ctype, col, clause in unique_constraints:
            print(f"   • {col}")

    if check_constraints:
        print(f"\n✓ CHECK 제약:")
        for cname, ctype, col, clause in check_constraints:
            if clause:
                print(f"   • {clause[:60]}...")

    print()


def show_fk_relations(conn, table_name):
    """외래키 관계 표시"""
    # 이 테이블이 참조하는 테이블
    fks = get_foreign_keys(conn, table_name)

    # 이 테이블을 참조하는 테이블
    query = """
        SELECT
            tc.table_name as referencing_table,
            kcu.column_name as referencing_column,
            ccu.column_name as referenced_column
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND ccu.table_name = %s
    """
    with conn.cursor() as cur:
        cur.execute(query, (table_name,))
        refs = cur.fetchall()

    print(f"\n🔗 테이블 관계: {table_name}")
    print("=" * 60)

    if fks:
        print(f"\n→ {table_name}이(가) 참조하는 테이블:")
        for col, ftable, fcol, cname in fks:
            print(f"   {table_name}.{col} → {ftable}.{fcol}")

    if refs:
        print(f"\n← {table_name}을(를) 참조하는 테이블:")
        for reftable, refcol, mycol in refs:
            print(f"   {reftable}.{refcol} → {table_name}.{mycol}")

    if not fks and not refs:
        print("   (관계 없음)")
    print()


def show_all_relations(conn):
    """모든 테이블 간 관계"""
    query = """
        SELECT
            tc.table_name as from_table,
            kcu.column_name as from_column,
            ccu.table_name as to_table,
            ccu.column_name as to_column
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public'
        ORDER BY tc.table_name, ccu.table_name
    """
    with conn.cursor() as cur:
        cur.execute(query)
        relations = cur.fetchall()

    print(f"\n🔗 전체 테이블 관계도 ({len(relations)}개)")
    print("=" * 70)

    if not relations:
        print("   (외래키 관계 없음)")
    else:
        for from_t, from_c, to_t, to_c in relations:
            print(f"   {from_t}.{from_c:<30} → {to_t}.{to_c}")
    print()


# ============================================
# 데이터 분석
# ============================================

def analyze_table(conn, table_name):
    """테이블 데이터 분석 (컬럼별 통계)"""
    # 먼저 컬럼 목록 가져오기
    col_query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(col_query, (table_name,))
        columns = cur.fetchall()

    if not columns:
        print(f"❌ 테이블 '{table_name}'을 찾을 수 없습니다.")
        return

    # 행 수
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = cur.fetchone()[0]

    print(f"\n📊 테이블 분석: {table_name}")
    print(f"   총 행 수: {total_rows:,}")
    print("=" * 80)

    for col_name, col_type in columns:
        print(f"\n▸ {col_name} ({col_type})")

        with conn.cursor() as cur:
            # NULL 개수
            cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} IS NULL")
            null_count = cur.fetchone()[0]
            null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0

            # DISTINCT 개수
            cur.execute(f"SELECT COUNT(DISTINCT {col_name}) FROM {table_name}")
            distinct_count = cur.fetchone()[0]

            print(f"   NULL: {null_count:,} ({null_pct:.1f}%) | DISTINCT: {distinct_count:,}")

            # 숫자형이면 min/max/avg
            if col_type in ('integer', 'bigint', 'numeric', 'real', 'double precision'):
                cur.execute(f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}) FROM {table_name}")
                min_val, max_val, avg_val = cur.fetchone()
                if min_val is not None:
                    print(f"   MIN: {min_val} | MAX: {max_val} | AVG: {avg_val:.2f if avg_val else 0}")

            # 문자형이면 샘플 값들
            elif col_type in ('character varying', 'text', 'character'):
                cur.execute(f"""
                    SELECT {col_name}, COUNT(*) as cnt
                    FROM {table_name}
                    WHERE {col_name} IS NOT NULL
                    GROUP BY {col_name}
                    ORDER BY cnt DESC
                    LIMIT 5
                """)
                samples = cur.fetchall()
                if samples:
                    print(f"   TOP 값: ", end="")
                    sample_strs = [f"'{v}'({c})" for v, c in samples]
                    print(", ".join(sample_strs))
    print()


def show_distinct_values(conn, table_column):
    """특정 컬럼의 고유값 목록"""
    if '.' not in table_column:
        print("❌ 형식: 테이블명.컬럼명 (예: v2_staff_manager.staff_status)")
        return

    table_name, col_name = table_column.split('.', 1)

    query = f"""
        SELECT {col_name}, COUNT(*) as cnt
        FROM {table_name}
        GROUP BY {col_name}
        ORDER BY cnt DESC
    """

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            values = cur.fetchall()

        print(f"\n📋 고유값: {table_name}.{col_name} ({len(values)}개)")
        print("-" * 50)

        for val, cnt in values:
            val_str = str(val) if val is not None else '(NULL)'
            print(f"   {val_str:<30} {cnt:>10}")
        print()

    except Exception as e:
        print(f"❌ 오류: {e}")


def check_nulls(conn, table_name):
    """컬럼별 NULL 비율 체크"""
    col_query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(col_query, (table_name,))
        columns = [row[0] for row in cur.fetchall()]

        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cur.fetchone()[0]

    if not columns:
        print(f"❌ 테이블 '{table_name}'을 찾을 수 없습니다.")
        return

    print(f"\n📊 NULL 비율: {table_name} (총 {total:,}행)")
    print("-" * 50)

    for col in columns:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col} IS NULL")
            null_count = cur.fetchone()[0]

        pct = (null_count / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))

        if null_count > 0:
            print(f"   {col:<30} {bar} {pct:>5.1f}% ({null_count:,})")
    print()


# ============================================
# 데이터 조회
# ============================================

def select_data(conn, table_name, fields=None, where=None, like=None, order=None, limit=10, as_json=False):
    """데이터 조회"""
    field_str = ', '.join(fields) if fields else '*'
    query = f"SELECT {field_str} FROM {table_name}"
    params = []

    conditions = []

    # WHERE 조건
    if where:
        for w in where:
            if '=' in w:
                key, value = w.split('=', 1)
                conditions.append(f"{key.strip()} = %s")
                params.append(value.strip())

    # LIKE 조건
    if like:
        if '=' in like:
            key, value = like.split('=', 1)
            conditions.append(f"{key.strip()} LIKE %s")
            params.append(value.strip())

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if order:
        query += f" ORDER BY {order}"

    if limit:
        query += f" LIMIT {limit}"

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        if as_json:
            print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False, default=json_serial))
            return rows

        print(f"\n🔍 조회 결과: {table_name} ({len(rows)}건)")
        print(f"   Query: {query}")
        if params:
            print(f"   Params: {params}")
        print("-" * 80)

        if not rows:
            print("  (데이터 없음)")
        else:
            for i, row in enumerate(rows):
                print(f"\n[{i+1}]", end=" ")
                # ID 계열 먼저
                id_keys = [k for k in row.keys() if 'id' in k.lower()]
                name_keys = [k for k in row.keys() if 'name' in k.lower()]
                priority_keys = id_keys + name_keys

                shown = []
                for key in priority_keys:
                    if key in row:
                        print(f"{key}={row[key]}", end=" | ")
                        shown.append(key)
                print()

                for key, value in row.items():
                    if key not in shown:
                        value_str = str(value)
                        if len(value_str) > 60:
                            value_str = value_str[:60] + "..."
                        print(f"    {key}: {value_str}")

        print()
        return rows

    except Exception as e:
        print(f"❌ 조회 실패: {e}")
        return None


def execute_sql(conn, sql):
    """직접 SQL 실행"""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)

            if sql.strip().upper().startswith('SELECT'):
                rows = cur.fetchall()
                print(f"\n🔍 SQL 실행 결과 ({len(rows)}건)")
                print(f"   Query: {sql}")
                print("-" * 80)

                for i, row in enumerate(rows):
                    print(f"[{i+1}] {dict(row)}")
                return rows
            else:
                conn.commit()
                print(f"✅ SQL 실행 성공")
                print(f"   영향받은 행: {cur.rowcount}개")
                return True

    except Exception as e:
        conn.rollback()
        print(f"❌ SQL 실행 실패: {e}")
        return None


# ============================================
# CUD 작업
# ============================================

def insert_data(conn, table_name, data_json):
    """데이터 삽입"""
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return False

    columns = list(data.keys())
    values = list(data.values())
    placeholders = ', '.join(['%s'] * len(values))

    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING *"

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            result = cur.fetchone()
            conn.commit()

        print(f"✅ INSERT 성공: {table_name}")
        print(f"   삽입된 데이터: {dict(result)}")
        return True

    except Exception as e:
        conn.rollback()
        print(f"❌ INSERT 실패: {e}")
        return False


def update_data(conn, table_name, data_json, where):
    """데이터 업데이트"""
    if not where:
        print("❌ UPDATE에는 --where 조건이 필요합니다 (안전을 위해)")
        return False

    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return False

    set_parts = []
    params = []
    for key, value in data.items():
        set_parts.append(f"{key} = %s")
        params.append(value)

    query = f"UPDATE {table_name} SET {', '.join(set_parts)}"

    conditions = []
    for w in where:
        if '=' in w:
            key, value = w.split('=', 1)
            conditions.append(f"{key.strip()} = %s")
            params.append(value.strip())

    query += " WHERE " + " AND ".join(conditions)

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            affected = cur.rowcount
            conn.commit()

        print(f"✅ UPDATE 성공: {table_name}")
        print(f"   영향받은 행: {affected}개")
        return True

    except Exception as e:
        conn.rollback()
        print(f"❌ UPDATE 실패: {e}")
        return False


def delete_data(conn, table_name, where):
    """데이터 삭제"""
    if not where:
        print("❌ DELETE에는 --where 조건이 필요합니다 (안전을 위해)")
        return False

    query = f"DELETE FROM {table_name}"
    params = []

    conditions = []
    for w in where:
        if '=' in w:
            key, value = w.split('=', 1)
            conditions.append(f"{key.strip()} = %s")
            params.append(value.strip())

    query += " WHERE " + " AND ".join(conditions)

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            affected = cur.rowcount
            conn.commit()

        print(f"✅ DELETE 성공: {table_name}")
        print(f"   삭제된 행: {affected}개")
        return True

    except Exception as e:
        conn.rollback()
        print(f"❌ DELETE 실패: {e}")
        return False


# ============================================
# Main
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description='Supabase Query Tool - MCP 대용 만능 DB 조회 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 기본 옵션
    parser.add_argument('--table', '-t', help='테이블명')
    parser.add_argument('--fields', '-f', help='조회할 필드 (쉼표 구분)')
    parser.add_argument('--where', '-w', action='append', help='WHERE 조건')
    parser.add_argument('--like', help='LIKE 조건 (예: name=%%test%%)')
    parser.add_argument('--order', '-o', help='정렬 (예: created_at DESC)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='결과 수 (기본: 10)')

    # 테이블/스키마 정보
    parser.add_argument('--list-tables', action='store_true', help='테이블 목록')
    parser.add_argument('--list-views', action='store_true', help='뷰 목록')
    parser.add_argument('--schema', '-s', help='테이블 스키마')
    parser.add_argument('--full-schema', help='전체 스키마 (PK, FK, 인덱스 포함)')
    parser.add_argument('--fk', help='외래키 관계')
    parser.add_argument('--indexes', help='인덱스 조회')
    parser.add_argument('--constraints', help='제약조건 조회')
    parser.add_argument('--relations', help='테이블 관계')
    parser.add_argument('--all-relations', action='store_true', help='전체 테이블 관계')

    # 데이터 분석
    parser.add_argument('--analyze', '-a', help='테이블 데이터 분석')
    parser.add_argument('--distinct', '-d', help='고유값 목록 (테이블.컬럼)')
    parser.add_argument('--null-check', help='NULL 비율 체크')

    # SQL
    parser.add_argument('--sql', help='직접 SQL 실행')

    # CUD
    parser.add_argument('--insert', help='INSERT (JSON)')
    parser.add_argument('--update', help='UPDATE (JSON)')
    parser.add_argument('--delete', action='store_true', help='DELETE')

    # 출력
    parser.add_argument('--json', action='store_true', help='JSON 출력')

    args = parser.parse_args()

    # 인자 없으면 도움말
    if len(sys.argv) == 1:
        print(__doc__)
        return

    conn = get_connection()
    print("✅ Supabase 연결 성공")

    try:
        # 테이블/뷰 목록
        if args.list_tables:
            list_tables(conn)
            return
        if args.list_views:
            list_views(conn)
            return

        # 스키마 정보
        if args.schema:
            get_schema(conn, args.schema)
            return
        if args.full_schema:
            show_full_schema(conn, args.full_schema)
            return
        if args.fk:
            show_fk_relations(conn, args.fk)
            return
        if args.indexes:
            indexes = get_indexes(conn, args.indexes)
            print(f"\n📇 인덱스: {args.indexes}")
            for idx in indexes:
                print(f"   {idx}")
            return
        if args.constraints:
            constraints = get_constraints(conn, args.constraints)
            print(f"\n✓ 제약조건: {args.constraints}")
            for c in constraints:
                print(f"   {c}")
            return
        if args.relations:
            show_fk_relations(conn, args.relations)
            return
        if args.all_relations:
            show_all_relations(conn)
            return

        # 데이터 분석
        if args.analyze:
            analyze_table(conn, args.analyze)
            return
        if args.distinct:
            show_distinct_values(conn, args.distinct)
            return
        if args.null_check:
            check_nulls(conn, args.null_check)
            return

        # SQL
        if args.sql:
            execute_sql(conn, args.sql)
            return

        # 테이블 필요한 작업들
        if not args.table:
            print("❌ --table 옵션이 필요합니다. 도움말: python supabase_query.py --help")
            return

        # CUD
        if args.insert:
            insert_data(conn, args.table, args.insert)
            return
        if args.update:
            update_data(conn, args.table, args.update, args.where)
            return
        if args.delete:
            delete_data(conn, args.table, args.where)
            return

        # SELECT
        fields = args.fields.split(',') if args.fields else None
        select_data(conn, args.table, fields, args.where, args.like, args.order, args.limit, args.json)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
