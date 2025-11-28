-- Table: CHN_batch
-- Backup Date: 2025-11-27T21:08:10.571733
-- Row Count: 2

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `CHN_batch`;

INSERT INTO `CHN_batch` (`CHN_batch_id`, `CHN_batch_title`, `CHN_batch_msg`, `staff_id`, `CHN_batch_registered_at`, `CHN_attachment`, `branch_id`) VALUES ('20250401205229', '김주순프로님 임시휴무 일정안내', '안녕하세요 
김주순프로님 임시휴무 일정 안내드립니다. 4월 6일(일)~~8일(화) 미리 잡혀있던 제주도 골프일정으로 임시휴무이시니 레슨을 원하시는 회원님들께서는 해당날짜 전후로 이용해주시길 부탁드립니다. 
레슨이용에 불편을 드려 죄송하오며, 늘 회원님의 실력향상을 위해 노력하는 프렌즈아카데미 목동프리미엄점이 되겠습니다.

나를 위한 골프연습장
프렌즈아카데미 목동프리미엄점', 2, '2025-04-01T20:52:28', '', 'famd');
INSERT INTO `CHN_batch` (`CHN_batch_id`, `CHN_batch_title`, `CHN_batch_msg`, `staff_id`, `CHN_batch_registered_at`, `CHN_attachment`, `branch_id`) VALUES ('20250403200049', '테스트', '테스트', 3, '2025-04-03T20:00:44', '', 'famd');

SET FOREIGN_KEY_CHECKS=1;
