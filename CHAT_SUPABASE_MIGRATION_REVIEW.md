# Firebase → Supabase 채팅 시스템 이전 검토 보고서

## 📋 개요

현재 Firebase Firestore 기반 채팅 시스템을 Supabase PostgreSQL로 이전하는 것에 대한 종합 검토입니다.

**현재 시스템:**
- Firebase Firestore (NoSQL) - 채팅 전용
- Firebase Realtime (snapshots)
- Firebase Cloud Functions (FCM 푸시)
- Firebase Anonymous Auth (Firestore 보안 규칙용)

**목표 시스템:**
- Supabase PostgreSQL (관계형 DB) - **이미 51개 테이블 마이그레이션 완료**
- Supabase Realtime (WebSocket 기반) - **Realtime 스키마 확인됨**
- Supabase Edge Functions 또는 외부 서비스 (푸시 알림)
- 기존 인증 유지 (Supabase/DB 기반)

### 🔍 실제 Supabase 프로젝트 상태 (2024년 확인)

**프로젝트 정보:**
- **프로젝트 ID**: `yejialakeivdhwntmagf`
- **URL**: `https://yejialakeivdhwntmagf.supabase.co`
- **데이터베이스**: PostgreSQL (AWS ap-northeast-2)
- **연결 제한**: max_connections = 60

**현재 테이블 현황:**
- ✅ **51개 테이블** 이미 마이그레이션 완료
- ✅ **Realtime 스키마** 존재 확인 (`realtime.schema_migrations`, `realtime.subscription`)
- ⚠️ **채팅 관련 테이블 없음** (`chat_rooms`, `chat_messages` 신규 생성 필요)
- ℹ️ `v2_message` 테이블 존재 (일반 메시지/알림용, 채팅과는 별개)

**의존성 상태:**
- ✅ `supabase_flutter: ^2.8.0` (myxplanner) - 설치됨
- ✅ `supabase_flutter: ^2.8.4` (crm, crm_lite_pro) - 설치됨
- ⚠️ Firebase 패키지 여전히 설치됨 (채팅용으로만 사용)

---

## 1. 데이터베이스 구조 전환

### 1.1 현재 Firestore 구조

```
chatRooms/{branchId}_{memberId}
├── branchId: string
├── memberId: string
├── memberName: string
├── memberPhone: string
├── memberType: string
├── createdAt: timestamp
├── lastMessage: string
├── lastMessageTime: timestamp
├── adminUnreadCount: number
└── memberUnreadCount: number

messages/{branchId}_{memberId}_{timestamp}
├── chatRoomId: string
├── branchId: string
├── senderId: string
├── senderType: "member" | "admin"
├── senderName: string
├── message: string
├── timestamp: timestamp
└── isRead: boolean
```

### 1.2 Supabase PostgreSQL 스키마 설계

**⚠️ 중요:** 현재 Supabase에는 채팅 관련 테이블이 **없습니다**. 아래 스키마를 신규 생성해야 합니다.

```sql
-- 채팅방 테이블 (신규 생성 필요)
CREATE TABLE chat_rooms (
    id TEXT PRIMARY KEY,  -- {branchId}_{memberId}
    branch_id TEXT NOT NULL,
    member_id TEXT NOT NULL,
    member_name TEXT NOT NULL,
    member_phone TEXT,
    member_type TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message TEXT DEFAULT '',
    last_message_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    admin_unread_count INTEGER DEFAULT 0,
    member_unread_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 메시지 테이블 (신규 생성 필요)
CREATE TABLE chat_messages (
    id TEXT PRIMARY KEY,  -- {branchId}_{memberId}_{timestamp}
    chat_room_id TEXT NOT NULL REFERENCES chat_rooms(id) ON DELETE CASCADE,
    branch_id TEXT NOT NULL,
    sender_id TEXT NOT NULL,
    sender_type TEXT NOT NULL CHECK (sender_type IN ('member', 'admin')),
    sender_name TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스 (성능 최적화)
CREATE INDEX idx_chat_rooms_branch_id ON chat_rooms(branch_id);
CREATE INDEX idx_chat_rooms_branch_active ON chat_rooms(branch_id, is_active);
CREATE INDEX idx_chat_rooms_member_id ON chat_rooms(member_id);
CREATE INDEX idx_chat_messages_room_id ON chat_messages(chat_room_id);
CREATE INDEX idx_chat_messages_branch_id ON chat_messages(branch_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp DESC);
CREATE INDEX idx_chat_messages_unread ON chat_messages(chat_room_id, sender_type, is_read) 
    WHERE is_read = FALSE;

-- Realtime 활성화 (Supabase Dashboard에서도 설정 필요)
ALTER PUBLICATION supabase_realtime ADD TABLE chat_rooms;
ALTER PUBLICATION supabase_realtime ADD TABLE chat_messages;

-- RLS (Row Level Security) 정책
-- 주의: 현재 프로젝트는 기존 인증 사용하므로 RLS는 선택사항
ALTER TABLE chat_rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- 옵션 1: RLS 비활성화 (애플리케이션 레벨 보안)
-- ALTER TABLE chat_rooms DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;

-- 옵션 2: RLS 활성화 (Service Role Key 사용 시)
CREATE POLICY "모든 사용자 조회 가능" ON chat_rooms FOR SELECT USING (true);
CREATE POLICY "모든 사용자 삽입 가능" ON chat_rooms FOR INSERT WITH CHECK (true);
CREATE POLICY "모든 사용자 업데이트 가능" ON chat_rooms FOR UPDATE USING (true);

CREATE POLICY "모든 사용자 조회 가능" ON chat_messages FOR SELECT USING (true);
CREATE POLICY "모든 사용자 삽입 가능" ON chat_messages FOR INSERT WITH CHECK (true);
CREATE POLICY "모든 사용자 업데이트 가능" ON chat_messages FOR UPDATE USING (true);
```

**기존 테이블과의 관계:**
- `v2_message`: 일반 메시지/알림용 (예약알림, 쿠폰발행 등) - **채팅과 별개**
- `v3_members`: 회원 정보 (member_id 참조 가능)
- `v2_branch`: 지점 정보 (branch_id 참조 가능)

### 1.3 주요 차이점 및 주의사항

| 항목 | Firestore | Supabase PostgreSQL | 영향도 |
|------|-----------|---------------------|--------|
| **ID 생성** | 자동 생성 또는 수동 | 수동 생성 필수 | ⚠️ 중간 |
| **타임스탬프** | Timestamp 객체 | TIMESTAMPTZ | ✅ 낮음 |
| **트랜잭션** | Batch 작업 | BEGIN/COMMIT | ⚠️ 중간 |
| **쿼리** | where() 체이닝 | SQL WHERE 절 | ⚠️ 중간 |
| **정렬** | orderBy() | ORDER BY | ✅ 낮음 |
| **제약조건** | 클라이언트 검증 | DB 레벨 제약 | ✅ 높음 (개선) |

**주의사항:**
1. **ID 형식 유지**: `{branchId}_{memberId}` 형식 유지 필요
2. **타임스탬프 변환**: Firestore Timestamp → PostgreSQL TIMESTAMPTZ
3. **대소문자**: PostgreSQL은 기본적으로 소문자, Firestore는 원본 유지
4. **NULL 처리**: Firestore는 필드 없음 = NULL, PostgreSQL은 명시적 NULL

---

## 2. 실시간 기능 전환

### 2.1 현재 Firestore 실시간

```dart
// 채팅방 목록 실시간 구독
_firestore
    .collection('chatRooms')
    .where('branchId', isEqualTo: branchId)
    .where('isActive', isEqualTo: true)
    .snapshots()
    .map((snapshot) => ...)

// 메시지 실시간 구독
_firestore
    .collection('messages')
    .where('chatRoomId', isEqualTo: chatRoomId)
    .snapshots()
    .map((snapshot) => ...)
```

### 2.2 Supabase Realtime 전환

```dart
// Supabase Realtime 구독
final channel = supabase
    .channel('chat_rooms')
    .onPostgresChanges(
        event: PostgresChangeEvent.all,
        schema: 'public',
        table: 'chat_rooms',
        filter: PostgresChangeFilter(
            type: PostgresChangeFilterType.eq,
            column: 'branch_id',
            value: branchId,
        ),
        callback: (payload) {
            // 채팅방 변경 처리
        },
    )
    .subscribe();

// 메시지 실시간 구독
final messageChannel = supabase
    .channel('chat_messages_$chatRoomId')
    .onPostgresChanges(
        event: PostgresChangeEvent.all,
        schema: 'public',
        table: 'chat_messages',
        filter: PostgresChangeFilter(
            type: PostgresChangeFilterType.eq,
            column: 'chat_room_id',
            value: chatRoomId,
        ),
        callback: (payload) {
            // 메시지 변경 처리
        },
    )
    .subscribe();
```

### 2.3 실시간 기능 비교

| 기능 | Firestore | Supabase Realtime | 평가 |
|------|-----------|-------------------|------|
| **연결 방식** | WebSocket (자동) | WebSocket (명시적) | ⚠️ 코드 변경 필요 |
| **필터링** | where() 클라이언트 | PostgresChangeFilter | ⚠️ 문법 차이 |
| **성능** | 매우 빠름 | 빠름 | ✅ 양호 |
| **안정성** | 매우 안정적 | 안정적 | ✅ 양호 |
| **재연결** | 자동 | 수동 처리 필요 | ⚠️ 추가 구현 |
| **동시 연결 수** | 무제한 (과금) | 플랜별 제한 | ⚠️ 확인 필요 |

**주의사항:**
1. **Realtime 활성화**: 
   - SQL: `ALTER PUBLICATION supabase_realtime ADD TABLE chat_rooms;`
   - 또는 Supabase Dashboard → Database → Replication에서 활성화
2. **연결 관리**: 채널 구독/해제 명시적 관리 필요
3. **재연결 로직**: 네트워크 끊김 시 재연결 처리 구현 필요
4. **필터 제한**: 복잡한 필터는 PostgreSQL 함수로 처리 필요
5. **연결 수 제한**: 현재 max_connections = 60 (주의 필요)

---

## 3. 인증 시스템

### 3.1 현재 Firebase Auth 사용

```dart
// Firebase Anonymous Auth (Firestore 보안 규칙용)
await FirebaseAuth.instance.signInAnonymously();
```

**현재 상황:**
- Firebase Auth는 **Firestore 보안 규칙용으로만 사용**
- 실제 인증은 **Supabase/기존 DB 기반** (ApiService)
- Firestore Rules: `allow read, write: if request.auth != null;`

### 3.2 Supabase 전환 옵션

#### 옵션 1: Supabase Auth 사용 (권장하지 않음)
- **문제점**: 기존 인증 시스템과 중복
- **장점**: RLS 정책 활용 가능
- **결론**: 기존 인증 유지 권장

#### 옵션 2: 기존 인증 유지 + Service Role Key (권장)
- **장점**: 기존 인증 시스템 유지
- **방법**: RLS 우회 또는 Service Role Key 사용
- **구현**:
```dart
// Service Role Key로 클라이언트 초기화 (서버 사이드만)
// 또는 RLS 정책에서 JWT 커스텀 클레임 사용
```

#### 옵션 3: RLS 비활성화 + 애플리케이션 레벨 보안
- **장점**: 단순함
- **단점**: DB 레벨 보안 없음
- **구현**: RLS OFF, 클라이언트에서 branchId/memberId 검증

**권장 방안:**
```sql
-- RLS 활성화하되, 애플리케이션 레벨에서 branch_id/member_id 검증
-- Service Role Key 사용 또는 커스텀 JWT 클레임 활용
```

---

## 4. 푸시 알림 시스템

### 4.1 현재 Firebase Cloud Functions

```javascript
// Firebase Cloud Functions
exports.sendChatNotification = functions.firestore
  .document('messages/{messageId}')
  .onCreate(async (snap, context) => {
    // FCM 푸시 알림 발송
  });
```

### 4.2 Supabase 전환 옵션

#### 옵션 1: Supabase Edge Functions + FCM (권장)
```typescript
// Supabase Edge Function
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // PostgreSQL Trigger → Edge Function 호출
  // FCM SDK로 푸시 알림 발송
})
```

**구현 방법:**
1. PostgreSQL Trigger 생성
2. Trigger → Supabase Edge Function 호출 (pg_net 확장)
3. Edge Function에서 FCM 푸시 발송

#### 옵션 2: 외부 서버리스 함수 (Vercel/Netlify)
- Supabase Webhook → 외부 함수 호출
- 외부 함수에서 FCM 푸시 발송

#### 옵션 3: Supabase Database Webhooks
- Supabase Dashboard에서 Webhook 설정
- 외부 엔드포인트로 POST 요청
- 외부 서버에서 FCM 푸시 발송

**권장 방안:**
```sql
-- PostgreSQL Trigger
CREATE OR REPLACE FUNCTION notify_new_message()
RETURNS TRIGGER AS $$
BEGIN
    -- Supabase Edge Function 호출 또는 Webhook
    PERFORM net.http_post(
        url := 'https://your-project.supabase.co/functions/v1/send-push',
        body := json_build_object(
            'message_id', NEW.id,
            'chat_room_id', NEW.chat_room_id,
            'sender_type', NEW.sender_type
        )::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_message_created
    AFTER INSERT ON chat_messages
    FOR EACH ROW
    EXECUTE FUNCTION notify_new_message();
```

---

## 5. 코드 변경 범위

### 5.1 영향받는 파일

#### CRM 앱 (crm, crm_lite_pro)
```
lib/services/chat_service.dart          → 완전 재작성
lib/models/chat_models.dart              → 부분 수정 (Firestore → Supabase)
lib/pages/chat/*.dart                    → 서비스 호출 부분 수정
pubspec.yaml                             → 의존성 변경
```

#### 회원 앱 (myxplanner)
```
lib/services/chatting/chatting_service.dart  → 완전 재작성
lib/services/chatting/chat_models.dart       → 부분 수정
lib/pages/chatting/*.dart                    → 서비스 호출 부분 수정
pubspec.yaml                                 → 의존성 변경
```

### 5.2 주요 코드 변경 예시

#### Before (Firestore)
```dart
// 메시지 전송
final messageRef = _firestore.collection('messages').doc(messageId);
batch.set(messageRef, chatMessage.toFirestore());

final chatRoomRef = _firestore.collection('chatRooms').doc(chatRoomId);
batch.update(chatRoomRef, {
  'lastMessage': message,
  'memberUnreadCount': FieldValue.increment(1),
});
await batch.commit();
```

#### After (Supabase)
```dart
// 메시지 전송
await supabase.from('chat_messages').insert({
  'id': messageId,
  'chat_room_id': chatRoomId,
  'branch_id': branchId,
  'sender_id': senderId,
  'sender_type': senderType,
  'sender_name': senderName,
  'message': message,
  'timestamp': DateTime.now().toIso8601String(),
  'is_read': false,
});

// 채팅방 업데이트 (트랜잭션 또는 함수)
await supabase.rpc('update_chat_room_on_message', {
  'p_chat_room_id': chatRoomId,
  'p_last_message': message,
  'p_increment_unread': senderType == 'member' ? 'admin' : 'member',
});
```

### 5.3 예상 작업량

| 작업 | 예상 시간 | 난이도 |
|------|----------|--------|
| DB 스키마 설계 및 생성 | 4시간 | 중간 |
| Supabase 서비스 클래스 작성 | 16시간 | 높음 |
| 실시간 구독 로직 전환 | 8시간 | 높음 |
| 푸시 알림 시스템 구축 | 12시간 | 높음 |
| 모델 클래스 수정 | 4시간 | 낮음 |
| UI 코드 수정 | 8시간 | 중간 |
| 테스트 및 디버깅 | 16시간 | 높음 |
| **총계** | **68시간** | - |

---

## 6. 잠재적 문제점 및 해결방안

### 6.1 실시간 성능

**문제:**
- Supabase Realtime은 Firestore보다 약간 느릴 수 있음
- 복잡한 필터링 시 성능 저하 가능

**해결:**
- 인덱스 최적화
- 필요한 데이터만 구독
- 클라이언트 사이드 캐싱

### 6.2 동시 연결 수 제한

**문제:**
- **현재 확인**: max_connections = 60 (매우 제한적)
- Supabase 무료 플랜: 제한적
- 유료 플랜도 연결 수 제한 존재
- 채팅은 실시간 연결이 많아 제한에 쉽게 도달 가능

**해결:**
- 플랜 업그레이드 검토 (Pro 플랜: 더 많은 연결 허용)
- 연결 풀링 최적화
- 불필요한 구독 해제
- 채널 재사용 (같은 채팅방은 하나의 채널로 관리)
- 연결 풀 모니터링 필요

### 6.3 데이터 마이그레이션

**문제:**
- 기존 Firestore 데이터를 PostgreSQL로 이전 필요
- 데이터 손실 위험

**해결:**
```python
# 마이그레이션 스크립트
# 1. Firestore 데이터 export
# 2. PostgreSQL 형식으로 변환
# 3. Supabase에 import
# 4. 검증 및 롤백 계획 수립
```

### 6.4 트랜잭션 처리

**문제:**
- Firestore Batch → PostgreSQL 트랜잭션
- 복잡한 비즈니스 로직 처리

**해결:**
```sql
-- PostgreSQL 함수로 트랜잭션 처리
CREATE OR REPLACE FUNCTION send_chat_message(
    p_chat_room_id TEXT,
    p_message TEXT,
    p_sender_type TEXT
) RETURNS void AS $$
BEGIN
    -- 메시지 삽입
    INSERT INTO chat_messages (...);
    
    -- 채팅방 업데이트
    UPDATE chat_rooms 
    SET last_message = p_message,
        member_unread_count = CASE 
            WHEN p_sender_type = 'admin' 
            THEN member_unread_count + 1 
            ELSE member_unread_count 
        END
    WHERE id = p_chat_room_id;
END;
$$ LANGUAGE plpgsql;
```

### 6.5 보안 정책 복잡도

**문제:**
- RLS 정책이 Firestore Rules보다 복잡할 수 있음
- branchId/memberId 기반 접근 제어

**해결:**
- 단순한 RLS 정책 + 애플리케이션 레벨 검증
- 또는 Service Role Key 사용

---

## 7. 비용 비교

### 7.1 Firebase (현재)

| 항목 | 무료 플랜 | Blaze (종량제) |
|------|----------|----------------|
| Firestore 읽기 | 50K/일 | $0.06/100K |
| Firestore 쓰기 | 20K/일 | $0.18/100K |
| 저장공간 | 1GB | $0.18/GB |
| Cloud Functions | 2M 호출/월 | $0.40/1M |
| **예상 월 비용** | **무료** | **$50-200** |

### 7.2 Supabase

| 항목 | 무료 플랜 | Pro ($25/월) |
|------|----------|--------------|
| 데이터베이스 | 500MB | 8GB |
| API 요청 | 무제한 | 무제한 |
| Realtime 연결 | 제한적 | 무제한 |
| Edge Functions | 500K 호출/월 | 2M 호출/월 |
| **예상 월 비용** | **무료** | **$25-50** |

**비용 절감:** Supabase가 더 저렴할 가능성 높음

---

## 8. 마이그레이션 전략

### 8.1 단계별 접근 (권장)

#### Phase 1: 준비 단계 (1주)
1. Supabase 프로젝트 생성
2. DB 스키마 설계 및 생성
3. 마이그레이션 스크립트 작성
4. 테스트 환경 구축

#### Phase 2: 개발 단계 (2주)
1. Supabase 서비스 클래스 개발
2. 실시간 구독 로직 구현
3. 푸시 알림 시스템 구축
4. 단위 테스트

#### Phase 3: 통합 테스트 (1주)
1. 기존 시스템과 병행 운영
2. 데이터 동기화 검증
3. 성능 테스트
4. 버그 수정

#### Phase 4: 전환 단계 (1주)
1. 데이터 마이그레이션
2. 점진적 사용자 전환
3. 모니터링 및 롤백 준비

#### Phase 5: 정리 단계 (3일)
1. Firebase 의존성 제거
2. 문서화
3. 최종 검증

### 8.2 롤백 계획

1. **데이터 백업**: 마이그레이션 전 Firestore 전체 백업
2. **이중 운영**: 전환 기간 동안 Firebase와 Supabase 병행
3. **기능 플래그**: 쉽게 전환 가능한 토글 구현
4. **모니터링**: 오류율, 지연시간 실시간 모니터링

---

## 9. 최종 권장사항

### ✅ 이전 권장 조건

1. **장기적 비용 절감**이 필요한 경우
2. **PostgreSQL의 관계형 데이터** 활용이 필요한 경우
3. **기존 Supabase 인프라**와 통합이 필요한 경우
4. **오픈소스 기반** 솔루션을 선호하는 경우

### ⚠️ 이전 신중 검토 필요

1. **현재 시스템이 안정적**으로 동작하는 경우
2. **마이그레이션 리스크**가 큰 경우
3. **개발 리소스**가 부족한 경우
4. **Firebase 특화 기능**을 많이 사용하는 경우

### 🎯 결론

**현재 상황 분석:**
- ✅ **Supabase 프로젝트 활성화됨** (51개 테이블 마이그레이션 완료)
- ✅ **Supabase Flutter SDK 설치됨** (모든 앱)
- ✅ **Realtime 스키마 존재** (기능 사용 가능)
- ✅ 기존 인증은 Supabase/DB 기반
- ✅ Firebase는 채팅용으로만 사용 (제거 가능)
- ⚠️ **채팅 테이블 신규 생성 필요** (스키마 설계 완료)
- ⚠️ **연결 수 제한 낮음** (max_connections = 60)
- ⚠️ 실시간 기능이 핵심 기능
- ⚠️ 마이그레이션 작업량 상당함

**⚠️ 중요: 보안 지적사항 확인됨**

**보안 감사 결과** (`SECURITY_AUDIT_REPORT.md` 참조):
- 🔴 **비밀번호 해싱 취약** (Salt 없음, SHA-256 50자 자르기)
- 🔴 **Firebase 보안 규칙 취약** (Anonymous Auth만으로 모든 접근 허용)
- 🟡 **하드코딩 자격증명** (Email, DB 비밀번호)
- 🟡 **Landing 페이지 평문 비교**

**권장 이전 순서:**
1. **Auth 보안 강화 먼저** (1-2주)
   - 비밀번호 해싱 개선 (bcrypt)
   - Firebase 보안 규칙 강화
   - 하드코딩 자격증명 제거
2. **채팅 이전 후속** (2-3주)
   - 강화된 Auth 기반으로 RLS 정책 설정
   - 일관된 보안 정책 적용

**이유:**
- 보안 취약점이 더 심각함
- 채팅 보안이 Auth에 의존
- 작업 효율성 및 일관성 확보

**권장 방안:**
1. **보안 우선**: Auth 보안 강화 후 채팅 이전
2. **단계적 이전**: 테스트 환경에서 먼저 검증
3. **병행 운영**: 전환 기간 동안 이중 운영
4. **점진적 전환**: 기능별로 단계적 전환
5. **충분한 테스트**: 실시간 기능 철저한 테스트

**예상 소요 시간:**
- Auth 보안 강화: 1-2주
- 채팅 이전: 2-3주
- **총계: 3-5주**

**실제 준비 상태:**
- ✅ Supabase 인프라: 준비 완료
- ✅ SDK 설치: 완료
- ⚠️ 보안 강화: 필요 (Auth 이전 필수)
- ⚠️ 채팅 테이블: 신규 생성 필요 (1일)
- ⚠️ 코드 전환: 2-3주
- ⚠️ 테스트: 1주

**즉시 시작 가능:** ⚠️ (보안 강화 후 권장)

---

## 10. 체크리스트

### 사전 준비
- [x] Supabase 프로젝트 생성 및 설정 (**완료**)
- [x] DB 스키마 설계 검토 (**완료**)
- [ ] 채팅 테이블 생성 (`chat_rooms`, `chat_messages`)
- [ ] Realtime 활성화 (테이블별)
- [ ] 인덱스 생성
- [ ] RLS 정책 설정
- [ ] 마이그레이션 스크립트 작성 (Firestore → Supabase)
- [ ] 테스트 환경 구축

### 개발
- [ ] Supabase 서비스 클래스 구현
- [ ] 실시간 구독 로직 구현
- [ ] 푸시 알림 시스템 구축
- [ ] 모델 클래스 수정
- [ ] UI 코드 수정

### 테스트
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 성능 테스트
- [ ] 보안 테스트

### 전환
- [ ] 데이터 마이그레이션
- [ ] 모니터링 설정
- [ ] 롤백 계획 수립
- [ ] 문서화

---

---

## 11. Supabase MCP 연결 상태

### 11.1 MCP 설정 확인

**설정 파일 위치:**
- 프로젝트 루트: `.cursor/settings.json`
- 전역 설정: `~/.cursor/mcp.json`

**설정 상태:**
- ✅ MCP 서버 설정됨 (`@supabase/mcp-server-supabase@latest`)
- ✅ Access Token 설정됨
- ⚠️ 실제 연결: 확인 필요 (리소스 조회 실패)

**대안:**
- ✅ `supabase_query.py`: Python 스크립트로 직접 DB 연결 (정상 작동)
- ✅ `SupabaseAdapter`: Flutter SDK (정상 작동)

**상세 내용:** `SUPABASE_MCP_STATUS.md` 참조

---

## 12. 실제 Supabase 프로젝트 확인 결과

### 11.1 데이터베이스 현황

**확인 일시:** 2024년 (실제 DB 조회)

**테이블 목록:**
- 총 **51개 테이블** 마이그레이션 완료
- 주요 테이블: `v3_members`, `v2_branch`, `v2_staff_pro`, `v2_staff_manager`, `v2_ls_orders` 등
- 채팅 관련: **없음** (신규 생성 필요)

**기존 메시지 테이블:**
- `v2_message`: 일반 메시지/알림용 (19건)
  - 용도: 예약알림, 쿠폰발행, 일반안내
  - 채팅 시스템과는 **별개**
  - 스키마: `msg_id`, `member_id`, `msg_type`, `msg`, `msg_status` 등

**Realtime 상태:**
- ✅ `realtime` 스키마 존재
- ✅ `realtime.schema_migrations` 테이블 확인
- ✅ `realtime.subscription` 테이블 확인
- ⚠️ 채팅 테이블에 Realtime 활성화 필요

**데이터베이스 설정:**
- PostgreSQL 버전: 확인됨
- max_connections: **60** (⚠️ 제한적)
- shared_buffers: 28672 (28MB)
- work_mem: 2184 (2MB)

### 11.2 의존성 확인

**Flutter 패키지:**
```yaml
# crm, crm_lite_pro
supabase_flutter: ^2.8.4  ✅ 설치됨
firebase_core: ^4.2.1     ⚠️ 채팅용 (제거 예정)
cloud_firestore: ^6.1.0  ⚠️ 채팅용 (제거 예정)

# myxplanner
supabase_flutter: ^2.8.0  ✅ 설치됨
firebase_core: ^4.2.1     ⚠️ 채팅용 (제거 예정)
cloud_firestore: ^6.1.0  ⚠️ 채팅용 (제거 예정)
```

### 11.3 준비 상태 평가

| 항목 | 상태 | 비고 |
|------|------|------|
| Supabase 프로젝트 | ✅ 완료 | 51개 테이블 마이그레이션됨 |
| Supabase SDK | ✅ 완료 | 모든 앱에 설치됨 |
| Realtime 인프라 | ✅ 준비됨 | 스키마 존재, 활성화 필요 |
| 채팅 테이블 | ❌ 없음 | 신규 생성 필요 |
| 인덱스 | ❌ 없음 | 테이블 생성 시 함께 생성 |
| RLS 정책 | ❌ 없음 | 테이블 생성 시 설정 |
| 마이그레이션 스크립트 | ❌ 없음 | 작성 필요 |
| 테스트 환경 | ❌ 없음 | 구축 필요 |

**준비도:** 약 40% (인프라는 준비됨, 채팅 전용 리소스는 미구축)

---

**작성일:** 2024년
**검토자:** AI Assistant
**버전:** 2.0 (실제 Supabase 상태 반영)
**최종 업데이트:** 실제 DB 조회 결과 반영

