-- Table: v2_ts_info
-- Backup Date: 2025-11-27T21:08:22.199428
-- Row Count: 12

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_ts_info`;

INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (1, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '주니어');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (2, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '주니어');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (3, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '주니어');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (4, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '주니어');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (5, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (6, '오픈', 'famd', '', 15000, 12000, 18600, 60, 30, 180, '예약가능', 5, 1, '');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (7, '단독', 'famd', '', 18000, 15000, 21600, 60, 30, 180, '예약가능', 5, 1, '');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (8, '단독', 'famd', '', 18000, 15000, 21600, 60, 30, 180, '예약가능', 5, 1, '');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (9, '단독', 'famd', '', 18000, 15000, 21600, 60, 30, 180, '예약가능', 5, 1, '');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (1, '스크린', 'test', '스크린타석 입니다', 15000, 12000, 18000, 60, 30, 180, '예약가능', 10, 2, '리프레쉬,아이코젠,주니어');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (2, '연습타석', 'test', '일반연습타석 입니다', 15000, 12000, 18000, 60, 30, 180, '예약가능', 10, 1, '리프레쉬,아이코젠');
INSERT INTO `v2_ts_info` (`ts_id`, `ts_type`, `branch_id`, `ts_description`, `base_price`, `discount_price`, `extracharge_price`, `ts_min_base`, `ts_min_minimum`, `ts_min_maximum`, `ts_status`, `ts_buffer`, `max_person`, `member_type_prohibited`) VALUES (3, '연습타석', 'test', NULL, 15000, 12000, 18000, 60, 30, 70, '예약가능', 10, 1, NULL);

SET FOREIGN_KEY_CHECKS=1;
