-- Table: v2_board_by_member_replies
-- Backup Date: 2025-11-27T21:08:19.935937
-- Row Count: 3

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_board_by_member_replies`;

INSERT INTO `v2_board_by_member_replies` (`branch_id`, `memberboard_id`, `reply_id`, `member_id`, `member_name`, `reply_by_member`, `created_at`, `updated_at`) VALUES ('test', 1, NULL, 901, NULL, '1212', '2025-08-14T23:41:32', '2025-08-14T23:41:32');
INSERT INTO `v2_board_by_member_replies` (`branch_id`, `memberboard_id`, `reply_id`, `member_id`, `member_name`, `reply_by_member`, `created_at`, `updated_at`) VALUES ('test', 2, NULL, NULL, '체험용 골프연습장', '댓글입니다.', '2025-08-15T03:42:03', '2025-08-15T03:42:03');
INSERT INTO `v2_board_by_member_replies` (`branch_id`, `memberboard_id`, `reply_id`, `member_id`, `member_name`, `reply_by_member`, `created_at`, `updated_at`) VALUES ('famd', 8, NULL, 44, '김현우', '구매 희망합니다', '2025-11-22T05:06:25', '2025-11-22T05:06:25');

SET FOREIGN_KEY_CHECKS=1;
