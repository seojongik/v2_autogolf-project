-- Table: v2_discount_coupon_setting
-- Backup Date: 2025-11-27T21:08:20.339252
-- Row Count: 8

SET FOREIGN_KEY_CHECKS=0;

TRUNCATE TABLE `v2_discount_coupon_setting`;

INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('test', 'test_001', '0', '정액권', 1500, 0, 7, '가능', '집중연습 할인쿠폰', '2025-07-16T23:28:09', '유효', '1,2');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('test', 'test_002', '100', '정률권', 0, 0, 7, '불가능', '무료이용쿠폰', '2025-07-13T03:04:36', '유효', '');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('test', 'test_003', '0', '시간권', 0, 60, 14, '불가능', '1시간 무료쿠폰', '2025-07-13T11:30:20', '무효', '');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('test', 'test_004', '0', '시간권', 0, 30, 14, '가능', '30분 할인쿠폰', '2025-07-13T11:30:51', '유효', NULL);
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('famd', 'famd_001', '10', '정률권', 0, 0, 7, '가능', '평일피크시간 할인', '2025-11-16T11:43:42', '유효', '1');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('famd', 'famd_002', '10', '정률권', 0, 0, 7, '가능', '집중연습할인(90분)', '2025-11-16T11:43:37', '유효', '2');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('famd', 'famd_003', '10', '정률권', 0, 0, 14, '가능', '주니어 부모할인', '2025-11-16T11:44:16', '유효', '4');
INSERT INTO `v2_discount_coupon_setting` (`branch_id`, `coupon_code`, `discount_ratio`, `coupon_type`, `discount_amt`, `discount_min`, `coupon_expiry_days`, `multiple_coupon_use`, `coupon_description`, `updated_at`, `setting_status`, `trigger_id`) VALUES ('famd', 'famd_004', '10', '정률권', 0, 0, 7, '가능', '집중연습할인(120분)', '2025-11-16T11:44:41', '유효', '5');

SET FOREIGN_KEY_CHECKS=1;
