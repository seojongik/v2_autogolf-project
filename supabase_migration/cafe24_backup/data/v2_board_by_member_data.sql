-- Table: v2_board_by_member
-- Backup Date: 2025-11-27T21:08:19.905484
-- Row Count: 6

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_board_by_member`;

INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('test', 1, '111', '1111', '공지사항', '2025-08-14T21:56:12', '2025-08-15T01:20:08', 901, NULL, NULL, NULL);
INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('test', 4, '공지사항입니다', '테스트입니다.', '공지사항', '2025-08-15T03:40:06', '2025-08-15T03:40:06', NULL, '진행', NULL, '체험용 골프연습장');
INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('test', 5, 'ㅁㄴㅇㄹ', 'ㅁㄴㅇㄹ', '공지사항', '2025-08-15T03:43:43', '2025-08-15T03:43:43', NULL, '진행', NULL, '체험용 골프연습장');
INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('famd', 6, '123', '123', '자유게시판', '2025-11-21T00:39:29', '2025-11-21T00:39:29', 293, NULL, NULL, 'HWANGYOONSUN');
INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('famd', 7, '1313', '1233', '자유게시판', '2025-11-21T00:50:23', '2025-11-21T00:50:23', 293, NULL, NULL, 'HWANGYOONSUN');
INSERT INTO `v2_board_by_member` (`branch_id`, `memberboard_id`, `title`, `content`, `board_type`, `created_at`, `updated_at`, `member_id`, `post_status`, `post_due_date`, `member_name`) VALUES ('famd', 8, '아이언 7번(성인 여성용)', '사용감 하', '중고판매', '2025-11-21T18:17:54', '2025-11-21T18:17:54', 871, '진행', NULL, '고민정');

SET FOREIGN_KEY_CHECKS=1;
